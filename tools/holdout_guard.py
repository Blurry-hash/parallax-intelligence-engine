#!/usr/bin/env python3
"""Prevent exact duplicate evaluation IDs/content across development and holdout JSONL.

This is a deterministic leakage check, NOT semantic contamination detection.
"""
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path

def inspect(dev:list,holdout:list)->dict:
    seen_ids=set();seen_hashes=set()
    def normalize(rows,scope):
        hashes=set();ids=set()
        for row in rows:
            if not isinstance(row,dict) or not isinstance(row.get('id'),str) or not isinstance(row.get('input'),str):
                raise ValueError('rows require id and input strings')
            rid=row['id'];h=hashlib.sha256(' '.join(row['input'].casefold().split()).encode()).hexdigest()
            if rid in ids or h in hashes:raise ValueError('duplicates within '+scope)
            ids.add(rid);hashes.add(h)
        return ids,hashes
    a,ah=normalize(dev,'development');b,bh=normalize(holdout,'holdout')
    return {'development':len(dev),'holdout':len(holdout),'overlap_ids':sorted(a&b),
            'overlap_content_count':len(ah&bh),'status':'overlap_detected' if a&b or ah&bh else 'no_exact_overlap'}
def read(path:Path)->list:
    return [json.loads(s) for s in path.read_text(encoding='utf8').splitlines() if s.strip()]
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('development',type=Path);p.add_argument('holdout',type=Path);a=p.parse_args()
    try:r=inspect(read(a.development),read(a.holdout));print(json.dumps(r,indent=2));raise SystemExit(1 if r['status']!='no_exact_overlap' else 0)
    except (OSError,ValueError) as e:p.error(str(e))
if __name__=='__main__':main()
