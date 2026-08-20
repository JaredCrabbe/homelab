# Homelab

My personal Linux-based homelab used to build practical experience with Linux administration, Docker, networking, storage, self-hosted services, automation, monitoring, and backup/recovery.

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
- Backup and recovery
- Data integrity verification
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

The current environment is built primarily around Docker containers managed with Docker Compose, with additional Python automation managed through systemd.

```text
                         Homelab Host
                          Fedora Linux
                               |
              +----------------+----------------+
              |                                 |
              v                                 v
         Docker Engine                       systemd
              |                                 |
    +---------+---------+             +---------+---------+
    |         |         |             |                   |
    v         v         v             v                   v
Networking Services   Storage    Homelab Monitor     Backup System
    |         |         |             |                   |
AdGuard    Homepage   NAS HDD          v                   v
NPM        Plex       Samba           ntfy            /srv/nas/backups
ntfy                                    |                   |
                                        v                   v
                                  Notifications        SHA-256 Verify
                                                            |
                                                            v
                                                       Retention
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
| Homelab Backup | Automated configuration backup and integrity verification |
| Nginx | Web server and Docker learning project |

---

## Project Structure

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
    └── homelab-backup/
        └── backup.py
```

The `compose/` directory contains the Docker infrastructure configuration.

The `scripts/` directory contains host-level automation that does not require Docker.

The `docs/` directory contains detailed documentation explaining what was built, why it was built, problems encountered, solutions, testing, and lessons learned.

The root `README.md` serves as the overview and entry point.

---

## Projects

### 00 — Homelab Overview

The overall homelab project and its goals.

[Documentation](docs/00-Homelab-Overview.md)

### 01 — Fedora/Linux Foundation

The Linux environment used as the foundation for the homelab.

[Documentation](docs/01-Fedora-Linux-Foundation.md)

### 02 — Docker & Containerization

Learning Docker Engine, containers, images, volumes, networking, and Docker Compose.

[Documentation](docs/02-Docker-and-Compose.md)

### 03 — Nginx

A simple Dockerised web server used as an early Docker and Compose project.

[Documentation](docs/03-Nginx-Container.md)

### 04 — NAS Storage

A 2.7 TB external HDD configured as NAS storage and mounted at `/srv/nas`.

[Documentation](docs/04-NAS-Storage.md)

### 05 — Samba / SMB

Network file sharing using Samba, allowing Windows and other clients to access the NAS.

[Documentation](docs/05-Samba-SMB.md)

### 06 — Plex

Self-hosted media server running in Docker, including GPU/transcoding configuration.

[Documentation](docs/06-Plex-Media-Server.md)

### 07 — Homelab Monitor

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

[Documentation](docs/07-Homelab-Monitor.md)

### 08 — Automated Backups

A custom Python backup system that automatically protects the homelab configuration.

The backup system currently provides:

- Daily automated backups
- NAS-backed storage
- Timestamped backup directories
- Seven-backup retention
- File and directory exclusions
- SHA-256 checksum generation
- Backup integrity verification
- Corruption detection
- Automatic cleanup of incomplete backups
- systemd service management
- systemd timer scheduling
- NAS mount dependency
- Failure detection
- ntfy failure notifications
- Tested restore procedure

Backups are stored under:

```text
/srv/nas/backups/homelab
```

The backup runs automatically every day at:

```text
13:00
```

[Documentation](docs/08-Automated-backups.md)

### 09 — Nginx Proxy Manager

Reverse-proxy infrastructure for routing web requests to internal services.

[Documentation](docs/09-nginx-proxy-manager.md)

### 10 — AdGuard Home

Local DNS and network-level ad blocking.

[Documentation](docs/10-adguard-home.md)

### 11 — Homepage

Central dashboard for accessing and monitoring homelab services.

[Documentation](docs/11-homepage.md)

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

## Automated Backups

The homelab configuration is automatically backed up to the NAS using a custom Python backup system.

The backup script is located at:

```text
~/homelab/scripts/homelab-backup/backup.py
```

Backups are stored at:

```text
/srv/nas/backups/homelab
```

Each backup uses a timestamped directory:

```text
YYYY-MM-DD_HH-MM-SS
```

The system retains the newest seven backups.

### Backup Process

