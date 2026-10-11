# Network Monitor

## Overview

The network monitor is a custom Python script that checks the host's Ethernet interface, local gateway, and internet reachability. It complements the Docker health monitor: one checks network connectivity while the other watches container health and running state.

## Current checks

- Interface: `enp3s0`
- Gateway: `192.168.10.1`
- Internet target: `1.1.1.1`
- Notification endpoint: `http://192.168.10.151:8082/homelab`
- Script directory: `~/homelab/scripts/network-monitor/`
- Main script: `network_monitor.py`
- Persistent target/interface state: `state.json`

The interface check reads Linux network status from `/sys/class/net/enp3s0/operstate` and `/sys/class/net/enp3s0/carrier`. Reachability checks use `ping` and parse the summary for packet loss and average latency.

## Target states

The intended target-state model is:

- `up` — 0% packet loss
- `degraded` — packet loss greater than 0% but less than 100%
- `down` — 100% packet loss or no usable ping result

The interface is tracked separately as `up` or `down`.

## State-change notifications

The monitor loads its previous state from `state.json`, compares it with the latest result, and saves the new state. ntfy notifications are sent only when a state transition occurs, avoiding repeated alerts on every run while a condition remains unchanged.

Expected target transitions include:

- `up` to `degraded`: warning with packet-loss/latency details where available
- `degraded` to `down`: critical connectivity alert
- `down` to `degraded`: degraded-state alert
- `degraded` or `down` to `up`: recovery notification

The first run establishes a baseline rather than reporting every initial state as a new incident. A controlled state-file test verified that a recovery transition produced an ntfy notification.

## systemd automation

Periodic execution uses:

- `homelab-network-monitor.service` — `Type=oneshot`, runs the Python script as `jared`
- `homelab-network-monitor.timer` — starts after boot and repeats at a one-minute interval

The timer is enabled and running (confirmed 2026-10-07), so the monitor is fully operational. Useful checks:

```bash
systemctl status homelab-network-monitor.timer
systemctl list-timers | grep homelab-network
journalctl -u homelab-network-monitor.service -n 30 --no-pager
```

Because this monitor runs periodically and exits after one check, `inactive (dead)` for the service after a successful `oneshot` run is normal; the timer should be active and waiting.

## Notification endpoint note

The notification URL uses the host's LAN address (`192.168.10.151:8082`). If ntfy's published port or binding changes, update the endpoint here and in the [Homelab Monitor](07-Homelab-Monitor.md) settings.

## Skills demonstrated

Python scripting, Linux interface inspection, ICMP checks, latency and packet-loss parsing, JSON state persistence, transition-based alerting, ntfy integration, systemd timers, log inspection, and network troubleshooting.

Related: [Homelab Monitor](07-Homelab-Monitor.md), [Tailscale Remote Access](13-Tailscale-Remote-Access.md), [AdGuard Home](10-adguard-home.md), [Ways to Scan a Network](Ways%20to%20Scan%20a%20Network.md)

Security: ntfy was reviewed during the hardening work and no authentication was added, so this monitor continues to publish to the LAN address unchanged. See [Security Hardening](14-Security-Hardening.md).
