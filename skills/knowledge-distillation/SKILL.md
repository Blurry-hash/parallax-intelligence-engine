---
name: knowledge-distillation
description: Extract transferable, testable procedures from model observations
---

# Knowledge Distillation

**Trigger:** Use this skill when the task is mainly about extract transferable, testable procedures from model observations.

## Operational procedure

1. Set target competency and a blind evaluation set before editing prompts.
2. Collect independent model outputs only from genuinely accessible models; archive model/version/settings/provenance.
3. Extract expressible procedural rules, examples, failure conditions and decision boundaries.
4. Reject unsupported claims about secret training data or internal thoughts.
5. Create SKILL.md module with trigger, steps, negative tests, fallbacks and expected output schema.
6. Compare performance against baseline on held-out tasks; retain only changes with evidence of improvement.
7. Track cost, latency and disagreement; distillation does not automatically transfer model weights.
**Check:** Is the new skill demonstrably better on unseen tests?

## Source access

Filter `sources/sources.json` by topic `reasoning` and fetch the smallest relevant subset. These references are not dependencies. Follow upstream licenses and all higher-priority instructions.
