import json
import subprocess
import urllib.request
import time
from datetime import datetime
from pathlib import Path

MONITORED_CONTAINERS = {
    "Homepage",
    "adguard-home",
    "plex",
    "nginx-proxy-manager",
    "samba",
}

NTFY_URL = "http://192.168.10.151:8082/homelab"
STATE_FILE = Path("state.json")

cmd = [
    "docker",
    "events",
    "--format",
    "{{json .}}",
    "--filter",
    "type=container",
    "--filter",
    "event=health_status",
]

process = subprocess.Popen(
    cmd,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    bufsize=1,
)

print("Homelab monitor started.")
print("Monitoring:", ", ".join(sorted(MONITORED_CONTAINERS)))


def load_states():
    if not STATE_FILE.exists():
        return {}

    try:
        with STATE_FILE.open("r", encoding="utf-8") as file:
            loaded_states = json.load(file)

        migrated_states = {}
        migration_needed = False

        for name, state in loaded_states.items():
            if isinstance(state, str):
                migrated_states[name] = {
                    "status": state,
                    "unhealthy_since": None,
                }
                migration_needed = True
            else:
                migrated_states[name] = state

        if migration_needed:
            print("[STATE] Migrating state file to new format.")

            temp_file = STATE_FILE.with_suffix(".tmp")

            with temp_file.open("w", encoding="utf-8") as file:
                json.dump(migrated_states, file, indent=2)
                file.write("\n")

            temp_file.replace(STATE_FILE)

            print("[STATE] State migration complete.")

        return migrated_states

    except (json.JSONDecodeError, OSError) as e:
        print(f"[STATE] Could not load state file: {e}")
        print("[STATE] Starting with empty state.")
        return {}


states = load_states()
print(f"[STATE] Loaded {len(states)} saved container states.")


def save_states(states):
    temp_file = STATE_FILE.with_suffix(".tmp")

    try:
        with temp_file.open("w", encoding="utf-8") as file:
            json.dump(states, file, indent=2)
            file.write("\n")

        temp_file.replace(STATE_FILE)

    except OSError as e:
        print(f"[STATE] Failed to save state: {e}")


def send_notification(message):
    try:
        data = message.encode("utf-8")

        request = urllib.request.Request(
            NTFY_URL,
            data=data,
            method="POST",
            headers={
                "Content-Type": "text/plain; charset=utf-8",
            },
        )

        with urllib.request.urlopen(request, timeout=10) as response:
            if response.status == 200:
                print(f"[NTFY] Sent: {message}")

    except Exception as e:
        print(f"[NTFY] Failed to send notification: {e}")


def format_time(timestamp):
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")


def format_duration(seconds):
    seconds = int(seconds)

    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)

    parts = []

    if days:
        parts.append(f"{days}d")

    if hours:
        parts.append(f"{hours}h")

    if minutes:
        parts.append(f"{minutes}m")

    parts.append(f"{seconds}s")

    return " ".join(parts)


for line in process.stdout:
    try:
        event = json.loads(line)

        attributes = event.get("Actor", {}).get("Attributes", {})
        name = attributes.get("name")
        status = event.get("Action")

        if name not in MONITORED_CONTAINERS:
            continue

        previous_state = states.get(name)

        if previous_state is None:
            previous_status = None
        else:
            previous_status = previous_state.get("status")

        print(
            f"[EVENT] {name}: {status} "
            f"(previous: {previous_status})"
        )

        # First event establishes the baseline.
        if previous_state is None:
            states[name] = {
                "status": status,
                "unhealthy_since": (
                    time.time()
                    if status == "health_status: unhealthy"
                    else None
                ),
            }

            save_states(states)

            print(
                f"[STATE] {name} baseline set to {status}"
            )

            continue

        # Ignore duplicate events.
        if previous_status == status:
            print(f"[STATE] {name} unchanged")
            continue

        now = time.time()

        # Container became unhealthy.
        if status == "health_status: unhealthy":
            states[name] = {
                "status": status,
                "unhealthy_since": now,
            }

            save_states(states)

            print(
                f"[STATE] {name}: "
                f"{previous_status} -> {status}"
            )

            send_notification(
                f"🚨 HOMELAB ALERT\n\n"
                f"Container: {name}\n"
                f"Status: UNHEALTHY\n"
                f"Host: homelab\n"
                f"Time: {format_time(now)}"
            )

        # Container recovered.
        elif status == "health_status: healthy":
            unhealthy_since = previous_state.get("unhealthy_since")

            states[name] = {
                "status": status,
                "unhealthy_since": None,
            }

            save_states(states)

            print(
                f"[STATE] {name}: "
                f"{previous_status} -> {status}"
            )

            if unhealthy_since is not None:
                downtime = now - unhealthy_since

                send_notification(
                    f"✅ HOMELAB RECOVERY\n\n"
                    f"Container: {name}\n"
                    f"Status: HEALTHY\n"
                    f"Host: homelab\n"
                    f"Time: {format_time(now)}\n"
                    f"Downtime: {format_duration(downtime)}"
                )
            else:
                # This can happen if the monitor starts with an already
                # unhealthy state that wasn't recorded with a timestamp.
                send_notification(
                    f"✅ HOMELAB RECOVERY\n\n"
                    f"Container: {name}\n"
                    f"Status: HEALTHY\n"
                    f"Host: homelab\n"
                    f"Time: {format_time(now)}"
                )

        # Unknown health status transition.
        else:
            states[name] = {
                "status": status,
                "unhealthy_since": previous_state.get(
                    "unhealthy_since"
                ),
            }

            save_states(states)

            print(
                f"[STATE] {name}: "
                f"{previous_status} -> {status}"
            )

    except json.JSONDecodeError:
        continue