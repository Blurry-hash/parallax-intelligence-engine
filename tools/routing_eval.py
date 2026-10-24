#!/usr/bin/env python3
"""Offline labeled retrieval evaluation; fixtures are not model-outcome evidence."""
from __future__ import annotations
import argparse,json
from pathlib import Path
from route_task import ROOT,candidates

def evaluate(rows,root=ROOT,k=3):
    if not isinstance(rows,list) or not rows or type(k) is not int or not 1<=k<=10:
        raise ValueError('nonempty labeled rows and k 1..10 required')
    results=[];seen=set()
    for row in rows:
        if not isinstance(row,dict) or not isinstance(row.get('query'),str) or not row['query'].strip() or not isinstance(row.get('relevant'),list) or not row['relevant']:
            raise ValueError('each row needs query and relevant skill names')
        if row['query'] in seen: raise ValueError('duplicate query')
        seen.add(row['query']);relevant=set(row['relevant'])
        if any(not isinstance(name,str) or '/' in name or not (root/'skills'/name/'SKILL.md').is_file() for name in relevant):
            raise ValueError('unknown relevant skill')
        ranked=[x['skill'] for x in candidates(row['query'],root=root,limit=k)]
        hits=len(set(ranked)&relevant)
        results.append({'query':row['query'],'ranked':ranked,'precision_at_k':hits/k,'recall_at_k':hits/len(relevant),'hit':bool(hits)})
    return {'k':k,'n_queries':len(results),'precision_at_k':sum(r['precision_at_k'] for r in results)/len(results),
            'recall_at_k':sum(r['recall_at_k'] for r in results)/len(results),
            'hit_rate_at_k':sum(r['hit'] for r in results)/len(results),'cases':results,
            'scope':'Curated local retrieval fixture; not a held-out model quality benchmark.'}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('fixture',type=Path);p.add_argument('--k',type=int,default=3);a=p.parse_args()
    print(json.dumps(evaluate(json.loads(a.fixture.read_text(encoding='utf-8')),k=a.k),indent=2))
