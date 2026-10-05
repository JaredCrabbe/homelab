# Homelab Overview

## Purpose

This homelab is a practical Linux and infrastructure learning environment built on Fedora Linux, Docker Compose, network storage, self-hosted services, monitoring, automation, and Git. It is developed incrementally, with each project reinforcing skills from earlier work.

## Environment

- **Host OS:** Fedora Linux 44 with Hyprland
- **Desktop setup:** Dual-boot with Windows
- **CPU / memory:** Intel Core i5-10400F, 16 GB RAM
- **GPU:** NVIDIA GeForce RTX 4060
- **Primary storage:** 1 TB NVMe SSD
- **NAS storage:** 2.7 TB external Western Digital HDD, ext4, mounted at `/srv/nas`
- **Repository:** `~/homelab`, tracked with Git and pushed to GitHub over SSH
- **Container platform:** Docker Engine and Docker Compose

## Project progression and current projects

1. Fedora/Linux foundation and system administration
2. Docker Engine, Docker Compose, container lifecycle, volumes, and networking
3. Nginx web-server container and custom HTML content
4. Git-managed infrastructure configuration and project documentation
5. NAS disk preparation, ext4, persistent mounting, and Linux permissions
6. Samba/SMB network file sharing for Windows access
7. Plex Media Server with persistent application data and hardware/transcoding troubleshooting
8. Docker health monitor written in Python, using Docker events, state persistence, startup reconciliation, and ntfy notifications
9. Nginx Proxy Manager for reverse-proxy management
10. AdGuard Home for local DNS filtering
11. Homepage dashboard for service access
12. Automated NAS backups with systemd scheduling, retention, SHA-256 checksums, verification, and failure notifications
12. Network monitor written in Python for interface state, gateway/internet reachability, latency, packet loss, and state-change alerts
13. Tailscale remote access for secure access to the homelab from outside the local network

## Current service and automation capabilities

- **Linux administration:** packages, users/groups, filesystem permissions, disks, logs, and systemd
- **Containerised services:** Nginx, Samba, Plex, Nginx Proxy Manager, AdGuard Home, Homepage, Docker monitor, and ntfy
- **Storage:** NAS directory structure under `/srv/nas/{media,documents,backups,shares}`
- **Monitoring:** Docker health/state monitoring and network connectivity monitoring
- **Notifications:** ntfy alerts for Docker/network state changes and backup failures
- **Backups:** daily scheduled snapshots, seven-backup retention, checksums, checksum verification, incomplete-backup cleanup, and a successful restore/verification test
- **Automation:** Python scripts and systemd services/timers
- **Remote access:** Tailscale for secure remote access to the homelab without relying on direct public exposure of internal services
- **Version control:** Git commits, GitHub SSH authentication, and documentation tracked alongside configuration

## Monitoring and scheduled jobs

The Docker monitor runs as `homelab-monitor.service` and restarts after failure. The backup job runs daily at 13:00 using `homelab-backup.timer`. The network monitor is designed as a short `oneshot` check run periodically by `homelab-network-monitor.timer` (every minute after its initial boot delay, once enabled and verified).

Network monitoring checks interface `enp3s0`, gateway `192.168.10.1`, and internet target `1.1.1.1`. It tracks `up`, `degraded`, and `down` states and sends ntfy notifications only when the saved state changes.

## Repository layout

```text
homelab/
├── compose/
│   ├── nginx/
│   ├── samba/
│   ├── plex/
│   ├── nginx-proxy-manager/
│   ├── adguard-home/
│   ├── homepage/
│   ├── homelab-monitor/
│   └── ntfy/
├── scripts/
│   ├── homelab-backup/
│   └── network-monitor/
├── docs/
└── README.md
```

The exact set of Compose directories can evolve as services are added or reorganised. Secrets and runtime state such as `.env` and `state.json` should not be committed when they contain private or machine-specific data.

## Backup project status

**Completed and tested.** The backup script creates timestamped backups under `/srv/nas/backups/homelab`, retains the most recent seven snapshots, creates SHA-256 checksums, verifies backup contents, and cleans up incomplete runs. The job is scheduled daily at 13:00 through systemd and depends on `/srv/nas` being mounted. A restore/verification test confirmed that the backed-up files passed `sha256sum -c checksums.sha256`.

## Current next steps

Automated backups are no longer a planned project; they are implemented and tested. The current focus is to finish verifying the network monitor's systemd timer and maintain the homelab documentation as the environment grows. Future ideas can include improving observability, documenting recovery procedures, and adding security-focused projects, but these are not represented as completed work.
