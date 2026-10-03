# Homelab Working Notes

This file is for short working notes and lessons that have not yet earned a dedicated project document. The numbered documents in this directory are the source of truth for completed project write-ups.

## Current project status

- Fedora Linux and Hyprland environment established
- Docker Engine and Compose working
- Nginx container deployed with custom HTML
- NAS mounted at `/srv/nas` with ext4 and structured directories
- Samba SMB share configured for network access
- Plex deployed with persistent application data; NVIDIA driver/runtime issue diagnosed and resolved by reboot
- Docker health monitor implemented with state persistence, startup reconciliation, incident timing, and ntfy alerts
- Nginx Proxy Manager deployed
- AdGuard Home deployed
- Homepage dashboard deployed
- Automated backups implemented, scheduled daily at 13:00, with seven-backup retention, SHA-256 verification, cleanup, and failure notification; restore/checksum verification succeeded
- Network monitor implemented for interface, gateway, internet reachability, packet loss, latency, and state-change notifications

## Network monitor

Main path: `~/homelab/scripts/network-monitor/network_monitor.py`

Targets:

- Gateway: `192.168.10.1`
- Internet: `1.1.1.1`
- Interface: `enp3s0`
- ntfy: `http://192.168.10.151:8082/homelab`

The monitor stores previous states in `state.json`. Alerts should only be sent on state transitions. Target states are `up`, `degraded`, and `down`; the interface uses `up`/`down`.

## systemd checks

```bash
systemctl list-timers --all
systemctl status homelab-backup.timer
systemctl status homelab-network-monitor.timer
journalctl -u homelab-backup.service -n 50 --no-pager
journalctl -u homelab-network-monitor.service -n 30 --no-pager
```

## Git workflow

After a project is tested and its documentation updated:

```bash
cd ~/homelab
git status
git add docs scripts compose
git commit -m "describe the change"
git push
```

Review `git status` and staged changes before committing. Do not commit secrets, `.env` files, or private runtime state.
