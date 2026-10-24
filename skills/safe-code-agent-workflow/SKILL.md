---
name: safe-code-agent-workflow
description: Reliable AI code agents and tool boundaries; use for letting any ai modify repositories while controlling damage
---

# Reliable AI code agents and tool boundaries

**Trigger:** Letting any AI modify repositories while controlling damage.

## Operational procedure

1. Read project policy, branch/permissions and test commands before edits.
2. Draft minimal patch with rollback; treat generated code and fetched repos as untrusted.
3. Require explicit consent for destructive operations, billing, deployment and privacy changes.

**Check:** Diff reviewed, checks recorded and no unauthorized external effect.

## Source access

Relevant upstream reference: https://github.com/openai/codex. Consult current documentation and its license before adopting code. A repository link is a pointer, not installed software or proof of a performance claim. Do not run untrusted scripts automatically.
