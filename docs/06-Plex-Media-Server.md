# Plex Media Server

## Overview

Plex is deployed as a Docker service for self-hosted media streaming. Media is stored on the NAS, while Plex application data is kept in a named Docker volume so metadata can persist independently of the container lifecycle.

## Container and persistence

Plex uses the LinuxServer.io Plex image. A Docker health check queries the local Plex identity endpoint so Docker can report whether the service is responding. The deployment has also been used to explore hardware access and transcoding behaviour.

## Hardware and driver troubleshooting

The homelab encountered a Plex startup failure caused by an NVIDIA library version mismatch after a driver update. Docker referenced a library file that no longer existed, and `nvidia-smi` reported a driver/library mismatch. A host reboot resolved the mismatch and Plex started correctly afterward.

This was a useful exercise in distinguishing an application problem from a host driver/runtime problem and using logs and system tools to investigate it.

## Monitoring integration

Plex is monitored by the custom Docker health monitor. A real Plex/NVIDIA incident was used to validate detection and recovery notifications, including the reporting of incident duration when a previous unhealthy state had been recorded.

## Skills demonstrated

- Docker Compose and persistent volumes
- NAS-backed media storage
- Docker health checks
- Hardware/transcoding troubleshooting
- NVIDIA driver/runtime diagnostics
- Container logs and service recovery
- Integrating a real incident with monitoring and alerting
