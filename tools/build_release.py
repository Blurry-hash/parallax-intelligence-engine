#!/usr/bin/env python3
"""Create and verify a deterministic, integrity-indexed local release archive.

Pure local I/O: no GitHub mutation, provider calls, secret transfers or downloads.
A SHA256 manifest detects accidental corruption, NOT malicious tampering by a
party that can replace both the archive and its manifest.
"""
from __future__ import annotations
import argparse, hashlib, json, stat, zipfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
EXCLUDE_DIRS={'.git','.venv','node_modules','__pycache__','.pytest_cache','.mypy_cache'}
EXCLUDE_FILES={'.DS_Store','RELEASE_MANIFEST.json'}
FIXED_DATE=(2026,10,23,0,0,0)

def pack(root:Path,destination:Path)->dict:
    root=root.resolve(); destination=destination.resolve()
    if destination.is_relative_to(root):
        raise ValueError('Destination must be outside the source repository')
    files=[]
    for p in root.rglob('*'):
        rel=p.relative_to(root)
        if set(rel.parts)&EXCLUDE_DIRS or p.name in EXCLUDE_FILES or p.suffix=='.pyc':continue
        if p.is_symlink():raise ValueError('Symlink in release source: '+str(rel))
        if p.is_file():files.append(p)
    files=sorted(files,key=lambda p:p.relative_to(root).as_posix())
    if not files or not (root/'README.md') in files or not (root/'MASTER_PROMPT.md') in files:
        raise ValueError('Incomplete repository: README and MASTER_PROMPT required')
    checksums={p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    manifest={'release':'PARALLAX v10.1','file_count':len(files),'sha256':checksums,'hash_scope':'archive members excluding manifest; no authenticity signature'}
    manifest_bytes=(json.dumps(manifest,indent=2,sort_keys=True)+'\n').encode()
    destination.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(destination,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in files:
            rel=p.relative_to(root).as_posix()
            info=zipfile.ZipInfo('parallax-intelligence-engine/'+rel,FIXED_DATE)
            info.compress_type=zipfile.ZIP_DEFLATED
            info.external_attr=(stat.S_IFREG|0o644)<<16
            z.writestr(info,p.read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
        info=zipfile.ZipInfo('parallax-intelligence-engine/RELEASE_MANIFEST.json',FIXED_DATE)
        info.compress_type=zipfile.ZIP_DEFLATED
        z.writestr(info,manifest_bytes,compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
    return manifest

def verify(archive:Path)->dict:
    with zipfile.ZipFile(archive) as z:
        if z.testzip() is not None:raise ValueError('CRC invalid')
        names=z.namelist()
        if len(names)!=len(set(names)):raise ValueError('duplicate archive members')
        prefix='parallax-intelligence-engine/'
        for name in names:
            p=PurePosixPath(name)
            if not name.startswith(prefix) or '..' in p.parts or p.is_absolute() or '\\' in name:
                raise ValueError('Unsafe ZIP entry: '+name)
        manifest=json.loads(z.read(prefix+'RELEASE_MANIFEST.json'))
        expected=manifest['sha256']
        if set(names)!={prefix+p for p in expected}|{prefix+'RELEASE_MANIFEST.json'}:
            raise ValueError('Archive contents differ from checksum manifest')
        for rel,h in expected.items():
            if hashlib.sha256(z.read(prefix+rel)).hexdigest()!=h:
                raise ValueError('SHA256 mismatch: '+rel)
        if len(expected)!=manifest['file_count']:raise ValueError('Manifest count mismatch')
        return {'result':'verified_against_embedded_manifest','files':len(expected),'sha256_zip':hashlib.sha256(archive.read_bytes()).hexdigest()}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    manifest=pack(ROOT,args.out)
    print(json.dumps(verify(args.out),indent=2))
