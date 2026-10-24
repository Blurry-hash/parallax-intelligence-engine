<div align="center">
  <img src="assets/parallax-signal.svg" alt="PARALLAX — Working intelligence" width="100%" />

**Think clearly. Build carefully. Check what matters.**

`Generation 2` · `Python 3.12+` · `Local-first tools`
</div>

PARALLAX gives an AI a practical way to approach unfamiliar work: understand the problem, choose the right methods, use the tools it has, and check the result. It brings together engineering, research, creative work and critical reasoning without making every conversation a heavyweight workflow.

The library is useful when a task needs more than a plausible answer. A debugging session needs a reproducible failure. A research question needs sources that bear on the claim. A video edit needs an actual timeline and a playable result. PARALLAX keeps those distinctions clear.

## Start with the work

| You want to… | Start here |
|:--|:--|
| Build or repair software | [Engineering](skills/coding-engineering/SKILL.md) · [Contract tests](skills/software-contract-testing/SKILL.md) |
| Research a difficult question | [Deep research](skills/deep-wide-research/SKILL.md) · [Experimental verification](skills/experimental-verification/SKILL.md) |
| Develop an argument | [Debate intelligence](skills/debate-intelligence/SKILL.md) |
| Understand a video | [Video understanding](skills/video-understanding/SKILL.md) |
| Make a consistent edit | [Editorial style](skills/editorial-style-system/SKILL.md) · [Video production](skills/video-code-production/SKILL.md) |
| Shape an image or interface | [Image generation](skills/image-generation/SKILL.md) · [Design direction](docs/DESIGN-DIRECTION.md) |
| Coordinate substantial work | [Agent orchestration](skills/adaptive-agent-orchestration/SKILL.md) · [Planning](docs/PLANNING.md) |
| Improve a working method | [Self-evolution](skills/self-evolution-engine/SKILL.md) · [Evaluation](docs/EVALUATION.md) |

## Use it with your AI

Give your assistant access to a checkout or an uploaded release, then use the [activation prompt](docs/UNIVERSAL-ACTIVATION.md). A [Claude Sonnet 4.5 prompt](docs/CLAUDE-SONNET-4-5.md) includes full-repository onboarding with an honest reading ledger. Once onboarded, load only the modules the current task needs.

For a private repository, use authenticated access or upload a reviewed release to the AI service. A public download link makes its contents publicly retrievable. [Private access options](docs/PRIVATE-ACCESS.md) explain the tradeoffs.

## Small tools, inspectable results

```bash
python tools/route_task.py "Review a video and extract its practical steps"
python tools/validate.py
python -m unittest discover -s tests -q
```

The [local MCP adapter](docs/MCP.md) exposes routing, validation and loop assessment to compatible clients. [Media ingestion](tools/media_ingest.py) prepares timestamped frames and optional audio for analysis; speech recognition and semantic review require an available backend. [Video QC](tools/video_qc.py) checks encoded media against explicit requirements.

## A library, not a promise

A skill is a procedure to apply and evaluate. It does not install a model, grant account access or guarantee better answers. Offline tests check the tools’ behavior; improvements in reasoning, originality, creativity or token use need controlled evaluations with unseen holdout tasks and inspectable evidence.

Browse the [complete skill catalog](docs/SKILL-CATALOG.md), the [source registry](sources/README.md) and the [evaluation protocol](docs/EVALUATION.md). The registry contains 157 linked references with separate access/provenance states; a listed reference is not proof of a skill’s effectiveness.

<sub>[Agent entrypoint](AGENTS.md) · [Working prompt](MASTER_PROMPT.md) · [Version policy](docs/VERSIONING.md) · [Continuity](docs/CONTINUITY.md)</sub>
