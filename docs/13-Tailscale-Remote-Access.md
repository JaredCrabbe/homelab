# Tailscale Remote Access

## Overview

Tailscale has been added to the homelab to provide secure remote access to the Linux host and selected internal homelab resources when away from the local network.

The goal is to make remote administration and access practical without requiring internal services to be directly exposed to the public internet through router port forwarding.

## Purpose

The Tailscale deployment adds a private remote-access layer to the existing homelab network. Instead of depending solely on the local `192.168.10.0/24` network, an authorised device can connect to the homelab remotely through the Tailscale network.

This complements the existing networking stack:

- AdGuard Home provides local DNS and network-level filtering.
- Nginx Proxy Manager handles reverse-proxy functionality for web services.
- The network monitor checks local and internet connectivity.
- Tailscale provides remote connectivity to the homelab.

## Remote Access Model

The homelab host participates in the Tailscale network as an authorised device. Remote access is controlled through the Tailscale network rather than by making the homelab host directly reachable from the public internet.

Only devices that are authorised to the Tailscale network should be able to use this remote-access path. Access to individual services should still be controlled by the service itself and by the host/network configuration.

No Tailscale authentication keys, private keys, passwords, or other sensitive credentials should be stored in this documentation or committed to Git.

## Configuration

Tailscale was installed and configured on the Fedora homelab host. The host was authenticated to the Tailscale network and remote access was enabled.

The configuration is intended to provide remote access to the homelab while keeping the existing local networking and Docker configuration unchanged.

## Verification

Remote access was tested by connecting to the homelab through the Tailscale network from an authorised remote device. This confirmed that the homelab could be reached remotely using the Tailscale connection.

Basic verification commands can include:

```bash
tailscale status
tailscale ip
```

These commands can be used to confirm the Tailscale connection and display the address assigned to the local Tailscale interface.

## Security Considerations

Tailscale reduces the need to expose individual homelab services directly to the public internet, but it does not replace service-level security.

The following practices remain important:

- Use strong authentication on remotely accessible services.
- Keep Fedora, Docker, and self-hosted applications updated.
- Do not commit Tailscale credentials or authentication secrets to Git.
- Only authorise trusted devices to the Tailscale network.
- Keep remote access limited to services that actually need it.
- Continue monitoring the host and network for connectivity or service failures.

## Skills Demonstrated

This project demonstrates practical experience with:

- Tailscale
- Private remote access
- Overlay networking
- Linux networking
- Remote system administration
- Network security considerations
- Service exposure and access control
- Troubleshooting remote connectivity

## Project Status

**Completed and tested.** Tailscale is installed on the homelab host and remote access has been enabled and verified from an authorised device.
