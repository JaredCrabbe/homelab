# AdGuard Home

## Overview

AdGuard Home is the homelab's self-hosted DNS filtering service. It can process DNS requests from devices configured to use it, apply filtering rules, and forward allowed requests to upstream DNS resolvers.

## Basic request flow

```text
Client device
     |
     v
AdGuard Home
     |
     +--> Filtered/blocked request
     |
     +--> Allowed request --> Upstream DNS
```

## Docker deployment

AdGuard Home runs as a Docker container managed with Compose. The homelab configuration includes DNS on TCP/UDP port `53` and a web interface exposed on host port `8088`. Check the current Compose file for the authoritative port mappings before making changes.

## Monitoring

The `adguard-home` container is included in the Docker health monitor. Its state is persisted and reconciled against the live Docker state when the monitor starts.

## Skills demonstrated

DNS fundamentals, Docker Compose, port configuration, network-service troubleshooting, container health monitoring, and self-hosted infrastructure administration.
