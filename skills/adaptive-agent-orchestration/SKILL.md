---
name: adaptive-agent-orchestration
description: Delegate independent work only when real workers improve the result
---

# Delegate independent work only when real workers improve the result

## Operational procedure

1. Estimate the task’s dependency graph, cost of errors and verification burden. Answer trivial work directly. Delegate only when independent research, isolated edits or adversarial review have enough work to outweigh setup and merge overhead.
2. Detect actual host subagent/tool APIs and available model choices. Default to at most four total active workers including the coordinator. Do not claim a CHEAP/MEDIUM/HIGH model was selected unless the API actually selected it; use available model IDs and measured fit rather than invented routing percentages.
3. Assign each worker one bounded goal, relevant file/context slice, ownership of edit paths, acceptance checks and expected report. Share interfaces before parallel edits; dependent tasks wait for upstream artifacts. A read-only reviewer should not silently modify the implementation.
4. Give the least expensive capable worker utilities and narrow checks, a stronger worker synthesis/debugging, and escalate uncertain failures to the coordinator. If models are fixed, adapt task size rather than pretending model routing occurred. No paid or external provider calls without relevant authorization.
5. Collect artifact paths, commands, test outcomes, assumptions and unresolved issues. Verify pivotal claims independently; conflicting outputs trigger a discriminating test, not majority voting. Cancel redundant work and prohibit two workers from editing the same path simultaneously.
6. Merge coherent outputs and run integration checks once. Keep a compact checkpoint with goal, decisions, evidence, owners and next step before context compaction. No automatic background work after a final answer unless a real scheduled service exists.

**Check:** If two subtasks both edit the same router file, partition ownership before spawning. If no real worker API exists, execute sequentially and do not invent agent transcripts.

## Source access

https://openai.github.io/openai-agents-python/ ; https://docs.anthropic.com/en/docs/claude-code/sub-agents . Verify current host documentation before integration.
