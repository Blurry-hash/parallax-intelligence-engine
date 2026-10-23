#!/usr/bin/env python3
"""Offline champion/challenger promotion gate. Never edits prompts or deploys changes.

Pairs scores by task, requires distinct dev/holdout sets and representative domains;
conservative deterministic quality, latency, cost and critical-safety gates.
"""
from __future__ import annotations
import argparse
import json
import math
from pathlib import Path


def _finite(x, field):
    if not isinstance(x, (int, float)) or isinstance(x, bool) or not math.isfinite(x):
        raise ValueError(f'{field}: finite number required')
    return float(x)


def _p95(values):
    s = sorted(values)
    return s[math.ceil(.95 * len(s)) - 1]


def evaluate(data: dict) -> dict:
    if not isinstance(data, dict) or not isinstance(data.get('cases'), list):
        raise ValueError('Expected object with cases list')
    cases = data['cases']
    if not 5 <= len(cases) <= 10000:
        raise ValueError('Need 5–10000 matched benchmark cases')
    seen = set(); holdouts = []; development = []; domains = set()
    for c in cases:
        if not isinstance(c, dict) or not isinstance(c.get('id'), str) or not c['id'].strip() or c['id'] in seen:
            raise ValueError('Missing/duplicate task ID')
        seen.add(c['id'])
        if c.get('split') not in ('development', 'holdout'):
            raise ValueError('Every case must specify development or holdout split')
        if not isinstance(c.get('domain'), str) or not c['domain'].strip():
            raise ValueError('Each case needs a domain')
        if c['split'] == 'holdout':
            holdouts.append(c); domains.add(c['domain'])
        else: development.append(c)
        for label in ('baseline','candidate'):
            x = c.get(label)
            if not isinstance(x, dict): raise ValueError(f'Missing {label} metrics')
            for key in ('quality','latency_ms','cost_usd'):
                val = _finite(x.get(key), key)
                if (key=='quality' and not 0 <= val <= 1) or (key != 'quality' and val < 0):
                    raise ValueError(f'Out-of-range {key}')
            if not isinstance(x.get('critical_failure'), bool):
                raise ValueError('critical_failure must be boolean')
    if len(holdouts) < 5 or len(domains) < 2 or not development:
        raise ValueError('Require >=5 unseen holdout cases across >=2 domains and >=1 development case')
    if not data.get('baseline_revision') or not data.get('candidate_revision') or data['baseline_revision']==data['candidate_revision']:
        raise ValueError('Distinct baseline and candidate revisions required')
    if data.get('holdout_was_used_to_tune') is not False:
        raise ValueError('Holdout contamination cannot be ruled out')
    avg = lambda label,key:sum(float(x[label][key]) for x in holdouts)/len(holdouts)
    bq,cq=avg('baseline','quality'),avg('candidate','quality')
    bl,cl=_p95([x['baseline']['latency_ms'] for x in holdouts]), _p95([x['candidate']['latency_ms'] for x in holdouts])
    bc,cc=avg('baseline','cost_usd'),avg('candidate','cost_usd')
    score_delta=cq-bq
    failures=[]
    if any(x['candidate']['critical_failure'] for x in holdouts): failures.append('candidate critical failure')
    if any(x['candidate']['quality'] < x['baseline']['quality'] - .05 for x in holdouts):
        failures.append('protected per-task quality regression >0.05')
    if score_delta < .02: failures.append('holdout quality gain below +0.02')
    if cl > bl * 1.15: failures.append('p95 latency regression >15%')
    if cc > bc * 1.20 and cc > bc + .0001: failures.append('average cost regression >20%')
    return {'decision':'eligible_for_human_review' if not failures else 'reject',
            'safe_to_auto_deploy':False, 'holdout_cases':len(holdouts), 'holdout_domains':len(domains),
            'quality_gain':round(score_delta,6), 'baseline_quality':round(bq,6), 'candidate_quality':round(cq,6),
            'p95_latency_ms':{'baseline':bl,'candidate':cl},
            'mean_cost_usd':{'baseline':round(bc,6),'candidate':round(cc,6)},
            'failures':failures,
            'note':'This gate tests provided measurements; cannot certify metrics were collected honestly.'}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('evidence',type=Path)
    a=p.parse_args();print(json.dumps(evaluate(json.loads(a.evidence.read_text(encoding='utf-8'))),indent=2))
