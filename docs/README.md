# Homelab

My personal Linux-based homelab used to build practical experience with Linux administration, Docker, networking, storage, self-hosted services, automation, and monitoring.

The homelab is both a learning environment and a practical portfolio of infrastructure projects.

---

## Goals

The main goals of this homelab are to gain practical experience with:

- Linux system administration
- Docker and Docker Compose
- Networking and DNS
- NAS and network storage
- SMB/Samba
- Reverse proxies
- Self-hosted applications
- Python automation
- Service monitoring
- systemd
- Git and version control
- Troubleshooting real infrastructure problems

---

## Hardware & Host

The homelab currently runs on my personal PC.

### Host OS

- Fedora Linux
- Hyprland desktop environment

### Hardware

- Intel Core i5-10400F
- NVIDIA GeForce RTX 4060
- 16 GB RAM
- 1 TB NVMe SSD
- 2.7 TB external HDD used for NAS storage

The system is also used as a normal desktop, so the homelab is designed around making efficient use of existing hardware rather than relying on dedicated server hardware.

---

## Architecture

The current environment is built primarily around Docker containers managed with Docker Compose.

```text
                         Homelab Host
                       Fedora Linux
                            |
                     Docker Engine
                            |
       +--------------------+--------------------+
       |                    |                    |
       v                    v                    v
   Networking            Services             Storage
       |                    |                    |
   AdGuard Home         Homepage              NAS HDD
   Nginx Proxy          Plex                  Samba
   Manager
       |
       +--------------------+
                            |
                            v
                    Homelab Monitor
                            |
                            v
                           ntfy
                            |
                            v
                     Notifications
```

---

## Services

| Service | Purpose |
|---|---|
| Homepage | Homelab dashboard |
| AdGuard Home | DNS and network-level ad blocking |
| Nginx Proxy Manager | Reverse proxy and web service routing |
| Plex | Self-hosted media server |
| Samba | Network file sharing / NAS |
| ntfy | Notification delivery |
| Homelab Monitor | Docker health and container-state monitoring |
| Nginx | Web server and Docker learning project |

---

## Project Structure

```text
homelab/
├── .gitignore
├── .env
├── README.md
│
├── compose/
│   ├── nginx/
│   ├── samba/
│   ├── plex/
│   ├── nginx-proxy-manager/
│   ├── adguard-home/
│   ├── homepage/
│   └── homelab-monitor/
│
└── docs/
    ├── 01-homelab-overview.md
    ├── 02-fedora-linux-foundation.md
    ├── 03-docker-containerization.md
    ├── 04-nginx.md
    ├── 05-nas-storage.md
    ├── 06-samba.md
    ├── 07-plex.md
    ├── 08-nginx-proxy-manager.md
    ├── 09-adguard-home.md
    ├── 10-homepage.md
    ├── 11-homelab-monitor.md
    └── 12-automated-backups.md
```

The `compose/` directory contains the actual infrastructure configuration.

The `docs/` directory contains detailed documentation explaining what was built, why it was built, problems encountered, solutions, and lessons learned.

The root `README.md` serves as the overview and entry point.

---

## Projects

### 01 — Homelab Overview

The overall homelab project and its goals.

[Documentation](docs/01-homelab-overview.md)

### 02 — Fedora/Linux Foundation

The Linux environment used as the foundation for the homelab.

[Documentation](docs/02-fedora-linux-foundation.md)

### 03 — Docker & Containerization

Learning Docker Engine, containers, images, volumes, networking, and Docker Compose.

[Documentation](docs/03-docker-containerization.md)

### 04 — Nginx

A simple Dockerised web server used as an early Docker and Compose project.

[Documentation](docs/04-nginx.md)

### 05 — NAS Storage

A 2.7 TB external HDD configured as NAS storage and mounted at `/srv/nas`.

[Documentation](docs/05-nas-storage.md)

### 06 — Samba / SMB

Network file sharing using Samba, allowing Windows and other clients to access the NAS.

[Documentation](docs/06-samba.md)

### 07 — Plex

Self-hosted media server running in Docker, including GPU/transcoding configuration.

[Documentation](docs/07-plex.md)

### 08 — Nginx Proxy Manager

Reverse-proxy infrastructure for routing web requests to internal services.

[Documentation](docs/08-nginx-proxy-manager.md)

### 09 — AdGuard Home

Local DNS and network-level ad blocking.

[Documentation](docs/09-adguard-home.md)

### 10 — Homepage

Central dashboard for accessing and monitoring homelab services.

[Documentation](docs/10-homepage.md)

### 11 — Homelab Monitor

