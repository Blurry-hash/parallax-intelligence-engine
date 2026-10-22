# Creativity validation protocol

**Purpose:** Compare creative output reliably. Do not confuse output length, number of ideas or lexical diversity with novelty or intelligence. No objective "50,000% better" metric exists without specifying a baseline, denominator and domain.

## Design

- Fix 12 held-out briefs: 3 hardware, 3 AI/software, 2 visual/video, 2 communications, 2 scientific ideation. Save requirements and prohibited shortcuts.
- Blindly compare baseline and updated instructions with the same model, temperature, tools, time budget and number of candidates. Randomize ordering.
- Use >=3 independent raters where feasible. Each rates originality, mechanistic difference, practical utility, feasibility, internal consistency, specificity and surprise from 1 to 5.
- Novelty requires prior-art review; otherwise report only *perceived originality*. Include obvious competitor solutions as counterexamples.
- Report mean and spread of ratings, duplicate-mechanism fraction, completion rate, latency p50/p95, tokens and tool cost. Track failures and invalid designs, not just winners.
- Test on unseen briefs after optimizing prompts. A procedure gets promoted only if it beats the prior version without reducing task completion or accuracy.

## Automated sanity check

`python3 tools/idea_diversity.py examples/creative-candidates.json` reports lexical overlap, **not** semantic similarity, feasibility or verified novelty.

## Source inspirations

- Google DeepMind [FunSearch](https://github.com/google-deepmind/funsearch): evolutionary program discovery with evaluators.
- USC [pyribs](https://github.com/icaros-usc/pyribs): quality-diversity search in measurable spaces.
- Stanford [DSPy](https://github.com/stanfordnlp/dspy): metric-driven program/prompt optimization.
- Google DeepMind [AlphaEvolve results](https://github.com/google-deepmind/alphaevolve_results): verifiable algorithmic results, not full agent code.
