# Code Logic & Performance v10.2

## Methods
1. Convert natural-language task to observable behavior, invariants, resource budgets and a failing test.
2. Select the smallest relevant specialist skill; inspect actual code and dependencies.
3. Propose candidates with complexity/assumption tradeoffs; baseline performance and correctness before edits.
4. Implement reversible changes; verify syntax/type/security/regressions and reject unsafe concurrency or cache scopes.
5. Measure paired task latency (p50/p95), correctness and cost on independent holdouts; log all test conditions.

## Tool contracts
- `complexity_guard.py`: AST heuristic for Python functions; **not Big-O estimation**, linter replacement, or full security verification.
- `critical_path.py`: pure deterministic DAG schedule; effort estimates supplied externally. Cycles/unknown references are rejected. Parallel frontiers are illustrative; real workers need authorization and conflict-free resources.
- `perf_gate.py`: paired case scorer; rejects missing/duplicate IDs, invalid data, correctness regressions or excessive p95 slowdown. Small samples are flagged as illustrative only.

These can be used by agents without paid APIs or model access, but do not install third-party packages automatically.
