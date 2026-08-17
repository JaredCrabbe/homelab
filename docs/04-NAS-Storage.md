# NAS Storage

## Overview

A 2.7 TB external Western Digital drive was repurposed as storage for the homelab NAS.

The drive was partitioned and formatted as ext4.

## Storage device

The external disk was identified as:

```text
WDC WD30NMZW-11LG6S1
```

The NAS partition was:

```text
/dev/sda1
```

Filesystem:

```text
ext4
```

Label:

```text
NAS
```

Mount point:

```text
/srv/nas
```

## Directory structure

The NAS storage was organised into:

```text
/srv/nas/
├── backups/
├── documents/
├── media/
└── shares/
```

## Permissions

Linux ownership and group permissions were configured so that the NAS storage could be managed safely by the appropriate users/groups.

The `nas` group was used for shared access.

The storage directory used permissions including the setgid bit so new files/directories could inherit the intended group.

## Skills demonstrated

- Identifying disks
- Partitioning
- Filesystem selection
- ext4
- Mount points
- Linux ownership
- Linux groups
- Shared directory permissions
- NAS directory organisation

## Future work

The existing NAS storage is intended to support automated backups and other homelab services.
