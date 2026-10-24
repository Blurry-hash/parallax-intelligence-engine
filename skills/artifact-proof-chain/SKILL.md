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

https://slsa.dev/spec/v1.0/provenance (artifact provenance) and https://docs.python.org/3/library/hashlib.html (content digests). Digests establish byte identity, not authorship.

## Fallback and limits

No model-weight updates, background execution, paid inference or external API calls occur merely by loading this skill.
