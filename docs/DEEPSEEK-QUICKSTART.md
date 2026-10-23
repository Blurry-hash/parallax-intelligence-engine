# DeepSeek Free — complete skill inventory and real code tests

**The missing 24 skills were a listing error.** Public GitHub's recursive tree API returned 142 actual `skills/*/SKILL.md` files, with `truncated: false`. The source registry contained 157 references. No skills require reinstalling.

## Step 1 — GET-only complete catalog

Start with this small JSON file:

https://raw.githubusercontent.com/Blurry-hash/parallax-intelligence-engine/main/bridge/v1/index.json

The pages are maintained by `python tools/deepseek_catalog.py` and checked in GitHub CI whenever the repository changes. Its `read_base` URL and `pages` arrays enumerate **12 short skills pages** and **20 short source pages**. Retrieve every page; if any GET fails, retry that page or report the list as PARTIAL. Count `entries` across all pages; don't confuse lazy-loaded GitHub HTML rows with missing skills.

**Fallback 1:** use GitHub's JSON tree: https://api.github.com/repos/Blurry-hash/parallax-intelligence-engine/git/trees/main?recursive=1 . Require `truncated:false`, and count paths matching `skills/<name>/SKILL.md`.

**Fallback 2:** use a specific GitHub file page, for example https://github.com/Blurry-hash/parallax-intelligence-engine/blob/main/bridge/v1/skills-12.json . Raw file URLs are preferred when supported. These catalogs contain paths, not the full 142 instruction files.

## Step 2 — actual Python execution through GitHub Actions

An AI limited to GET requests **cannot initiate arbitrary code execution**. The working workaround is a user-started, restricted GitHub runner:

1. Open [DeepSeek Remote Test Bench](https://github.com/Blurry-hash/parallax-intelligence-engine/actions/workflows/deepseek-test-bench.yml).
2. Click **Run workflow** on main, and choose `inventory`, `full`, `image` or `source-check`.
3. Once finished, provide DeepSeek the run URL or let it read GitHub's public Actions page. Compare run `head_sha` with latest `main` and check the job concluded `success`.

This runs real Python on GitHub-hosted hardware, **not inside DeepSeek**. It requires one user action; a web-only GET client cannot click or POST. Tests exercise repository code only, not arbitrary snippets supplied exclusively in the chat. Do not send credentials or tokens to DeepSeek.

## Step 3 — other fallbacks

- **Interactive browser:** The user can run Python via [JupyterLite](https://jupyterlite.github.io/demo/lab/index.html) and paste output back. Static GET cannot operate JavaScript or WebAssembly.
- **Owner-hosted relay:** a separately deployed, authenticated service can receive approved POST test jobs and expose bounded GET results; enforce isolation, quotas and approval. No such relay is bundled.
- **math.js arithmetic:** a GET result like `7*6=42` is not a general-purpose sandbox and may fail intermittently. Do not claim a second failed GET invalidates the first, or that either proves Python execution.

## Limitations DeepSeek should report naturally

No local shell, no file writes, no persistent memory API, no browser interaction and no external provider authorization means those actions were **not performed**. Public repo reading does not require a GitHub token. GitHub code-signature verification is separate from CI results. This repository currently has no top-level LICENSE; do not assume a reuse license. Never invent an implementation, signed commit or successful test.
