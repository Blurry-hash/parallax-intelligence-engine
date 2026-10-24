---
name: coding-engineering
description: Secure, production-quality software and maintainable debugging
---

# Coding Engineering

**Trigger:** Use this skill when the task is mainly about secure, production-quality software and maintainable debugging.

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
