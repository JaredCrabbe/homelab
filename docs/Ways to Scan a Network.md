---
title: Ways to Scan a Network
date: 2026-10-06
tags: [networking, nmap, homelab, security, reference]
aliases: [Network scanning, Network discovery, nmap cheatsheet]
---

# Ways to Scan a Network

> [!WARNING]
> Only scan networks you own or have written permission to test. Scanning someone else's network can be illegal and will trip their IDS. Home lab = fine; work or public networks = get permission first.

Network scanning answers four questions, roughly in this order:

1. **Which hosts are alive?** (host discovery)
2. **Which ports are open on them?** (port scanning)
3. **What is running on those ports?** (service / OS detection)
4. **Is any of it vulnerable or misconfigured?** (vulnerability scanning)

There is also a fifth, quieter option: **just listen** (passive discovery).

---

## 1. Host discovery (who is on the network?)

| Method | How it works | Good for | Example |
|---|---|---|---|
| **ARP scan** | Broadcasts "who has IP x?" on the local subnet. Hosts must answer; firewalls can't block it. | Most reliable on a LAN. Layer 2 only (same subnet). | `sudo arp-scan --localnet` |
| **ICMP ping sweep** | Echo requests to every IP. | Quick check, routed networks. Many hosts drop ICMP. | `nmap -sn 192.168.10.0/24` |
| **TCP SYN/ACK ping** | Sends a SYN or ACK to common ports and treats any reply as "alive". | Hosts that block ICMP. | `sudo nmap -sn -PS22,80,443 -PA80 192.168.10.0/24` |
| **UDP ping** | Probes a UDP port; an ICMP "port unreachable" proves the host exists. | Rarely needed, a fallback. | `sudo nmap -sn -PU53 192.168.10.0/24` |
| **fping** | Parallel ICMP pinger, scriptable. | Fast, clean output for scripts. | `fping -a -g 192.168.10.0/24 2>/dev/null` |
| **netdiscover** | ARP-based, active or passive. | Quick LAN map with vendor names. | `sudo netdiscover -r 192.168.10.0/24` |

> [!NOTE]
> On a local subnet, `nmap -sn` already uses ARP when run as root, which is why it finds hosts that ignore ping. Without `sudo` it falls back to TCP connects and can miss devices.

---

## 2. Port scanning (what is open?)

| Scan type | Flag | What it does | Trade-offs |
|---|---|---|---|
| **TCP SYN ("half-open")** | `-sS` | Sends SYN, reads SYN/ACK or RST, never completes the handshake. | Default as root. Fast and fairly quiet. |
| **TCP connect** | `-sT` | Full handshake using the OS `connect()` call. | Works without root; louder and slower, appears in app logs. |
| **UDP** | `-sU` | Sends UDP probes; open ports often stay silent. | Slow and ambiguous (`open\|filtered`). Needed for DNS, SNMP, DHCP, NTP. |
| **ACK** | `-sA` | Maps firewall rules (filtered vs unfiltered), not open ports. | Good for understanding a firewall. |
| **FIN / NULL / Xmas** | `-sF` `-sN` `-sX` | Odd flag combos that some stacks answer differently. | Mostly historical; unreliable on modern systems. |
| **Idle (zombie)** | `-sI` | Bounces the scan off a third host. | Niche; fun for learning how IP ID works. |

Scope control:

```bash
nmap -p 22,80,443 host        # specific ports
nmap -p- host                 # all 65535 TCP ports
nmap --top-ports 100 host     # most common 100
nmap -F host                  # fast: top 100
```

Timing (`-T0` to `-T5`): `-T3` is the default, `-T4` is fine on a home LAN, and `-T1`/`-T2` are slow and stealthier. Avoid `-T5` on anything fragile.

---

## 3. Service, version and OS detection

```bash
sudo nmap -sV host              # probe open ports to identify service + version
sudo nmap -O host               # OS fingerprinting (TCP/IP stack behaviour)
sudo nmap -A host               # -sV + -O + default scripts + traceroute
nmap -sV --version-intensity 9 host   # try harder to identify a service
```

Also useful:

- **Banner grabbing** by hand: `nc -v host 22` or `curl -I http://host`
- **TLS details**: `nmap --script ssl-cert,ssl-enum-ciphers -p 443 host`

---

## 4. Scripted and vulnerability scanning

