#!/usr/bin/env python3
"""Offline evaluation receipts for externally run, paired skill A/B experiments.

No judge/model calls. Checks task matching, ablation identity and measurement
provenance; statistical tests cannot authenticate self-reported observations.
"""
import argparse,json,math,sys,statistics
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from paired_stats import paired_summary

def assess(data):
 if not isinstance(data,dict) or data.get('provenance') not in ('observed','fixture'):raise ValueError('observed/fixture provenance required')
 if not isinstance(data.get('skill'),str) or not data['skill']:raise ValueError('skill required')
 runs=data.get('pairs')
 if not isinstance(runs,list) or not runs:raise ValueError('paired runs required')
 limits=data.get('limits',{'max_token_ratio':1.,'max_latency_ratio':1.})
 if not isinstance(limits,dict):raise ValueError('limits object required')
 for key in ('max_token_ratio','max_latency_ratio'):
  if type(limits.get(key)) not in (int,float) or not math.isfinite(limits[key]) or limits[key]<=0:raise ValueError('positive finite '+key+' required')
 ids=set();b=[];c=[];tb=[];tc=[];lb=[];lc=[];critical=[]
 for row in runs:
  if not isinstance(row,dict):raise ValueError('pair must be object')
  ident=row.get('task_id')
  if not isinstance(ident,str) or not ident or ident in ids:raise ValueError('distinct task IDs required')
  ids.add(ident)
  if row.get('split')!='holdout':raise ValueError('final report requires holdout pairs')
  for key in ('model','settings_hash','tools_hash','input_hash','judge_version'):
   if not isinstance(row.get(key),str) or not row[key]:raise ValueError(key+' required for matching')
  if row.get('baseline_skills')!=[] or row.get('candidate_skills')!=[data['skill']]:raise ValueError('single-skill ablation must change only selected skill')
  for key in ('baseline','candidate'):
   v=row.get(key)
   if not isinstance(v,dict):raise ValueError(key+' measurement required')
   for field in ('score','tokens','latency_ms'):
    x=v.get(field)
    if type(x) not in (int,float) or not math.isfinite(x) or x<0:raise ValueError('finite nonnegative '+field+' required')
   if not 0<=v['score']<=1:raise ValueError('scores must be 0..1')
   if type(v.get('critical_failure')) is not bool:raise ValueError('critical_failure boolean required')
  b.append(row['baseline']['score']);c.append(row['candidate']['score']);tb.append(row['baseline']['tokens']);tc.append(row['candidate']['tokens'])
  lb.append(row['baseline']['latency_ms']);lc.append(row['candidate']['latency_ms'])
  if row['candidate']['critical_failure']:critical.append(ident)
 stats=paired_summary(b,c)
 budget_ok=sum(tc)<=limits['max_token_ratio']*sum(tb) and sum(lc)<=limits['max_latency_ratio']*sum(lb)
 return {'skill':data['skill'],'quality':stats,'token_delta':paired_summary(tb,tc,higher_is_better=False),'latency_delta':paired_summary(lb,lc,higher_is_better=False),'budgets_pass':budget_ok,'declared_limits':limits,'critical_failures':critical,'eligible_for_review':budget_ok and data['provenance']=='observed' and stats['improvement_supported'] and not critical,'auto_promoted':False,'warning':'Supplied observations require independent provenance review; no model was run by this tool. Correct multiple-comparison testing before many-skill promotion.'}
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('file',type=Path);a=p.parse_args()
 try:print(json.dumps(assess(json.loads(a.file.read_text(encoding='utf-8'))),indent=2))
 except (ValueError,TypeError,KeyError) as e:p.exit(2,str(e)+'\n')
