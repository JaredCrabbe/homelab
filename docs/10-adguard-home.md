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

AdGuard Home runs as a Docker container managed with Compose. The homelab configuration includes DNS on TCP/UDP port `53` and a web interface on host port `8088`, which is bound to the loopback address only. Check the current Compose file for the authoritative port mappings before making changes.

## Monitoring

The `adguard-home` container is included in the Docker health monitor. Its state is persisted and reconciled against the live Docker state when the monitor starts.

## Security

The administration interface is isolated to the host, while DNS stays available to LAN clients:

```yaml
ports:
  - "53:53/tcp"
  - "53:53/udp"
  - "127.0.0.1:8088:8088"
```

The admin page on `127.0.0.1:8088` works from the host, and access to `192.168.10.151:8088` from the LAN fails as intended. LAN DNS resolution was confirmed afterwards with `nslookup example.com 192.168.10.151`. See [Security Hardening](14-Security-Hardening.md) for the full change record and validation.

## Availability

The homelab host is also a dual-boot daily desktop, so AdGuard Home is unavailable whenever the host is shut down or booted into Windows. If the router hands out this host as the LAN's DNS server, confirm the router also has a secondary/fallback DNS configured so devices keep resolving names during those periods.

## Skills demonstrated

DNS fundamentals, Docker Compose, port configuration, administrative interface isolation, network-service troubleshooting, container health monitoring, and self-hosted infrastructure administration.

Related: [Nginx Proxy Manager](09-nginx-proxy-manager.md), [Tailscale Remote Access](13-Tailscale-Remote-Access.md), [Homepage](11-homepage.md), [Network Monitor](12-Network-Monitor.md), [Security Hardening](14-Security-Hardening.md)
