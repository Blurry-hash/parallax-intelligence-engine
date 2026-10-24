#!/usr/bin/env python3
"""Paired, per-scenario regressions gate. Explicit synthetic vs observed provenance.

Rejects improvements based only on an aggregate average or absent holdouts.
"""
from __future__ import annotations
import argparse, json, math
from pathlib import Path
try:
    from paired_stats import paired_summary
except ModuleNotFoundError:
    from tools.paired_stats import paired_summary


def assess(data:dict)->dict:
    if not isinstance(data,dict) or set(data)!={'provenance','minimum_improvement','cases'}:raise ValueError('invalid evaluation contract')
    if data['provenance'] not in ('fixture','observed'):raise ValueError('invalid provenance')
    threshold=data['minimum_improvement']
    if type(threshold) not in (float,int) or not math.isfinite(threshold) or not 0<=threshold<=1:raise ValueError('invalid improvement threshold')
    cases=data['cases']
    if not isinstance(cases,list) or not 2<=len(cases)<=100:raise ValueError('need 2-100 matched cases')
    names=set(); bad=[]; totals=[0.,0.]; holdout=0
    for row in cases:
        if not isinstance(row,dict) or set(row)!={'name','split','baseline','candidate','critical'}:raise ValueError('invalid case fields')
        if not isinstance(row['name'],str) or not row['name'].strip() or row['name'] in names:raise ValueError('duplicate or missing case name')
        names.add(row['name'])
        if row['split'] not in ('development','holdout') or type(row['critical']) is not bool:raise ValueError('invalid split/critical')
        if row['split']=='holdout':holdout+=1
        scores=[]
        for key in ('baseline','candidate'):
            v=row[key]
            if type(v) not in (int,float) or not math.isfinite(v) or not 0<=v<=1:raise ValueError('scores must be finite in [0,1]')
            scores.append(float(v))
        totals[0]+=scores[0];totals[1]+=scores[1]
        # A critical regression blocks even if the aggregate improves.
        if row['critical'] and scores[1]<scores[0]-1e-9:bad.append(row['name'])
    if not holdout:raise ValueError('holdout cases required')
    change=round((totals[1]-totals[0])/len(cases),8)
    holdout_changes=[r['candidate']-r['baseline'] for r in cases if r['split']=='holdout']
    if min(holdout_changes)<-1e-9:bad += [r['name'] for r in cases if r['split']=='holdout' and r['candidate']<r['baseline']-1e-9]
    holdouts=[r for r in cases if r['split']=='holdout']
    inference=paired_summary([r['baseline'] for r in holdouts],[r['candidate'] for r in holdouts])
    safe=not bad and change>=threshold and inference['improvement_supported'] and inference['mean_delta_bootstrap_ci'][0]>=threshold
    return {'decision':'PROMOTE_CANDIDATE' if safe and data['provenance']=='observed' else ('FIXTURE_ONLY' if data['provenance']=='fixture' else 'REJECT_CANDIDATE'),
            'candidate_passes_numeric_gates':safe,'regressed_cases':sorted(set(bad)),
            'mean_gain':change,'holdout_count':holdout,'holdout_inference':inference,
            'note':'Numeric checks do not establish data independence, experimental validity, statistical significance or authorization to deploy.'}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('file',type=Path);a=p.parse_args()
    print(json.dumps(assess(json.loads(a.file.read_text(encoding='utf8'))),indent=2))
if __name__=='__main__':main()
