---
name: counterexample-discovery-loop
description: Generate adversarial cases and shrinking failure probes to invalidate weak candidate claims.
---
# Counterexample Discovery Loop

## Activation
Load only for tasks benefiting from iterative improvement; simple user questions do not require loops. Do not activate optional Professor Omnis. A task-specific workflow must respect the caller's actual tools and permission boundaries.

## Operational procedure
1. Freeze formal invariants, critical edge cases and a working baseline.
2. Construct boundary, counterexample, malformed-input, adversarial and abuse cases. Include at least two distinct observable passing stress tests for every accepted candidate.
3. Run tests externally. On failure, isolate a minimal reproducer and feed it into the next revision; do not silently discard the failure.
4. Reject any critical failure even if aggregate quality improves; retain challenge cases for later regression testing.
5. Evaluate the offline ledger via `python tools/loop_controller.py examples/loop-adversarial.json`; this only checks provided outcomes, not code execution.

## Evidence contract
Only an external check is eligible for quality promotion; a self-review is an idea generator, not verification. Record candidate IDs, costs, failure modes, tested SHA when relevant, and what was not executed. Use strict budgets and stop conditions. Keep the previous best when a new iteration regresses.

## Verification criteria
Pass: matched reproducible evidence, safety gate, and no hidden permissions. Fail: missing test evidence, leaked holdout, unsafe or unauthorized side effects, repeated unproductive loops, or hand-waved model-weight improvements.

## References
- [Self-Refine (NeurIPS 2023)](https://papers.nips.cc/paper/2023/hash/91edff07232fb1b55a505a9e9f6c0ff3-Abstract-Conference.html)
- [Reflexion (NeurIPS 2023)](https://papers.nips.cc/paper_files/paper/2023/hash/1b44b878bb782e6954cd888628510e90-Abstract-Conference.html)
- [GEPA open source](https://github.com/gepa-ai/gepa)
- [Limits of self-correction (TACL 2024)](https://aclanthology.org/2024.tacl-1.78/)
