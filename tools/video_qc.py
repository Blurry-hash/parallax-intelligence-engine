#!/usr/bin/env python3
"""Machine-check video files via ffprobe. No invented playback/visual-quality claims.

Optional diagnostics use FFmpeg for one actual decoded-frame sample; no network.
"""
from __future__ import annotations
import argparse,json,math,shutil,subprocess
from fractions import Fraction
from pathlib import Path

class VideoQualityError(ValueError):pass

def rational(value:str)->float:
    try:
        r=Fraction(str(value))
        f=float(r)
        if not math.isfinite(f) or f<=0:raise ValueError
        return f
    except (ValueError,ZeroDivisionError,OverflowError):raise VideoQualityError(f'invalid fps: {value!r}') from None

def assess(probe:dict,spec:dict)->dict:
    if not isinstance(probe,dict) or not isinstance(spec,dict):raise VideoQualityError('probe/spec must be objects')
    streams=probe.get('streams');fmt=probe.get('format')
    if not isinstance(streams,list) or not isinstance(fmt,dict):raise VideoQualityError('ffprobe output missing streams/format')
    video=next((s for s in streams if isinstance(s,dict) and s.get('codec_type')=='video'),None)
    audio=[s for s in streams if isinstance(s,dict) and s.get('codec_type')=='audio']
    failures=[];warnings=[];observed={'has_video':bool(video),'has_audio':bool(audio)}
    if video is None:failures.append('missing video stream')
    else:
        for key in ('width','height','codec_name'):
            observed[key]=video.get(key)
            if key in spec and spec[key]!=video.get(key):failures.append(f'{key} expected {spec[key]!r} observed {video.get(key)!r}')
        try:
            fps=rational(video.get('avg_frame_rate') or video.get('r_frame_rate'))
            observed['fps']=round(fps,6)
            if 'fps' in spec and (type(spec['fps']) not in (int,float) or not math.isfinite(float(spec['fps'])) or abs(fps-float(spec['fps']))>0.01):failures.append('fps differs from contract')
        except VideoQualityError:
            fps=None
            (failures if 'fps' in spec else warnings).append('fps metadata unavailable')
        frame_count=video.get('nb_frames')
        if frame_count not in (None,'N/A'):
            try: observed['nb_frames']=int(frame_count)
            except ValueError:warnings.append('invalid nb_frames metadata')
        else:warnings.append('frame count not supplied by container (not decoded)')
    try:
        duration=float(fmt['duration'])
        if not math.isfinite(duration) or duration<=0:raise ValueError
        observed['duration_seconds']=round(duration,6)
        if 'duration_seconds' in spec:
            if type(spec['duration_seconds']) not in (float,int) or not math.isfinite(spec['duration_seconds']) or spec['duration_seconds']<=0:raise VideoQualityError('bad duration spec')
            tol=spec.get('duration_tolerance',0.1)
            if type(tol) not in (int,float) or not math.isfinite(tol) or tol<0:raise VideoQualityError('invalid duration_tolerance')
            tolerance=float(tol)
            if abs(duration-float(spec['duration_seconds']))>tolerance:failures.append('duration outside tolerance')
    except (KeyError,ValueError,TypeError):
        (failures if 'duration_seconds' in spec else warnings).append('duration metadata unavailable')
    if 'has_audio' in spec:
        if type(spec['has_audio']) is not bool:raise VideoQualityError('has_audio must be boolean')
        if observed['has_audio']!=spec['has_audio']:failures.append('audio stream presence differs from contract')
    return {'status':'pass' if not failures else 'fail','failures':failures,'warnings':warnings,'observed':observed,'limitations':['Metadata checks do not establish visual quality, stable identity or correct lip synchronization.']}

def probe_file(path:Path)->dict:
    if not path.is_file():raise FileNotFoundError(path)
    executable=shutil.which('ffprobe')
    if not executable:raise RuntimeError('ffprobe executable unavailable')
    cmd=[executable,'-v','error','-show_entries','format=duration,format_name:stream=codec_type,codec_name,width,height,r_frame_rate,avg_frame_rate,nb_frames','-of','json',str(path)]
    r=subprocess.run(cmd,capture_output=True,text=True,check=True,timeout=60)
    return json.loads(r.stdout)

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('media',type=Path);p.add_argument('--contract',type=Path,required=True);a=p.parse_args()
    try:
        spec=json.loads(a.contract.read_text(encoding='utf-8'))
        result=assess(probe_file(a.media),spec)
        print(json.dumps(result,indent=2))
        if result['status']!='pass':raise SystemExit(1)
    except (OSError,ValueError,RuntimeError,subprocess.CalledProcessError,subprocess.TimeoutExpired) as exc:p.error(str(exc))
if __name__=='__main__':main()
