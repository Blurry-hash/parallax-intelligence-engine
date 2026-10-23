#!/usr/bin/env python3
"""Search PARALLAX capability contracts; no external AI/models/network needed."""
import argparse,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def search(query,limit=8):
    if not isinstance(query,str) or not query.strip() or not 1<=limit<=50:raise ValueError('Invalid query or limit')
    rows=json.loads((ROOT/'catalog/150-capability-contracts.json').read_text(encoding='utf-8'))['capabilities']
    terms=set(query.lower().replace('-',' ').split())
    ranked=[]
    for row in rows:
        name=row['name'].lower();text=(name+' '+row['domain'].lower()+' '+row['procedure'].lower())
        score=sum(3 if t in name else 1 if t in text else 0 for t in terms)
        if score:ranked.append((score,row['id'],row))
    return [r for _,__,r in sorted(ranked,key=lambda x:(-x[0],x[1]))[:limit]]
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('query');p.add_argument('--limit',type=int,default=8);a=p.parse_args()
    print(json.dumps(search(a.query,a.limit),indent=2))
