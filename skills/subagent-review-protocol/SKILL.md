---
name: subagent-review-protocol
description: Independent review with bounded subagent scope, explicit capabilities, attributable outputs and human approval for consequential changes.
---

# Subagent review protocol

## Operational procedure

1. Identify distinct hypotheses or review questions before delegation. Choose structure, logic, evidence and permissions as separate lanes.
2. Run genuine connected LLM agents only if their model/tool access and costs are authorized. Offline deterministic reviewer functions are valid tool workers, not separate language models.
3. Limit each worker to declared read-only files and structured findings. Allow no hidden background processes, arbitrary shell or shared writes.
4. Collect independent results without hiding disagreements. Demand a decisive test before resolving contradictory outcomes.
5. The orchestrator integrates reviewed changes and runs regression tests. External publication follows a separate explicit authorization gate.

**Check:** Workers have separately labeled results; failure in one worker is visible and does not erase the others. No nonexistent model calls are claimed.

## Source access

https://github.com/openai/openai-agents-python and https://github.com/microsoft/agent-framework — current handoff/guardrail patterns, optional SDKs.

## Fallback and limits

A deterministic audit worker is not an AI subagent and cannot replace independent generative reasoning. Do not impersonate inaccessible specialists.
