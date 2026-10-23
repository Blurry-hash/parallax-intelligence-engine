#!/usr/bin/env python3
"""Assemble independent deterministic gates into a fail-closed project review.

Read-only checks. Neither a green gate nor a supplied approval argument proves
real-world authorization, model quality, artifact authenticity or agent execution.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
from plan_engine import compile_plan
from resource_scheduler import schedule
from agent_audit import run_audits
from goal_trace import audit_ledger
from quality_gate import assess
from artifact_proof import verify

ROOT=Path(__file__).resolve().parents[1]

def review(plan:dict,*,root=ROOT,ledger=None,metrics=None,proof=None,approvals=())->dict:
    plan_result=compile_plan(plan)
    scheduler=schedule(plan,approvals=approvals)
    audits=run_audits(plan,root=root)
    findings=[]
    if not audits['pass']:findings.append('independent audit worker failure')
    if scheduler['blocked']:findings.append('work blocked by approval gates: '+', '.join(scheduler['blocked']))
    if not scheduler['within_requested_budget']:findings.append('estimated schedule exceeds requested budget')
    if ledger is None:findings.append('no task evidence ledger supplied')
    else:
        try:
            traced=audit_ledger(plan,ledger)
            if not traced['complete']:findings.append('task evidence ledger incomplete')
        except ValueError as exc:findings.append('task evidence invalid: '+str(exc))
    if metrics is None:findings.append('no benchmark evidence supplied')
    else:
        try:
            report=assess(metrics)
            if not report['candidate_passes_numeric_gates'] or metrics['provenance']!='observed':findings.append('benchmark does not prove observed improvement')
        except ValueError as exc:findings.append('benchmark invalid: '+str(exc))
    if proof is None:findings.append('no content manifest supplied')
    else:
        try:verify(root,proof)
        except ValueError as exc:findings.append('content manifest failed: '+str(exc))
    return {'status':'REVIEW_READY_NOT_RELEASE_AUTHORIZED' if not findings else 'BLOCKED',
            'plan_sha256':plan_result['plan_sha256'],'findings':findings,
            'estimated_schedule_minutes':scheduler['estimated_makespan_minutes'],
            'review_workers':len(audits['workers']),
            'note':'All gates are software checks, not identity/authentication or authority to deploy.'}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('plan',type=Path);p.add_argument('--root',type=Path,default=ROOT)
    p.add_argument('--ledger',type=Path);p.add_argument('--metrics',type=Path);p.add_argument('--manifest',type=Path)
    a=p.parse_args()
    def read(x):return json.loads(x.read_text(encoding='utf8')) if x else None
    out=review(read(a.plan),root=a.root,ledger=read(a.ledger),metrics=read(a.metrics),proof=read(a.manifest))
    print(json.dumps(out,indent=2))
    if out['status']=='BLOCKED':raise SystemExit(2)
if __name__=='__main__':main()
