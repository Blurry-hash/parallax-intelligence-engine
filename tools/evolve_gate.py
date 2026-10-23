#!/usr/bin/env python3
"""Conservative offline champion/challenger gate: no prompt mutation or auto-deployment."""
import argparse,json,math
from pathlib import Path

def finite(value):
    if isinstance(value,bool) or not isinstance(value,(float,int)) or not math.isfinite(value):
        raise ValueError("finite metric required")
    return float(value)
def p95(values):
    return sorted(values)[math.ceil(.95*len(values))-1]
def evaluate(evidence):
    cases=evidence.get("cases") if isinstance(evidence,dict) else None
    if not isinstance(cases,list) or not 5<=len(cases)<=10000:
        raise ValueError("5..10000 matched cases required")
    if not evidence.get("baseline_revision") or not evidence.get("candidate_revision") or evidence["baseline_revision"]==evidence["candidate_revision"]:
        raise ValueError("distinct revisions required")
    if evidence.get("holdout_was_used_to_tune") is not False:
        raise ValueError("holdout contamination cannot be ruled out")
    ids=set();holdout=[];dev=[];domains=set()
    for c in cases:
        if not isinstance(c,dict) or not isinstance(c.get("id"),str) or not c["id"] or c["id"] in ids:
            raise ValueError("duplicate or invalid case ID")
        ids.add(c["id"])
        if c.get("split") not in ("development","holdout") or not c.get("domain"):
            raise ValueError("split/domain required")
        (holdout if c["split"]=="holdout" else dev).append(c)
        if c["split"]=="holdout":domains.add(c["domain"])
        for side in ("baseline","candidate"):
            row=c.get(side)
            if not isinstance(row,dict):raise ValueError("missing metrics")
            for name in ("quality","latency_ms","cost_usd"):
                val=finite(row.get(name))
                if (name=="quality" and not 0<=val<=1) or (name!="quality" and val<0):
                    raise ValueError("out of range metric")
            if not isinstance(row.get("critical_failure"),bool):
                raise ValueError("critical_failure must be a bool")
    if len(holdout)<5 or len(domains)<2 or not dev:
        raise ValueError("need development and >=5 holdouts across >=2 domains")
    mean=lambda side,key:sum(c[side][key] for c in holdout)/len(holdout)
    bq,cq=mean("baseline","quality"),mean("candidate","quality")
    bl,cl=p95([c["baseline"]["latency_ms"] for c in holdout]),p95([c["candidate"]["latency_ms"] for c in holdout])
    bc,cc=mean("baseline","cost_usd"),mean("candidate","cost_usd")
    fails=[]
    if any(c["candidate"]["critical_failure"] for c in holdout):fails.append("critical failure")
    if any(c["baseline"]["quality"]-c["candidate"]["quality"]>.05 for c in holdout):fails.append("case quality regression")
    if cq-bq<.02:fails.append("quality improvement below 0.02")
    if cl>bl*1.15:fails.append("p95 latency regression")
    if cc>bc*1.2 and cc>bc+.0001:fails.append("cost regression")
    return {"decision":"eligible_for_human_review" if not fails else "reject",
            "safe_to_auto_deploy":False,"failures":fails,"holdout_cases":len(holdout),
            "holdout_domains":len(domains),"quality_gain":round(cq-bq,6),
            "p95_ms":{"baseline":bl,"candidate":cl},
            "note":"Input measurements have not been independently authenticated."}
if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("evidence",type=Path)
    args=p.parse_args()
    print(json.dumps(evaluate(json.loads(args.evidence.read_text())),indent=2))
