---
name: subagent-review-protocol
description: Independent, permission-bounded specialist workers for planning, provenance, structural validation and decision quality.
---

# Subagent review protocol

## Operational procedure

1. Define the workers' different hypotheses or review areas before any worker sees another review. Do **not** claim separate AI models exist when they do not.
2. Prefer true available model/tool agents when configured, consented to, and justified. For offline checks run `python tools/agent_audit.py examples/planning-v10.3.json`; this starts **four real read-only parallel deterministic worker functions**, not LLM assistants.
3. Give each worker minimum scope: explicit inputs, no external secrets, no writes or network, a timeout where supported, and an output schema with `pass`, `findings`, and observed metrics.
4. Keep distinct findings rather than averaging away disagreement. Resolve blocking disagreements with a decisive test; preserve unverified observations and uncertain sources separately.
5. Allow one responsible orchestrator to merge findings and make changes, only within approved boundaries. Never create subagents as performative filler if one check would suffice.

**Check:** Four independent reviews ran and are separately attributable; forced worker failure appears as failure while other reviews remain intact. No external providers were consulted unless evidenced.

## Source access

OpenAI Agents SDK guardrails/handoffs: https://github.com/openai/openai-agents-python . Microsoft Agent Framework orchestration: https://github.com/microsoft/agent-framework . Their SDKs are optional, NOT bundled.

## Fallback and limits

Tool workers cannot introspect closed-model hidden reasoning or simulate independent LLM opinions. Read-only routines are still valuable subagents for structural verification, not equivalent to AI peer review.
