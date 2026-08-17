# Homelab Docker Health Monitor

## Overview

The Homelab Monitor is a Python service created to monitor the Docker services running in the homelab and send notifications when services become unhealthy or stop.

The monitor was developed incrementally and is now considered complete.

## Monitored containers

The monitor currently watches:

```text
Homepage
adguard-home
plex
nginx-proxy-manager
samba
```

## Monitoring method

The monitor uses:

```text
docker events
```

with container events for:

- `health_status`
- `die`
- `start`

It also uses `docker inspect` to determine the actual current state of a container.

## States

The monitor distinguishes between:

```text
health_status: healthy
health_status: unhealthy
health_status: starting
container_status: stopped
```

## Persistent state

Container state is stored in:

```text
state.json
```

The state contains information such as:

```json
{
  "Homepage": {
    "status": "health_status: healthy",
    "unhealthy_since": null
  }
}
```

The monitor can migrate the original state-file format to the newer structure.

State writes use a temporary file followed by replacement so that a partial write is less likely to corrupt the state file.

## Startup reconciliation

A major feature is startup reconciliation.

When the monitor starts, it does not assume that the saved state is still correct.

It checks each monitored container with Docker and compares the actual state with the saved state.

This allows the monitor to detect situations such as:

- A container being unhealthy while the monitor was offline.
- A container being stopped while the monitor was offline.
- A previously unhealthy container recovering before the monitor restarted.

## Incident timing

When a container becomes unhealthy or stops, the monitor records the incident time in:

```text
unhealthy_since
```

When the container recovers, the monitor calculates the downtime and includes it in the recovery notification.

## Notifications

Notifications are sent to the homelab ntfy topic:

```text
http://192.168.10.151:8082/homelab
```

Alerts include:

- Container
- Status
- Host
- Time

Recovery notifications additionally include downtime when an incident time was recorded.

## systemd

The monitor runs as:

```text
homelab-monitor.service
```

The service uses:

```text
User=jared
WorkingDirectory=/home/jared/homelab/compose/homelab-monitor
Environment=PYTHONUNBUFFERED=1
```

It starts the monitor with:

```text
/usr/bin/python3 /home/jared/homelab/compose/homelab-monitor/monitor.py
```

It is configured to restart after failure:

```text
Restart=on-failure
RestartSec=5
```

## Testing

The monitor was tested against:

- Normal healthy states
- Unhealthy containers
- Container stops
- Container starts
- Service restarts
- State persistence
- Startup reconciliation
- Recovery notifications
- Downtime calculation
- A real Plex/NVIDIA failure

## Result

The monitor is complete and committed to Git.

It provides a practical example of combining:

- Python
- Docker
- Docker events
- Docker health checks
- Linux
- systemd
- JSON persistence
- HTTP notifications
- Git
- Troubleshooting
