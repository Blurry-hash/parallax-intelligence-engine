#!/usr/bin/env python3
"""Rank only actually registered, authorized provider options; never call a model.

Model names/specs are user-provided inventory, NOT provider capabilities verified here.
"""
from __future__ import annotations
import argparse,json,math
from pathlib import Path

class ModelGateError(ValueError):pass

def choose(registry:dict,request:dict)->dict:
    if not isinstance(registry,dict) or not isinstance(registry.get('models'),list) or not isinstance(request,dict):raise ModelGateError('invalid input')
    needs=request.get('requires',[])
    if not isinstance(needs,list) or not all(isinstance(a,str) for a in needs):raise ModelGateError('invalid requirements')
    max_cost=request.get('max_cost',float('inf'))
    if isinstance(max_cost,bool) or not isinstance(max_cost,(int,float)) or math.isnan(max_cost) or max_cost<0:raise ModelGateError('invalid budget')
    eligible=[];rejected=[];seen=set()
    for m in registry['models']:
        if not isinstance(m,dict):raise ModelGateError('model must be object')
        ident=m.get('id');caps=m.get('capabilities',[]);price=m.get('estimated_cost');latency=m.get('estimated_latency_ms')
        if not isinstance(ident,str) or not ident or ident in seen:raise ModelGateError('duplicate model id')
        seen.add(ident)
        if not isinstance(caps,list) or any(not isinstance(c,str) for c in caps):raise ModelGateError('invalid capabilities')
        if (any(isinstance(v,bool) or not isinstance(v,(int,float)) or not math.isfinite(v) or v<0 for v in (price,latency))):raise ModelGateError('invalid metrics')
        reason=[]
        if not m.get('connected',False):reason.append('not connected')
        if not m.get('authorized',False):reason.append('not authorized')
        if not set(needs)<=set(caps):reason.append('missing capability')
        if price>max_cost:reason.append('over budget')
        if reason:rejected.append({'id':ident,'reasons':reason})
        else:eligible.append({'id':ident,'estimated_cost':price,'estimated_latency_ms':latency})
    # Pareto-friendly default: lowest estimated cost first, latency ties; no claims about intelligence.
    eligible.sort(key=lambda x:(x['estimated_cost'],x['estimated_latency_ms'],x['id']))
    return {'selected':eligible[0]['id'] if eligible else None,'eligible':eligible,
            'rejected':rejected,'provider_calls':0,'note':'estimates supplied by registry; quality not inferred'}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('registry',type=Path);p.add_argument('request',type=Path);a=p.parse_args()
    try: print(json.dumps(choose(json.loads(a.registry.read_text(encoding='utf-8')),json.loads(a.request.read_text(encoding='utf-8'))),indent=2))
    except (ValueError,OSError) as e:p.error(str(e))
if __name__=='__main__':main()
