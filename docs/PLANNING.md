# Planning / 10.3

A good plan is falsifiable. It doesn't simply name tasks: it shows what must change, which work can run independently, what would disprove success and when to stop.

## The operating contract

- **Objective first.** Define output artifact, protected constraints, user-approved publication boundary and non-goals.
- **Decompose.** DAG tasks with explicit dependencies, impact, estimated effort, risk and measurable acceptance.
- **Choose the next check by decision value.** Do the least costly experiment that can change the decision. Avoid repeating work solely to fill a requested duration.
- **Delegate bounded work.** Up to four specialist workers when useful. Prefer independent review perspectives. In a restricted environment use the bundled read-only deterministic workers; do not pretend they are AI models.
- **Evidence over confidence.** Link task-state claims to artifacts/tests and actual approvals, using a plan fingerprint. Keep regressions and exceptions visible.
- **Stop honestly.** Report real elapsed time, verified outcome and blockers. Longer requests do not authorize paid services or indefinite background operation.

## Try it — no paid services, no network

```bash
python tools/plan_engine.py examples/planning-v10.3.json --output /tmp/parallax-plan.json
python tools/agent_audit.py examples/planning-v10.3.json --out /tmp/parallax-agent-audit.json
python -m unittest tests.test_planning_v10_3 -v
```

The planner generates advisory parallel waves and a *lower-bound estimate*, not a future promise. The agent audit executes four separate read-only Python workers concurrently; no external models are called. A real cloud multi-agent deployment needs provider auth, execution permissions and separate testing.

`tools/goal_trace.py` validates a task/evidence ledger against the plan's SHA-256, dependency states and approval gates. Evidence must still be independently checked for external delivery claims.

## Sources and choices

- [OpenAI Agents SDK](https://github.com/openai/openai-agents-python) — handoffs, guardrails, tracing. Optional SDK, not bundled.
- [Microsoft Agent Framework](https://github.com/microsoft/agent-framework) — workflow graph and multiple agents, with explicit runtime.
- [LangGraph](https://github.com/langchain-ai/langgraph) — durable graph state and checkpointing.
- [Temporal Python](https://github.com/temporalio/sdk-python) — durable long-running workflows with infrastructure. A reference only, not ChatGPT background execution.

## Known limits

Deterministic audits detect structural errors, not subtle model hallucinations. Estimated task times are guesses until observed. Local proof does not establish model intelligence gain or production readiness. No model weights, third-party sandbox, provider account, persistent process or autonomous memory is installed by these Markdown files.
