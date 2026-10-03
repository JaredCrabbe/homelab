# Nginx Container

## Overview

Nginx was the first practical Docker Compose service built in the homelab. It was used to learn the basic Compose workflow before moving to more involved services.

## Configuration

- Host port: `8080`
- Container port: `80`
- Host content directory: `~/homelab/compose/nginx/html/`
- Container document root: `/usr/share/nginx/html`

The HTML directory is bind-mounted into the container, allowing the page to be edited on the host and served by Nginx without rebuilding the image.

## Workflow

1. Create a dedicated Compose project directory.
2. Define the service in `compose.yaml`.
3. Publish the host port and bind-mount the HTML directory.
4. Start the service with Docker Compose.
5. Verify the result at `http://localhost:8080`.
6. Inspect logs and container status when troubleshooting.
7. Track the configuration in Git.

## Skills demonstrated

- Basic web-server deployment
- Docker Compose
- Port publishing
- Bind mounts
- Container lifecycle and logs
- Git-based configuration tracking
