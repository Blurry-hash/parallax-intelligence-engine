# PARALLAX v10 — Publication and visibility policy

The owner has explicitly designated `Blurry-hash/parallax-intelligence-engine` as **public for now**. Publishing v10 must never change the visibility of this or any other repository. No admin-level visibility operations are part of the release workflow.

## GitHub connector release

1. Verify the target owner/name, current visibility, default branch, and current HEAD SHA.
2. Audit release files for credentials, sensitive information, license conflicts and executable CI actions.
3. Validate the release ZIP and `RELEASE_MANIFEST.json` SHA-256 digests.
4. Create Git blobs and a tree based on the current branch tree, preserving unrelated files.
5. Create a commit with the current branch HEAD as parent; advance the branch **without force**.
6. Fetch the updated tree and README and verify the live GitHub Actions result. Report failures rather than claiming success.

## Windows local fallback

The legacy filename `scripts/private-release.ps1` is retained for backward compatibility, **but its implementation no longer changes repo visibility**. It selects the latest PARALLAX ZIP in Downloads, previews by default, and pushes only when `-Apply` is supplied.

```cmd
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%USERPROFILE%\Downloads\private-release.ps1"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%USERPROFILE%\Downloads\private-release.ps1" -Apply
```

`gh auth status` must show the intended account. If workflow changes are rejected, use `gh auth refresh -h github.com -s workflow`; this authorizes changes to GitHub Actions definitions without changing the repo visibility. Do not use `--force` on push.

## Verification

```bash
python tools/validate.py
python -m unittest discover -s tests -v
python tools/video_timeline.py --help
python tools/video_qc.py --help
```

A source reference, file inclusion or green test badge does not demonstrate a generic increase in AI intelligence. Benchmark actual task outcomes and costs on held-out workloads.