A custom Python monitoring service that watches Docker health and container lifecycle events.

The monitor currently handles:

- Healthy containers
- Unhealthy containers
- Containers entering a stopped state
- Container startup
- Recovery notifications
- Persistent state
- Startup state reconciliation
- Downtime tracking
- ntfy notifications
- systemd service management

[Documentation](docs/11-homelab-monitor.md)

### 12 — Automated Backups

Planned project.

The goal is to develop an automated backup system for important homelab data and configuration.

[Documentation](docs/12-automated-backups.md)

---

## Monitoring

The homelab includes a custom Python monitoring application.

```text
Docker Events
     |
     v
monitor.py
     |
     +--> state.json
     |
     +--> State reconciliation
     |
     +--> Incident detection
     |
     v
    ntfy
     |
     v
Notifications
```

The monitor runs as a systemd service:

```text
homelab-monitor.service
```

It monitors:

```text
Homepage
adguard-home
nginx-proxy-manager
plex
samba
```

State is persisted in:

```text
state.json
```

This allows the monitor to remember incidents across restarts rather than treating every startup as a new incident.

---

## Storage

The NAS storage is provided by a 2.7 TB external HDD.

The main storage mount is:

```text
/srv/nas
```

The NAS contains directories for areas such as:

```text
backups/
documents/
media/
shares/
```

Samba provides network access to the storage using SMB.

---

## Networking

The homelab includes several network-facing services.

### DNS

AdGuard Home provides local DNS functionality and filtering.

### Reverse Proxy

Nginx Proxy Manager provides reverse-proxy functionality for web services.

### SMB

Samba provides network file sharing over SMB.

Modern SMB connections use TCP port:

```text
445
```

---

## Security & Configuration

Secrets and environment-specific configuration are kept outside version control.

The root `.env` file is intentionally excluded from Git using `.gitignore`.

The repository should therefore contain configuration templates or documentation rather than passwords, tokens, or other sensitive values.

---

## Version Control

The homelab is managed with Git.

The repository tracks:

- Docker Compose files
- Python source code
- Configuration files
- Documentation
- Infrastructure changes

Sensitive files such as `.env` and runtime state that should not be version controlled are excluded where appropriate.

---

## Troubleshooting & Lessons Learned

A major part of this homelab is learning by solving real problems.

Examples include:

- Docker volume and bind-mount configuration
- Samba configuration and permissions
- Windows SMB access
- Docker health checks
- Docker event handling
- Persistent monitor state
- systemd service behaviour
- Startup state reconciliation
- Container stopped-state detection
- ntfy notification encoding
- NVIDIA container/runtime issues
- NVIDIA driver/library mismatches affecting Plex
- Container startup failures

These problems have been documented in the individual project documentation where relevant.

---

## Current Status

### Completed

- [x] Fedora/Linux homelab foundation
- [x] Docker Engine
- [x] Docker Compose
- [x] Nginx
- [x] NAS storage
- [x] Samba/SMB
- [x] Plex
- [x] Nginx Proxy Manager
- [x] AdGuard Home
- [x] Homepage
- [x] ntfy notifications
- [x] Custom Docker health monitor
- [x] Persistent monitor state
- [x] Startup state reconciliation
- [x] Stopped-container detection
- [x] systemd integration
- [x] Git documentation

### Next

- [ ] Automated backups
- [ ] Continue improving NAS backup strategy
- [ ] Expand monitoring as new services are added
- [ ] Continue improving infrastructure documentation

---

## Skills Demonstrated

This homelab demonstrates practical experience with:

**Linux**

- Fedora
- systemd
- journalctl
- permissions
- mounts
- filesystems
- services
- troubleshooting

**Docker**

- Docker Engine
- Docker Compose
- Containers
- Images
- Volumes
- Health checks
- Docker events
- Container networking

**Networking**

- DNS
- SMB
- HTTP/HTTPS
- Reverse proxies
- Port forwarding
- Local network services

**Automation**

- Python
- subprocess
- Docker API/CLI interaction
- JSON state management
- Event-driven monitoring
- ntfy notifications

**Development**

- Git
- Git commits
- Configuration management
- Documentation
- Troubleshooting

---

## Philosophy

The homelab is intentionally built around real problems rather than following a single tutorial.

When something breaks, the goal is to:

1. Identify the problem.
2. Gather evidence.
3. Test possible causes.
4. Fix the underlying issue.
5. Document what happened.
6. Improve the infrastructure where appropriate.

This makes the homelab both a learning environment and a practical demonstration of troubleshooting and IT infrastructure skills.
