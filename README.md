# PARALLAX

*Methods, tools and independent checks for better AI-assisted work.*

**v10.3** · **114 skills** · **141 linked references** · **Python 3.12+**

> Multiple perspectives. One verifiable result.

PARALLAX is not another language model. It is a practical method library for serious research, engineering, design, creativity and originality. Inspect the goal, choose relevant skills, work efficiently, check the evidence and stop when the result holds up. The emphasis is on decisions and artifacts—not performance theatre.

## Find your route

| Goal | Relevant modules |
|---|---|
| Plan complex work | [Planning](docs/PLANNING.md) · [Orchestration](skills/planning-orchestration/SKILL.md) |
| Code and verify | [Engineering](skills/coding-engineering/SKILL.md) · [Contract tests](skills/software-contract-testing/SKILL.md) |
| Independent review | [Subagents](skills/subagent-review-protocol/SKILL.md) · [Evidence](skills/acceptance-evidence-ledger/SKILL.md) |
| Image, video, audio | [Image](skills/image-generation/SKILL.md) · [Video](skills/video-intelligence/SKILL.md) · [Audio](skills/audio-speech-engineering/SKILL.md) |
| Faster research | [Efficiency](skills/adaptive-efficiency/SKILL.md) · [Research](skills/deep-wide-research/SKILL.md) |

## Try it

```bash
python tools/validate.py
python -m unittest discover -s tests -q
python tools/plan_engine.py examples/planning-v10.3.json
python tools/agent_audit.py examples/planning-v10.3.json
```

The audit runs four real, independent read-only Python workers. These are deterministic checks, **not** external AI models. No paid service is installed or triggered.

## Give it to an AI

> Read the latest [AGENTS.md](AGENTS.md) and [MASTER_PROMPT.md](MASTER_PROMPT.md) and use the relevant PARALLAX SKILL.md modules. Establish actual tools and permissions, prefer first-principles reasoning and independent evidence, validate code, and report real outcomes. Use planning for complex work; do not load every skill needlessly. Do not invent research, external model calls, holdout results, memory changes or elapsed time.

[Source registry](sources/sources.json) · [Project continuity](docs/CONTINUITY.md) · [Validation](AUDIT.md) · [Release instructions](PUBLISHING.md)

**Boundaries:** PARALLAX is public by the owner's choice; no other repository's visibility is changed. Method descriptions do not grant new tools or background execution. A source URL is not measured proof of improvement.

<details>
<summary>All 114 specialist skills</summary>

`acceptance-evidence-ledger` · `accessibility-assurance` · `action-audit-trail` · `adaptive-efficiency`
`agent-evaluation` · `agent-interoperability` · `algorithmic-complexity` · `api-contract-engineering`
`api-evolution-compatibility` · `artifact-delivery-gates` · `ast-safe-transformations` · `audio-provider-routing`
`audio-realtime-streaming` · `audio-speech-engineering` · `browser-compute-bridge` · `browser-regression`
`cache-invalidation-design` · `capability-contract` · `causal-inference` · `checkpoint-resume-reliability`
`code-synthesis-evaluation` · `coding-engineering` · `concept-laboratory` · `context-engineering`
`continuous-learning-memory` · `core-orchestration` · `cost-aware-architecture` · `creative-discovery`
`creative-quality-diversity` · `cross-platform-apps` · `data-quality-pipelines` · `database-query-planning`
`database-reliability` · `decision-systems` · `deep-reasoning` · `deep-wide-research`
`deliberate-work-sessions` · `dependency-graph-acceleration` · `design-system-engineering` · `differential-testing`
`document-ingestion` · `durable-automation` · `evolution-governance` · `experimental-verification`
`expressive-audio-production` · `fault-tolerant-distributed-systems` · `formal-assumption-register` · `formal-invariants`
`frontier-model-routing` · `graphics-render-pipeline` · `hardware-physical` · `human-communication`
`humor-writing` · `image-generation` · `incremental-build-analysis` · `interface-design`
`interface-state-testing` · `knowledge-distillation` · `latency-budgeting` · `learning-curriculum`
`model-routing-benchmarks` · `multimodal-evidence-alignment` · `multimodal-fusion` · `mutation-testing-strategy`
`networking-digital` · `observability-latency` · `originality-evaluation` · `parallel-execution-correctness`
`performance-regression-detection` · `performance-speed` · `performance-validation` · `planning-orchestration`
`policy-authorization` · `privacy-by-design` · `property-based-testing-lab` · `reproducible-environments`
`research-source-independence` · `retrieval-quality` · `root-cause-debugging` · `runtime-memory-analysis`
`safe-code-agent-workflow` · `scientific-computation` · `scientific-research` · `security-reliability`
`self-evolution-engine` · `skill-supply-chain` · `software-contract-testing` · `source-discovery`
`speech-quality-laboratory` · `streaming-backpressure` · `structured-output-reliability` · `subagent-review-protocol`
`symbolic-execution-planning` · `threat-modeling` · `type-directed-code-synthesis` · `ui-render-performance`
`video-audio-sync-lab` · `video-captions-accessibility` · `video-code-production` · `video-color-science`
`video-encoding-efficiency` · `video-generation-backends` · `video-generative-workflows` · `video-intelligence`
`video-media-provenance` · `video-qc-telemetry` · `video-render-budget` · `video-shot-grammar`
`video-storytelling-critique` · `video-temporal-consistency` · `video-timeline-engineering` · `visual-production-pipeline`
`visual-regression` · `voice-synthesis-architecture`

</details>

*Clear mechanisms. Real artifacts. No performance theatre.*
