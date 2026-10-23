#!/usr/bin/env python3
"""Compile frame-accurate timeline JSON to FFmpeg storyboard + SRT captions.

Offline, deterministic, no external assets fetched and no subprocess executed.
Identity consistency checks operate on declared metadata only; they do not inspect pixels.
"""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path

COLOR=re.compile(r'^#[a-fA-F0-9]{6}$')
SHOT_ID=re.compile(r'^[a-zA-Z][a-zA-Z0-9_-]{0,63}$')
class TimelineError(ValueError):pass

def srt_clock(frames:int, fps:int)->str:
    if type(frames)!=int or frames<0 or type(fps)!=int or not 1<=fps<=120:raise TimelineError('invalid frame/timebase')
    ms=(frames*1000+fps//2)//fps
    h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000)
    return f'{h:02}:{m:02}:{s:02},{ms:03}'

def compile_timeline(data:dict)->dict:
    if not isinstance(data,dict):raise TimelineError('timeline must be object')
    fps,w,h=data.get('fps'),data.get('width'),data.get('height')
    if type(fps)!=int or not 1<=fps<=120:raise TimelineError('fps must be 1..120')
    if any(type(a)!=int or a%2 or not 128<=a<=3840 for a in (w,h)):raise TimelineError('even dimensions 128..3840 required')
    shots=data.get('shots'); locked=data.get('locked_state',{})
    if not isinstance(shots,list) or not 1<=len(shots)<=24:raise TimelineError('shots must have 1..24 items')
    if not isinstance(locked,dict) or any(not isinstance(k,str) or not isinstance(v,(str,int,float,bool)) for k,v in locked.items()):raise TimelineError('invalid locked_state')
    offset=0;ids=set();scene_data=[];srt=[];edl=[]
    for index,shot in enumerate(shots,1):
        if not isinstance(shot,dict):raise TimelineError(f'shot {index} must be object')
        sid=shot.get('id'); frames=shot.get('frames'); color=shot.get('background'); states=shot.get('state',{})
        if not isinstance(sid,str) or not SHOT_ID.fullmatch(sid) or sid in ids:raise TimelineError('duplicate or invalid shot id')
        ids.add(sid)
        if type(frames)!=int or frames < max(1,(fps+4)//5) or frames>120*fps:raise TimelineError('shot duration must be 0.2..120 seconds')
        if not isinstance(color,str) or not COLOR.fullmatch(color):raise TimelineError('invalid background')
        if not isinstance(states,dict) or any(k in locked and locked[k]!=v for k,v in states.items()):raise TimelineError('locked_state conflict')
        title,sub,caption=(shot.get(k,'') for k in ('title','subtitle','caption'))
        if any(not isinstance(v,str) or len(v)>500 for v in (title,sub,caption)):raise TimelineError('text fields must be strings <=500 characters')
        if '\x00' in title+sub+caption:raise TimelineError('null character in text')
        scene_data.append({'seconds':frames/fps,'title':title,'subtitle':sub,'background':color})
        end=offset+frames
        edl.append({'shot_id':sid,'start_frame':offset,'end_frame_exclusive':end,'duration_frames':frames,'start':srt_clock(offset,fps),'end':srt_clock(end,fps)})
        if caption.strip():
            clean=caption.strip().replace('\r\n','\n').replace('\r','\n')
            srt.append(f'{len(srt)+1}\n{srt_clock(offset,fps)} --> {srt_clock(end,fps)}\n{clean}\n')
        offset=end
    if offset>fps*300:raise TimelineError('total duration >300 seconds')
    return {'storyboard':{'width':w,'height':h,'fps':fps,'scenes':scene_data},'edl':edl,'srt':'\n'.join(srt)+'\n' if srt else '', 'duration_frames':offset,'duration_seconds':offset/fps,'checks':{'locked_state':'metadata_consistent_not_visual_identity_verified','rendered':False}}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('timeline',type=Path);p.add_argument('--storyboard-out',type=Path,required=True);p.add_argument('--srt-out',type=Path,required=True);p.add_argument('--edl-out',type=Path,required=True)
    a=p.parse_args()
    try:
        result=compile_timeline(json.loads(a.timeline.read_text(encoding='utf-8')))
        for dest,key in [(a.storyboard_out,'storyboard'),(a.srt_out,'srt'),(a.edl_out,'edl')]:
            dest.parent.mkdir(parents=True,exist_ok=True)
            dest.write_text(result[key] if key=='srt' else json.dumps(result[key],indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
        print(json.dumps({'duration_frames':result['duration_frames'],'duration_seconds':result['duration_seconds'],'rendered':False,'shots':len(result['edl'])},indent=2))
    except (OSError,ValueError) as exc:p.error(str(exc))
if __name__=='__main__':main()
