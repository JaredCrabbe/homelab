import json
import subprocess
import urllib.request

MONITORED_CONTAINERS = {
    "Homepage",
    "adguard-home",
    "plex",
    "nginx-proxy-manager",
    "samba",
}

NTFY_URL = "http://192.168.10.151:8082/homelab"

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

states = {}

print("Homelab monitor started.")
print("Monitoring:", ", ".join(sorted(MONITORED_CONTAINERS)))


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


for line in process.stdout:
    try:
        event = json.loads(line)

        attributes = event.get("Actor", {}).get("Attributes", {})
        name = attributes.get("name")
        status = event.get("Action")

        if name not in MONITORED_CONTAINERS:
            continue

        print(f"[EVENT] {name}: {status} (previous: {states.get(name)})")

        previous = states.get(name)

        # First event establishes the baseline
        if previous is None:
            states[name] = status
            print(f"[STATE] {name} baseline set to {status}")
            continue

        # Ignore duplicate events
        if previous == status:
            print(f"[STATE] {name} unchanged")
            continue

        # State actually changed
        states[name] = status

        print(f"[STATE] {name}: {previous} -> {status}")

        if status == "health_status: unhealthy":
            send_notification(
                f"🚨 {name} is UNHEALTHY"
            )

        elif status == "health_status: healthy":
            send_notification(
                f"✅ {name} has recovered and is HEALTHY"
            )

    except json.JSONDecodeError:
        continue