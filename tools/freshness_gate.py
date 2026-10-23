#!/usr/bin/env python3
"""Opt-in GitHub revision check with TTL state; never schedules background work."""
from __future__ import annotations
import argparse, datetime as dt, json, re, urllib.request
from pathlib import Path

PAT = re.compile(r'^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$')

def inspect(repo: str, state: Path, *, force: bool = False, ttl_hours: float = 24,
            now: dt.datetime | None = None, fetcher=None) -> dict:
    if not PAT.fullmatch(repo) or any(p in ('.', '..') for p in repo.split('/')) or ttl_hours < 0:
        raise ValueError('Invalid repository or TTL')
    now = now or dt.datetime.now(dt.timezone.utc)
    previous = json.loads(state.read_text()) if state.exists() else {}
    if previous and not force and previous.get('repository') == repo:
        try:
            checked = dt.datetime.fromisoformat(previous['checked_at'])
            age=(now-checked).total_seconds()
            if 0 <= age < ttl_hours * 3600:
                return {'status':'cached','sha':previous['sha'],'checked_at':previous['checked_at'],'repository':repo}
        except (ValueError, KeyError, TypeError): pass
    url=f'https://api.github.com/repos/{repo}/commits/main'
    if fetcher is None:
        def fetcher(url):
            req=urllib.request.Request(url,headers={'Accept':'application/vnd.github+json','User-Agent':'parallax-readonly-freshness/1.0'})
            with urllib.request.urlopen(req,timeout=12) as response:
                return json.load(response)
    try:
        result=fetcher(url)
        sha=result['sha']
        if not isinstance(sha,str) or not re.fullmatch(r'[0-9a-f]{40}',sha): raise ValueError('Invalid commit sha')
    except Exception as exc:
        return {'status':'unverified','repository':repo,'error':str(exc),'last_known_sha':previous.get('sha')}
    changed=previous.get('sha') != sha
    payload={'repository':repo,'sha':sha,'checked_at':now.isoformat()}
    state.parent.mkdir(parents=True,exist_ok=True)
    state.write_text(json.dumps(payload,indent=2)+'\n')
    return {'status':'changed' if changed else 'unchanged',**payload}

if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--repo',default='Blurry-hash/parallax-intelligence-engine'); p.add_argument('--state',type=Path,default=Path('.parallax-freshness-state.json'));p.add_argument('--force',action='store_true');p.add_argument('--ttl-hours',type=float,default=24)
    a=p.parse_args();print(json.dumps(inspect(a.repo,a.state,force=a.force,ttl_hours=a.ttl_hours),indent=2))
