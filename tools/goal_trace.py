#!/usr/bin/env python3
"""Evidence-gated task completion checker. Does not execute or authenticate actions."""
import argparse,json
from pathlib import Path
from plan_engine import compile_plan
VALID={'pending','in_progress','blocked','verified'}
def audit_ledger(plan,ledger):
    compiled=compile_plan(plan)
    if not isinstance(ledger,dict) or set(ledger)!={'plan_sha256','tasks'}:raise ValueError('invalid ledger')
    if ledger['plan_sha256']!=compiled['plan_sha256']:raise ValueError('plan hash mismatch')
    tasks={t['id']:t for t in plan['tasks']};records=ledger['tasks']
    if not isinstance(records,list) or len(records)!=len(tasks):raise ValueError('missing records')
    found={}
    for r in records:
        if not isinstance(r,dict) or set(r)!={'id','state','evidence','approved'}:raise ValueError('invalid record')
        i=r['id']
        if not isinstance(i,str) or i not in tasks or i in found:raise ValueError('duplicate/unknown task')
        if not isinstance(r['state'],str) or r['state'] not in VALID or type(r['approved']) is not bool:raise ValueError('invalid state')
        e=r['evidence']
        if not isinstance(e,list) or any(not isinstance(v,str) or not 12<=len(v.strip())<=500 for v in e):raise ValueError('invalid evidence')
        if r['state']=='verified' and not e:raise ValueError('verified without evidence')
        found[i]=r
    for i,r in found.items():
        if r['state']=='verified':
            if tasks[i]['approval_required'] and not r['approved']:raise ValueError('approval required')
            if any(found[d]['state']!='verified' for d in tasks[i]['depends_on']):raise ValueError('unverified dependency')
    return {'plan_sha256':compiled['plan_sha256'],'verified':sorted(i for i,r in found.items() if r['state']=='verified'),
        'blocked':sorted(i for i,r in found.items() if r['state']=='blocked'),
        'complete':all(r['state']=='verified' for r in found.values()),
        'note':'Self-reported evidence pointers are not authenticated proof; confirm external results independently.'}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('plan',type=Path);ap.add_argument('ledger',type=Path);x=ap.parse_args()
    try:res=audit_ledger(json.loads(x.plan.read_text(encoding='utf-8')),json.loads(x.ledger.read_text(encoding='utf-8')))
    except (ValueError,OSError) as exc:ap.error(str(exc))
    print(json.dumps(res,indent=2))
if __name__=='__main__':main()
