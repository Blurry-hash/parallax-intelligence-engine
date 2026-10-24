#!/usr/bin/env python3
"""Inventory tracked files; inventory alone never proves model reading."""
import hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def manifest(root=ROOT):
 root=Path(root).resolve();paths=subprocess.check_output(['git','ls-files','-z'],cwd=root).decode('utf-8').split('\0');rows=[]
 for rel in sorted(x for x in paths if x):
  p=root/rel
  if p.is_symlink():raise ValueError('symlink: '+rel)
  data=p.read_bytes()
  try:text=data.decode('utf-8');readable='\x00' not in text
  except UnicodeDecodeError:readable=False;text=''
  rows.append({'path':rel,'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data),'lines':len(text.splitlines()) if readable else None,'type':'text' if readable else 'binary','read_by_model':False})
 return {'revision':subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),'files':rows,'rule':'Update read receipts only after complete content was presented without truncation. Inspect binaries separately; reading source is not executing it.'}
if __name__=='__main__':print(json.dumps(manifest(),ensure_ascii=False,indent=2))
