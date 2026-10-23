# Repository refresh contract

**Current source of truth:** live `main` commit and its files, not the remembered version number.

When to recheck: first activation in a new chat; explicit owner update; task starts after 24+ hours and version matters; before changing repo; after publish; a test failure suggests drift. Reuse recent verified SHA for routine responses to avoid wasting calls. A commit change alone does not imply better quality.

Inspect `AGENTS.md`, `MASTER_PROMPT.md`, `README.md`, `docs/CONTINUITY.md`, then only task-relevant `SKILL.md`; compare differences and invalidate affected assumptions. Record source, observation time, commit SHA and whether files were actually read. If offline, label `CACHED`.

`python tools/freshness_gate.py --repo Blurry-hash/parallax-intelligence-engine --force` fetches read-only revision metadata when network works; it cannot schedule itself. Persistent monitoring requires a genuinely installed scheduler or agent and user approval.
