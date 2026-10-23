#!/usr/bin/env python3
"""Offline provenance audit. Unconfirmed sources do not become verified by inclusion.

Counts source attestations, flags insufficient caveats; does not fetch URLs.
"""
from __future__ import annotations
import collections,json,argparse
from pathlib import Path

def summary(registry:dict)->dict:
    entries=registry['sources']
    status=collections.Counter(x.get('status','missing') for x in entries)
    trust=collections.Counter(x.get('trust','missing') for x in entries)
    unchecked=[x['url'] for x in entries if x.get('status')!='verified-page']
    missing_notes=[x['url'] for x in entries if (x.get('trust')=='unverified' or x.get('status')=='unconfirmed') and not x.get('notes','').strip()]
    return {'total':len(entries),'status':dict(status),'trust':dict(trust),
            'unchecked':len(unchecked),'missing_required_caveats':missing_notes,
            'warning':'Verified-page means URL was checked, not that code or model claims were reproduced.'}
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('index',nargs='?',default=str(Path(__file__).resolve().parents[1]/'sources'/'sources.json'))
    args=p.parse_args()
    s=summary(json.loads(Path(args.index).read_text(encoding='utf8')))
    print(json.dumps(s,indent=2))
    if s['missing_required_caveats']:raise SystemExit(1)
