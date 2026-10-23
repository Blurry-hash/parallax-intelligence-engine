#!/usr/bin/env python3
"""Regenerate small read-only JSON index pages for GET-only AI clients."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://raw.githubusercontent.com/Blurry-hash/parallax-intelligence-engine/main/bridge/v1/'


def canonical(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')) + '\n').encode('utf-8')


def generate(root=ROOT):
    root=Path(root)
    skill_names=sorted(p.parent.name for p in (root/'skills').glob('*/SKILL.md'))
    sources=json.loads((root/'sources/sources.json').read_text(encoding='utf-8'))['sources']
    compact=[{key:x[key] for key in ('name','url','topic','trust','status')} for x in sources]
    files={};pages={}
    for kind,records,per in [('skills',skill_names,12),('sources',compact,8)]:
        pages[kind]=[]
        for offset in range(0,len(records),per):
            number=offset//per+1;name=f'{kind}-{number:02d}.json'
            page={'kind':kind,'page':number,'total_pages':(len(records)+per-1)//per,
                  'offset':offset,'count':len(records[offset:offset+per]),'entries':records[offset:offset+per]}
            files[name]=canonical(page);pages[kind].append(name)
    files['index.json']=canonical({
        'format':'parallax-get-catalog-v1','repository':'Blurry-hash/parallax-intelligence-engine',
        'read_base':BASE,'counts':{'skills':len(skill_names),'sources':len(sources)},'pages':pages,
        'read_rule':'Fetch index, then EVERY numbered page for the count you need. If pages are missing, report partial, not absent.',
        'execution_rule':'GET reads repository data and CI results; it cannot execute arbitrary code or start authenticated workflows.',
        'latest_commit_url':'https://api.github.com/repos/Blurry-hash/parallax-intelligence-engine/commits/main',
        'actions_url':'https://api.github.com/repos/Blurry-hash/parallax-intelligence-engine/actions/runs?per_page=3'
    })
    return files


def run(root=ROOT, check=False):
    files=generate(root);directory=Path(root)/'bridge/v1'
    mismatches=[name for name,data in files.items() if not (directory/name).exists() or (directory/name).read_bytes()!=data]
    if check:
        if mismatches:raise ValueError('Outdated GET catalog: '+', '.join(mismatches))
    else:
        directory.mkdir(parents=True,exist_ok=True)
        for name,data in files.items():(directory/name).write_bytes(data)
    print(f"{'PASS' if check else 'GENERATED'}: {len(files)} pages; skills and sources fully indexed")
    return files


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');args=p.parse_args()
    run(check=args.check)
