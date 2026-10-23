#!/usr/bin/env python3
"""Paired offline benchmark comparison with matched ids; no invented performance gains.

Input JSON list of {id,baseline_correct,candidate_correct,baseline_ms,candidate_ms}.
Rates indicate task-level correctness, not general intelligence.
"""
from __future__ import annotations
import argparse, json, math, statistics
from pathlib import Path

def percentile(samples:list[float],q:float)->float:
    v=sorted(samples)
    if not v:raise ValueError('nonempty samples required')
    pos=(len(v)-1)*q;lo=math.floor(pos);hi=math.ceil(pos)
    return v[lo]*(hi-pos)+v[hi]*(pos-lo) if lo!=hi else v[lo]

def compare(records:list[dict])->dict:
    if not records:raise ValueError('No evaluation records')
    ids=set(); clean=[]
    for r in records:
        if not isinstance(r,dict) or not isinstance(r.get('id'),str) or not r['id'] or r['id'] in ids:
            raise ValueError('Task ids must be distinct nonempty strings')
        ids.add(r['id'])
        for k in ('baseline_correct','candidate_correct'):
            if type(r.get(k)) is not bool:raise ValueError(f'{k}: boolean required')
        for k in ('baseline_ms','candidate_ms'):
            x=r.get(k)
            if isinstance(x,bool) or not isinstance(x,(float,int)) or not math.isfinite(x) or x<=0:
                raise ValueError(f'{k}: finite positive number required')
        clean.append(r)
    n=len(clean)
    baseline=[float(r['baseline_ms']) for r in clean]
    candidate=[float(r['candidate_ms']) for r in clean]
    b_correct=sum(r['baseline_correct'] for r in clean)
    c_correct=sum(r['candidate_correct'] for r in clean)
    return {
        'n_paired':n,
        'baseline_accuracy':round(b_correct/n,5),
        'candidate_accuracy':round(c_correct/n,5),
        'accuracy_delta_pp':round(100*(c_correct-b_correct)/n,3),
        'baseline_p50_ms':round(statistics.median(baseline),2),
        'candidate_p50_ms':round(statistics.median(candidate),2),
        'baseline_p95_ms':round(percentile(baseline,.95),2),
        'candidate_p95_ms':round(percentile(candidate,.95),2),
        'mean_latency_ratio_candidate_to_baseline':round(statistics.mean(candidate)/statistics.mean(baseline),4),
        'candidate_only_correct':sum(r['candidate_correct'] and not r['baseline_correct'] for r in clean),
        'baseline_only_correct':sum(r['baseline_correct'] and not r['candidate_correct'] for r in clean),
        'caution':'No uncertainty intervals or causality established; use repeated randomized, blinded holdouts before broad claims.'
    }

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('records',type=Path)
    a=parser.parse_args()
    data=json.loads(a.records.read_text(encoding='utf8'))
    print(json.dumps(compare(data),indent=2))
