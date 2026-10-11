# Security Hardening

## Overview

This project records the security hardening work completed on the homelab host on 2026-10-08. The aim was attack surface reduction: remove network exposure that had no operational purpose, restrict remote access to what is actually needed, and confirm after every change that the required services still worked.

The work is documented as a hardening pass, not a claim that the host is fully secured. Some exposure is an accepted exception and several reviews are deliberately deferred; both are listed at the end of this document.

## Context

The homelab runs on a Fedora Linux 44 workstation that is also the daily desktop, so the host has a larger attack surface than a dedicated server would. This is an accepted constraint of building the homelab on existing hardware, and it is the reason the work focused on controlling exposure rather than trying to remove every listener.

| Item | Value |
|---|---|
| LAN interface | `enp3s0` |
| LAN address | `192.168.10.151` |
| Gateway | `192.168.10.1` |
| Tailscale address | `100.73.94.31` |
| Remote administration | Tailscale SSH |

## Goals

- Keep administrative interfaces away from the LAN where remote access is not needed.
- Replace unrestricted Tailscale access with least-privilege access.
- Remove overly broad firewall port ranges.
- Preserve every service the homelab actually depends on.
- Test functionality after each change instead of applying changes blindly.
- Use several layers of control rather than relying on a single one.

## Changes implemented

### 1. Nginx Proxy Manager administrative interface isolation

NPM previously published ports `80`, `81`, and `443` on all interfaces, which made the administration interface on `81` reachable from other devices on the LAN. Because the homelab is administered from the host itself, LAN access to the admin page provided no benefit.

The Compose port mappings were changed so that only the admin interface is bound to the loopback address:

```yaml
ports:
  - "80:80"
  - "127.0.0.1:81:81"
  - "443:443"
```

Binding at the Docker publication level is the control that actually applies here. Docker adds its own forwarding rules for published ports, so adjusting the host firewall alone is not a reliable way to close them.

| Test | Result |
|---|---|
| HTTP on port `80` from the LAN | Still accessible |
| HTTPS on port `443` | Still accessible |
| `192.168.10.151:81` from the LAN | Fails, as intended |
| `127.0.0.1:81` on the host | Works |

### 2. AdGuard Home administrative interface isolation

The same approach was applied to AdGuard Home. DNS has to stay available to LAN clients, so only the web administration interface was moved to loopback:

```yaml
ports:
  - "53:53/tcp"
  - "53:53/udp"
  - "127.0.0.1:8088:8088"
```

| Test | Result |
|---|---|
| DNS on port `53` from the LAN | Still available |
| `192.168.10.151:8088` from the LAN | Fails, as intended |
| `127.0.0.1:8088` on the host | Works |
| LAN DNS resolution | Successful |

DNS resolution from the LAN was tested with:

```bash
nslookup example.com 192.168.10.151
```

### 3. SSH hardening

Normal LAN SSH access was removed from the firewall path. Remote administration is now performed through Tailscale SSH.

The Tailscale SSH policy was changed so that:

- Tailscale members may use SSH.
- Non-root users are allowed.
- Root access is not allowed.

Tailscale SSH was tested successfully after the change:

```bash
ssh jared@100.73.94.31
```

A Tailscale SELinux warning remains on the host. Tailscale SSH worked in testing, but the warning has not been investigated or resolved, and it is not treated as fixed (see Known issues).

### 4. Tailscale least-privilege access

The Fedora homelab machine was assigned the Tailscale tag `tag:homelab`, and the previous unrestricted access policy was replaced with a restricted one that grants access to that tagged machine only for the services that are needed remotely.

| Port | Purpose |
|---|---|
| 22 | SSH |
| 445 | Samba |
| 8082 | ntfy |

Remote Tailscale access is not required for the NPM admin interface (`81`) or the AdGuard admin interface (`8088`), so neither is included. The SSH policy applies to Tailscale members, allows non-root users only, and targets the tagged homelab machine.

Tailscale connectivity and SSH were tested successfully after the policy change. The exact policy is maintained in the Tailscale admin console and is not reproduced here.

### 5. Firewall hardening

The Fedora firewall previously allowed two very broad dynamic port ranges:

```text
1025-65535/tcp
1025-65535/udp
```

These ranges were removed. The active listeners were reviewed first, and UDP `41641` was retained because Tailscale uses it for direct connections.

The changes were applied and tested before being made permanent, and were then made persistent.

Rather than allowing large dynamic port ranges, the firewall was reduced to intentionally required service ports and the specific UDP port needed for Tailscale direct connections.

