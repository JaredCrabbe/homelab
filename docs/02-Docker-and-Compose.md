# Docker and Docker Compose

## Overview

Docker Engine and Docker Compose are the common deployment layer for the homelab's self-hosted services. Docker was installed from the Docker repository and verified with the `hello-world` container.

## Project structure

Services are organised into individual directories under `~/homelab/compose/`, with custom scripts kept under `~/homelab/scripts/` and project notes under `~/homelab/docs/`.

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
└── docs/
```

## Concepts practised

- Images, containers, names, and restart policies
- Publishing host ports to container ports
- Bind mounts for configuration and web content
- Named volumes for persistent application data, including Plex metadata
- Docker Compose project files and lifecycle commands
- Inspecting container state and logs with `docker ps`, `docker inspect`, and `docker logs`
- Docker events and health checks
- Docker bridge networks
- Keeping individual services independently manageable
- Tracking configuration changes with Git

## Docker Engine vs Docker Desktop

The homelab uses Docker Engine on Linux rather than Docker Desktop. Services are managed from the terminal and through Compose files.

## Persistence and configuration

Bind mounts are used where direct host-file management is useful, such as Nginx's custom HTML and Samba configuration. Named Docker volumes are used where Docker-managed persistent application data is preferred. Secrets, environment files, and generated state should be excluded from Git when appropriate.

## Result

Docker provides a repeatable way to deploy and manage the homelab's web, media, DNS, file-sharing, dashboard, and monitoring services.
