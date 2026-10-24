# PARALLAX — five evidence-gated loop strategies (v11.3)

The user requested one advanced loop plus four complementary techniques. Each is a *specialist protocol* and a mode in an **offline, deterministic evidence controller**, not an always-on model engine. **Never force loops on routine questions; do not activate Professor Omnis.**

| Mode | Specialist skill | What it does | Why it can fail |
|---|---|---|---|
| `verification` | [Adaptive Verification](../skills/adaptive-verification-loop/SKILL.md) | Observe, compare, retain best | Missing external evidence |
| `adversarial` | [Counterexample Discovery](../skills/counterexample-discovery-loop/SKILL.md) | Stress-test and falsify assumptions | Aggregate score hides edge-case failure |
| `multipath` | [Parallel Hypothesis](../skills/parallel-hypothesis-loop/SKILL.md) | Compare genuinely distinct routes | Correlated strategies and no independent test |
| `prompt_opt` | [Holdout Prompt Optimization](../skills/holdout-prompt-optimization-loop/SKILL.md) | Tune on development, gate once on holdout | Holdout leakage or reward hacking |
| `regression` | [Regression Reflection](../skills/regression-reflection-loop/SKILL.md) | Preserve passing cases and derive bounded lessons | Stale tests, fake durable memory |

## Run a real local controller check

```bash
python tools/loop_controller.py examples/loop-verification.json
python tools/loop_controller.py examples/loop-adversarial.json
python tools/loop_controller.py examples/loop-multipath.json
python tools/loop_controller.py examples/loop-prompt-opt.json
python tools/loop_controller.py examples/loop-regression.json
python -m unittest tests.test_loops -v
```

The fixture examples contain **synthetic evaluation scores**; passing them validates controller logic, not evidence that an LLM improved its answers. Gather observations from independent tools and record provenance before claiming a real gain. No model invocation, hosted execution, persistent memory, deployment, autonomous recurrence, or external permission is granted by these files. The controller never runs untrusted Python and never writes user data.

Mode selection: creative alternatives benefit from `multipath`; formal or unsafe edge cases call for `adversarial`; many repeated prompts call for `prompt_opt`; evolving code calls for `regression`; a typical objectively testable output calls for `verification`. Choose only when expected value exceeds loop cost. Run with at most 1–3 relevant skills, not all five by default.

## Scientific caveat

- [Self-Refine (NeurIPS 2023)](https://papers.nips.cc/paper/2023/hash/91edff07232fb1b55a505a9e9f6c0ff3-Abstract-Conference.html) demonstrates the potential of feedback refinement in studied settings.
- [Reflexion (NeurIPS 2023)](https://papers.nips.cc/paper_files/paper/2023/hash/1b44b878bb782e6954cd888628510e90-Abstract-Conference.html) uses task feedback and episodic reflection; it does not update model weights.
- [GEPA](https://github.com/gepa-ai/gepa) illustrates trace-driven prompt evolution, requiring genuine evaluator/model access to reproduce its claims.
- [TACL critical survey (2024)](https://aclanthology.org/2024.tacl-1.78/) finds that self-correction without reliable external feedback can fail; do not mistake repeated self-confidence for evidence.
