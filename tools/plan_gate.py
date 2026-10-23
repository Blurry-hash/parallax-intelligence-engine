#!/usr/bin/env python3
"""Dry-run workflow DAG and explicit capability/approval policy. No execution.

Plan is declarative JSON; all validation is offline. Unknown capabilities are denied.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path

RISKS = {'read', 'execute', 'network', 'publish', 'write', 'paid', 'destructive', 'private_data'}
RESTRICTED = RISKS - {'read'}

class PlanError(ValueError):
    pass

def inspect(plan: dict, grants: set[str] | None = None) -> dict:
    if not isinstance(plan, dict) or not isinstance(plan.get('steps'), list):
        raise PlanError('steps must be a list')
    grants = set(grants or ())
    if not grants <= RISKS:
        raise PlanError('unknown grants')
    steps = plan['steps']
    if not steps or len(steps)>100:
        raise PlanError('1..100 steps required')
    graph: dict[str,list[str]] = {}
    pending: list[dict] = []
    for step in steps:
        if not isinstance(step,dict) or set(step)-{'id','action','requires','risk','evidence'}:
            raise PlanError('unexpected step fields')
        sid=step.get('id')
        if not isinstance(sid,str) or not sid.isidentifier() or len(sid)>64 or sid in graph:
            raise PlanError('duplicate/invalid id')
        if not isinstance(step.get('action'),str) or not step['action'].strip() or len(step['action'])>300:
            raise PlanError('action required')
        deps=step.get('requires',[])
        if not isinstance(deps,list) or not all(isinstance(x,str) for x in deps) or len(set(deps))!=len(deps):
            raise PlanError('invalid dependencies')
        risk=step.get('risk','read')
        if risk not in RISKS:
            raise PlanError('unknown risk')
        graph[sid]=deps
        if risk in RESTRICTED and risk not in grants:
            pending.append({'step':sid,'reason':f'grant required: {risk}'})
    for sid,deps in graph.items():
        if sid in deps or any(dep not in graph for dep in deps):
            raise PlanError('self or missing dependency')
    ordered=[]; visited=set(); active=set()
    def visit(sid):
        if sid in active:raise PlanError('dependency cycle')
        if sid in visited:return
        active.add(sid)
        for dep in graph[sid]:visit(dep)
        active.remove(sid);visited.add(sid);ordered.append(sid)
    for sid in graph:visit(sid)
    # Grants are observations supplied by host/user, never inferred from prose.
    return {'status':'blocked' if pending else 'eligible_not_executed','order':ordered,
            'blocked':pending,'executed':False,'grants_observed':sorted(grants)}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('plan',type=Path)
    p.add_argument('--grant',action='append',choices=sorted(RISKS),default=[])
    a=p.parse_args()
    try:print(json.dumps(inspect(json.loads(a.plan.read_text()),set(a.grant)),indent=2))
    except (ValueError,OSError) as e:p.error(str(e))
if __name__=='__main__':main()
