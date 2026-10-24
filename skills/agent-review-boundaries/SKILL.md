---
name: agent-review-boundaries
description: Coordinate independent scoped software workers while maintaining clear distinction from separate language-model agents.
---

# Agent Review Boundaries

## Operational procedure

1. Use `tools/agent_audit.py` when independent deterministic workers suffice. Report their names, input scopes, software identity, outputs and runtime.
2. When authorized external LLM agents exist, use a provider adapter with explicit tool policies, handoff boundaries, budget and human review; do not hallucinate availability.
3. Avoid multiple workers editing the same files. Keep review workers read-only whenever possible and cross-check disagreements against primary evidence.
4. Prefer a single worker for low-complexity tasks. Parallelism can increase coordination and failure costs.

**Check:** Verify each worker failure is surfaced independently and that no agent is claimed to exist without actual execution.

## Source access

Official reference design: https://developers.google.com/optimization/scheduling/job_shop (resource scheduling), https://developers.openai.com/api/docs/guides/agents/guardrails-approvals (gated agent actions), https://github.com/openai/openai-agents-python (optional authorized multi-model runtime). These are documentation links, not installed providers or execution capabilities.

## Fallback and limits

No model-weight updates, background execution, paid inference or external API calls occur merely by loading this skill.
