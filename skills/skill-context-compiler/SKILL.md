---
name: skill-context-compiler
description: Reduce context waste using bounded deterministic skill selection with an explicit truncation warning.
---

# Skill Context Compiler

## Operational procedure

1. Start with `tools/skill_dispatch.py "task description" --max-skills 3 --max-chars 6000` for candidate modules.
2. Inspect the returned sources: lexical overlap is not semantic understanding. Select by the actual objective, compatibility and protected constraints.
3. Read full skill files before actions; any truncated excerpt is a navigation hint, not complete execution instructions.
4. Measure skill selection precision and end-to-end task success; smaller prompt size is not automatically a quality win.

**Check:** Feed image, code, audio and Swedish planning queries; test budget caps and explicitly review false negatives.

## Source access

Official reference design: https://developers.google.com/optimization/scheduling/job_shop (resource scheduling), https://developers.openai.com/api/docs/guides/agents/guardrails-approvals (gated agent actions), https://github.com/openai/openai-agents-python (optional authorized multi-model runtime). These are documentation links, not installed providers or execution capabilities.

## Fallback and limits

No model-weight updates, background execution, paid inference or external API calls occur merely by loading this skill.
