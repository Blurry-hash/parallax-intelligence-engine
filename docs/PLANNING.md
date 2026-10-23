# Planning / v10.3

PARALLAX planning starts with a testable outcome, not a long to-do list.

**Scope → dependency graph → bounded work → independent review → evidence → stop.**

Define each task's dependencies, risk, impact, estimated effort and concrete acceptance criteria. High-risk actions and delivery require actual approval. Use at most four genuinely available independent workers where useful; avoid simultaneous edits to the same shared state.

The new offline tools are: `tools/plan_engine.py` (advisory DAG), `tools/agent_audit.py` (four read-only deterministic worker reviews), and `tools/goal_trace.py` (plan-hash/evidence gate). They do not install other AI models or run in the background.

For requested multi-hour work, record requested versus *actual measured* runtime. Keep a meaningful backlog but never sleep or loop only to fill time.

References: [OpenAI Agents SDK](https://github.com/openai/openai-agents-python), [Microsoft Agent Framework](https://github.com/microsoft/agent-framework), [LangGraph](https://github.com/langchain-ai/langgraph). These are optional sources, not automatic capabilities.

## Example

```bash
python tools/plan_engine.py examples/planning-v10.3.json
python tools/agent_audit.py examples/planning-v10.3.json
python -m unittest discover -s tests -q
```

**Known limit:** A successful deterministic audit is not an AI peer review and does not prove a model has become faster or more intelligent.
