# Evaluating skills rather than counting them

Three layers answer different questions:

1. Unit/integration tests establish that deterministic tools reject known bad inputs and produce expected outputs.
2. Golden behavior specifications give each skill a task, expected behavior and negative trap. They define what to assess, but reading a specification does not demonstrate the model followed it.
3. Controlled A/B and single-skill ablations measure whether instructions help actual model behavior on representative, unseen tasks.

`benchmarks/skill-golden-specs.json` indexes a behavior specification for every installed skill. Initial specifications draw acceptance language from each skill and need domain review before they are treated as a high-quality evaluation set. They are not fabricated passed model tests. Use the curated cases in `benchmarks/behavior-cases.json` to exercise specific important failures; expand them with genuinely unseen tasks and blinded human judgments.

Hold model version, settings, tools and inputs fixed. Randomize baseline/candidate order and repeat stochastic runs; keep task-level dependence intact rather than treating repeat seeds as independent tasks. Pin evaluator/rubric versions. Record actual output, objective checks, human rubric, latency, tokens, cost and provenance. Never optimize on final holdout results.

`tools/skill_eval.py` validates externally supplied paired observations for a selected skill, produces bootstrap intervals and an exact paired sign test, and flags critical failures. Default mean token and latency budgets do not allow increases; predeclared positive `limits.max_token_ratio` and `limits.max_latency_ratio` can set explicit alternative budgets. Every report includes paired quality, token and latency summaries. Baseline uses no optional skill and challenger uses only that skill: the simplest ablation. `tools/bench_compare.py` supports broader comparisons. Neither generates model outputs or authenticates judge truth.

The shared 20-pair minimum is a policy floor, not a universal power calculation. Use a task-specific practical threshold and power plan. Report all registered outcomes and apply a multiple-comparison correction (for example Holm) before testing many skills. Unequal tasks, contaminated holdouts or correlated cases can invalidate inference even with a narrow interval.

Do not automatically delete low-scoring skills. Check routing coverage, domain difficulty and regression risk; replicate, merge redundant procedures, retain failures, and retire only after review. Cost efficiency means quality at a measured token/latency budget, not the shortest prompt at any cost.
