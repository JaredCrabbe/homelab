# NAS Storage

## Overview

A 2.7 TB external Western Digital HDD was repurposed as storage for the homelab. The disk was formatted with ext4 and mounted at `/srv/nas`.

## Storage device

- Model: `WDC WD30NMZW-11LG6S1`
- Filesystem: `ext4`
- Filesystem label: `NAS`
- Mount point: `/srv/nas`

Use the current device path reported by the host rather than assuming the disk will always be assigned the same `/dev/sdX` name. The filesystem label and mount configuration help keep the mount predictable.

## Directory structure

```text
/srv/nas/
├── backups/
├── documents/
├── media/
└── shares/
```

## Mounting and permissions

The filesystem is configured for persistent mounting through `/etc/fstab`. After changing the mount configuration, `sudo mount -a` can be used to validate it, and systemd may need to reload unit configuration when relevant.

A `nas` group is used for shared access. The NAS root and shared directories use `root:nas` ownership with setgid directory permissions (`2770`) so group ownership can be inherited by new content. The user `jared` belongs to the `nas` group.

## Services using the NAS

- Samba exposes files from the shares directory over SMB.
- Plex reads media stored on the NAS.
- The backup system writes timestamped backup snapshots beneath `/srv/nas/backups/homelab`.

The backup system uses a systemd mount dependency so it does not intentionally run without the NAS mount being available.

## Skills demonstrated

Disk identification, filesystem preparation, ext4, persistent mounts, Linux ownership and groups, setgid permissions, storage organisation, and integrating storage with containerised services and scheduled backups.
