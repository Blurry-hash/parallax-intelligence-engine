#!/usr/bin/env python3
"""Offline PCM WAV analysis and peak normalization. Not TTS, LUFS or true-peak analysis."""
import argparse, json, math, sys, wave
from array import array
from pathlib import Path

def load(path):
    path=Path(path)
    if not path.is_file() or path.stat().st_size>100_000_000:
        raise ValueError("missing or oversized WAV file")
    with wave.open(str(path),"rb") as f:
        rate,channels,width,frames=f.getframerate(),f.getnchannels(),f.getsampwidth(),f.getnframes()
        if f.getcomptype()!="NONE" or width!=2 or channels not in (1,2) or not 8000<=rate<=192000 or not 1<=frames<=20_000_000:
            raise ValueError("Only 16-bit uncompressed mono/stereo PCM WAV accepted")
        data=f.readframes(frames)
    if len(data)!=frames*channels*2:raise ValueError("truncated PCM audio")
    a=array("h");a.frombytes(data)
    if sys.byteorder!="little":a.byteswap()
    return a,rate,channels

def _db(x):
    return round(20*math.log10(x),3) if x>0 else None

def stats(a,rate,channels):
    if not a or len(a)%channels:raise ValueError("invalid samples")
    peak=max(abs(int(x)) for x in a)
    rms=(sum(int(x)**2 for x in a)/len(a))**.5/32768
    return {"duration_sec":round(len(a)/channels/rate,5),"sample_rate":rate,"channels":channels,
            "sample_peak_dbfs":_db(peak/32768),"rms_dbfs":_db(rms),
            "clipped_sample_ratio":round(sum(abs(int(x))>=32767 for x in a)/len(a),6),
            "dc_offset":round(sum(int(x) for x in a)/len(a)/32768,6),
            "near_silence_sample_ratio":round(sum(abs(int(x))<=32 for x in a)/len(a),6),
            "note":"Sample peak is not true peak; RMS is not LUFS; subjective naturalness requires listening."}

def analyze(path):
    a,rate,ch=load(path)
    return stats(a,rate,ch)

def normalize(source,target,peak_dbfs=-3.,fade_ms=5.):
    source,target=Path(source),Path(target)
    if not -20<=peak_dbfs<=-0.1 or not 0<=fade_ms<=1000:
        raise ValueError("unsafe processing parameters")
    if source.resolve()==target.resolve() or target.exists():
        raise ValueError("Refuse to overwrite any existing source or output")
    a,rate,ch=load(source)
    maximum=max(abs(int(x)) for x in a)
    if not maximum:raise ValueError("cannot normalize silence")
    before=stats(a,rate,ch)
    gain=32767*10**(peak_dbfs/20)/maximum
    frames=len(a)//ch
    fade=min(int(rate*fade_ms/1000),frames//2)
    b=array("h")
    for i,x in enumerate(a):
        frame=i//ch
        envelope=min(1.,frame/fade,(frames-1-frame)/fade) if fade else 1.
        b.append(max(-32768,min(32767,round(int(x)*gain*max(0.,envelope)))))
    target.parent.mkdir(parents=True,exist_ok=True)
    output=array("h",b)
    if sys.byteorder!="little":output.byteswap()
    with wave.open(str(target),"wb") as w:
        w.setnchannels(ch);w.setsampwidth(2);w.setframerate(rate);w.writeframes(output.tobytes())
    return {"before":before,"after":stats(b,rate,ch),"gain_db":round(20*math.log10(gain),3),"output":str(target)}

if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input",type=Path)
    parser.add_argument("--out",type=Path)
    parser.add_argument("--peak-dbfs",type=float,default=-3.)
    parser.add_argument("--fade-ms",type=float,default=5.)
    args=parser.parse_args()
    result=normalize(args.input,args.out,args.peak_dbfs,args.fade_ms) if args.out else analyze(args.input)
    print(json.dumps(result,indent=2))
