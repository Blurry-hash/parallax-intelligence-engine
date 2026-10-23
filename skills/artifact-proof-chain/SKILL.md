---
name: artifact-proof-chain
description: Verify the bytes of real local deliverables and reject symlinks, path traversal or tampering.
---

# Artifact Proof Chain

## Operational procedure

1. Identify final generated artifacts and a trusted local root. Run `tools/artifact_proof.py <root> <relative-file> ...` to record size and SHA-256 for every file.
2. Store the manifest with the release record and run `tools/artifact_proof.py <root> --verify manifest.json` after moving or unpacking files.
3. Stop if the bytes differ, a symlink appears, a path escapes the root, or file size exceeds limits.
4. Distinguish content integrity (matching an embedded manifest) from authenticity (trusted signer and external verified provenance). Add signing only through a real authorized key service.

**Check:** Tamper with the file and verify it is rejected; attempt `../` traversal and a directory symlink. Do not call self-issued digests independent proof of authorship.

## Source access

Official reference design: https://developers.google.com/optimization/scheduling/job_shop (resource scheduling), https://developers.openai.com/api/docs/guides/agents/guardrails-approvals (gated agent actions), https://github.com/openai/openai-agents-python (optional authorized multi-model runtime). These are documentation links, not installed providers or execution capabilities.

## Fallback and limits

No model-weight updates, background execution, paid inference or external API calls occur merely by loading this skill.
