# Fedora Linux Foundation

## Overview

Fedora Linux 44 is the operating-system foundation for the homelab. The machine uses Hyprland and is dual-booted with Windows, allowing the existing gaming PC to double as a Linux learning environment without requiring separate hardware.

## Hardware context

- Intel Core i5-10400F
- 16 GB RAM
- NVIDIA GeForce RTX 4060
- 1 TB NVMe SSD
- 2.7 TB external HDD used for NAS storage

## Administration skills practised

- Navigating and managing files from the terminal
- Installing and updating packages with Fedora's package manager
- Managing users, groups, ownership, and permissions
- Identifying disks, filesystems, and mount points
- Configuring persistent mounts through `/etc/fstab`
- Managing and troubleshooting systemd services and timers
- Inspecting logs with `journalctl`
- Inspecting network interfaces and connectivity
- Investigating hardware and NVIDIA driver/runtime issues
- Using Git to track infrastructure configuration and documentation

## systemd usage

systemd is used for long-running monitoring and scheduled automation. Examples include the Docker health monitor, daily NAS backup job and its timer, backup-failure notification handling, and the network monitor's periodic `oneshot` check.

## Design principle

The homelab is being built on the existing Fedora installation rather than repeatedly reinstalling the operating system. Projects are kept in version-controlled directories and documented as the configuration develops.
