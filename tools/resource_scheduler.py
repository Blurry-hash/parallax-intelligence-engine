#!/usr/bin/env python3
"""Bounded, deterministic dependency/resource scheduler. Plans ONLY; never executes tasks.

Uses a list-scheduling heuristic. Its makespan is NOT optimal. Numeric durations are
estimates supplied by the caller and do not measure real execution time.
"""
from __future__ import annotations
import argparse, heapq, json, math
from pathlib import Path
from plan_engine import compile_plan


def schedule(plan: dict, *, approvals=()) -> dict:
    summary = compile_plan(plan)  # performs the strict existing DAG validation
    approvals = set(approvals)
    tasks = {t['id']: t for t in plan['tasks']}
    if not all(isinstance(x,str) and x in tasks for x in approvals):
        raise ValueError('approvals contain an unknown task id')
    workers = plan['max_workers']
    permitted = {i for i,t in tasks.items() if not t['approval_required'] or i in approvals}
    blocked = set(tasks) - permitted
    # Block downstream tasks transitively. A prerequisite cannot be bypassed.
    changed = True
    while changed:
        old=len(blocked)
        blocked.update(i for i,t in tasks.items() if any(d in blocked for d in t['depends_on']))
        changed=len(blocked)!=old
    eligible = set(tasks) - blocked
    predecessors = {i:set(t['depends_on']) for i,t in tasks.items()}
    # Work below only on allowed subgraph, but still uses real dependencies.
    children = {i:[] for i in tasks}
    for i,t in tasks.items():
        for d in t['depends_on']:children[d].append(i)
    memo={}
    def remaining(i):
        if i in memo:return memo[i]
        memo[i]=tasks[i]['estimated_minutes'] + max((remaining(c) for c in children[i] if c in eligible),default=0)
        return memo[i]
    for i in sorted(eligible):remaining(i)
    ready={i for i in eligible if not predecessors[i]}
    running=[]  # (finish, worker, task id)
    idle=set(range(workers))
    completed=set();events=[];clock=0.0
    while ready or running:
        # Earliest available workers schedule the most consequential critical tasks.
        while idle and ready:
            i=min(ready,key=lambda k:(-remaining(k), -tasks[k]['impact'], k))
            worker=min(idle);idle.remove(worker);ready.remove(i)
            finish=clock+tasks[i]['estimated_minutes']
            heapq.heappush(running,(finish,worker,i))
            events.append({'id':i,'worker':worker,'start_minute':round(clock,6), 'end_minute':round(finish,6)})
        if not running:raise ValueError('deadlocked schedule')
        clock=running[0][0]
        while running and math.isclose(running[0][0],clock,rel_tol=0,abs_tol=1e-8):
            _,worker,i=heapq.heappop(running)
            idle.add(worker);completed.add(i)
        for i in sorted(eligible - completed - {x[2] for x in running}):
            if predecessors[i] <= completed:ready.add(i)
    result={'plan_sha256':summary['plan_sha256'],'status':'ESTIMATED_NOT_EXECUTED',
            'estimated_makespan_minutes':round(clock,6),'worker_limit':workers,
            'scheduled':sorted(events,key=lambda e:(e['start_minute'],e['worker'],e['id'])),
            'blocked':sorted(blocked),'within_requested_budget':clock<=plan['requested_minutes'],
            'note':'List scheduling heuristic, not an optimal constraint solver or actual duration. Approval arguments must be backed by external authorization.'}
    check_schedule(plan,result,approvals=approvals)
    return result


def check_schedule(plan,result,*,approvals=()):
    tasks={t['id']:t for t in plan['tasks']}
    schedule=result['scheduled']; by_id={s['id']:s for s in schedule}
    if len(by_id)!=len(schedule):raise ValueError('duplicate task')
    if set(by_id) | set(result['blocked'])!=set(tasks) or set(by_id)&set(result['blocked']):raise ValueError('coverage error')
    for ident,s in by_id.items():
        if ident not in tasks or s['worker'] not in range(plan['max_workers']):raise ValueError('invalid worker')
        if tasks[ident]['approval_required'] and ident not in approvals:raise ValueError('approval violation')
        if s['start_minute']<0 or s['end_minute']<=s['start_minute']:raise ValueError('invalid timing')
        if abs((s['end_minute']-s['start_minute'])-tasks[ident]['estimated_minutes'])>1e-5:raise ValueError('duration mismatch')
        for dependency in tasks[ident]['depends_on']:
            if dependency not in by_id or by_id[dependency]['end_minute']>s['start_minute']+1e-7:raise ValueError('precedence violation')
    for i,a in enumerate(schedule):
        for b in schedule[i+1:]:
            if a['worker']==b['worker'] and min(a['end_minute'],b['end_minute'])>max(a['start_minute'],b['start_minute'])+1e-7:raise ValueError('worker overlap')
    return True


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('plan',type=Path);p.add_argument('--approve',action='append',default=[])
    a=p.parse_args();out=schedule(json.loads(a.plan.read_text(encoding='utf8')),approvals=a.approve)
    print(json.dumps(out,indent=2,ensure_ascii=False))
if __name__=='__main__':main()
