#!/usr/bin/env python3
"""Offline claim-evidence ledger validator. Does not itself verify sources."""
from __future__ import annotations
import argparse,json
from pathlib import Path

class EvidenceError(ValueError):pass

def inspect(data:dict)->dict:
    if not isinstance(data,dict) or not isinstance(data.get('claims'),list) or not isinstance(data.get('sources'),list):
        raise EvidenceError('claims and sources required')
    source_ids=set();claim_ids=set();unsupported=[]; contested=[]
    for source in data['sources']:
        if not isinstance(source,dict):raise EvidenceError('source must be object')
        sid=source.get('id')
        if not isinstance(sid,str) or not sid or sid in source_ids:raise EvidenceError('duplicate/invalid source id')
        if source.get('status') not in ('checked','unconfirmed'):
            raise EvidenceError('source must have checked/unconfirmed status')
        if not isinstance(source.get('url'),str) or not source['url'].startswith('https://'):
            raise EvidenceError('source URL must be HTTPS')
        source_ids.add(sid)
    for claim in data['claims']:
        if not isinstance(claim,dict):raise EvidenceError('claim must be object')
        cid=claim.get('id')
        if not isinstance(cid,str) or not cid or cid in claim_ids:raise EvidenceError('duplicate/invalid claim id')
        claim_ids.add(cid)
        refs=claim.get('supports',[]);opposes=claim.get('opposes',[])
        if any(not isinstance(a,list) for a in (refs,opposes)) or any(s not in source_ids for s in refs+opposes):
            raise EvidenceError('claim references unknown source')
        if set(refs)&set(opposes):raise EvidenceError('same source supports and opposes same claim')
        if not isinstance(claim.get('statement'),str) or not claim['statement'].strip():raise EvidenceError('statement required')
        if not refs:unsupported.append(cid)
        if opposes:contested.append(cid)
    return {'claims':len(claim_ids),'sources':len(source_ids),'unsupported':unsupported,
            'contested':contested,'status':'ledger_checked_not_facts_verified'}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('ledger',type=Path);a=p.parse_args()
    try: print(json.dumps(inspect(json.loads(a.ledger.read_text(encoding='utf8'))),indent=2))
    except (OSError,ValueError) as e:p.error(str(e))
if __name__=='__main__':main()
