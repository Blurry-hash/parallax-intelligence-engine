# PARALLAX — versioned operating memory

This file is a *project checkpoint*, not ChatGPT account memory or model-weight retraining.

## 2026-10-23 — v10.1 Audio Intelligence + Self-Evolution
- Goal: add substantially deeper audio/voice capability guidance, practical offline signal processing and credible self-optimizing evaluation.
- Added 7 purpose-specific skills and three executable tools (`audio_lab.py`, `voice_route.py`, `evolve_gate.py`).
- Sources: refreshed references to actively maintained Coqui fork, F5-TTS, VibeVoice, AudioCraft, pyannote, DSPy/GEPA and evaluation research.
- Protected constraints: all repository visibility controlled only by user; user previously authorized PARALLAX to remain **public**; no access to unconnected voice providers or persistent model memory; no fake audio synthesis.
- Validation: record GitHub Actions commit and test results after publication. Do not mark unexecuted checks as passing.
- Next opportunities: integration adapters behind explicit provider auth, a human blind-listening evaluation harness, and benchmark reporting without data leakage.

## How to use this checkpoint
Read only the most relevant current section and linked `SKILL.md` files. Verify the repository state before trusting old notes. Do not infer unseen changes in connected ChatGPT memory.

## 2026-10-23 — v10.2 coding logic and performance
- Added 26 targeted skills for algorithm design, invariants, typed synthesis, AST transforms, robust test oracles, concurrency, cache correctness, critical-path scheduling and multimedia/UI throughput.
- Added deterministic offline complexity heuristic, DAG critical-path scheduler and paired latency/correctness gate, plus negative-case tests.
- Source registry expanded with links marked `unconfirmed` pending individual page verification.
- Preserve existing v10.1 audio, bounded self-evolution and explicit public visibility; no automatic changes to other repositories.
- No assertion of intelligence/speed improvement without representative baseline comparisons.

## 2026-10-23 — v10.2 timed work extension
- Added `deliberate-work-sessions` skill, audited allowlisted work runner with checkpoint ledger, and documentation/example for a requested 50-minute work session.
- Work is measured by real time and completed distinct steps; code refuses unsupported commands and stops at substantive-work exhaustion. A 50-minute request is not proof of 50 minutes of actual work.
- Durable scheduling requires an actual external runtime and authorization, never simulated ChatGPT background execution.

## 2026-10-23 — v10.3 planning and accountable subagents
- New task-DAG planning, explicit risk/approval gates, evidence-ledger checks and four truly independent parallel read-only Python worker functions.
- These tool workers are not separate LLMs, and planning duration estimates are not measured execution time.
- Baseline local project: 122/122 unit tests passed. GitHub CI is a separate remote check that must not be claimed without a successful run.
- Keep the explicit public visibility of PARALLAX. Never touch other repositories without specific authorization.
- Research: OpenAI Agents SDK, Microsoft Agent Framework and LangGraph; these are references, not installed dependencies.
