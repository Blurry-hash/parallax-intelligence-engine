---
name: self-evolution-engine
description: Improve procedures through reproducible failures and controlled comparisons
---

# Improve procedures through reproducible failures and controlled comparisons

## Operational procedure

1. Capture a real failure as a small reproducible case: objective, input, observed error, expected behavior and source artifact. Record a correction only after checking its cause; user preference changes are not evidence that a technical method improved.
2. Classify the cause: missing context, stale source, weak hypothesis, wrong tool, implementation bug, overclaim, wasted work or evaluation flaw. Propose the smallest change capable of preventing recurrence. Preserve constraints, public interfaces and a rollback revision.
3. Keep training/development examples separate from final holdout. Predeclare task families, metrics, minimum practical gain, budget and protected regression cases. Do not repeatedly inspect the same holdout while tuning; retire contaminated cases to development.
4. Compare champion and challenger with the same model/settings/tools, paired task IDs and randomized run order when relevant. Record correctness, latency, token/cost usage and failures; use shared statistics for intervals and a paired test. Small synthetic fixtures validate tool logic, not model intelligence.
5. Promote only when evidence supports the target behavior with no protected regression; inconclusive results remain candidates. One artifact hash proves identity, not truth; self-assessed scores alone cannot demonstrate improvement. Require authorized review for deployment/external publication.
6. Save a concise lesson with scope, mechanism, evidence, counterexample and expiry/recheck trigger. Merge duplicates; remove obsolete rules. Prefer retrieval of relevant lessons over appending the entire history to every prompt.
7. Stop on budget, plateau, unreliable measurement or rising regressions. If a promoted change fails in real use, rollback and retain the negative result. Periodically ablate a skill on unseen tasks; remove it only after replicated evidence or clear redundancy with preserved coverage.

**Check:** A candidate that is faster but fails a protected task is rejected. A correction with five self-rated examples and no independent outcomes remains unproven. A lesson cannot claim to retrain weights or create cross-chat memory.

**Output:** failure case → causal hypothesis → minimal patch → measured comparison → promote/retain/reject → rollback and retrieval key.

## Source access

https://arxiv.org/abs/2303.11366 (Reflexion); https://arxiv.org/abs/2303.17651 (Self-Refine); https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.bootstrap.html . Self-feedback literature is motivation, not proof that this implementation improves a model.
