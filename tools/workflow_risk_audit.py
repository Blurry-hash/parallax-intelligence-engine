#!/usr/bin/env python3
"""Static, read-only n8n workflow risk hints; NEVER executes imported nodes."""
import argparse,json
from pathlib import Path
class WorkflowError(ValueError): pass
RISK=('executecommand','webhook','httprequest','gmail','emailsend','stripe','slack','telegram','code','function')
def audit(obj):
    if not isinstance(obj,dict) or not isinstance(obj.get('nodes'),list): raise WorkflowError('nodes must be a list')
    if len(obj['nodes'])>5000: raise WorkflowError('workflow too large')
    findings=[]
    for index,node in enumerate(obj['nodes']):
        if not isinstance(node,dict) or not isinstance(node.get('type'),str) or not node['type']: raise WorkflowError('invalid node')
        name=node.get('name',str(index));type_name=node['type'].lower()
        if any(word in type_name for word in RISK): findings.append({'node':name,'reason':'external or executable node','severity':'high'})
        if node.get('credentials'): findings.append({'node':name,'reason':'credential-binding','severity':'medium'})
        if '169.254.169.254' in json.dumps(node) or '127.0.0.1' in json.dumps(node): findings.append({'node':name,'reason':'local-network endpoint','severity':'high'})
    return {'node_count':len(obj['nodes']),'findings':findings,'requires_review':bool(findings),'executed':False}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('file',type=Path);a=p.parse_args();print(json.dumps(audit(json.loads(a.file.read_text(encoding='utf-8'))),indent=2))
