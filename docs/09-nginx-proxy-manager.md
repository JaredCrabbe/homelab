# Nginx Proxy Manager

## Overview

Nginx Proxy Manager (NPM) was added to the homelab to provide a simple web interface for managing reverse-proxy hosts and routing traffic to services running on the homelab.

It complements the Docker-based service architecture by providing a central place to manage HTTP/HTTPS access to internal services.

## Purpose

The project provides experience with:

- Reverse proxying
- HTTP/HTTPS routing
- Docker networking
- Web-based infrastructure administration
- Managing access to self-hosted services

## Homelab Role

NPM sits between clients and internal web services:

```text
Client
  |
  v
Nginx Proxy Manager
  |
  +--> Homepage
  +--> Other web services
```

Instead of exposing every service directly, NPM can receive the request and forward it to the appropriate internal container.

## Docker Deployment

NPM runs as a Docker container using Docker Compose.

The container exposes the standard NPM management and proxy ports:

- `80` — HTTP
- `81` — NPM administration interface
- `443` — HTTPS

The service is monitored by the homelab health monitor.

## Monitoring

NPM was added to the monitor's watched container list:

```text
nginx-proxy-manager
```

Its Docker health status is tracked alongside Homepage, AdGuard Home, Plex, and Samba.

The monitor can detect:

- Healthy
- Unhealthy
- Stopped
- Recovery after an incident

## Skills Demonstrated

- Docker Compose
- Reverse-proxy concepts
- HTTP/HTTPS
- Service routing
- Container health monitoring
- Linux service administration

## Lessons Learned

NPM demonstrates how a self-hosted environment can centralise access to multiple web services instead of configuring each service independently.