- **Nmap Scripting Engine (NSE)**: hundreds of scripts, grouped by category.
  - `nmap -sC host` runs the default safe set.
  - `nmap --script vuln host` checks for known vulnerabilities.
  - `nmap --script "http-*" -p 80,443 host` runs a family of scripts.
- **OpenVAS / Greenbone**: free, full vulnerability scanner with a web UI; can be self-hosted in Docker.
- **Nessus Essentials**: free for up to 16 IPs, polished reports.
- **Nikto**: web server misconfiguration scanner (`nikto -h http://host`).
- **Lynis**: audits the *local* machine's hardening rather than scanning remotely.

---

## 5. Fast, internet-scale scanners

When nmap is too slow for huge ranges:

| Tool | Notes |
|---|---|
| **masscan** | Asynchronous, can do millions of packets per second. Syntax is nmap-like: `sudo masscan 192.168.10.0/24 -p1-65535 --rate 1000` |
| **RustScan** | Finds open ports very quickly, then hands them to nmap for detail. |
| **ZMap** | Single-port scans across enormous address spaces. Research-oriented. |

> [!TIP]
> Common pattern: fast scanner to find open ports, then `nmap -sV -sC -p <those ports>` for depth.

---

## 6. Passive discovery (no packets sent)

Useful when you don't want to disturb sensitive devices, or just want to see who is actually talking.

- **Router / DHCP lease table**: the easiest source of truth for a home network.
- **ARP cache**: `ip neigh` shows what your machine has already seen.
- **Packet capture**: `sudo tcpdump -i enp3s0 -nn arp` shows hosts announcing themselves.
- **Wireshark**: inspect everything; filter with `arp`, `dhcp`, `mdns`.
- **Zeek / Suricata**: continuous network monitoring and logging.
- **netdiscover -p**: passive ARP mode.
- **mDNS / SSDP discovery**: `avahi-browse -art` lists advertised services.

Limit: passive only sees devices that transmit while you're listening, and only traffic your NIC can see (switches don't flood everything to you unless you use a mirror/SPAN port).

---

## 7. GUI and phone tools

- **Zenmap**: official GUI for nmap, with topology view.
- **Angry IP Scanner**: simple cross-platform sweep.
- **Fing**: phone app for quick home-network inventory.
- **Advanced IP Scanner**: Windows.

---

## Handy homelab recipes

```bash
# 1. Who's on my LAN right now?
sudo nmap -sn 192.168.10.0/24

# 2. Quick look at one box: common ports + versions
sudo nmap -sV -T4 192.168.10.151

# 3. Full TCP audit of one host, saved in all formats
sudo nmap -sS -sV -sC -p- -T4 -oA scans/host-151 192.168.10.151

# 4. Check the key UDP services
sudo nmap -sU -p 53,67,123,161 192.168.10.1

# 5. Diff two scans over time to spot new/open ports
ndiff scans/old.xml scans/new.xml
```

Output formats: `-oN` (normal text), `-oX` (XML), `-oG` (greppable), `-oA name` (all three).

---

## Staying out of trouble (and getting good results)

- Get **permission**, and note the scope (IP ranges, time window).
- Scan from a **wired** connection when possible; Wi-Fi drops probes and gives false negatives.
- A "filtered" port means a firewall swallowed the probe, not that it's closed.
- Run scans from **inside and outside** the network to compare what a firewall exposes.
- Fragile gear (old printers, PLCs, IoT) can fall over under aggressive scans. Use `-T2` and fewer ports.
- Keep results in version control or a dated folder so you can diff changes.

---

## Quick cheat sheet

| I want to... | Run |
|---|---|
| List live hosts on my LAN | `sudo arp-scan --localnet` |
| Same, with nmap | `sudo nmap -sn 192.168.10.0/24` |
| Open ports on one host | `sudo nmap -sS host` |
| What software is running | `sudo nmap -sV host` |
| Everything, aggressively | `sudo nmap -A -p- host` |
| Vulnerability check | `nmap --script vuln host` |
| Scan huge range fast | `sudo masscan <range> -p80,443 --rate 1000` |
| Just watch, don't touch | `sudo tcpdump -i <iface> -nn arp` |

---

Related: [Homelab Overview](00-Homelab-Overview.md), [Network Monitor](12-Network-Monitor.md), [Security baseline](security-baseline.md)
 sorted, tell me and I'll retry. It will create test.md containing just "test".