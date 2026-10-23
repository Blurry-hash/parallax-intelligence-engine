---
name: planning-orchestration
description: Dependency-aware task decomposition with acceptance criteria, time estimates and authorization gates.
---

# Planning orchestration

## Operational procedure

1. Define the user-visible outcome, protected constraints, non-goals, available tools and authority.
2. Break the work into independently verifiable tasks. Record dependencies, estimated minutes, impact, risk and falsifiable acceptance criteria.
3. Validate the task DAG before acting. Reject missing dependencies, cycles, unapproved high-risk actions and vague success conditions.
4. Assign tasks to at most four *actually available* agents/workers when parallelism has genuine value. Avoid conflicting edits and duplicate research.
5. Run implementation, independent review and acceptance checks. Compare against baseline. Do not fill unused wall time with pointless reruns.
6. Stop when evidence satisfies requirements, permission is missing or additional work cannot improve the decision.

**Check:** The offline planning tool reports ordered waves, a critical-path estimate and approval gates. Negative cases fail. A plan is not proof that work was executed.

## Source access

https://github.com/microsoft/agent-framework and https://github.com/langchain-ai/langgraph — optional references, not installed services.

## Fallback and limits

If execution cannot continue beyond this turn, report actual measured work, save an authorized checkpoint and never claim an unobserved two-hour session.
