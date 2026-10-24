#!/usr/bin/env python3
"""Deterministic instruction retrieval from local SKILL.md, with context budget.

BM25 retrieval over every local skill, not an LLM or proof of execution. Excerpts are
never trusted as policy. Prompt injection in a retrieved skill is NOT executed.
"""
from __future__ import annotations
import argparse, json, re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def choose(query:str,root:Path=ROOT,*,max_skills=3,max_chars=6000)->dict:
    if not isinstance(query,str) or not query.strip() or len(query)>2000:raise ValueError('task must be 1-2000 characters')
    if type(max_skills) is not int or not 1<=max_skills<=6 or type(max_chars) is not int or not 1000<=max_chars<=30000:raise ValueError('invalid budget')
    # Use the same all-skills retrieval as the CLI router, with no provider calls.
    import importlib.util
    spec=importlib.util.spec_from_file_location('parallax_route',Path(__file__).with_name('route_task.py'))
    router=importlib.util.module_from_spec(spec);spec.loader.exec_module(router)
    ranked=[]
    for result in router.candidates(query,root=root,limit=max_skills):
        name=result['skill'];p=root/'skills'/name/'SKILL.md';body=p.read_text(encoding='utf-8')
        desc=next((line.partition(':')[2].strip() for line in body.splitlines()[:10] if line.startswith('description:')), '')
        ranked.append((result['score'],name,p,body,desc))
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
    return {'method':'BM25 all-skills retrieval; no embeddings, inference, execution, or provider calls','query':query,
            'selected':selected,'chars_used':used,'budget_chars':max_chars,
            'warning':'Read full source for production decisions; excerpt length is NOT a true tokenizer count.'}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('task');p.add_argument('--max-skills',type=int,default=3);p.add_argument('--max-chars',type=int,default=6000)
    a=p.parse_args();print(json.dumps(choose(a.task,max_skills=a.max_skills,max_chars=a.max_chars),indent=2,ensure_ascii=False))
if __name__=='__main__':main()
