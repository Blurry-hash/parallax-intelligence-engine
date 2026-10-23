---
name: acceptance-evidence-ledger
description: Link completed task claims to a versioned plan, test evidence, prerequisites and approval gates.
---

# Acceptance evidence ledger

## Operational procedure

1. Bind the plan to a canonical hash and assign a unique record to each task.
2. Record pending, in-progress, blocked or verified status with attributable test/artifact evidence.
3. Before marking verified, require evidence, verified dependencies and any required human approval. Reject stale hashes, duplicates and unsupported completion.
4. Validate the ledger with tools/goal_trace.py when available. Review externally supplied evidence independently for consequential actions.
5. Report incomplete tasks as incomplete. Separate proposed, implemented, locally tested, CI-verified and deployed outcomes.

**Check:** Negative tests reject missing evidence, wrong plan hashes, unapproved deliveries and unmet prerequisites.

## Source access

https://github.com/langchain-ai/langgraph and https://github.com/temporalio/sdk-python — optional durable workflow references.

## Fallback and limits

Self-reported evidence is not proof of external deployment. Verify provider state rather than treating a ledger as authority.
