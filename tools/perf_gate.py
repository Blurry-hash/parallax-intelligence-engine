#!/usr/bin/env python3
"""Conservative paired correctness/latency gate, without empirical claims about fixture data."""
import argparse
import json
import math
from pathlib import Path
try:
    from paired_stats import paired_summary
except ModuleNotFoundError:
    from tools.paired_stats import paired_summary


def percentile(values:list[float], percent:float)->float:
    ordered=sorted(values)
    return ordered[min(len(ordered)-1, math.ceil(percent/100*len(ordered))-1)]


def compare(data: dict)->dict:
    rows=data.get('cases')
    if not isinstance(rows,list) or len(rows)<3:
        raise ValueError('Need at least three matched tasks; larger samples recommended')
    allowed=data.get('max_p95_regression_percent',5.0)
    if type(allowed) not in (float,int) or not math.isfinite(allowed) or allowed<0:
        raise ValueError('Invalid p95 regression threshold')
    seen=set(); bl=[]; cl=[]; reg=[]; corrected=0
    for row in rows:
        if not isinstance(row,dict) or not isinstance(row.get('id'),str) or not row['id'] or row['id'] in seen:
            raise ValueError('case IDs must be unique nonempty strings')
        seen.add(row['id'])
        b,c=row.get('baseline'),row.get('candidate')
        if not isinstance(b,dict) or not isinstance(c,dict):
            raise ValueError('case needs baseline/candidate objects')
        for item in (b,c):
            t=item.get('latency_ms')
            if type(t) not in (float,int) or not math.isfinite(t) or t<=0:
                raise ValueError('latency_ms must be finite positive')
            if type(item.get('correct')) is not bool:
                raise ValueError('correct must be a boolean')
        bl.append(float(b['latency_ms']));cl.append(float(c['latency_ms']))
        if b['correct'] and not c['correct']:
            reg.append(row['id'])
        if not b['correct'] and c['correct']:corrected+=1
    bp=percentile(bl,95);cp=percentile(cl,95)
    limit=bp*(1+allowed/100)
    inference=paired_summary(bl,cl,higher_is_better=False)
    # Numeric compatibility is reported separately; acceptance requires enough
    # independently collected pairs, not a significant speedup claim.
    numeric_passes=not reg and cp<=limit
    accepted=numeric_passes and inference['sample_sufficient']
    return {'accepted':accepted, 'reason':('correctness regression' if reg else 'p95 latency regression' if cp>limit else 'insufficient matched sample' if not inference['sample_sufficient'] else 'passes stated gates'),
            'latency_inference':inference,'numeric_gates_pass':numeric_passes,'sample_count':len(rows),'correctness_regressions':reg,'correctness_improvements':corrected,
            'baseline_p50_ms':percentile(bl,50),'candidate_p50_ms':percentile(cl,50),
            'baseline_p95_ms':bp,'candidate_p95_ms':cp,
            'paired_sum_latency_change_percent':round((sum(cl)/sum(bl)-1)*100,2),
            'note':'Small or synthetic samples are not proof of real-world speed improvements; validate with holdouts.'}


def main()->int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('file')
    parser.add_argument('--report-only',action='store_true',help='Emit an assessment without using acceptance as process exit status (for synthetic smoke fixtures)')
    args=parser.parse_args()
    try: out=compare(json.loads(Path(args.file).read_text(encoding='utf-8')))
    except (ValueError,OSError,UnicodeError) as exc: parser.error(str(exc))
    print(json.dumps(out,indent=2))
    return 0 if args.report_only or out['accepted'] else 1

if __name__=='__main__':raise SystemExit(main())
