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
3. Git-managed infrastructure configuration and project documentation
4. NAS disk preparation, ext4, persistent mounting, and Linux permissions
5. Samba/SMB network file sharing for Windows access
6. Plex Media Server with persistent application data and hardware/transcoding troubleshooting
7. Docker health monitor written in Python, using Docker events, state persistence, startup reconciliation, and ntfy notifications
8. Nginx Proxy Manager for reverse-proxy management
9. AdGuard Home for local DNS filtering
10. Homepage dashboard for service access
11. Automated NAS backups with systemd scheduling, retention, SHA-256 checksums, verification, and failure notifications
12. Network monitor written in Python for interface state, gateway/internet reachability, latency, packet loss, and state-change alerts
13. Tailscale remote access for secure access to the homelab from outside the local network
14. Security hardening: administrative interface isolation, least-privilege Tailscale access, SSH restriction, and firewall range reduction, with post-change validation
15. Prometheus, node_exporter, and Grafana for host metrics collection, 30-day history, and dashboards

## Current service and automation capabilities

- **Linux administration:** packages, users/groups, filesystem permissions, disks, logs, and systemd
- **Containerised services:** Samba, Plex, Nginx Proxy Manager, AdGuard Home, Homepage, Docker monitor, ntfy, Prometheus, node_exporter, and Grafana
- **Storage:** NAS directory structure under `/srv/nas/{media,documents,backups,shares}`
- **Monitoring:** Docker health/state monitoring, network connectivity monitoring, and Prometheus/Grafana host metrics
- **Notifications:** ntfy alerts for Docker/network state changes and backup failures
- **Backups:** daily scheduled snapshots, seven-backup retention, checksums, checksum verification, incomplete-backup cleanup, and a successful restore/verification test
- **Automation:** Python scripts and systemd services/timers
- **Remote access:** Tailscale for secure remote access to the homelab without relying on direct public exposure of internal services
- **Security hardening:** admin interfaces bound to localhost, least-privilege Tailscale access and SSH, and a reduced firewall port set, validated after each change
- **Version control:** Git commits, GitHub SSH authentication, and documentation tracked alongside configuration
- **Metrics and dashboards:** Prometheus (30-day retention) scraping node_exporter, with Grafana dashboards; Prometheus and Grafana are bound to localhost

## Monitoring and scheduled jobs

The Docker monitor runs as `homelab-monitor.service` and restarts after failure. The backup job runs daily at 13:00 using `homelab-backup.timer`. The network monitor is a short `oneshot` check run by `homelab-network-monitor.timer` every minute after its initial boot delay; the timer is enabled and running.

Network monitoring checks interface `enp3s0`, gateway `192.168.10.1`, and internet target `1.1.1.1`. It tracks `up`, `degraded`, and `down` states and sends ntfy notifications only when the saved state changes.

Prometheus scrapes itself and node_exporter every 15 seconds and keeps 30 days of data in a named volume. Grafana reads from Prometheus and shows the Node Exporter Full dashboard. Both are reachable from the host only (`127.0.0.1:9090` and `127.0.0.1:3000`). See [14 Prometheus and Grafana](14-Prometheus-and-Grafana.md).

## Repository layout

```text
homelab/
├── compose/
│   ├── adguard-home/
│   ├── homelab-monitor/
│   ├── homepage/
│   ├── nginx-proxy-manager/
│   ├── ntfy/
│   ├── plex/
│   ├── prometheus/
│   └── samba/
├── scripts/
│   ├── homelab-backup/
│   └── network-monitor/
├── docs/
└── README.md
```

The exact set of Compose directories can evolve as services are added or reorganised. Secrets and runtime state such as `.env` and `state.json` should not be committed when they contain private or machine-specific data.

## Backup project status

**Completed and tested.** The backup script creates timestamped backups under `/srv/nas/backups/homelab`, retains the most recent seven snapshots, creates SHA-256 checksums, verifies backup contents, and cleans up incomplete runs. The job is scheduled daily at 13:00 through systemd and depends on `/srv/nas` being mounted. A restore/verification test confirmed that the backed-up files passed `sha256sum -c checksums.sha256`.

## Security hardening status

**Hardening phase completed and validated.** Admin interfaces for Nginx Proxy Manager and AdGuard Home are bound to localhost, remote access runs through Tailscale with a least-privilege policy and non-root SSH, and the firewall's broad port ranges were removed. Plex is an accepted exception and several reviews are deferred. See [13 Security Hardening](13-Security-Hardening.md).

## Metrics and dashboards status

**Prometheus, node_exporter, and Grafana deployed and verified (2026-10-19).** Host metrics are collected and graphed, and both Prometheus and Grafana are bound to localhost. Per-container metrics and alerting are not yet implemented. See [14 Prometheus and Grafana](14-Prometheus-and-Grafana.md).

## Current next steps

The current focus is to maintain the homelab documentation as the environment grows. Future ideas can include per-container metrics with cAdvisor, alerting to ntfy, the deferred security reviews listed in the hardening document, and documenting recovery procedures, but these are not represented as completed work.

## Documentation index

- [01 Fedora Linux Foundation](01-Fedora-Linux-Foundation.md): OS, hardware, systemd usage, design principle
- [02 Docker and Compose](02-Docker-and-Compose.md): deployment layer and project structure
- [03 NAS Storage](03-NAS-Storage.md): disk, mount, permissions, `/srv/nas` layout
- [04 Samba SMB](04-Samba-SMB.md): Windows file sharing from the NAS
- [05 Plex Media Server](05-Plex-Media-Server.md): media streaming and the NVIDIA incident
- [06 Homelab Monitor](06-Homelab-Monitor.md): Docker health monitor and ntfy alerts
- [07 Automated Backups](07-Automated-backups.md): timer, retention, checksums, restore test
- [08 Nginx Proxy Manager](08-nginx-proxy-manager.md): reverse proxy
- [09 AdGuard Home](09-adguard-home.md): DNS filtering
- [10 Homepage](10-homepage.md): service dashboard
- [11 Network Monitor](11-Network-Monitor.md): interface, gateway and internet checks
- [12 Tailscale Remote Access](12-Tailscale-Remote-Access.md): remote access and access policy
- [13 Security Hardening](13-Security-Hardening.md): admin isolation, least-privilege access, firewall reduction, validation, deferred work
- [14 Prometheus and Grafana](14-Prometheus-and-Grafana.md): host metrics, dashboards, localhost-only access, verification
- [Docker notes](docker-notes.md): concepts, commands, troubleshooting approach
- [Working notes](notes.md): status list and short lessons
- [Ways to Scan a Network](Ways%20to%20Scan%20a%20Network.md): scanning methods and nmap recipes
