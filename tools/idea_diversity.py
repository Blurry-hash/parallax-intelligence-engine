#!/usr/bin/env python3
"""Dependency-free surface-level idea diversity diagnostic, NOT a true novelty metric."""
import argparse
import itertools
import json
import re
from pathlib import Path


def tokens(text):
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def jaccard(a, b):
    a, b = tokens(a), tokens(b)
    return (len(a & b) / len(a | b)) if a | b else 1.0


def assess(ideas):
    if not isinstance(ideas,list) or len(ideas)<2 or any(not isinstance(s,str) or not s.strip() for s in ideas):
        raise ValueError("Provide at least two nonempty string ideas")
    pairs = [{"indices": [i, j], "overlap": round(jaccard(a,b),4)} for (i,a),(j,b) in itertools.combinations(enumerate(ideas),2)]
    return {"idea_count": len(ideas), "pair_count": len(pairs), "lexical_diversity": round(1 - sum(p['overlap'] for p in pairs)/len(pairs),4), "high_overlap_pairs": [p for p in pairs if p['overlap']>=0.65], "warning": "Lexical overlap is not conceptual novelty: assess mechanisms and compare with prior art separately."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('file',type=Path)
    args=parser.parse_args()
    raw=json.loads(args.file.read_text(encoding='utf-8'))
    data = raw.get('ideas') if isinstance(raw,dict) else raw
    print(json.dumps(assess(data),indent=2,ensure_ascii=False))

if __name__=='__main__': main()
