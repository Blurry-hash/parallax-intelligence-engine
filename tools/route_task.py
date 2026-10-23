#!/usr/bin/env python3
"""Explainable, deterministic skill shortlist; no API keys, model calls or external requests.

This is a conservative *lexical* router, not semantic reasoning. The caller
selects/overrides the candidate skills after understanding actual user intent.
"""
from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
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


def candidates(query: str, root: Path = ROOT, limit: int = 3) -> list[dict]:
    if not isinstance(query, str) or len(query)>10000 or limit<1 or limit>10:
        raise ValueError('query must be a string of <=10000 characters; limit 1..10')
    q = ' '.join(re.findall(r'[^\W_]+', query.casefold(), flags=re.UNICODE))
    matched=[]
    for name, words in KEYWORDS.items():
        if not (root/'skills'/name/'SKILL.md').is_file():
            continue
        keys=[]
        for phrase in words:
            phrase=' '.join(re.findall(r'[^\W_]+', phrase.casefold(), flags=re.UNICODE))
            if re.search(r'(?<!\w)'+re.escape(phrase)+r'(?!\w)', q):
                keys.append(phrase)
        if keys:
            matched.append({'skill':name,'matches':keys,'score':len(keys)})
    return sorted(matched,key=lambda x:(-x['score'],x['skill']))[:limit]


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('query',help='Task description (no secrets)')
    parser.add_argument('--limit',type=int,default=3)
    args=parser.parse_args()
    print(json.dumps({'mode':'lexical-hints-only','external_calls':0,
                      'recommendations':candidates(args.query,limit=args.limit)},indent=2))

if __name__=='__main__':
    main()
