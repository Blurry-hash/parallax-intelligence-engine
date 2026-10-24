#!/usr/bin/env python3
"""Conservative precommit diagnostic for candidate secret material. Not a full secrets scanner."""
from __future__ import annotations
import argparse,json,re
from pathlib import Path

# Generic patterns deliberately report candidates, never echo sensitive values.
PATTERNS={
 'private_key_header': re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
 'github_classic_token':re.compile(r'\bghp_[A-Za-z0-9]{36}\b'),
 'github_fine_grained_token':re.compile(r'\bgithub_pat_[A-Za-z0-9_]{20,}\b'),
 'anthropic_token': re.compile(r'\bsk-ant-[A-Za-z0-9_-]{20,}\b'),
 'openai_project_token': re.compile(r'\bsk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{32,}\b'),
 'slack_token': re.compile(r'\bxox[baprs]-[A-Za-z0-9-]{20,}\b'),
 'stripe_secret': re.compile(r'\b(?:sk|rk)_(?:live|test)_[A-Za-z0-9]{16,}\b'),
 'aws_access_key':re.compile(r'\b(?:AKIA|ASIA)[A-Z0-9]{16}\b'),
}
EXCLUDE={'.git','node_modules','.venv','__pycache__'}
def inspect(root:Path)->dict:
    root=root.resolve()
    if not root.is_dir():raise ValueError('root must be directory')
    issues=[];checked=0
    for p in sorted(root.rglob('*')):
        if not p.is_file() or set(p.relative_to(root).parts)&EXCLUDE or p.is_symlink() or p.stat().st_size>2_000_000:continue
        if not p.name.startswith('.env') and p.suffix.lower() not in {'.py','.md','.txt','.json','.yaml','.yml','.toml','.env','.ps1','.js','.ts'}:continue
        checked+=1
        try:s=p.read_text(encoding='utf-8')
        except UnicodeError:continue
        for name,pat in PATTERNS.items():
            for match in pat.finditer(s):
                issues.append({'path':p.relative_to(root).as_posix(),'line':s.count('\n',0,match.start())+1,'pattern':name})
    return {'checked_files':checked,'issues':issues,'status':'candidate_secret_patterns_only',
            'secrets_printed':False}
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('directory',type=Path);args=ap.parse_args()
    r=inspect(args.directory);print(json.dumps(r,indent=2));raise SystemExit(1 if r['issues'] else 0)
if __name__=='__main__':main()
