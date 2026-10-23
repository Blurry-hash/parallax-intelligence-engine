---
name: acceptance-evidence-ledger
description: Prevent false completed/verified claims by requiring per-task evidence, satisfied dependencies and approval gates.
---

# Acceptance evidence ledger

## Operational procedure

1. Bind a task plan to its canonical SHA-256 fingerprint. Record exactly one state for every task: `pending`, `in_progress`, `blocked`, or `verified`.
2. Verify requirements before marking done: measurable acceptance criteria, an attributable evidence item, all prerequisite tasks verified, and any required human approval confirmed.
3. Run `python tools/goal_trace.py plan.json ledger.json`; never accept mismatched plan hashes or unsupported verified claims. Do not store credentials, personal data or protected content in the ledger.
4. After implementation, re-run tests with a fresh revision identifier. Logs supplied by a worker are evidence pointers, not automatically trusted truth; review output/artifact hashes independently for consequential releases.
5. Identify remaining blockers and stop. Do not label proposals, drafts or unexecuted code as completed. Separate local tests, CI tests, deployment and real-world measured improvements.

**Check:** Negative tests reject unverifiable completion, unapproved delivery, stale plan fingerprints, duplicates and unverified prerequisites.

## Source access

LangGraph checkpointing https://github.com/langchain-ai/langgraph and Temporal workflows https://github.com/temporalio/sdk-python provide optional persistent execution patterns; do not assume availability.

## Fallback and limits

No ledger is cryptographic proof that an external action happened. Independently verify external state using the actual provider before claiming an action completed.

## v11.0 — Three targeted extensions

1. **Task-specific contract:** For **acceptance-evidence-ledger**, freeze the task objective, known input constraints and actual available tools; avoid loading this skill when it adds no user value.
2. **Adversarial failure probe:** Test the strongest failure case for this skill, including incompatible requirements, unavailable tools and unverified claims; record what was not executed.
3. **Lean evidence and fallback:** Prefer a small decisive verification or truthful alternative over unnecessary tool use. Image/video rendering is optional and never required for a nonimage request.
