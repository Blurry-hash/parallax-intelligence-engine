---
name: reproducible-environments
description: Hermetic toolchains and build provenance; use for making developer, ci and deployment results consistent
---

# Hermetic toolchains and build provenance

**Trigger:** Making developer, CI and deployment results consistent.

**Goal:** Make a concrete, reviewable improvement without inventing new model capabilities.

## Operational procedure

1. Establish the workload, correctness contract, resource budget, accessible tooling and protected requirements.
2. Pin runtime/toolchain and dependencies; declare required system tools.
3. Use deterministic artifacts, checksums and isolated build steps; avoid hidden network installs.
4. Rebuild from clean checkout and compare manifest, tests and output hashes.
5. Record measured results, counterexamples and rollback steps; compare with baseline and avoid introducing unnecessary dependencies.

**Check:** Recreated build behaves identically within documented nondeterminism.

## Source access

Relevant upstream reference: https://github.com/reproducible-builds/reproducible-website. Consult current documentation and its license before adopting code. A repository link is a pointer, not installed software or proof of a performance claim. Do not run untrusted scripts automatically.

## Fallback and limits

If no executor is available, provide an executable test plan or patch and label it NOT EXECUTED. Never pretend to have measured speed, quality, security or correctness without running the relevant checks.

## v11.0 — Three targeted extensions

1. **Task-specific contract:** For **reproducible-environments**, freeze the task objective, known input constraints and actual available tools; avoid loading this skill when it adds no user value.
2. **Adversarial failure probe:** Test the strongest failure case for this skill, including incompatible requirements, unavailable tools and unverified claims; record what was not executed.
3. **Lean evidence and fallback:** Prefer a small decisive verification or truthful alternative over unnecessary tool use. Image/video rendering is optional and never required for a nonimage request.
