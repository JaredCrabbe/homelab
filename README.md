# Homelab

My personal Linux-based homelab used to build practical experience with Linux administration, Docker, networking, storage, self-hosted services, automation, monitoring, and backup/recovery.

The homelab is both a learning environment and a practical portfolio of infrastructure projects.

---

## Homelab

The environment currently runs on my personal PC using:

- Fedora Linux
- Intel Core i5-10400F
- NVIDIA GeForce RTX 4060
- 16 GB RAM
- 1 TB NVMe SSD
- 2.7 TB external HDD for NAS storage

Most services run as Docker containers managed with Docker Compose, while host-level automation uses Python and systemd.

---

## Services

| Service | Purpose |
|---|---|
| Homepage | Central homelab dashboard |
| AdGuard Home | DNS and network-level ad blocking |
| Nginx Proxy Manager | Reverse proxy and service routing |
| Plex | Self-hosted media server |
| Samba | SMB network file sharing |
| ntfy | Notification delivery |
| Homelab Monitor | Docker health and state monitoring |
| Homelab Backup | Automated backup and integrity verification |

---

## Projects

| # | Project | What I Learned |
|---|---|---|
| 00 | [Homelab Overview](docs/00-Homelab-Overview.md) | Infrastructure planning and architecture |
| 01 | [Fedora Linux Foundation](docs/01-Fedora-Linux-Foundation.md) | Linux administration and system configuration |
| 02 | [Docker & Compose](docs/02-Docker-and-Compose.md) | Containers, images, volumes, networking and Compose |
| 03 | [Nginx Container](docs/03-Nginx-Container.md) | Docker deployment, ports and bind mounts |
| 04 | [NAS Storage](docs/04-NAS-Storage.md) | Filesystems, mounting, permissions and storage |
| 05 | [Samba / SMB](docs/05-Samba-SMB.md) | Network file sharing and Windows/Linux interoperability |
| 06 | [Plex Media Server](docs/06-Plex-Media-Server.md) | Media hosting, Docker and GPU configuration |
| 07 | [Homelab Monitor](docs/07-Homelab-Monitor.md) | Python, Docker events, state tracking, systemd and notifications |
| 08 | [Automated Backups](docs/08-Automated-backups.md) | Python automation, systemd timers, SHA-256 verification and recovery |
| 09 | [Nginx Proxy Manager](docs/09-nginx-proxy-manager.md) | Reverse proxies and internal service routing |
| 10 | [AdGuard Home](docs/10-adguard-home.md) | DNS and network filtering |
| 11 | [Homepage](docs/11-homepage.md) | Service dashboards and Docker integration |

---

## Repository Structure

```text
homelab/
├── .gitignore
├── README.md
│
├── compose/
│   ├── adguard-home/
│   ├── homelab-monitor/
│   ├── homepage/
│   ├── nginx-proxy-manager/
│   ├── ntfy/
│   ├── plex/
│   └── samba/
│
├── docs/
│   ├── 00-Homelab-Overview.md
│   ├── 01-Fedora-Linux-Foundation.md
│   ├── 02-Docker-and-Compose.md
│   ├── 03-Nginx-Container.md
│   ├── 04-NAS-Storage.md
│   ├── 05-Samba-SMB.md
│   ├── 06-Plex-Media-Server.md
│   ├── 07-Homelab-Monitor.md
│   ├── 08-Automated-backups.md
│   ├── 09-nginx-proxy-manager.md
│   ├── 10-adguard-home.md
│   └── 11-homepage.md
│
└── scripts/
    ├── homelab-backup/
    │   └── backup.py
    │
    └── network-monitor/
        └── network_monitor.py
```

`compose/` contains Docker infrastructure.

`scripts/` contains host-level Python automation.

`docs/` contains the detailed build notes, configuration, troubleshooting, testing, and lessons learned for each project.

---

## Skills Demonstrated

### Linux

- Fedora Linux
- systemd services and timers
- journalctl
- Filesystems and mounts
- Users, groups and permissions
- Service troubleshooting

### Docker

- Docker Engine
- Docker Compose
- Container networking
- Volumes and bind mounts
- Health checks
- Docker events

### Networking

- DNS
- SMB
- HTTP/HTTPS
- Reverse proxies
- Local network services

### Automation & Monitoring

- Python
- Event-driven monitoring
- Persistent state
- Failure handling
- ntfy notifications
- Automated backups
- SHA-256 integrity verification
- Restore testing

### Development

- Git
- GitHub
- Version control
- Configuration management
- Technical documentation
- Troubleshooting

---

## Current Status

### Completed

- [x] Linux homelab foundation
- [x] Docker and Docker Compose
- [x] Nginx
- [x] NAS storage
- [x] Samba / SMB
- [x] Plex Media Server
- [x] Nginx Proxy Manager
- [x] AdGuard Home
- [x] Homepage
- [x] ntfy notifications
- [x] Custom Docker health monitor
- [x] Automated backup system
- [x] Backup integrity verification
- [x] Backup failure notifications
- [x] Restore testing

### In Progress

- [ ] Basic network monitoring

---

## Current Project

### HOMELAB-18 — Basic Network Monitoring

Building a Python-based network monitoring system to gain practical experience with:

- Host availability monitoring
- ICMP/ping
- Latency
- Network service checks
- Incident detection
- Recovery detection
- Persistent monitoring state
- ntfy alerts

The project will be documented once completed.

---

## Purpose

This homelab is intentionally built by working through real infrastructure problems rather than following a single end-to-end tutorial.

The general process for each project is:

1. Plan the project.
2. Build the initial implementation.
3. Test it.
4. Break things deliberately where useful.
5. Troubleshoot problems.
6. Verify the solution.
7. Document the finished project.

The goal is to develop practical IT skills while creating a portfolio that demonstrates the systems I have actually built and maintained.
