# Nginx Container

## Overview

Nginx was the first practical Docker Compose service created for the homelab.

The project was intentionally simple so Docker Compose concepts could be learned before moving to more complicated services.

## Configuration

The Nginx container exposed:

```text
Host port: 8080
Container port: 80
```

A local HTML directory was bind-mounted into the Nginx document root:

```text
~/homelab/compose/nginx/html/
    -> /usr/share/nginx/html
```

## Compose workflow

The project demonstrated:

1. Creating a Compose project directory.
2. Creating `compose.yaml`.
3. Creating local web content.
4. Starting the container with Docker Compose.
5. Verifying the service through the browser.
6. Stopping/removing the service when required.
7. Committing the project to Git.

## Skills demonstrated

- Docker Compose
- Port mapping
- Bind mounts
- Container lifecycle management
- Basic web-server deployment
- Git tracking of infrastructure configuration
