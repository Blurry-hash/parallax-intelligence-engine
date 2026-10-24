# Finding the right skill

`route_task.py` indexes every installed `skills/*/SKILL.md`. BM25 ranks full text with extra weight on names and descriptions; small exact alias priors help existing English and Swedish entry points. A new skill becomes searchable without a router code change. An exact skill-name query must retrieve that skill first, which the coverage test checks across the current catalog.

```sh
python tools/route_task.py "Check video frame rate duration and resolution"
python tools/skill_dispatch.py "Check video frame rate duration and resolution" --max-skills 2 --max-chars 6000
python tools/routing_eval.py examples/routing-labeled.json --k 3
python tools/validate.py --content-report
```

Both routing interfaces use the same ranker. Dispatch returns budgeted excerpts and marks truncation; read selected files fully before applying them. Character budgets are not tokenizer measurements. Reuse previously read, unchanged skills in the same session instead of repeatedly loading the catalog.

The labeled fixture reports precision@k, recall@k and hit rate. A single relevant skill in the top three yields precision 1/3 even when recall is perfect. These curated examples test retrieval plumbing, not human task success, unseen generalization or intelligence. Maintain a separate held-out set before tuning aliases or comparing ranking revisions. Evaluate multilingual paraphrases, ambiguous tasks and irrelevant queries as well as exact terms. Ablation means running the same tasks with and without a skill, with paired scoring and explicit execution provenance; retrieval metrics alone cannot establish a skill's benefit.

Content validation reports the fraction of substantial lines shared across five or more skills, warns when a skill has fewer than four unique substantial lines, and rejects exact duplicate operational procedures. Short headers and frontmatter are excluded. Shared safety instructions can be legitimate; a warning calls for editorial review, not automatic deletion. Unique prose can still be incorrect. Golden task fixtures and outcome evaluations remain necessary.
