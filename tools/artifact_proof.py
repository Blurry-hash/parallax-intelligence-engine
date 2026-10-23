#!/usr/bin/env python3
"""Content-addressed, symlink-safe evidence for LOCAL files, not an authenticity signature.

Creates and verifies a compact SHA256 manifest. No network or shell execution.
"""
from __future__ import annotations
import argparse, hashlib, json, re
from pathlib import Path, PurePosixPath
MAX_FILES=256
MAX_BYTES=100*1024*1024
SHA_RE=re.compile(r'^[a-f0-9]{64}$')


def _checked(root:Path, rel:str)->Path:
    if not isinstance(rel,str) or not rel or '\\' in rel or rel.startswith('/') or ':' in rel:
        raise ValueError('unsafe artifact path')
    posix=PurePosixPath(rel)
    if posix.is_absolute() or any(p in ('','.','..') for p in posix.parts) or str(posix)!=rel:
        raise ValueError('unsafe artifact path')
    candidate=root
    for part in posix.parts:
        candidate=candidate/part
        if candidate.is_symlink():raise ValueError('symlink artifact path')
    if not candidate.is_file() or not candidate.resolve().is_relative_to(root.resolve()):raise ValueError('artifact not found inside root')
    if candidate.stat().st_size>MAX_BYTES:raise ValueError('artifact exceeds size limit')
    return candidate


def manifest(root:Path, names:list[str])->dict:
    if not isinstance(names,list) or not 1<=len(names)<=MAX_FILES or len(names)!=len(set(names)):
        raise ValueError('missing, duplicate, or excessive artifact names')
    root=root.resolve(); files={}
    for name in sorted(names):
        file=_checked(root,name)
        files[name]={'sha256':hashlib.sha256(file.read_bytes()).hexdigest(),'bytes':file.stat().st_size}
    return {'schema':1,'algorithm':'sha256','artifacts':files,
            'claim':'content integrity only; no identity, provenance or authenticity guarantee'}


def verify(root:Path, data:dict)->dict:
    if not isinstance(data,dict) or set(data)!={'schema','algorithm','artifacts','claim'} or data['schema']!=1 or data['algorithm']!='sha256':
        raise ValueError('invalid manifest contract')
    entries=data['artifacts']
    if not isinstance(entries,dict) or not 1<=len(entries)<=MAX_FILES:raise ValueError('invalid artifact mapping')
    for name,item in entries.items():
        if not isinstance(item,dict) or set(item)!={'sha256','bytes'} or not isinstance(item['sha256'],str) or not SHA_RE.fullmatch(item['sha256']) or type(item['bytes']) is not int or item['bytes']<0:
            raise ValueError('invalid artifact digest metadata')
        f=_checked(root.resolve(),name)
        if f.stat().st_size!=item['bytes'] or hashlib.sha256(f.read_bytes()).hexdigest()!=item['sha256']:
            raise ValueError('artifact content mismatch: '+name)
    return {'verified_files':len(entries),'result':'MATCHED_MANIFEST_NOT_AUTHENTICATED'}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('root',type=Path);p.add_argument('files',nargs='*')
    p.add_argument('--verify',type=Path)
    a=p.parse_args()
    if a.verify:
        if a.files:p.error('file arguments incompatible with --verify')
        print(json.dumps(verify(a.root,json.loads(a.verify.read_text(encoding='utf8'))),indent=2))
    else:
        print(json.dumps(manifest(a.root,a.files),indent=2))
if __name__=='__main__':main()
