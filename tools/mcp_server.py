#!/usr/bin/env python3
"""Local MCP stdio adapter: read-only tools, no shell/network/remote service."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(Path(__file__).resolve().parent))
from route_task import candidates
from validate import validate
from loop_controller import evaluate
TOOLS=[{'name':'route_task','description':'Rank local skills; does not execute them.','inputSchema':{'type':'object','properties':{'query':{'type':'string','maxLength':10000},'limit':{'type':'integer','minimum':1,'maximum':10}},'required':['query'],'additionalProperties':False}},{'name':'validate','description':'Validate local repository.','inputSchema':{'type':'object','properties':{},'additionalProperties':False}},{'name':'loop_controller','description':'Assess supplied evidence; no experiment execution.','inputSchema':{'type':'object','properties':{'evidence':{'type':'object'}},'required':['evidence'],'additionalProperties':False}}]
def call(name,args):
 if not isinstance(args,dict):raise ValueError('arguments must be object')
 if name=='route_task':
  if set(args)-{'query','limit'} or 'query' not in args:raise ValueError('query required; unexpected arguments')
  return {'recommendations':candidates(args['query'],limit=args.get('limit',3))}
 if name=='validate':
  if args:raise ValueError('validate accepts no arguments')
  errors,sources,skills=validate();return {'errors':errors,'sources':sources,'skills':skills}
 if name=='loop_controller':
  if set(args)!={'evidence'}:raise ValueError('evidence required')
  return evaluate(args['evidence'])
 raise ValueError('unknown tool')
def respond(m):
 if not isinstance(m,dict) or m.get('jsonrpc')!='2.0':raise ValueError('JSON-RPC 2.0 object required')
 if 'id' not in m:return None
 method=m.get('method');ident=m['id']
 if not isinstance(m.get('params',{}),dict):return {'jsonrpc':'2.0','id':ident,'error':{'code':-32602,'message':'params must be an object'}}
 if method=='tools/call' and (not isinstance(m.get('params',{}).get('name'),str) or not isinstance(m.get('params',{}).get('arguments',{}),dict)):
  return {'jsonrpc':'2.0','id':ident,'error':{'code':-32602,'message':'tool name and object arguments required'}}
 if method=='initialize':
  requested=m.get('params',{}).get('protocolVersion');version=requested if requested in ('2024-11-05','2025-03-26','2025-06-18') else '2025-06-18'
  result={'protocolVersion':version,'capabilities':{'tools':{'listChanged':False}},'serverInfo':{'name':'parallax-local','version':(ROOT/'VERSION').read_text(encoding='utf-8').strip()}}
 elif method=='ping':result={}
 elif method=='tools/list':result={'tools':TOOLS}
 elif method=='tools/call':
  params=m.get('params',{})
  try:value=call(params.get('name'),params.get('arguments',{}));result={'content':[{'type':'text','text':json.dumps(value,ensure_ascii=False)}],'isError':False}
  except (ValueError,TypeError,KeyError,OSError) as e:result={'content':[{'type':'text','text':str(e)}],'isError':True}
 else:return {'jsonrpc':'2.0','id':ident,'error':{'code':-32601,'message':'Method not found'}}
 return {'jsonrpc':'2.0','id':ident,'result':result}
def main():
 for stream in (sys.stdin,sys.stdout,sys.stderr):
  if hasattr(stream,'reconfigure'):stream.reconfigure(encoding='utf-8')
 for line in sys.stdin:
  try:
   if len(line)>1024*1024:raise ValueError('oversized message')
   response=respond(json.loads(line))
  except (ValueError,TypeError,AttributeError):response={'jsonrpc':'2.0','id':None,'error':{'code':-32700,'message':'Invalid JSON-RPC input'}}
  if response is not None:print(json.dumps(response,ensure_ascii=False),flush=True)
if __name__=='__main__':main()
