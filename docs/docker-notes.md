# Docker Notes

## Core concepts

- **Image:** template used to create containers.
- **Container:** a running or stopped instance of an image.
- **Port publishing:** maps a host port to a container port, for example `8080:80` for Nginx.
- **Bind mount:** maps a specific host path into a container. Useful for editable content and configuration.
- **Named volume:** Docker-managed persistent storage, useful for application data such as Plex metadata.
- **Compose:** declarative service configuration that makes deployments repeatable.
- **Health check:** command Docker runs to report whether a service is healthy.
- **Restart policy:** controls whether Docker restarts a container after it exits.
- **Docker events:** event stream useful for reacting to container lifecycle and health changes.

## Useful commands

```bash
docker ps
docker ps -a
docker images
docker volume ls
docker network ls
docker logs <container>
docker inspect <container>
docker events
docker compose up -d
docker compose ps
docker compose logs -f
docker compose down
```

Run Compose commands from the relevant project directory or use `-f` to specify a Compose file.

## Homelab examples

- Nginx uses a bind mount for custom HTML and publishes host port `8080` to container port `80`.
- Plex uses a named volume for persistent application data and NAS-backed media storage.
- Samba uses a bind-mounted `smb.conf` and the NAS share directory.
- Homepage, AdGuard Home, Plex, Nginx Proxy Manager, and Samba are watched by the custom Docker health monitor.

## Troubleshooting approach

1. Check whether the container exists and is running with `docker ps -a`.
2. Inspect logs with `docker logs` or `docker compose logs`.
3. Inspect mounts, ports, environment, and runtime settings with `docker inspect`.
4. Validate host paths and permissions for bind mounts.
5. Check network and port conflicts.
6. Change one thing at a time and verify the result.

## Persistence reminder

A container's writable layer should not be treated as durable storage. Use bind mounts or named volumes for data that must survive container replacement. Keep secrets and machine-specific runtime state out of Git.
