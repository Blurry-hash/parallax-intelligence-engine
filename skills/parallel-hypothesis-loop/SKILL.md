---
name: parallel-hypothesis-loop
description: Explore independent solving strategies and select using observed evaluations, not consensus alone.
---
# Parallel Hypothesis Loop

## Activation
Load only for tasks benefiting from iterative improvement; simple user questions do not require loops. Do not activate optional Professor Omnis. A task-specific workflow must respect the caller's actual tools and permission boundaries.

## Operational procedure
1. Define a common problem specification, hard requirements and comparable quality measure before creating approaches.
2. Generate genuinely distinct strategies (e.g. algebraic proof vs computation, causal model vs retrieval); do not count paraphrases as independent.
3. Test each path on the same benchmark and comparable tool budgets; attribute scores to distinct external evidence IDs.
4. Select the best verified feasible approach. Require at least two distinct externally evaluated strategies before making a comparative claim.
5. Use `python tools/loop_controller.py examples/loop-multipath.json` as a deterministic evidence gate; it does not create subagents or model calls.

## Evidence contract
Only an external check is eligible for quality promotion; a self-review is an idea generator, not verification. Record candidate IDs, costs, failure modes, tested SHA when relevant, and what was not executed. Use strict budgets and stop conditions. Keep the previous best when a new iteration regresses.

## Verification criteria
Pass: matched reproducible evidence, safety gate, and no hidden permissions. Fail: missing test evidence, leaked holdout, unsafe or unauthorized side effects, repeated unproductive loops, or hand-waved model-weight improvements.

## References
- [Self-Refine (NeurIPS 2023)](https://papers.nips.cc/paper/2023/hash/91edff07232fb1b55a505a9e9f6c0ff3-Abstract-Conference.html)
- [Reflexion (NeurIPS 2023)](https://papers.nips.cc/paper_files/paper/2023/hash/1b44b878bb782e6954cd888628510e90-Abstract-Conference.html)
- [GEPA open source](https://github.com/gepa-ai/gepa)
- [Limits of self-correction (TACL 2024)](https://aclanthology.org/2024.tacl-1.78/)
