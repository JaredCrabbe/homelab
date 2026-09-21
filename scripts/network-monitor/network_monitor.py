import subprocess
import json
from pathlib import Path
import urllib.request

NETWORK_INTERFACE = "enp3s0"

TARGETS = {
    "gateway": "192.168.10.1",
    "internet": "1.1.1.1",
}

STATE_FILE = Path(__file__).parent / "state.json"

NTFY_URL = "http://192.168.10.151:8082/homelab"

def load_states():
    if not STATE_FILE.exists():
        return{}

    try:
        with STATE_FILE.open("r", encoding="utf-8") as file:
            return json.load(file)

    except (json.JSONDecodeError, OSError):
        return{}

def save_states(states):
    with STATE_FILE.open("w", encoding="utf-8") as file:
        json.dump(states, file, indent=2)
        file.write("\n")



def check_interface():
    operstate_path = Path(
        f"/sys/class/net/{NETWORK_INTERFACE}/operstate"
    )
    carrier_path = Path(
        f"/sys/class/net/{NETWORK_INTERFACE}/carrier"
    )

    try:
        operstate = operstate_path.read_text(
            encoding="utf-8"
        ).strip()

        carrier = carrier_path.read_text(
            encoding="utf-8"
        ).strip()

        return operstate == "up" and carrier == "1"

    except OSError:
        return False

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

    except Exception as error:
        print(f"[NTFY] Failed to send notification: {error}")

def ping_target(address):
    result = subprocess.run(
        ["ping", "-c", "3", "-W", "2", address],
        capture_output=True,
        text=True,
    )

    packet_loss = None
    average_latency = None

    for line in result.stdout.splitlines():
        if "packet loss" in line:
            loss_part = line.split(",")[2].strip()
            packet_loss = float(
                loss_part.split("%")[0]
            )

        elif "min/avg/max" in line:
            stats = line.split("=")[1].strip()
            average_latency = float(
                stats.split("/")[1]
            )

    if packet_loss is None:
        return False, None, 100.0

    if packet_loss == 100:
        return False, None, packet_loss

    return True, average_latency, packet_loss



def check_targets():
    states = load_states()
    interface_up = check_interface()
    current_interface_status = "up" if interface_up else "down"
    previous_interface_status= states.get("interface")



    if previous_interface_status is None:
        print(
            f"[STATE] interface baseline set to "
            f"{current_interface_status}"
        )

    elif previous_interface_status != current_interface_status:
        print(
            f"[STATE] interface: "
            f"{previous_interface_status} -> "
            f"{current_interface_status}"
        )

        if current_interface_status == "down":
            send_notification(
                f"🚨 NETWORK ALERT\n\n"
                f"Interface: {NETWORK_INTERFACE}\n"
                f"Status: DOWN"
            )

        elif current_interface_status == "up":
            send_notification(
                f"✅ NETWORK RECOVERY\n\n"
                f"Interface: {NETWORK_INTERFACE}\n"
            f"Status: UP"
            )

    else:
        print("[STATE] interface unchanged")

    states["interface"] = current_interface_status

    for name, address in TARGETS.items():
        reachable, latency, packet_loss = ping_target(address)

        #current_status = "up" if reachable else "down"
        if packet_loss == 100:
            current_status = "down"
        elif packet_loss > 0:
            current_status = "degraded"
        else:
            current_status = "up"
        
        previous_status = states.get(name) 

        if reachable:
            if latency is not None:    
                print(f"[UP] {name} ({address}) - {latency:.2f} ms - {packet_loss:.0f}% packet loss")
            else:
                print(f"[DOWN] {name} ({address})")
        else:
            print(f"[DOWN] {name} ({address})")

        if previous_status is None:
            print(
                f"[STATE] {name} baseline set to " 
                f"{current_status}"
            )
        elif previous_status != current_status:
            print(
                f"[STATE] {name}: "
                f"{previous_status} -> {current_status}"
            )

            if current_status == "degraded":
                send_notification(
                    f"🚨 NETWORK DEGRADED \n\n"
                    f"Target: {name} \n"
                    f"Adress: {address}\n"
                    f"Packet loss: {packet_loss:.0f}% \n"
                    f"Latency: {latency:.2f} ms"
                    if latency is not None
                    else
                    f"⚠️ NETWORK DEGRADED\n\n"
                    f"Target: {name} \n"
                    f"Adress: {address} \n"
                    f"Packet loss: {packet_loss:.0f}%"
                )
            elif current_status == "down":
                send_notification(
                    f"🚨 NETWORK DOWN\n\n"
                    f"Target: {name}\n"
                    f"Address: {Address}\n"
                    f"Packet loss: {packet_loss:.0f}%"
                )
            elif current_status == "up":
                send_notification(
                    f"✅ NETWORK RECOVERY \n\n"
                    f"Target: {name}\n"
                    f"Address: {address}\n"
                    f"Status: UP\n"
                    f"Packet loss: {packet_loss:.0f}%\n"
                    f"Latency: {latency:.2f} ms"
                    if latency is not None
                    else
                    f"✅ NETWORK RECOVERY\n\n"
                    f"Target: {name}\n"
                    f"address: {address}\n"
                    f"Status: UP"
                )

        else:
            print(f"[STATE] {name} unchanged")
        states[name] = current_status

    save_states(states)

check_targets()


