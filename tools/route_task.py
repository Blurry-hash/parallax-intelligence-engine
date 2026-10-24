#!/usr/bin/env python3
"""Explainable, deterministic skill shortlist; no API keys, model calls or external requests.

This is corpus-wide BM25 lexical retrieval, not semantic reasoning. The caller
selects/overrides the candidate skills after understanding actual user intent.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KEYWORDS: dict[str, tuple[str, ...]] = {
    "coding-engineering": ("code", "coding", "bug", "function", "repository", "refactor", "kod", "programmer"),
    "deep-wide-research": ("research", "sources", "citations", "compare studies", "evidence", "forsk", "källor"),
    "creative-discovery": ("invent", "creative", "novel", "original", "brainstorm", "uppfinn", "kreativ"),
    "interface-design": ("interface", "dashboard", "layout", "web design", "ui", "ux", "design"),
    "design-system-engineering": ("component", "design system", "tokens", "storybook", "komponent"),
    "accessibility-assurance": ("accessibility", "screenreader", "wcag", "keyboard navigation", "tillgänglighet"),
    "image-generation": ("image", "photo", "photorealistic", "picture", "bild", "fotoreal"),
    "video-intelligence": ("video", "mp4", "ffmpeg", "film", "klipp"),
    "audio-speech-engineering": ("audio", "speech", "voice", "podcast", "music", "ljud", "röst"),
    "multimodal-fusion": ("multimodal", "audio and video", "synchronize", "transcript", "timecode"),
    "hardware-physical": ("hardware", "esp32", "pcb", "electronics", "circuit", "sensor", "hårdvara"),
    "networking-digital": ("wifi", "network", "router", "latency", "ip address", "nätverk"),
    "api-contract-engineering": ("api", "endpoint", "schema", "http", "pagination", "webhook"),
    "database-reliability": ("database", "sql", "postgres", "index", "migration", "databas"),
    "data-quality-pipelines": ("pipeline", "etl", "data quality", "dataset", "ingestion", "datakvalitet"),
    "durable-automation": ("automate", "automation", "schedule", "job", "retry", "automatisk"),
    "policy-authorization": ("permissions", "rbac", "policy", "authorization", "behörighet"),
    "threat-modeling": ("threat", "attack surface", "security review", "hotmodell", "säkerhet"),
    "privacy-by-design": ("privacy", "gdpr", "personal data", "data protection", "sekretess", "integritet"),
    "capability-contract": ("sandbox", "tools available", "capabilities", "browser compute", "verktyg"),
    "skill-supply-chain": ("skill", "prompt injection", "supply chain", "mcp security"),
    "scientific-computation": ("simulation", "physics", "equation", "numerical", "simulering"),
    "causal-inference": ("causal", "correlation", "confound", "randomized", "orsakssamband"),
    "structured-output-reliability": ("json", "structured", "schema validation", "parse", "format"),
    "retrieval-quality": ("retrieval", "rag", "embedding", "search quality", "sök"),
    "root-cause-debugging": ("crash", "exception", "error", "failed", "root cause", "felsök"),
    "performance-validation": ("benchmark", "performance", "speed", "faster", "snabbare"),
}


STOP = {'the','and','for','with','this','that','from','your','are','should','skill','skills','use','using','how','what','can','att','och','för','med','som','det','jag','vill','ska','till'}


def tokens(text: str) -> list[str]:
    return [x for x in re.findall(r"[^\W_]+", text.casefold(), flags=re.UNICODE) if x not in STOP and len(x)>1]


def candidates(query: str, root: Path = ROOT, limit: int = 3) -> list[dict]:
    """Rank every installed skill using BM25; aliases assist multilingual queries.

    Body terms make every skill reachable, including newly installed skills.
    Exact skill-name queries are intentionally pinned first. Scores are retrieval
    relevance, never calibrated probabilities or evidence of execution.
    """
    from collections import Counter
    from math import log
    if not isinstance(query, str) or len(query)>10000 or type(limit) is not int or not 1<=limit<=10:
        raise ValueError('query must be a string of <=10000 characters; limit 1..10')
    q=set(tokens(query))
    if not q: return []
    docs=[]
    for path in sorted((root/'skills').glob('*/SKILL.md')):
        body=path.read_text(encoding='utf-8')
        name=path.parent.name
        desc=next((line.partition(':')[2] for line in body.splitlines()[:10] if line.startswith('description:')), '')
        # Repeat discriminative metadata rather than overweighting shared boilerplate.
        words=tokens((name.replace('-',' ')+' '+desc+' ')*3+body+' '+' '.join(KEYWORDS.get(name,())))
        docs.append((name,Counter(words),len(words)))
    if not docs: return []
    avg=sum(n for _,_,n in docs)/len(docs)
    df={term:sum(term in counts for _,counts,_ in docs) for term in q}
    ranked=[]
    normalized=' '.join(tokens(query.replace('-',' ')))
    for name,counts,length in docs:
        matched=sorted(q & counts.keys())
        if not matched: continue
        score=sum(log(1+(len(docs)-df[t]+.5)/(df[t]+.5))*counts[t]*2.2/(counts[t]+1.2*(.25+.75*length/avg)) for t in matched)
        # Small exact alias prior preserves multilingual entry points; all skills
        # remain eligible through corpus retrieval. No substring matches.
        alias_matches=[phrase for phrase in KEYWORDS.get(name,()) if re.search(r'(?<!\w)'+re.escape(phrase)+r'(?!\w)',query.casefold())]
        score+=4*len(alias_matches)
        if normalized==' '.join(tokens(name.replace('-',' '))): score+=1000
        ranked.append({'skill':name,'matches':matched,'score':round(score,6)})
    return sorted(ranked,key=lambda x:(-x['score'],x['skill']))[:limit]


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('query',help='Task description (no secrets)')
    parser.add_argument('--limit',type=int,default=3)
    args=parser.parse_args()
    print(json.dumps({'mode':'BM25 local retrieval; hints only','external_calls':0,
                      'recommendations':candidates(args.query,limit=args.limit)},indent=2))

if __name__=='__main__':
    main()
