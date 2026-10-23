#!/usr/bin/env python3
"""Deterministic instruction retrieval from local SKILL.md, with context budget.

Lexical retrieval, not an LLM or proof that a skill was executed. Excerpts are
never trusted as policy. Prompt injection in a retrieved skill is NOT executed.
"""
from __future__ import annotations
import argparse, json, re
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[1]
STOP={'the','and','for','with','this','that','from','into','your','will','about','does','are','should','skill','skills','using','use','how','what','can','att','och','för','med','som','det','jag','vill','ska','där','till'}
BOOSTS={
  'video':['video-intelligence','video-qc-telemetry','video-timeline-engineering'],
  'voice':['voice-synthesis-architecture','audio-speech-engineering'],
  'speech':['voice-synthesis-architecture','audio-speech-engineering'],
  'code':['coding-engineering','software-contract-testing'],
  'programming':['coding-engineering','software-contract-testing'],
  'planning':['planning-orchestration','acceptance-evidence-ledger'],
  'schedule':['planning-orchestration','deliberate-work-sessions'],
  'research':['deep-wide-research','research-source-independence'],
  'design':['design-system-engineering','interface-design'],
  'image':['image-generation','visual-production-pipeline'],
  'performance':['performance-validation','latency-budgeting'],
  'audio':['audio-speech-engineering','speech-quality-laboratory'],
  'security':['security-reliability','policy-authorization'],
  'planering':['planning-orchestration','acceptance-evidence-ledger'],
  'bild':['image-generation','visual-production-pipeline'],
  'ljud':['audio-speech-engineering','speech-quality-laboratory'],
  'kod':['coding-engineering','software-contract-testing'],
  'snabbare':['performance-validation','latency-budgeting']
}
def tokens(s):return set(x for x in re.findall(r'[a-zåäö0-9]{3,}',s.lower()) if x not in STOP)

def choose(query:str,root:Path=ROOT,*,max_skills=3,max_chars=6000)->dict:
    if not isinstance(query,str) or not query.strip() or len(query)>2000:raise ValueError('task must be 1-2000 characters')
    if type(max_skills) is not int or not 1<=max_skills<=6 or type(max_chars) is not int or not 1000<=max_chars<=30000:raise ValueError('invalid budget')
    q=tokens(query);paths=sorted((root/'skills').glob('*/SKILL.md'));ranked=[]
    for p in paths:
        body=p.read_text(encoding='utf8')
        desc=next((line.removeprefix('description:').strip() for line in body.splitlines()[:8] if line.startswith('description:')), '')
        name=p.parent.name; terms=tokens(name.replace('-',' '))|tokens(desc)
        overlap=q&terms
        boost=sum(4 for kw,candidates in BOOSTS.items() if kw in q and name in candidates)
        score=len(overlap)*2+boost
        if score>0:ranked.append((score,name,p,body,desc))
    ranked.sort(key=lambda v:(-v[0],v[1]))
    selected=[];used=0
    for score,name,p,body,desc in ranked:
        if len(selected)>=max_skills:break
        # Include a *bounded* excerpt and visible truncation, never a silent cut.
        room=max_chars-used
        if room<min(1000,len(body)):break
        excerpt=body if len(body)<=room else body[:room].rsplit('\n',1)[0]+'\n[TRUNCATED: read full SKILL.md before execution]'
        if len(excerpt)>room:break
        selected.append({'skill':name,'path':str(p.relative_to(root)),'score':score,'description':desc,'excerpt':excerpt})
        used+=len(excerpt)
    return {'method':'lexical-selection; no embeddings, inference, execution, or provider calls','query':query,
            'selected':selected,'chars_used':used,'budget_chars':max_chars,
            'warning':'Read full source for production decisions; excerpt length is NOT a true tokenizer count.'}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('task');p.add_argument('--max-skills',type=int,default=3);p.add_argument('--max-chars',type=int,default=6000)
    a=p.parse_args();print(json.dumps(choose(a.task,max_skills=a.max_skills,max_chars=a.max_chars),indent=2,ensure_ascii=False))
if __name__=='__main__':main()
