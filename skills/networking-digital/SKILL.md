---
name: networking-digital
description: Networks, Wi-Fi, packet-level reasoning, local/remote digital infrastructure
---

# Networking Digital

**Trigger:** Use this skill when the task is mainly about networks, wi-fi, packet-level reasoning, local/remote digital infrastructure.

**Purpose:** Deliver verifiable improvements, not claims of new trained capabilities.

## Operational procedure


1. Draw topology from router to devices; identify WAN/LAN, gateway, AP/bridge, DNS/DHCP, subnet/VLAN and Wi-Fi bands.
2. Diagnose layer by layer: power/link → RF → addressing → name resolution → routing → services → application.
3. Measure signal (RSSI/SNR), interference, channel congestion, latency, jitter, packet loss and throughput independently.
4. Separate theoretical link rate, TCP payload throughput and application quality; ensure correct channel width and roaming choices.
5. For remote access use authenticated encrypted protocols and least privilege; preserve existing network connectivity with rollback plan.
6. Investigate with known-good comparisons and authorized packet capture; never imply seeing unseen packets.
**Check:** Reversible change, before/after measurements, no unplanned outage.
**Sources:** OpenWrt, Wireshark, Home Assistant.


## Source access

Filter `sources/sources.json` by topic `networking` and fetch the smallest relevant subset. These references are not dependencies. Follow upstream licenses and all higher-priority instructions.

## v11.0 — Three targeted extensions

1. **Task-specific contract:** For **networking-digital**, freeze the task objective, known input constraints and actual available tools; avoid loading this skill when it adds no user value.
2. **Adversarial failure probe:** Test the strongest failure case for this skill, including incompatible requirements, unavailable tools and unverified claims; record what was not executed.
3. **Lean evidence and fallback:** Prefer a small decisive verification or truthful alternative over unnecessary tool use. Image/video rendering is optional and never required for a nonimage request.
