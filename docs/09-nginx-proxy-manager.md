# Nginx Proxy Manager

## Overview

Nginx Proxy Manager (NPM) provides a web interface for configuring reverse-proxy hosts and routing HTTP/HTTPS requests to services running in the homelab.

## Role in the homelab

```text
Client
  |
  v
Nginx Proxy Manager
  |
  +--> Homepage
  +--> Other configured web services
```

A reverse proxy provides a central place to route requests instead of requiring every web service to be accessed directly by its own host port. It does not automatically make services public; exposure depends on the network, DNS, firewall, and proxy configuration.

## Docker deployment

NPM is deployed through Docker Compose. Its commonly used ports are:

- `80` — HTTP proxy traffic
- `81` — administration interface (bound to `127.0.0.1` only)
- `443` — HTTPS proxy traffic

The container is included in the custom Docker health monitor.

## Security

The administration interface is isolated to the host. The Compose port mappings publish `80` and `443` normally but bind `81` to the loopback address:

```yaml
ports:
  - "80:80"
  - "127.0.0.1:81:81"
  - "443:443"
```

HTTP and HTTPS proxy traffic remain available to the LAN. The admin page on `127.0.0.1:81` works from the host, and access to `192.168.10.151:81` from the LAN fails as intended. See [Security Hardening](14-Security-Hardening.md) for the full change record and validation.

## Skills demonstrated

Docker Compose, reverse-proxy concepts, HTTP/HTTPS, internal service routing, web-based infrastructure administration, administrative interface isolation, container monitoring, and Linux service troubleshooting.

Related: [Homepage](11-homepage.md), [AdGuard Home](10-adguard-home.md), [Tailscale Remote Access](13-Tailscale-Remote-Access.md), [Nginx Container](03-Nginx-Container.md), [Security Hardening](14-Security-Hardening.md)
