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
- `81` — administration interface
- `443` — HTTPS proxy traffic

The container is included in the custom Docker health monitor.

## Skills demonstrated

Docker Compose, reverse-proxy concepts, HTTP/HTTPS, internal service routing, web-based infrastructure administration, container monitoring, and Linux service troubleshooting.
