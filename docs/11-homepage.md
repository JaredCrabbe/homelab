# Homepage Dashboard

## Overview

Homepage is the homelab's central dashboard for organising and accessing self-hosted services. It reduces the need to remember each service's individual address.

## Role

The dashboard provides links and service information for components such as AdGuard Home, Nginx Proxy Manager, Plex, and Samba. The exact widgets and integrations depend on the current Homepage configuration.

## Docker deployment and health

Homepage runs as a Docker container named `Homepage` and has a Docker health check. It was the first service used to validate the custom Docker monitor's health-state tracking.

The monitor uses Homepage to exercise baseline detection, state persistence, startup reconciliation, and recovery notifications. Repeated healthy events should not be treated as new incidents; notifications are intended to correspond to meaningful state changes.

## Skills demonstrated

Docker Compose, dashboard configuration, service organisation, health checks, Python monitoring integration, JSON state persistence, and ntfy notifications.
