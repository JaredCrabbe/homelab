# Samba / SMB Network Storage

## Overview

Samba runs in Docker and makes the NAS share available to compatible devices, including Windows through File Explorer. The exported share is named `shares` and uses the host directory `/srv/nas/shares`.

## Deployment

Samba has a dedicated Compose project under `~/homelab/compose/samba/`. The configuration file `smb.conf` is bind-mounted into the container. The container logs confirmed Samba started successfully.

SMB is exposed on TCP port `445`. SMB1 is disabled; the minimum protocol is SMB2 or newer.

## Permissions and access

The NAS uses a `nas` group for shared access. The share directory is configured with group-based permissions and setgid inheritance. Test content was created to verify file and directory permissions, including a test file owned by `jared:nas` with mode `660` and a directory using mode `2770`.

Samba's user/share configuration and Linux filesystem permissions both affect whether a client can read or write a file; both layers must be checked during troubleshooting.

## Troubleshooting lesson

An early startup problem came from a missing `./` prefix in a relative bind-mount path for `smb.conf`. Correcting the host path allowed the configuration to mount correctly and Samba to start.

## Skills demonstrated

- SMB and Samba configuration
- Docker Compose and bind mounts
- `smb.conf`
- Modern SMB protocol settings
- Linux ownership, groups, and permissions
- Windows-to-Linux file sharing
- Container log inspection and configuration troubleshooting