## Validation

The firewall changes were not applied and left untested. After the change, each service the homelab relies on was checked:

| Service | Test | Result |
|---|---|---|
| Nginx Proxy Manager | `http://192.168.10.151` | Successful |
| ntfy | `http://192.168.10.151:8082` | Successful |
| Samba | `\\192.168.10.151\shares` | Successful |
| AdGuard DNS | `nslookup example.com 192.168.10.151` | Successful |
| Tailscale SSH | `ssh jared@100.73.94.31` | Successful |

## Intended network exposure

After this work, the intended exposure of the host is:

| Port | Protocol | Service | Purpose |
|---|---|---|---|
| 53 | TCP/UDP | AdGuard Home | DNS |
| 80 | TCP | Nginx Proxy Manager | HTTP |
| 443 | TCP | Nginx Proxy Manager | HTTPS |
| 445 | TCP | Samba | SMB/NAS |
| 8082 | TCP | ntfy | Notifications |
| 41641 | UDP | Tailscale | Direct connections |
| 32400 | TCP | Plex | Media server |

Plex on `32400` is an existing accepted exception. It was intentionally not hardened as part of this work, and nothing in this document should be read as securing it.

## Layered controls

No single control is relied on. The layers in place are:

1. **Docker publication:** administrative interfaces are bound to `127.0.0.1`.
2. **Host firewall:** broad port ranges removed; only required service ports and the Tailscale UDP port remain.
3. **Tailscale access policy:** remote access to the tagged homelab machine is limited to ports `22`, `445`, and `8082`.
4. **Tailscale SSH policy:** non-root users only, with no root access.
5. **Service-level behaviour:** administrative pages that are not needed remotely are not reachable remotely at all.

## Security review: ntfy

ntfy was reviewed to decide whether application-level authentication should be added.

- Image: `binwiederhier/ntfy:latest`
- Two internal scripts publish to it: `homelab-monitor/monitor.py` and `network-monitor/network_monitor.py`
- Both use `http://192.168.10.151:8082/homelab`

**Decision: reviewed, no configuration change required.**

Reasoning:

- LAN access to ntfy is intentional.
- Remote access is limited through Tailscale, and the Tailscale policy restricts access to the intended service.
- Adding authentication would mean managing credentials and changing the monitoring scripts.
- The current network-level controls are considered sufficient for the current threat model.

## Accepted exceptions and known issues

- **Plex (`32400`):** accepted exception; not hardened during this work.
- **Tailscale SELinux warning:** still present. Tailscale SSH works, but the warning is unresolved and has not been investigated here.
- **Combined desktop and server host:** accepted architectural constraint, as described in the context above.

## Deferred work

The following items were intentionally left for later. None of them is complete.

| Item | Status |
|---|---|
| n8n exposure review (port `5678`; not part of the intended exposure above) | Deferred |
| mDNS review | Deferred |
| LLMNR review | Deferred |
| Unnecessary firewall services review | Deferred |
| Docker networking and published-port review | Deferred |
| IPv6 exposure review | Deferred |
| Post-hardening network scans | Deferred |
| Plex security review | Deferred |

The post-hardening scans are the main way to confirm the intended exposure table above from outside the host. See [Ways to Scan a Network](Ways%20to%20Scan%20a%20Network.md) for methods.

## Re-checking current state

Reference commands for comparing the live system with the intended exposure above:

```bash
sudo firewall-cmd --list-all
sudo ss -tulpn
tailscale status
```

## Skills demonstrated

Attack surface reduction, administrative interface isolation, Docker port publication and loopback binding, firewall review and hardening, least-privilege access control, Tailscale access policy and tagging, SSH access control, defence in depth, post-change validation, documenting accepted exceptions and deferred work, and risk-based decision making.

## Project Status

**Hardening phase completed and validated.** Administrative interface isolation, least-privilege Tailscale access, SSH restriction, and firewall range reduction are implemented and tested. The accepted exception and deferred reviews above remain open.

Related: [Nginx Proxy Manager](09-nginx-proxy-manager.md), [AdGuard Home](10-adguard-home.md), [Tailscale Remote Access](13-Tailscale-Remote-Access.md), [Samba SMB](05-Samba-SMB.md), [Plex Media Server](06-Plex-Media-Server.md), [Homelab Monitor](07-Homelab-Monitor.md), [Network Monitor](12-Network-Monitor.md), [Homelab Overview](00-Homelab-Overview.md)
