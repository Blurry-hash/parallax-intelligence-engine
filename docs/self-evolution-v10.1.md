# Self-Evolution v10.1 — A measurable, reversible improvement loop

**Scope:** skill instructions, tool selection, code modules, benchmark datasets and release process. This is *not* neural weight training, independent human-level self-improvement or an always-on background daemon.

## Loop: OBSERVE → HYPOTHESIZE → EXPERIMENT → CHALLENGE → PROMOTE → CHECKPOINT

1. Collect real failures and user corrections. Retain source provenance, privacy limits, model versions and task settings.
2. Identify one falsifiable weakness and propose a minimal intervention; keep independent candidates where possible.
3. Freeze a baseline and development/holdout splits **before** tuning. Prevent leaks from the evaluation set into candidate design.
4. Run paired tasks with identical tools, budgets, prompts except the proposed intervention and reproducible measurements.
5. Use `tools/evolve_gate.py` to enforce minimum holdout coverage, safety gates, per-task regressions, quality gains, cost and latency constraints.
6. A gate passing means **eligible for human review**, never auto-deployed. Store a reversible diff and explicit rollback.
7. Re-test in production-like conditions only with authorization, measure drift and revise the module if improvement does not generalize.

Reference techniques: [DSPy GEPA](https://github.com/stanfordnlp/dspy), [GEPA](https://github.com/gepa-ai/gepa), and [DeepEval](https://github.com/confident-ai/deepeval). Treat benchmark numbers from source repositories as unverified for this project until replicated.

## Invariants

- Do not modify credentials, personal information, public visibility or security policies in response to automated feedback.
- No auto-mutation of production prompts, policies, GitHub branches, memory summaries or model weights.
- A held-out set cannot be repeatedly inspected to cherry-pick candidate changes; rotate/re-freeze when evaluation is consumed.
- Reject even a higher average score if any critical failure appears or protected regression exceeds the configured threshold.
- Generated example cases are synthetic; example gate output is a functionality test, not evidence of a real model improvement.

## Memory and continuity

Versioned releases use `docs/CONTINUITY.md` to record scope, sources, regressions and next steps. This persistent **repository state** does not mean ChatGPT's account Memory feature or base model weights are directly updated. A new chat must load the repository content again as its available access allows.

## Offline demo

```bash
python tools/evolve_gate.py examples/evolution-fixture.json
```
