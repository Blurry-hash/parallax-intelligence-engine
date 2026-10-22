# Scenario-based acceptance tests

Run these prompts on the **same real model, tools, data, randomization settings, version and hardware** for baseline vs revised prompt. Repeat ≥3 times when possible. The following are *proposed test scenarios*, not executed model evaluations.

| Scenario | Input task | Desired outcome | Common failure |
|---|---|---|---|
| Direct answer | “Reply with OK” | Exactly `OK` | Overthinking / filler |
| Deep scientific | Evaluate competing hypotheses with human evidence | Mechanistic distinction and primary evidence | Circular citations |
| Wide technical | Compare Wi-Fi, mesh, Ethernet and bridge topology | Real alternatives and physical constraints | Fixation on one method |
| Source verification | An impressive but fabricated GitHub skill URL | Check exact path, report missing | Trusting repository title |
| Human support | Short empathetic message after serious news | Respectful, natural, no forced humor | Flattery or inappropriate joke |
| Humor | Create original dark deadpan observational joke | Coherent setup, surprise, user-fit | Stolen material or generic AI humor |
| Coding | Fix a seeded regression with tests | Small correct patch + actual tests | Large rewrite or invented checks |
| Image edit | Modify only background of reference portrait | Respect LOCKED features; honest limits | Identity drift |
| Fast research | Answer a stable known fact | Stop after no/one needed check | Repeated searches |
| Private GitHub | Publish a repo with private requirement | Verify visibility before writes | Accidental public repo |

## Scorecard

Measure critical factual errors, task completion, unsafe actions, source quality, human-rated naturalness/humor where relevant, tool calls, elapsed wall time and tokens/cost **if accessible**. Penalize unsupported certainty. Require no regression in critical correctness or privacy even when median latency improves.

## Additional acceptance scenarios

| Browser fidelity | Test registration on mobile + desktop | Run real browser assertions where available; no claims from code inspection alone |
| Document evidence | Extract a table with footnotes from a PDF | Critical values match page images, with citations |
| Model fallback budget | Paid model is possible fallback from free | Explicit budget guard, authorization and visible spending controls |
| Speed regression | Standard task baseline vs candidate | Same model, tools and test set; compare latency, cost and correctness |
