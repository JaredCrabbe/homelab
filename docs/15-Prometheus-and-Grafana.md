# Prometheus and Grafana

## Overview

Prometheus and Grafana add metrics collection, history, and dashboards to the homelab. Prometheus scrapes numeric metrics and stores them as time series; Grafana queries Prometheus and displays the results. node_exporter supplies the host metrics.

This complements the custom monitors rather than replacing them. The [Docker health monitor](07-Homelab-Monitor.md) and the [Network Monitor](12-Network-Monitor.md) send ntfy alerts when a state changes, while Prometheus and Grafana show how CPU, memory, disk, and network usage change over time.

## Components

| Component | Image | Role | Exposure |
|---|---|---|---|
| Prometheus | `prom/prometheus:latest` | Scrapes and stores metrics, 30-day retention | `127.0.0.1:9090` |
| node_exporter | `prom/node-exporter:latest` | Host CPU, memory, disk, and network metrics | Host networking, port `9100`, not reachable from the LAN |
| Grafana | `grafana/grafana-oss:latest` | Dashboards on top of Prometheus | `127.0.0.1:3000` |

All three run from one Compose project in `~/homelab/compose/prometheus/`. The Compose file, `prometheus.yml`, `grafana-datasource.yml`, and a gitignored `.env` file sit together in that directory. Check the current Compose file for the authoritative port mappings and mounts before making changes.

## Prometheus

Prometheus uses a 15-second scrape interval and two scrape jobs:

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: prometheus
    static_configs:
      - targets: ["localhost:9090"]

  - job_name: node
    static_configs:
      - targets: ["host.docker.internal:9100"]
```

The configuration is bind-mounted read-only from `prometheus.yml` next to the Compose file. `host.docker.internal` is mapped to the host gateway with `extra_hosts`, which lets the container reach node_exporter on the host.

Time-series data is stored in the named volume `prometheus-data`, with retention set to 30 days (`--storage.tsdb.retention.time=30d`). Docker prefixes volume names with the Compose project name, so the volume appears as `prometheus_prometheus-data`. Renaming the project directory would make Compose create a new empty volume and leave the old data behind, so the directory name should stay as it is.

## node_exporter

node_exporter runs with host networking and host PID visibility, and the host's root filesystem is mounted read-only at `/host` (`--path.rootfs=/host`). Because it uses host networking, it listens on all interfaces on port `9100`, and the host firewall is what keeps that port away from the LAN.

SELinux label separation is disabled for this container (`label=disable`) because Fedora's SELinux policy otherwise blocks the host mounts. This is a deliberate trade-off for a read-only metrics exporter and is recorded here so it is not forgotten.

## Grafana

Grafana is provisioned with Prometheus as its default data source from `grafana-datasource.yml`, using the URL `http://prometheus:9090` (the container name on the shared Compose network). It was running version 13.0.2 at deployment.

- **Login:** user `admin`. The password comes from `GF_SECURITY_ADMIN_PASSWORD` in `.env`, which is not committed to Git. Sign-up is disabled.
- **Dashboard:** Node Exporter Full (Grafana dashboard ID 1860) was imported for host metrics.
- **Persistence:** dashboards and settings are stored in the named volume `grafana-data`.

The admin password variable is only applied when Grafana first creates its database. If the password stops working, or the variable was added after the first start, reset it inside the container:

```bash
docker exec -it grafana grafana cli admin reset-admin-password '<new-password>'
```

## Access

Both interfaces are reached from the host: `http://localhost:9090` for Prometheus and `http://localhost:3000` for Grafana. This follows the same pattern as the Nginx Proxy Manager and AdGuard Home admin pages, which are also bound to loopback. Grafana is not behind an Nginx Proxy Manager proxy host.

Ports `9090` and `3000` are not part of the Tailscale access policy, which allows only `22`, `445`, and `8082`. If remote access to Grafana is ever needed, an SSH port forward over Tailscale SSH would keep the policy unchanged, but this has not been configured or tested.

## Security

- Prometheus and Grafana are bound to `127.0.0.1`, so they are not reachable from the LAN.
- node_exporter is the only component that listens on all interfaces, and port `9100` is intentionally not in the firewall's allowed set.
- Grafana's admin password lives in `.env`, which is excluded from Git. `git status` was checked to confirm it is untracked.
- Prometheus has no authentication of its own. Loopback binding is the control that applies.

See [Security Hardening](14-Security-Hardening.md) for the exposure model these services were added under.

## Verification

Checked on 2026-10-19:

| Check | Result |
|---|---|
| Prometheus targets `prometheus` and `node` | Both `up` |
| Prometheus listener | `127.0.0.1:9090` only |
| Access from a phone on the LAN | Failed, as intended |
| `docker compose down && docker compose up -d` | Targets `up` again; WAL segments replayed and the named volume was present |
| Existing services (ntfy, Samba, and others) | Still available |
| Grafana health endpoint | `database: ok`, version 13.0.2 |
| Grafana listener | `127.0.0.1:3000` only |
| Node Exporter dashboard | Imported and still present after a Grafana restart |
| `.env` in `git status` | Not listed |

Useful commands:

```bash
curl -s localhost:9090/api/v1/targets | grep -o '"health":"[a-z]*"'
curl -s localhost:3000/api/health
ss -tlnp | grep -E '9090|9100|3000'
docker logs prometheus 2>&1 | grep -iE "wal|replay"
docker volume ls | grep -E "prometheus|grafana"
```

## Troubleshooting and lessons

- **Validate before starting.** `docker compose config -q` checks the Compose file, and `promtool check config` checks Prometheus's configuration:

  ```bash
  docker run --rm --entrypoint promtool \
    -v "$PWD/prometheus.yml:/p.yml:ro,Z" \
    prom/prometheus:latest check config /p.yml
  ```

- **YAML structure matters.** Mixed indentation from pasted snippets caused a parse error in one file. A missing `-` in front of `targets:` under `static_configs` produced a "cannot unmarshal !!map into []*targetgroup.Group" error, because `static_configs` must be a list.
- **Missing bind-mount sources become directories.** When the host path for a file bind mount does not exist at start-up, Docker creates it as an empty directory, and the container then fails with "not a directory" while mounting. The fix was to remove the empty directory (`sudo rmdir`), create the real file next to the Compose file, and use a path relative to that Compose file. Create config files before running `docker compose up -d`.

## Not yet implemented

These are planned and are not part of the completed work above:

- Per-container metrics with cAdvisor
- Alerting from Prometheus or Grafana to ntfy
- Adding these containers to the Docker health monitor's watched set
- Remote access to Grafana

## Skills demonstrated

Prometheus configuration and scrape jobs, node_exporter, Grafana provisioning and dashboards, Docker Compose, named volumes and bind mounts, host networking, SELinux awareness on Fedora, loopback port binding, secrets handling with `.env` and Git, configuration validation with `promtool`, post-change verification, and troubleshooting YAML and mount errors.

## Project Status

**Prometheus, node_exporter, and Grafana deployed and verified (2026-10-19).** Host metrics are collected and graphed. Container metrics and alerting are not yet implemented.

Related: [Docker and Compose](02-Docker-and-Compose.md), [Homelab Monitor](07-Homelab-Monitor.md), [Network Monitor](12-Network-Monitor.md), [Security Hardening](14-Security-Hardening.md), [Homelab Overview](00-Homelab-Overview.md), [Docker notes](docker-notes.md)

Security: Prometheus and Grafana are loopback-only, and node_exporter's port `9100` is not exposed to the LAN. See [Security Hardening](14-Security-Hardening.md).
