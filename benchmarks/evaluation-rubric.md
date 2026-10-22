# Evaluation rubric

Score each axis 0–5 with **documented evidence**. Never claim an uplift from an unpaired example.

| Axis | 0 | 3 | 5 |
|---|---|---|---|
| Accuracy | False | Mostly correct | All critical facts verified |
| Functional result | Fails | Partial | Acceptance criteria met |
| Security/privacy | Unsafe | Basic checks | Risks modeled and tested |
| Reliability | Not tested | Unit checked | Regression and failure-path checks |
| Efficiency | Worse than baseline | Similar | Repeated measurable improvement |
| Source trust | Fabricated | Source given | Primary, current, relevant provenance |
| Transparency | Unfounded claims | Limits mentioned | Executed vs proposed clearly distinguished |

## Evaluation design
- Freeze a baseline prompt/model/tool configuration and use a **held-out** test suite.
- Benchmark ≥3 runs per case if runtime permits; compare both median and tail latency.
- Separate tokens, tool calls, cost and correctness; fastest low-quality response is not the winner.
- Track regressions and failures, not only successful cases.
- Do not imply this repository's methods are benchmark-validated until actual benchmark data is committed.

## Test report template
```markdown
Task: 
Model/tool/version:
Baseline configuration:
Candidate configuration:
Datasets and sample sizes:
Tests actually executed:
Accuracy / pass rate:
Median / p95 latency:
Cost / tokens:
Known caveats:
Decision: retain / revise / reject
```
