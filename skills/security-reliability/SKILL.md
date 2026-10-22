---
name: security-reliability
description: Defensive application, system and operational reliability engineering
---

# Security Reliability

**Trigger:** Use this skill when the task is mainly about defensive application, system and operational reliability engineering.

**Purpose:** Deliver verifiable improvements, not claims of new trained capabilities.

## Operational procedure


1. Map trust boundaries, assets, data flow, identities and adversarial entry points.
2. Check authentication/authorization, input validation, SSRF, injection, XSS, CSRF, secrets, dependency integrity and data retention.
3. Apply OWASP guidance appropriate to runtime; derive security requirements from assets and threat model.
4. Build observability with safe structured logs, trace IDs, metrics, alert thresholds and SLOs; redact sensitive values.
5. Validate backup restoration, rollout controls, migrations, rate limits, circuit breakers and disaster recovery.
6. Demonstrate vulnerability only within owned/authorized environments and minimize impact.
**Check:** Security recommendation has threat, mitigation and validation method; no untested security guarantee.


## Source access

Filter `sources/sources.json` by topic `security` and fetch the smallest relevant subset. These references are not dependencies. Follow upstream licenses and all higher-priority instructions.
