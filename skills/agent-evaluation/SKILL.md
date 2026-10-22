---
name: agent-evaluation
description: Controlled evaluations of prompts, agent workflows and model performance
---

# Agent Evaluation

**Trigger:** A prompt/skill change, model comparison, multi-agent workflow or claim of improved quality/speed.

**Purpose:** Replace subjective impressions of improvement with calibrated reproducible evidence.

## Operational procedure

1. State the desired outcome and guardrails; choose metrics (task pass rate, groundedness, latency p50/p95, cost, security).
2. Record the exact model IDs, versions if known, runtime, temperature/effort, tools, prompts and test-set provenance. Do not assume labels identify stable weights.
3. Establish an unchanged baseline and separate development examples from blind holdout tasks; use paired inputs and comparable tool access.
4. Include easy, difficult, adversarial, malformed and regression cases. Require explicit expected outcomes rather than grading vague prose alone.
5. Run repeated trials when possible; record raw failures and variability as well as means or medians.
6. Use established evaluation harnesses (such as Promptfoo) only when installed and authorized. Guard against hidden network calls, credential exposure, paid model use and sensitive data in logs.
7. Accept changes only if the improvements are credible, material and do not break protected constraints. Document inconclusive outcomes and rollbacks.

**Check:** A measured delta against a reproducible baseline—not merely a longer prompt or a single impressive output.

## Source access

Look up topic `evaluation` and `agents` in `sources/sources.json`. Use relevant evaluation design in `benchmarks/evaluation-rubric.md`.
