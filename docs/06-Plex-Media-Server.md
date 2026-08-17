# Plex Media Server

## Overview

Plex was added as a self-hosted media service running in Docker.

The Plex project was also used to learn about GPU access, Docker runtime configuration, Linux device permissions, and troubleshooting hardware/software integration.

## Container

The Plex container uses the LinuxServer.io Plex image.

The container was configured to use the system's media/transcoding hardware, including `/dev/dri` devices.

The Plex logs confirmed that the container could access:

```text
/dev/dri/renderD128
/dev/dri/card1
```

## Health check

Plex has a Docker health check based on the local Plex identity endpoint:

```text
curl -fsS HTTP://127.0.0.1:32400/identity >/dev/null || exit 1
```

This allows Docker to report whether Plex is healthy.

## NVIDIA troubleshooting

A real startup failure occurred where Plex could not create its container task because Docker attempted to mount an NVIDIA library that no longer existed:

```text
failed to fulfil mount request:
open /usr/lib64/libEGL_nvidia.so.610.43.03:
no such file or directory
```

The host had newer NVIDIA 610.57 libraries installed.

`nvidia-smi` also reported:

```text
Failed to initialize NVML:
Driver/library version mismatch
```

The installed packages showed multiple NVIDIA kernel module versions, including the older 610.43.03 version and newer 610.57.04 packages.

The NVIDIA container toolkit was installed and Docker reported the NVIDIA runtime and CDI devices.

A system restart resolved the driver/library mismatch and Plex subsequently started correctly.

## Monitoring integration

The Plex failure became a useful real-world test of the homelab monitor.

After the NVIDIA issue was fixed, the monitor detected Plex recovering and sent a notification containing:

- Container name
- Status
- Host
- Recovery time
- Downtime

## Skills demonstrated

- Docker Compose
- Plex deployment
- Docker health checks
- `/dev/dri` device access
- NVIDIA container integration
- NVIDIA driver troubleshooting
- `nvidia-smi`
- `nvidia-container-cli`
- Docker runtime troubleshooting
- Service monitoring
