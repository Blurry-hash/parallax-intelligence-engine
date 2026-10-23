---
name: planning-orchestration
description: Turn open-ended objectives into a scoped dependency graph, realistic execution budget, acceptance gates and stop conditions.
---

# Planning orchestration

## Operational procedure

1. Inspect the actual repo / task constraints, current tools and permissions. Write a one-sentence **outcome** and explicit non-goals. Do not assume time spent is equivalent to quality.
2. Decompose into independent deliverables with unique IDs, task kind, dependencies, impact (1–5), risk, estimated minutes and *verifiable acceptance criteria*. Require explicit approval before high-risk actions or delivery/publication. If a task has no falsifiable criterion, refine it.
3. Compile the DAG with `python tools/plan_engine.py examples/planning-v10.3.json`. The result is an **advisory** wave schedule and estimated critical path, not real execution, an actual time guarantee or permission to use external providers.
4. Assign genuinely separable work to up to four independent, authorized workers. Avoid concurrent edits to the same files or external state. Run a review wave after synthesis, not only before implementation.
5. Stop when evidence and tests satisfy acceptance, high risk needs approval, or further work has low expected decision value. Record what ran and measured elapsed time separately from the requested budget.

**Check:** Test missing IDs, cycles, duplicate dependencies, invalid estimates, unapproved delivery tasks and false claims of completion. Never hide these failures by inventing a successful plan.

## Source access

Official inspirations: https://github.com/microsoft/agent-framework and https://github.com/langchain-ai/langgraph . Read actual current docs before using integrations. Their presence here installs no runtime.

## Fallback and limits

This skill cannot grant persistent runtime, additional reasoning tokens, cloud tools, model access or an exact duration. For a time request, apply `deliberate-work-sessions` and document actual elapsed and evidence.
