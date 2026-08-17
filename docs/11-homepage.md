# Homepage

## Overview

Homepage is the dashboard for the homelab. It provides a central interface for viewing and accessing the services running on the server.

It gives the homelab a single starting point instead of requiring individual service addresses to be remembered.

## Purpose

The project provides experience with:

- Docker Compose
- Self-hosted dashboards
- Service organisation
- Container health checks
- Infrastructure monitoring

## Homelab Role

Homepage acts as the front-end dashboard:

```text
                    +--> AdGuard Home
                    |
User --> Homepage --+--> Nginx Proxy Manager
                    |
                    +--> Plex
                    |
                    +--> Samba
```

The dashboard provides an overview of the services and their current state.

## Docker Deployment

Homepage runs as a Docker container.

The container is named:

```text
Homepage
```

The container is configured with a Docker health check, allowing the homelab monitor to track its health.

## Health Monitoring

Homepage was the first service used to validate the homelab monitor's health-status tracking.

The monitor records states such as:

```text
health_status: healthy
health_status: unhealthy
```

Homepage's state is persisted to `state.json`, allowing the monitor to remember the previous condition across restarts.

## Monitoring Development

Homepage was particularly useful during development of the monitor because it provided a reliable test case for:

- Initial state/baseline detection
- Duplicate event handling
- State persistence
- Startup state reconciliation
- Health recovery notifications

The final monitor can detect when Homepage changes state and send an ntfy notification.

## Skills Demonstrated

- Docker Compose
- Docker health checks
- Python automation
- JSON state persistence
- Event-driven monitoring
- Linux/systemd administration
- ntfy notifications

## Lessons Learned

Homepage became more than a dashboard: it was also an important test service during development of the monitoring system.

It helped validate that the monitor could distinguish between a normal repeated healthy event and a genuine state change.
