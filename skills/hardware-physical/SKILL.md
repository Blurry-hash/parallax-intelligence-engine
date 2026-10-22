---
name: hardware-physical
description: Electronics, embedded firmware, mechanics, fabrication and testing
---

# Hardware Physical

**Trigger:** Use this skill when the task is mainly about electronics, embedded firmware, mechanics, fabrication and testing.

**Purpose:** Deliver verifiable improvements, not claims of new trained capabilities.

## Operational procedure


1. Identify exact board/revision/datasheet, power source, interfaces, environment and safe operating envelope.
2. Compute electrical margins (V/I/P), regulator loss, thermal dissipation, decoupling, pull-ups and wiring tolerances.
3. For radio/sensors: verify RF region, antenna, bandwidth, synchronization, noise sources and calibration.
4. For firmware: model bootloader, timing, memory, interrupt behavior, GPIO electrical constraints and watchdog/failsafe.
5. For CAD/PCB: check dimensions, mechanical loads, fit, thermal pathways, clearance/creepage and manufacturability.
6. Propose staged diagnostics using multimeter, oscilloscope, logs or measured samples where available.
7. Never claim hands-on measurement; avoid unsafe mains wiring, high-voltage modifications or unverified medical-device conclusions.
**Check:** All units and device limits verified with authoritative hardware documentation.
**Sources:** ESP-IDF, Zephyr, KiCad, FreeCAD.


## Source access

Filter `sources/sources.json` by topic `hardware` and fetch the smallest relevant subset. These references are not dependencies. Follow upstream licenses and all higher-priority instructions.
