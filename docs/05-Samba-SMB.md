# Samba / SMB Network Storage

## Overview

Samba was deployed to make the Linux NAS storage accessible to other devices over the network using SMB.

## Storage

The Samba service uses the NAS storage mounted at:

```text
/srv/nas
```

The Samba container exposes SMB on the standard modern SMB port:

```text
445
```

## Docker deployment

Samba was deployed as a Docker container with a dedicated Compose project.

The Samba configuration was mounted into the container using a bind mount.

An early configuration issue occurred because the bind mount path was missing the required `./` prefix. The resulting error indicated that `/etc/samba/smb.conf` did not map to an existing file.

The path was corrected and Samba subsequently started successfully.

## Configuration concepts

The Samba configuration used:

- User-based security
- SMB2 or newer as the minimum protocol
- Shared storage
- Forced user/group settings
- `catia`
- `fruit`
- `streams_xattr`

## Permissions

The Linux NAS permissions were configured alongside Samba permissions.

A test file was created under the shared storage and ownership/permissions were checked to confirm that the Samba configuration and Linux filesystem permissions worked together.

## Windows access

The project included testing access from Windows File Explorer and discussing ways to access the share without repeatedly typing the server IP.

## Skills demonstrated

- SMB
- Samba
- Dockerised Samba
- `smb.conf`
- Network shares
- Port 445
- Linux filesystem permissions
- Windows-to-Linux file sharing
- Docker bind mounts
- Troubleshooting container configuration
