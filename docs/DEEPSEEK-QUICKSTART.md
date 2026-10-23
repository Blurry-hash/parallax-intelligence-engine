# DeepSeek Free — complete skill inventory and real code tests

**The missing 24 skills were a listing error.** Public GitHub's recursive tree API returned 142 actual `skills/*/SKILL.md` files, with `truncated: false`. The source registry contained 157 references. No skills require reinstalling.

## Step 1 — GET-only complete catalog

Start with this small JSON file:

https://raw.githubusercontent.com/Blurry-hash/parallax-intelligence-engine/main/bridge/v1/index.json

The pages are maintained by `python tools/deepseek_catalog.py` and checked in GitHub CI whenever the repository changes. Its `read_base` URL and `pages` arrays enumerate **12 short skills pages** and **20 short source pages**. Retrieve every page; if any GET fails, retry that page or report the list as PARTIAL. Count `entries` across all pages; don't confuse lazy-loaded GitHub HTML rows with missing skills.

**Fallback 1:** use GitHub's JSON tree: https://api.github.com/repos/Blurry-hash/parallax-intelligence-engine/git/trees/main?recursive=1 . Require `truncated:false`, and count paths matching `skills/<name>/SKILL.md`.

**Fallback 2:** use a specific GitHub file page, for example https://github.com/Blurry-hash/parallax-intelligence-engine/blob/main/bridge/v1/skills-12.json . Raw file URLs are preferred when supported. These catalogs contain paths, not the full 142 instruction files.

## Step 2 — actual CI proof with **GET only**

GitHub runs the ordinary validation suite after each push. A second, restricted DeepSeek test bench now runs the full Python suite **daily at 03:17 UTC** (best effort); no manual action is required for a scheduled run. These tests execute in GitHub Actions, **not inside DeepSeek**.

Read these public endpoints in order:

1. Current default-branch SHA: `https://api.github.com/repos/Blurry-hash/parallax-intelligence-engine/commits/main` (read `sha`).
2. Latest push validation: `https://api.github.com/repos/Blurry-hash/parallax-intelligence-engine/actions/workflows/validate.yml/runs?branch=main&per_page=5`.
3. Scheduled full-suite test: `https://api.github.com/repos/Blurry-hash/parallax-intelligence-engine/actions/workflows/deepseek-test-bench.yml/runs?event=schedule&branch=main&per_page=5`. GitHub's scheduler may delay, skip or disable runs.
4. If either filtered API endpoint is unavailable, try `https://api.github.com/repos/Blurry-hash/parallax-intelligence-engine/actions/runs?per_page=3` and inspect `path`, `event`, `head_sha`, `status`, `conclusion`.
5. Accept a test claim only when `head_sha` exactly matches current `main`, `status` is `completed` and `conclusion` is `success`. For public job steps: `https://api.github.com/repos/Blurry-hash/parallax-intelligence-engine/actions/runs/{run_id}/jobs` (replace `{run_id}` with the run ID). Raw logs may require login; run metadata does not.
6. If no same-commit finished successful run appears, state exactly that. Never treat a green test of an older SHA, `in_progress` run or unsigned commit as a passing current test.

The small [GET catalog](../bridge/v1/index.json) repeats these links and displays the source-page verification labels. Its `verified-page` label means only that someone fetched the page, not that the information was scientifically or technically validated.

### Optional immediate manual test

[Run workflow in GitHub](https://github.com/Blurry-hash/parallax-intelligence-engine/actions/workflows/deepseek-test-bench.yml), choose `inventory`, `full`, `image` or `source-check`. Only an authenticated person or authorized tool can launch it. DeepSeek's read-only web search cannot POST, click or submit arbitrary Python. Keep tokens out of URLs and chats.

## Step 3 — other fallbacks

- **Interactive browser:** The user can run Python via [JupyterLite](https://jupyterlite.github.io/demo/lab/index.html) and paste output back. Static GET cannot operate JavaScript or WebAssembly.
- **Owner-hosted relay:** a separately deployed, authenticated service can receive approved POST test jobs and expose bounded GET results; enforce isolation, quotas and approval. No such relay is bundled.
- **math.js arithmetic:** a GET result like `7*6=42` is not a general-purpose sandbox and may fail intermittently. Do not claim a second failed GET invalidates the first, or that either proves Python execution.

## Limitations DeepSeek should report naturally

No local shell, no file writes, no persistent memory API, no browser interaction and no external provider authorization means those actions were **not performed**. Public repo reading does not require a GitHub token. GitHub code-signature verification is separate from CI results. This repository currently has no top-level LICENSE; do not assume a reuse license. Never invent an implementation, signed commit or successful test.
