# Time-budgeted work — v10.2

User example: **"Förbättra detta i 50 minuter"**. Treat 50 minutes as a *requested active-work budget*, not a guarantee of uninterrupted ChatGPT execution or quality improvement.

## Contract
- If your host supports actual sustained agent execution: identify verified wall-clock deadline, resource cap, the goal, checkpoints, and meaningful independent work items. Keep working while useful tasks and budget remain. Do not sleep/loop merely to satisfy a clock. Replan after evidence changes.
- If host stops tools or replies early: honestly report the measured duration and remaining work; do not claim 50 minutes were completed. A separate authorized durable workflow engine (e.g. Temporal) may resume work across sessions, but this repository cannot turn a read-only chatbot into a persistent worker.
- Keep separate `requested`, `actual_wall_seconds` and `actual_execution_seconds`. The last is not model reasoning time, and there is no API measuring private model thought duration.
- If quality has converged before requested duration, explain why further time would be counterproductive. Real tests and comparison against baseline matter more than how long the agent appeared active.
- Paid API/model/tool use requires consent. Never exfiltrate secrets into external runtimes. Allow explicit user cancellation.

## Runnable offline demo

```bash
python tools/work_budget.py examples/work-session-50min.json --output /tmp/parallax-work-ledger.json
```

This demo usually finishes **well before** 50 minutes because it executes a finite list of five checks. It honestly records `work_exhausted`, *not* `50 minutes completed`, and provides an auditable ledger. Extend the plan with distinct authorized tasks when needed. The script does not invoke AI models and must not be mistaken for 50 minutes of generative reasoning.

## Example host integration
1. Host detects requested effort duration and has persistent job support.
2. Agent decomposes the work into a target-driven backlog with criteria and dependencies; issues genuine tool/model calls through available channels.
3. Runtime records a monotonic clock, actual executions, code/output hashes and checkpoint state across restarts.
4. After each meaningful milestone, run tests and benchmark regressions; compare user-visible results.
5. Stop on time limit, no useful work or safety/budget boundary, and deliver actual results. No background claim without scheduling/worker infrastructure.
