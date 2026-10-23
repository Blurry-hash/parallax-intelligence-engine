# PARALLAX v10.4 — operating gates

A compact, offline path for higher-value AI-assisted work. No network, paid providers or model weights are included.

| Stage | Tool | What it actually establishes |
|---|---|---|
| Select | `skill_dispatch.py` | Bounded lexical candidate skills; full content still needs review |
| Plan | `plan_engine.py` | Valid task DAG, approval flags and estimated critical path |
| Schedule | `resource_scheduler.py` | Deterministic non-overlapping worker assignment; heuristic estimated makespan |
| Inspect | `agent_audit.py` | Four truly executed read-only deterministic software workers; no LLMs |
| Prove | `artifact_proof.py` | Bytes match an embedded SHA-256 manifest; not cryptographic authentication |
| Compare | `quality_gate.py` | Numeric paired development/holdout regression gates; fixtures cannot prove real gains |
| Review | `mission_review.py` | Fails closed if key results are absent or negative; not deployment authorization |

## Try it

```bash
python tools/skill_dispatch.py "Design a fast accessible UI" --max-chars 6000
python tools/resource_scheduler.py examples/planning-v10.3.json
python tools/quality_gate.py examples/quality-v10.4.json
python tools/agent_audit.py examples/planning-v10.3.json
python tools/mission_review.py examples/planning-v10.3.json # expected BLOCKED (exit code 2)
python -m unittest discover -s tests -q
```

## Why the boundaries exist

A plan is not execution. A completion note is not verified evidence. A digest is not a trusted signature. A test fixture is not a real-world benchmark. A parallel Python auditor is not an LLM worker. More time or context can be beneficial only when there is meaningful work and measured gain.

For actual AI handoffs, the runtime must expose real models and tools; use provider documentation, guardrails, output validation and human approval before allowing side effects. See [OpenAI Agents SDK](https://developers.openai.com/api/docs/guides/agents/sdk), [human-review controls](https://developers.openai.com/api/docs/guides/agents/guardrails-approvals) and Google's [job-shop scheduling reference](https://developers.google.com/optimization/scheduling/job_shop).
