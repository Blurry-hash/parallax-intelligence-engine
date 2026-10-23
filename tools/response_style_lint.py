#!/usr/bin/env python3
"""Check unrequested bracketed status labels in a sample assistant answer."""
import argparse,json,re
from pathlib import Path
PAT=re.compile(r'\[(?:ESTABLISHED|APPROVED|PROBABLE|VERIFIED|SPECULATIVE|UNKNOWN|TESTED|BLOCKED)\]',re.I)
def check(text,structured_requested=False):
    hits=PAT.findall(text)
    return {'passes':bool(structured_requested) or not hits,'mechanical_tags':hits,'explicit_format_override':bool(structured_requested)}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('file',type=Path);p.add_argument('--structured-requested',action='store_true');a=p.parse_args()
    answer=check(a.file.read_text(encoding='utf-8'),a.structured_requested);print(json.dumps(answer))
    if not answer['passes']:raise SystemExit(1)
