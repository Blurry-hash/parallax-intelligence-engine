---
name: regression-reflection-loop
description: Use externally verified corrections and bounded, nonpersistent lesson capsules with rollback safeguards.
---
# Regression Reflection Loop

## Activation
Load only for tasks benefiting from iterative improvement; simple user questions do not require loops. Do not activate optional Professor Omnis. A task-specific workflow must respect the caller's actual tools and permission boundaries.

## Operational procedure
1. Define a baseline regression suite and identify protected previously passing behavior.
2. Run changed candidate through all protected cases; any missing, failed or changed existing case blocks adoption.
3. Record short lessons only from a winning, externally tested candidate. Lessons need provenance IDs, are bounded and may omit sensitive information.
4. Prefer rollback over continued blind edits when tests fail, budgets run out or improvements stagnate.
5. Use `python tools/loop_controller.py examples/loop-regression.json`. The JSON capsule is returned to the caller; it is NOT ChatGPT long-term memory and is never written automatically.

## Evidence contract
Only an external check is eligible for quality promotion; a self-review is an idea generator, not verification. Record candidate IDs, costs, failure modes, tested SHA when relevant, and what was not executed. Use strict budgets and stop conditions. Keep the previous best when a new iteration regresses.

## Verification criteria
Pass: matched reproducible evidence, safety gate, and no hidden permissions. Fail: missing test evidence, leaked holdout, unsafe or unauthorized side effects, repeated unproductive loops, or hand-waved model-weight improvements.

## References
- [Self-Refine (NeurIPS 2023)](https://papers.nips.cc/paper/2023/hash/91edff07232fb1b55a505a9e9f6c0ff3-Abstract-Conference.html)
- [Reflexion (NeurIPS 2023)](https://papers.nips.cc/paper_files/paper/2023/hash/1b44b878bb782e6954cd888628510e90-Abstract-Conference.html)
- [GEPA open source](https://github.com/gepa-ai/gepa)
- [Limits of self-correction (TACL 2024)](https://aclanthology.org/2024.tacl-1.78/)
