# AdGuard Home

## Overview

AdGuard Home was deployed as the homelab's network-level DNS and ad-blocking service.

It provides a local DNS service that can process DNS requests from devices on the network and apply filtering rules before forwarding permitted requests upstream.

## Purpose

The project provides practical experience with:

- DNS
- Network services
- Docker
- Port management
- Network troubleshooting
- Self-hosted infrastructure

## Homelab Role

The basic flow is:

```text
Client Device
     |
     v
AdGuard Home
     |
     +--> Blocked request
     |
     +--> Allowed request
              |
              v
         Upstream DNS
```

This allows DNS filtering to be handled centrally rather than requiring software to be installed on every device.

## Docker Deployment

AdGuard Home runs as a Docker container.

Important ports in the deployment include:

- `53/tcp` — DNS
- `53/udp` — DNS
- `8088` — web interface exposed by the homelab configuration

The container also exposes the other ports required by AdGuard Home internally.

## Monitoring

AdGuard Home is included in the homelab Docker health monitor:

```text
adguard-home
```

Its health status is persisted in the monitor's `state.json` file and is checked during startup reconciliation.

## Skills Demonstrated

- DNS fundamentals
- Docker Compose
- Network port configuration
- Linux administration
- Troubleshooting network services
- Monitoring infrastructure

## Lessons Learned

AdGuard Home adds an important networking component to the homelab. It moves the project beyond simply running containers and into managing actual network infrastructure and DNS services.
