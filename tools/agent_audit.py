#!/usr/bin/env python3
"""Four concurrent read-only deterministic specialist workers, NOT LLM agents."""
import argparse,concurrent.futures,json,time
from pathlib import Path
from plan_engine import compile_plan
ROOT=Path(__file__).resolve().parents[1]
def structure(root,plan):
    from validate import validate
    e,src,skills=validate(root)
    return {'pass':not e,'findings':e[:20],'metrics':{'sources':src,'skills':skills}}
def planning(root,plan):
    s=compile_plan(plan);a=[]
    if s['work_estimate_exceeds_budget']:a.append('Insufficient aggregate worker budget')
    if s['estimated_critical_path_minutes']>s['requested_minutes']:a.append('Critical path exceeds budget')
    return {'pass':not a,'findings':a,'metrics':{'waves':len(s['parallel_waves']),'critical_minutes':s['estimated_critical_path_minutes']}}
def sources(root,plan):
    rows=json.loads((root/'sources/sources.json').read_text(encoding='utf-8'))['sources']
    errors=[r.get('name','?') for r in rows if r.get('trust')=='unverified' and not r.get('notes')]
    return {'pass':not errors,'findings':errors,'metrics':{'unconfirmed_sources':sum(r.get('status')=='unconfirmed' for r in rows)}}
def permissions(root,plan):
    errors=[t['id'] for t in plan['tasks'] if (t['risk']=='high' or t['kind']=='delivery') and not t['approval_required']]
    return {'pass':not errors,'findings':errors,'metrics':{'approval_gates':sum(t['approval_required'] for t in plan['tasks'])}}
WORKERS={'structure':structure,'planning':planning,'source_provenance':sources,'permissions':permissions}
def run_audits(plan,root=ROOT):
    check=compile_plan(plan);start=time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        fut={name:pool.submit(fn,root,plan) for name,fn in WORKERS.items()}
        results={}
        for name in sorted(fut):
            try:results[name]=fut[name].result()
            except Exception as e:results[name]={'pass':False,'findings':[type(e).__name__+': '+str(e)[:250]],'metrics':{}}
    return {'execution':'Four independent concurrent read-only Python workers; no external LLM called',
      'plan_sha256':check['plan_sha256'],'worker_count':len(WORKERS),
      'elapsed_seconds':round(time.perf_counter()-start,6),
      'pass':all(x['pass'] for x in results.values()),'workers':results}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('plan',type=Path);ap.add_argument('--root',type=Path,default=ROOT);ap.add_argument('--out',type=Path)
    x=ap.parse_args()
    try:result=run_audits(json.loads(x.plan.read_text(encoding='utf-8')),x.root)
    except (ValueError,OSError) as e:ap.error(str(e))
    output=json.dumps(result,indent=2)+'\n'
    if x.out:x.out.write_text(output,encoding='utf-8')
    print(output,end='')
    if not result['pass']:raise SystemExit(1)
if __name__=='__main__':main()
