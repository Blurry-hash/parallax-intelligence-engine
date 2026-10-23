#!/usr/bin/env python3
"""Offline capability selection; selects a plan, NEVER executes a voice model."""
import argparse,json
from pathlib import Path

def route(task,providers):
    if not isinstance(task,dict) or task.get("task") not in {"tts","asr","sound_effects","enhance_recording"}:
        raise ValueError("invalid audio task")
    if not isinstance(task.get("language"),str) or not task["language"] or len(task["language"])>30:
        raise ValueError("invalid language")
    if task.get("consent") not in {"original_synthetic","authorized_recording","not_obtained"}:
        raise ValueError("invalid consent")
    if not task.get("use_case"):raise ValueError("use_case required")
    if task.get("speaker_reference") and task["consent"]!="authorized_recording":
        return {"status":"blocked","reason":"No documented consent for reference voice"}
    if not isinstance(providers,list):raise ValueError("providers must be a list")
    candidates=[]
    for p in providers:
        if not isinstance(p,dict) or not p.get("verified_available"):continue
        if task["task"] not in p.get("tasks",[]):continue
        if task["language"] not in p.get("languages",[]) and "*" not in p.get("languages",[]):continue
        if task.get("streaming") and not p.get("streaming"):continue
        if task.get("commercial") and not p.get("commercial_licensed"):continue
        if p.get("requires_cloud") and not task.get("cloud_authorized"):continue
        candidates.append(p)
    if not candidates:
        return {"status":"not_executed","reason":"No verified eligible provider. Use consented recording or reproducible offline path."}
    candidates.sort(key=lambda p:(p.get("estimated_latency_ms",10**9),p.get("id","")))
    return {"status":"planned_only","backend":candidates[0]["id"],"note":"No synthesis has been executed"}
if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("task",type=Path);parser.add_argument("backends",type=Path)
    a=parser.parse_args()
    print(json.dumps(route(json.loads(a.task.read_text()),json.loads(a.backends.read_text())),indent=2))
