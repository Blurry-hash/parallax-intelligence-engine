---
name: safe-code-agent-workflow
description: Reliable AI code agents and tool boundaries; use for letting any ai modify repositories while controlling damage
---

# Reliable AI code agents and tool boundaries

**Trigger:** Letting any AI modify repositories while controlling damage.

**Goal:** Make a concrete, reviewable improvement without inventing new model capabilities.

## Operational procedure

1. Establish the workload, correctness contract, resource budget, accessible tooling and protected requirements.
2. Read project policy, branch/permissions and test commands before edits.
3. Draft minimal patch with rollback; treat generated code and fetched repos as untrusted.
4. Require explicit consent for destructive operations, billing, deployment and privacy changes.
5. Record measured results, counterexamples and rollback steps; compare with baseline and avoid introducing unnecessary dependencies.

**Check:** Diff reviewed, checks recorded and no unauthorized external effect.

## Source access

Relevant upstream reference: https://github.com/openai/codex. Consult current documentation and its license before adopting code. A repository link is a pointer, not installed software or proof of a performance claim. Do not run untrusted scripts automatically.

## Fallback and limits

If no executor is available, provide an executable test plan or patch and label it NOT EXECUTED. Never pretend to have measured speed, quality, security or correctness without running the relevant checks.

## v11.0 — Three targeted extensions

1. **Task-specific contract:** For **safe-code-agent-workflow**, freeze real delegated capabilities and permission boundaries; avoid loading this skill when it adds no user value.
2. **Adversarial failure probe:** Test the strongest failure case for this skill, including incompatible requirements, unavailable tools and unverified claims; record what was not executed.
3. **Lean evidence and fallback:** Prefer a small decisive verification or truthful alternative over unnecessary tool use. Image/video rendering is optional and never required for a nonimage request.
