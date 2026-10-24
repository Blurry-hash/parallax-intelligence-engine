---
name: mission-release-review
description: Compose plan, independent software auditors, artifact digests, task traces and evaluation into a fail-closed release recommendation.
---

# Mission Release Review

## Operational procedure

1. Run `tools/mission_review.py examples/planning-v10.3.json` as a default blocked case: without independent artifacts, task evidence and observed holdout metrics it must block.
2. For real work, provide task evidence, benchmarks and a digest manifest. Verify the origin and independence of those materials manually or through separately authenticated systems.
3. Treat the aggregate as an advisory review, never an automatic GitHub publish or a source of account permissions.
4. Keep the last green revision available for rollback and record any blocker in `docs/CONTINUITY.md`.

**Check:** Deliberately omit evidence and corrupt manifest data; review must return BLOCKED.

## Source access

https://slsa.dev/spec/v1.0/requirements (release provenance) and https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches (required checks).

## Fallback and limits

No model-weight updates, background execution, paid inference or external API calls occur merely by loading this skill.
