#!/usr/bin/env python3
"""Validate image/edit task specifications, without rendering, network or model calls."""
import argparse, json
from pathlib import Path
class ContractError(ValueError): pass
MODES={'describe','generate','edit','composite','vector','code-ui','retrieve'}
ROLES={'edit-target','identity','pose','composition','style','lighting','material','negative','background'}
def validate(x):
    if not isinstance(x,dict) or x.get('mode') not in MODES: raise ContractError('Unsupported image task mode')
    if not isinstance(x.get('requested_output'),str) or not x['requested_output'].strip(): raise ContractError('Output required')
    render=x.get('render_required',False)
    if not isinstance(render,bool): raise ContractError('Render flag must be boolean')
    if render and x['mode'] in {'describe','retrieve','vector','code-ui'}: raise ContractError('A bitmap render cannot be mandatory for a nonbitmap task')
    refs=x.get('references',[])
    if not isinstance(refs,list) or len(refs)>24: raise ContractError('Invalid references')
    ids=set()
    for ref in refs:
        if not isinstance(ref,dict) or not isinstance(ref.get('id'),str) or not ref['id'] or ref['id'] in ids: raise ContractError('Bad reference ID')
        ids.add(ref['id'])
        roles=ref.get('roles',[])
        if not isinstance(roles,list) or not roles or any(role not in ROLES for role in roles): raise ContractError('Invalid reference role')
    locked=x.get('locked',[]); editable=x.get('editable',[])
    if not isinstance(locked,list) or not isinstance(editable,list) or any(not isinstance(v,str) or not v.strip() for v in locked+editable): raise ContractError('Invalid constraints')
    if {v.casefold().strip() for v in locked} & {v.casefold().strip() for v in editable}: raise ContractError('Locked/editable conflict')
    if x['mode']=='edit' and not any('edit-target' in r['roles'] for r in refs): raise ContractError('Edit requires an edit-target')
    if x.get('pixel_exact') and x['mode'] in {'generate','edit'}: raise ContractError('Generative operation cannot guarantee pixel-exact preservation')
    return {'mode':x['mode'],'render_required':render,'references':len(refs),'executed':False,'note':'Contract validated without rendering'}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('file',type=Path);a=p.parse_args()
    print(json.dumps(validate(json.loads(a.file.read_text(encoding='utf-8'))),indent=2))
