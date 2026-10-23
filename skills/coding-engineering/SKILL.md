---
name: coding-engineering
description: Secure, production-quality software and maintainable debugging
---

# Coding Engineering

**Trigger:** Use this skill when the task is mainly about secure, production-quality software and maintainable debugging.

**Purpose:** Deliver verifiable improvements, not claims of new trained capabilities.

## Operational procedure


1. Inspect repository tree, architecture, runtime, dependencies, CI, relevant files and recent changes.
2. Reproduce symptom with exact input/expected vs actual; isolate root cause instead of patching around it.
3. Formulate smallest safe change, preserving public interfaces, migrations and user data.
4. Implement focused tests: unit, integration, contract and regression as the risk warrants.
5. Run formatter, lint, typecheck, tests and build when configured; report each actual result.
6. Review security (auth, injection, secrets), error paths, observability, performance and rollout/rollback.
7. Prefer static analysis and explicit boundary types; never invent API endpoints or package versions.
**Check:** Reproduced failure fixed, regression captured, no unrelated behavior changed.
**Sources:** OpenAI Codex, Anthropic Claude Code, Aider, SWE-agent, Google engineering practices, pytest.


## Source access

Filter `sources/sources.json` by topic `coding` and fetch the smallest relevant subset. These references are not dependencies. Follow upstream licenses and all higher-priority instructions.

## v11.0 — Three targeted extensions

1. **Task-specific contract:** For **coding-engineering**, freeze the task objective, known input constraints and actual available tools; avoid loading this skill when it adds no user value.
2. **Adversarial failure probe:** Test the strongest failure case for this skill, including incompatible requirements, unavailable tools and unverified claims; record what was not executed.
3. **Lean evidence and fallback:** Prefer a small decisive verification or truthful alternative over unnecessary tool use. Image/video rendering is optional and never required for a nonimage request.
