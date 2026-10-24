#!/usr/bin/env python3
"""Prepare sampled local video frames and optional audio; no ASR/OCR or model calls."""
import argparse,hashlib,json,math,shutil,subprocess
from pathlib import Path

def prepare(source,out,*,interval=5.,max_frames=120,audio=False):
 source,out=Path(source).resolve(),Path(out).resolve()
 if not source.is_file():raise ValueError('Input media file required')
 if not math.isfinite(interval) or interval<=0:raise ValueError('Positive finite interval required')
 if type(max_frames) is not int or not 1<=max_frames<=500:raise ValueError('max_frames must be 1..500')
 if out.exists():raise ValueError('Output directory must not exist')
 for t in ('ffprobe','ffmpeg'):
  if not shutil.which(t):raise ValueError(t+' unavailable')
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(source)],timeout=30))
 duration=float(probe['format']['duration'])
 if not math.isfinite(duration) or duration<=0:raise ValueError('Positive finite duration required')
 video=any(s.get('codec_type')=='video' for s in probe['streams']);sound=any(s.get('codec_type')=='audio' for s in probe['streams'])
 count=min(max_frames,max(1,math.ceil(duration/interval))) if video else 0
 spacing=max(interval,duration/count) if count else interval
 out.mkdir(parents=True);frames=[]
 for i in range(count):
  t=i*spacing;name=f'frame-{i:04d}.jpg'
  subprocess.run(['ffmpeg','-nostdin','-v','error','-ss',str(t),'-i',str(source),'-frames:v','1','-vf','scale=960:-2','-n',str(out/name)],check=True,timeout=60)
  if not (out/name).is_file():raise ValueError('No decoded frame at '+str(t))
  frames.append({'seconds':round(t,6),'file':name})
 audio_path=None
 if audio and sound:
  audio_path='audio.wav';subprocess.run(['ffmpeg','-nostdin','-v','error','-i',str(source),'-vn','-ac','1','-ar','16000','-c:a','pcm_s16le','-n',str(out/audio_path)],check=True,timeout=max(60,min(1800,duration*2)))
 digest=hashlib.sha256()
 with source.open('rb') as f:
  for chunk in iter(lambda:f.read(1024*1024),b''):digest.update(chunk)
 report={'source_name':source.name,'sha256':digest.hexdigest(),'duration':duration,'probe':probe,'frames':frames,'audio_file':audio_path,'coverage':{'visual':'sampled frames prepared, not reviewed','speech':'not transcribed','ocr':'not performed','motion':'not assessed'},'effective_interval':spacing,'requested_interval':interval}
 (out/'coverage.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');return report
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('input',type=Path);p.add_argument('--out',required=True,type=Path);p.add_argument('--interval',type=float,default=5);p.add_argument('--max-frames',type=int,default=120);p.add_argument('--audio',action='store_true');a=p.parse_args()
 try:
  r=prepare(a.input,a.out,interval=a.interval,max_frames=a.max_frames,audio=a.audio);print(json.dumps({'frames_prepared':len(r['frames']),'audio_extracted':bool(r['audio_file']),'duration':r['duration'],'coverage_file':str(a.out/'coverage.json')}))
 except (ValueError,OSError,subprocess.SubprocessError) as e:p.exit(2,str(e)+'\n')
