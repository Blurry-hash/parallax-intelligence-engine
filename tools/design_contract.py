#!/usr/bin/env python3
"""Small offline design token contract and WCAG contrast check; not visual screenshot QA."""
from __future__ import annotations
import argparse, json, math, re
from pathlib import Path
HEX=re.compile(r'^#[0-9a-fA-F]{6}$')

def luminance(color:str)->float:
    if not isinstance(color,str) or not HEX.fullmatch(color): raise ValueError('Expected six-digit hex color')
    channels=[int(color[i:i+2],16)/255 for i in (1,3,5)]
    linear=[v/12.92 if v<=0.04045 else ((v+0.055)/1.055)**2.4 for v in channels]
    return sum(w*v for w,v in zip((0.2126,0.7152,0.0722),linear))

def check_contract(c:dict)->list[str]:
    errors=[]
    if not isinstance(c,dict):return ['Contract must be object']
    colors=c.get('colors')
    if not isinstance(colors,dict) or not colors:return ['Missing semantic colors']
    for k,v in colors.items():
        try:luminance(v)
        except ValueError:errors.append(f'Invalid color {k}')
    pairings=c.get('contrast_pairs')
    if not isinstance(pairings,list) or not pairings:errors.append('Missing contrast pairs');return errors
    for i,pair in enumerate(pairings):
        if not isinstance(pair,dict):errors.append(f'Invalid contrast pair {i}');continue
        a,b=pair.get('foreground'),pair.get('background')
        if a not in colors or b not in colors:errors.append(f'Unknown color in pair {i}');continue
        try:
            high,low=sorted((luminance(colors[a]),luminance(colors[b])),reverse=True)
            ratio=(high+0.05)/(low+0.05)
            limit=3 if pair.get('large_text',False) else 4.5
            if ratio+1e-9 < limit:errors.append(f'Low contrast pair {i}: {ratio:.2f} < {limit}')
        except ValueError:errors.append(f'Invalid colors in pair {i}')
    return errors

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('contract',type=Path);a=p.parse_args();errors=check_contract(json.loads(a.contract.read_text(encoding='utf-8')));print(json.dumps({'ok':not errors,'errors':errors},indent=2));raise SystemExit(1 if errors else 0)
