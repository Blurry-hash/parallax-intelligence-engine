"""Shared exploratory paired inference. No dependencies; fixed-seed reproducibility.

20 independent holdout pairs is a minimum policy, not a power guarantee. The
bootstrap resamples whole matched tasks. Sign test is exact, two-sided, ignores
zero differences and assumes independent pairs. Neither proves causality.
"""
from __future__ import annotations
import math
import random
import statistics

MIN_PAIRS = 20
CONFIDENCE = .95
BOOTSTRAP_RESAMPLES = 2000


def paired_summary(baseline, candidate, *, seed=1729, higher_is_better=True):
    baseline, candidate = list(baseline), list(candidate)
    if not baseline or len(baseline) != len(candidate) or len(baseline)>10000:
        raise ValueError('nonempty matched observations required')
    if any(type(x) not in (int, float) or not math.isfinite(x) for x in baseline + candidate):
        raise ValueError('finite numeric observations required')
    diffs = [float(c)-float(b) for b,c in zip(baseline,candidate)]
    n=len(diffs); rng=random.Random(seed)
    samples=sorted(statistics.mean(rng.choices(diffs,k=n)) for _ in range(BOOTSTRAP_RESAMPLES))
    def quantile(q):
        p=(len(samples)-1)*q; a=math.floor(p); b=math.ceil(p)
        return samples[a]+(samples[b]-samples[a])*(p-a)
    positive=sum(d>0 for d in diffs); negative=sum(d<0 for d in diffs)
    discordant=positive+negative; tail=min(positive,negative)
    # Binomial(0.5) tail via lgamma avoids enormous integer-to-float overflow.
    p=min(1.,2*sum(math.exp(math.lgamma(discordant+1)-math.lgamma(k+1)-math.lgamma(discordant-k+1)-discordant*math.log(2)) for k in range(tail+1))) if discordant else 1.
    ci=[quantile(.025),quantile(.975)]
    sufficient=n>=MIN_PAIRS
    return {'n_pairs':n,'minimum_pairs':MIN_PAIRS,'sample_sufficient':sufficient,
            'mean_delta':statistics.mean(diffs),'confidence':CONFIDENCE,
            'mean_delta_bootstrap_ci':ci,'bootstrap_resamples':BOOTSTRAP_RESAMPLES,
            'paired_test':'exact_two_sided_sign_test','p_value':p,
            'nonzero_pairs':discordant,'positive_pairs':positive,'negative_pairs':negative,
            'higher_is_better':higher_is_better,
            'improvement_supported':sufficient and (ci[0]>0 if higher_is_better else ci[1]<0) and p<.05,
            'note':'Exploratory inference; independent representative holdouts and a prespecified metric are required. Multiple comparisons need correction; sample minimum is not a power calculation.'}
