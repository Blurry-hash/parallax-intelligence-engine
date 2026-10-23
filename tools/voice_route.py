#!/usr/bin/env python3
"""Describe voice production requirements; route conservatively against ACTUALLY available backends.
No model is bundled and no synthesis is performed by this tool.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path


def route(task: dict, installed: list[dict]) -> dict:
    required={'task','language','consent','use_case'}
    if not isinstance(task, dict) or not required.issubset(task):
        raise ValueError('task requires task/language/consent/use_case')
    if task['task'] not in ('tts','asr','sound_effects','enhance_recording'):
        raise ValueError('Unsupported audio task')
    if not isinstance(task['language'],str) or len(task['language'])>30 or not task['language']:
        raise ValueError('Invalid language')
    if task['consent'] not in ('original_synthetic','authorized_recording','not_obtained'):
        raise ValueError('Invalid consent status')
    if task.get('speaker_reference') and task['consent'] != 'authorized_recording':
        return {'status':'blocked','reason':'Reference-voice generation requires documented consent'}
    if task['consent']=='not_obtained' and task['task']=='tts' and task.get('speaker_reference'):
        return {'status':'blocked','reason':'Consent not obtained'}
    choices=[]
    for p in installed:
        if not isinstance(p,dict) or not p.get('verified_available') or task['task'] not in p.get('tasks',[]):continue
        if task['language'] not in p.get('languages',[]) and '*' not in p.get('languages',[]):continue
        if task.get('streaming') and not p.get('streaming'):continue
        if task.get('commercial') and not p.get('commercial_licensed'):continue
        if p.get('requires_cloud') and not task.get('cloud_authorized'):continue
        choices.append(p)
    if not choices:
        return {'status':'not_executed','reason':'No verified eligible provider; use a consented recorded voice or an offline audio edit workflow.', 'next':'Verify runtime, checkpoint, license and access first'}
    choices.sort(key=lambda x:(x.get('estimated_latency_ms',10**9),x.get('id','')))
    return {'status':'planned_only','backend':choices[0]['id'],'reason':'Capability match; synthesis has not been executed', 'verification':'Review output with audio_lab.py and listening tests'}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('task',type=Path);p.add_argument('backends',type=Path)
    a=p.parse_args();print(json.dumps(route(json.loads(a.task.read_text()),json.loads(a.backends.read_text())),indent=2))
