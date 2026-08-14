import json
import subprocess
import os
import urllib.request

MONITORED_CONTAINERS = {
    "Homepage",
    "adguard-home",
    "plex",
    "nginx-proxy-manager",
    "samba",
}

NTFY_URL = os.getenv("NTFY_URL", "http://192.168.10.151:8082")
NTFY_TOPIC = os.getenv("NTFY_URL", "homelab")


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


def send_notification(title, message, priority="default"):
    url = f"{NTFY_URL}/{NTFY_TOPIC}"

    request = urllib.request.Request(
        url,
        data=message.encode("utf-8"),
        headers={
            "Title": title,
            "Priority": priority,
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            print(f"[NTFY] Sent notification: HTTP {response.status}")
    except Exception as error:
        print(f"[NTFY] Failed to send notification: {error}")

process = subprocess.Popen(
    cmd,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    bufsize=1,
)

print("Homelab monitor started.")
print("Monitoring:", ", ".join(sorted(MONITORED_CONTAINERS)))

for line in process.stdout:
    try:
        event = json.loads(line)

        attributes = event.get("Actor", {}).get("Attributes", {})
        name = attributes.get("name")
        status = event.get("Action")

        if name not in MONITORED_CONTAINERS:
            continue

        print(f"[EVENT] {name}: {status}")

        if status == "health_status: unhealthy":
            send_notification(
                "HOMELAB ALERT",
                f"{name} is unhealthy.",
                "high",
            )

        elif status == "health_status: healthy":
            send_notification(
            "HOMELAB RECOVERY",
            f"{name} is healthy again.",
            "default",
        )

    except json.JSONDecodeError:
        continue