```text
13:00 systemd timer
        |
        v
Check /srv/nas mount dependency
        |
        v
Run backup.py
        |
        v
Copy homelab configuration
        |
        v
Generate SHA-256 checksums
        |
        v
Verify copied files
        |
   +----+----+
   |         |
 PASS       FAIL
   |         |
   v         v
Keep      Remove incomplete
backup    backup
   |         |
   v         v
Apply     systemd failure
retention    |
             v
            ntfy
             |
             v
        Notification
```

### Integrity Verification

Every completed backup contains:

```text
checksums.sha256
```

The backup script calculates SHA-256 hashes for the copied files and verifies the copied data before considering the backup successful.

Corruption detection was tested by deliberately modifying a backed-up file after checksum generation.

The system correctly detected:

```text
Checksum mismatch: .gitignore
```

and removed the invalid backup.

### Failure Handling

If copying or verification fails:

1. The error is reported.
2. The incomplete backup directory is removed.
3. Python exits with a non-zero status.
4. systemd marks the backup service as failed.
5. `homelab-backup-failure.service` is triggered.
6. An ntfy notification is sent.

### Restore Testing

A backup was restored into a temporary clean location:

```text
/tmp/homelab-restore-test
```

The restored files were verified using:

```bash
sha256sum -c checksums.sha256
```

Every restored file returned:

```text
OK
```

This confirmed that the stored backup could be successfully restored and passed integrity verification.

---

## Storage

The NAS storage is provided by a 2.7 TB external HDD.

The main storage mount is:

```text
/srv/nas
```

The NAS contains:

```text
backups/
documents/
media/
shares/
```

Samba provides network access to the storage using SMB.

The `backups/` directory also stores the automated homelab configuration backups.

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

### Notifications

ntfy provides local notification delivery for monitoring and backup failures.

---

## Security & Configuration

Secrets and environment-specific configuration are kept outside version control.

`.env` files are intentionally excluded from Git using `.gitignore`.

Runtime files such as monitor state, logs, Python cache files, and other temporary data are also excluded where appropriate.

The backup system can preserve configuration files that are excluded from Git, providing a local recovery mechanism without publishing sensitive configuration to the Git repository.

Passwords, tokens, and other sensitive values should never be committed to version control.

---

## Version Control

The homelab is managed with Git.

The repository tracks:

- Docker Compose files
- Python source code
- Configuration files
- Documentation
- Infrastructure changes
- Automation scripts

Sensitive files such as `.env`, logs, Python cache files, and runtime state that should not be version controlled are excluded where appropriate.

Git provides version history for the homelab configuration, while the NAS backup system provides an additional local recovery mechanism.

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
- systemd timer scheduling
- NAS mount dependencies
- Backup retention
- Python exception handling
- Incomplete backup cleanup
- SHA-256 checksum generation
- Backup integrity verification
- Corruption detection
- systemd failure handling
- Automated failure notifications
- Backup restore testing

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
- [x] Automated daily backups
- [x] Backup retention
- [x] Backup integrity verification
- [x] Incomplete backup cleanup
- [x] Backup failure notifications
- [x] Backup restore testing
- [x] Git documentation

### Next

- [ ] Expand monitoring as new services are added
- [ ] Continue improving infrastructure documentation
- [ ] Continue building new homelab services and automation

---

## Skills Demonstrated

This homelab demonstrates practical experience with:

### Linux

- Fedora
- systemd
- systemd timers
- journalctl
- permissions
- mounts
- filesystems
- services
- troubleshooting

### Docker

- Docker Engine
- Docker Compose
- Containers
- Images
- Volumes
- Health checks
- Docker events
- Container networking

### Networking

- DNS
- SMB
- HTTP/HTTPS
- Reverse proxies
- Port forwarding
- Local network services

### Automation

- Python
- subprocess
- Docker CLI interaction
- JSON state management
- Event-driven monitoring
- ntfy notifications
- Automated backups
- Backup retention
- Exception handling
- Failure handling

### Backup & Recovery

- NAS-based backups
- Automated scheduling
- Backup retention policies
- SHA-256 hashing
- Integrity verification
- Corruption detection
- Incomplete backup cleanup
- Restore procedures
- Restore verification

### Development

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
5. Verify the solution.
6. Document what happened.
7. Improve the infrastructure where appropriate.

This makes the homelab both a learning environment and a practical demonstration of troubleshooting and IT infrastructure skills.