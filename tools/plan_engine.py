#!/usr/bin/env python3
"""Deterministic, side-effect-free task planning; never executes user tasks."""
import argparse, hashlib, json, math, re
from pathlib import Path
KINDS={'research','design','implementation','verification','review','delivery'}
RISKS={'low','medium','high'}
class PlanError(ValueError): pass
def compile_plan(data):
    if not isinstance(data,dict) or set(data)!={'version','goal','requested_minutes','max_workers','tasks'} or data['version']!='1':
        raise PlanError('invalid plan schema/version')
    if not isinstance(data['goal'],str) or not 12<=len(data['goal'].strip())<=800:raise PlanError('invalid goal')
    minutes=data['requested_minutes'];workers=data['max_workers']
    if type(minutes) not in (int,float) or not math.isfinite(minutes) or not 0<minutes<=1440:raise PlanError('invalid time budget')
    if type(workers) is not int or not 1<=workers<=4:raise PlanError('workers must be 1..4')
    tasks=data['tasks']
    if not isinstance(tasks,list) or not 1<=len(tasks)<=80:raise PlanError('invalid tasks')
    required={'id','title','kind','depends_on','estimated_minutes','impact','risk','approval_required','acceptance'}
    items={}
    for task in tasks:
        if not isinstance(task,dict) or set(task)!=required:raise PlanError('invalid task fields')
        ident=task['id']
        if not isinstance(ident,str) or not re.fullmatch(r'[a-z][a-z0-9_-]{0,47}',ident):raise PlanError('invalid task id')
        if ident in items:raise PlanError('duplicate task id')
        if not isinstance(task['title'],str) or not 6<=len(task['title'].strip())<=180:raise PlanError('invalid title')
        if not isinstance(task['kind'],str) or task['kind'] not in KINDS:raise PlanError('invalid kind')
        if not isinstance(task['risk'],str) or task['risk'] not in RISKS:raise PlanError('invalid risk')
        if type(task['approval_required']) is not bool:raise PlanError('invalid approval flag')
        if (task['risk']=='high' or task['kind']=='delivery') and not task['approval_required']:raise PlanError('explicit approval gate required')
        n=task['estimated_minutes']
        if type(n) not in (int,float) or not math.isfinite(n) or not 0<n<=1440:raise PlanError('invalid estimate')
        if type(task['impact']) is not int or not 1<=task['impact']<=5:raise PlanError('invalid impact')
        deps=task['depends_on']
        if not isinstance(deps,list) or any(not isinstance(x,str) for x in deps) or len(deps)!=len(set(deps)):raise PlanError('invalid dependencies')
        acceptance=task['acceptance']
        if not isinstance(acceptance,list) or not 1<=len(acceptance)<=8 or any(not isinstance(x,str) or not 12<=len(x.strip())<=260 for x in acceptance):raise PlanError('invalid acceptance criteria')
        items[ident]=task
    for ident,t in items.items():
        for dep in t['depends_on']:
            if dep not in items:raise PlanError('unknown dependency')
            if dep==ident:raise PlanError('self dependency')
    complete=set();remaining=set(items);waves=[];end={}
    while remaining:
        ready=[items[i] for i in sorted(remaining) if set(items[i]['depends_on'])<=complete]
        if not ready:raise PlanError('dependency cycle')
        ready.sort(key=lambda t:(-t['impact'],t['estimated_minutes'],t['id']))
        picked=[t['id'] for t in ready[:workers]]
        for i in picked:
            t=items[i];end[i]=float(t['estimated_minutes'])+max([end[d] for d in t['depends_on']],default=0)
        waves.append(picked);complete.update(picked);remaining.difference_update(picked)
    encoded=json.dumps(data,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False)
    total=sum(float(t['estimated_minutes']) for t in tasks)
    return {'plan_sha256':hashlib.sha256(encoded.encode()).hexdigest(),'status':'ADVISORY_ONLY_NOT_EXECUTED',
       'goal':data['goal'],'task_count':len(tasks),'worker_limit':workers,'parallel_waves':waves,
       'estimated_work_minutes_sum':round(total,3),'estimated_critical_path_minutes':round(max(end.values()),3),
       'requested_minutes':minutes,'approval_gates':sorted(t['id'] for t in tasks if t['approval_required']),
       'work_estimate_exceeds_budget':total>minutes*workers,
       'note':'Planning and estimates only. No model, worker or task execution is implied.'}
def main():
    a=argparse.ArgumentParser(description=__doc__);a.add_argument('plan',type=Path);a.add_argument('--output',type=Path);x=a.parse_args()
    try:res=compile_plan(json.loads(x.plan.read_text(encoding='utf-8')))
    except (OSError,ValueError) as exc:a.error(str(exc))
    output=json.dumps(res,indent=2,ensure_ascii=False)+'\n'
    if x.output:x.output.write_text(output,encoding='utf-8')
    print(output,end='')
if __name__=='__main__':main()
