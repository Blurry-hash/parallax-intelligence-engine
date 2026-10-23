# Self-Evolution v10.1 — Bounded empirical improvement

This means optimizing reusable methods and skill files, NOT altering neural weights, permanent ChatGPT memory or self-modifying privileged instructions.

## Loop
1. OBSERVE actual task failures and user corrections; capture reproducible evidence.
2. HYPOTHESIZE an atomic intervention and alternatives; preserve baseline revision.
3. FREEZE development/holdout split and representative domain coverage.
4. EVALUATE paired cases with identical models, tools, budgets and protected requirements.
5. CHALLENGE candidate with critical safety gates, material per-case regressions, cost and p95 latency.
6. PROMOTE only after a human reviews passing evidence and reversible diff.
7. CHECKPOINT decisions, limitations and next checks in [CONTINUITY.md](CONTINUITY.md).

Offline test: `python tools/evolve_gate.py examples/evolution-fixture.json`. The example is SYNTHETIC, not proof of actual improvement. GEPA/DSPy and DeepEval are optional references, not silently installed optimization runtimes.

Do not cherry-pick repeated holdout tests, expose secrets, make unsolicited paid calls or mutate other repos. No deployment without explicit authorization.