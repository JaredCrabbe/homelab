# Homelab Docker Health Monitor

## Overview

The Docker health monitor is a custom Python service that watches selected homelab containers and sends ntfy notifications when their health or running state changes. It is separate from the network monitor documented in [Network Monitor](12-Network-Monitor.md).

## Monitored containers

The monitor watches the configured service containers, including Homepage, AdGuard Home, Plex, Nginx Proxy Manager, and Samba.

## Detection and state

The monitor listens to Docker events such as health-status changes, container exits, and starts, and uses `docker inspect` to reconcile the actual current container state. It distinguishes healthy, unhealthy, starting, and stopped states.

Previous state is persisted in `state.json`. On startup, the monitor checks live Docker state instead of assuming that the saved state is still accurate. This startup reconciliation helps detect incidents or recoveries that happened while the monitor was offline. State writes use a temporary file and replacement to reduce the chance of a partially written state file.

When an incident is detected, the monitor records when the unhealthy/stopped period began. On recovery, it can calculate downtime and include it in the notification.

## Notifications

Notifications are sent to the local ntfy topic:

```text
http://192.168.10.151:8082/homelab
```

Alerts include the affected container and status. Recovery notifications can include the host, recovery time, and downtime.

If ntfy's published port or binding is ever changed (for example to localhost or Tailscale only), update this URL here and in the [Network Monitor](12-Network-Monitor.md) and [backup](08-Automated-backups.md) notification settings, and check that the phone's ntfy subscription can still reach the server.

## systemd

The service is managed by `homelab-monitor.service`, runs as `jared`, uses the project working directory under `/home/jared/homelab/compose/homelab-monitor`, and starts the Python monitor script. It is configured to restart after failure with a short delay.

## Testing and lessons

The monitor has been exercised with healthy states, unhealthy containers, stopped/started containers, service restarts, state persistence, startup reconciliation, recovery notifications, downtime calculation, and the real Plex/NVIDIA issue.

## Skills demonstrated

Python, Docker events, health checks, `docker inspect`, JSON state persistence, systemd, HTTP notifications, incident timing, Git, and troubleshooting.

Related: [Network Monitor](12-Network-Monitor.md), [Docker and Compose](02-Docker-and-Compose.md), [Docker notes](docker-notes.md), [Homepage](11-homepage.md), [Automated Backups](08-Automated-backups.md)

Security: ntfy was reviewed during the hardening work and no authentication was added, because LAN access is intentional and remote access is restricted through Tailscale. Adding authentication would require changes to this monitor's script. See [Security Hardening](14-Security-Hardening.md).
