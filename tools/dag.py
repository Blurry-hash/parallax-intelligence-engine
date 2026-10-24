"""Common dependency graph contract for all planning adapters.

Task IDs use ASCII lowercase letters, digits, underscore and hyphen (1-48 chars,
starting with a letter). Validation and deterministic topology are shared;
resource scheduling and domain-specific fields remain adapter responsibilities.
"""
import re
ID_RE=re.compile(r'^[a-z][a-z0-9_-]{0,47}$')

def valid_id(value):
    return isinstance(value,str) and ID_RE.fullmatch(value) is not None

def topological_layers(graph):
    if not graph: raise ValueError('nonempty graph required')
    for ident,deps in graph.items():
        if not valid_id(ident): raise ValueError(f'invalid task id: {ident!r}')
        if not isinstance(deps,list) or any(not valid_id(d) for d in deps):
            raise ValueError(f'{ident}: invalid dependencies')
        if len(deps)!=len(set(deps)) or ident in deps: raise ValueError('duplicate dependency or self-cycle')
        if any(d not in graph for d in deps): raise ValueError('missing dependency')
    remaining=set(graph); complete=set(); layers=[]
    while remaining:
        ready=sorted(i for i in remaining if set(graph[i])<=complete)
        if not ready: raise ValueError('dependency cycle detected')
        layers.append(ready);complete.update(ready);remaining.difference_update(ready)
    return layers
