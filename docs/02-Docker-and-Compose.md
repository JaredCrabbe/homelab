# Docker and Docker Compose

## Overview

Docker was introduced as the main platform for running homelab services.

Docker Engine was installed and verified with the standard `hello-world` container.

## Project structure

Services were separated into individual project directories under the homelab repository.

Example structure:

```text
homelab/
└── compose/
    ├── nginx/
    ├── samba/
    ├── plex/
    └── homelab-monitor/
```

## Docker concepts practiced

- Images
- Containers
- Container names
- Ports
- Bind mounts
- Volumes
- Docker Compose
- Compose files
- Container logs
- `docker inspect`
- `docker ps`
- Docker events
- Docker health checks

## Docker Engine vs Docker Desktop

The homelab uses Docker Engine rather than Docker Desktop because the environment is a Linux server/homelab setup.

## Git integration

Docker projects were stored inside the Git-controlled homelab directory so configuration could be tracked and changes committed.

## Result

Docker became the common deployment layer for the homelab services.
