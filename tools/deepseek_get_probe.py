#!/usr/bin/env python3
"""Create (or explicitly probe) a safe math.js GET expression URL. NOT arbitrary code."""
from __future__ import annotations
import argparse, json, re, urllib.parse, urllib.request

SAFE=re.compile(r'^[0-9+*() /.-]{1,96}$')

def url_for(expr:str)->str:
    if not isinstance(expr,str) or not SAFE.fullmatch(expr):
        raise ValueError('Only small arithmetic expressions; no Python/JS, identifiers, URLs or secrets')
    if '**' in expr or '//' in expr: raise ValueError('Avoid operator ambiguity')
    return 'https://api.mathjs.org/v4/?'+urllib.parse.urlencode({'expr':expr})

def probe(expr: str, *, fetcher=None) -> dict:
    url=url_for(expr)
    if fetcher is None:
        def fetcher(url):
            req=urllib.request.Request(url,headers={'User-Agent':'PARALLAX-mathjs-probe/1.0'})
            with urllib.request.urlopen(req,timeout=9) as res:return res.read(256).decode('utf-8')
    try:
        result=fetcher(url).strip()
        return {'status':'executed_get','url':url,'response':result,'warning':'Math expression only; not a Python or JavaScript sandbox'}
    except Exception as exc:
        return {'status':'blocked','url':url,'error':str(exc),'warning':'No test result was obtained'}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('expression');p.add_argument('--execute',action='store_true');a=p.parse_args();print(json.dumps(probe(a.expression) if a.execute else {'status':'url_only','url':url_for(a.expression)},indent=2))
