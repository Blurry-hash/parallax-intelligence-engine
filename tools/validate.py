#!/usr/bin/env python3
"""Deterministic offline validation. Never fetches remote URLs or executes source code."""

import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = (
    "README.md", "MASTER_PROMPT.md", "AGENTS.md", "PUBLISHING.md",
    "AUDIT.md", "benchmarks/evaluation-rubric.md", "sources/README.md",
    "examples/video-storyboard.json", "tools/render_video.py",
)
TRUST = {"official", "third-party", "unverified"}
STATUS = {"verified-page", "unconfirmed"}
URL_HOSTS = {"github.com", "huggingface.co", "projects.blender.org", "ffmpeg.org", "www.ffmpeg.org"}
LINK_PATTERN = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


def skill_content_audit(root: Path, min_unique_lines: int = 4) -> dict:
    """Detect shared padding and exact duplicate procedures without judging truth.

    Uniqueness is measured across the installed corpus after headings, frontmatter
    and short lines are removed. Warnings invite editorial review, not deletion:
    safety rules may legitimately repeat. Exact duplicated procedures are errors.
    """
    from collections import Counter, defaultdict
    files=sorted((root/'skills').glob('*/SKILL.md')); rows={}; procedures=defaultdict(list); empty=[]
    for path in files:
        body=path.read_text(encoding='utf-8')
        content=body.split('---',2)[-1] if body.startswith('---') else body
        lines=[re.sub(r'^\s*(?:\d+[.)]|[-*])\s*','',line.strip()).casefold() for line in content.splitlines() if len(line.strip())>=40 and not line.lstrip().startswith('#')]
        rows[path.parent.name]=lines
        match=re.search(r'## Operational procedure\s*(.*?)(?=\n## |\Z)',content,re.S)
        procedure=re.sub(r'\s+',' ',match.group(1)).strip() if match else ''
        if procedure: procedures[procedure].append(path.parent.name)
        else: empty.append(path.parent.name)
    frequency=Counter(line for lines in rows.values() for line in set(lines))
    total=sum(map(len,rows.values()));shared=sum(frequency[line]>=5 for lines in rows.values() for line in lines)
    warnings=[]
    for name,lines in rows.items():
        unique=sum(frequency[line]==1 for line in set(lines))
        if unique<min_unique_lines: warnings.append(f'{name}: {unique} unique substantial lines; editorial review recommended (target {min_unique_lines})')
    duplicates=[names for names in procedures.values() if len(names)>1]
    return {'skill_count':len(files),'substantial_lines':total,'shared_in_5_or_more':shared,
            'shared_fraction':round(shared/total,4) if total else 0,'warnings':warnings,
            'duplicate_procedures':duplicates,'empty_procedures':empty,'limitations':'Content diversity does not establish correctness or usefulness.'}


def validate(root: Path | None = None) -> tuple[list[str], int, int]:
    root = Path(root) if root is not None else ROOT
    errors: list[str] = []
    for rel in REQUIRED:
        if not (root / rel).is_file():
            errors.append(f"Missing {rel}")
    index = root / "sources" / "sources.json"
    if not index.is_file():
        return errors + ["Missing sources/sources.json"], 0, 0
    try:
        data = json.loads(index.read_text(encoding="utf-8"))
    except (ValueError, UnicodeError) as exc:
        return errors + [f"Invalid sources JSON: {exc}"], 0, 0
    entries = data.get("sources")
    if not isinstance(entries, list) or not entries:
        return errors + ["sources must be a non-empty list"], 0, 0
    seen: set[str] = set()
    for i, item in enumerate(entries):
        if not isinstance(item, dict):
            errors.append(f"Invalid source object #{i}")
            continue
        for field in ("name", "topic", "trust", "status"):
            if not isinstance(item.get(field), str) or not item[field].strip():
                errors.append(f"Source #{i}: missing {field}")
        if item.get("trust") not in TRUST:
            errors.append(f"Source #{i}: invalid trust {item.get('trust')!r}")
        if item.get("status") not in STATUS:
            errors.append(f"Source #{i}: invalid status {item.get('status')!r}")
        if (item.get("trust") == "unverified" or item.get("status") == "unconfirmed") and not item.get("notes", "").strip():
            errors.append(f"Source #{i}: provenance caveat required")
        url = item.get("url", "")
        if not isinstance(url, str):
            errors.append(f"Source #{i}: URL must be string")
            continue
        p = urlsplit(url)
        if p.scheme != "https" or p.hostname not in URL_HOSTS or not p.path.strip("/") or p.username or p.password:
            errors.append(f"Invalid URL #{i}: {url}")
        if url in seen:
            errors.append(f"Duplicate URL {url}")
        seen.add(url)
    skill_files = sorted((root / "skills").glob("*/SKILL.md"))
    if not skill_files:
        errors.append("Missing skills")
    for path in skill_files:
        body = path.read_text(encoding="utf-8")
        if not body.startswith("---\n") or "## Operational procedure" not in body:
            errors.append(f"Invalid skill structure {path.relative_to(root)}")
            continue
        front = body.split("---", 2)[1]
        if not re.search(rf"(?m)^name:\s*{re.escape(path.parent.name)}\s*$", front):
            errors.append(f"Invalid skill name {path.relative_to(root)}")
        if not re.search(r"(?m)^description:\s*\S", front):
            errors.append(f"Missing skill description {path.relative_to(root)}")
    for path in sorted(root.rglob("*.md")):
        if ".git" in path.parts:
            continue
        body = path.read_text(encoding="utf-8")
        for raw in LINK_PATTERN.findall(body):
            href = raw.split()[0].strip("<>")
            if href.startswith(("https://", "http://", "mailto:", "#")):
                continue
            local = unquote(href.split("#", 1)[0])
            if not local:
                continue
            target = (path.parent / local).resolve()
            if not target.is_relative_to(root.resolve()) or not target.exists():
                errors.append(f"Broken local link {path.relative_to(root)}: {href}")
    readme = root / "README.md"
    if readme.is_file():
        text = readme.read_text(encoding="utf-8")
        if f"{len(entries)} linked references" not in text:
            errors.append("README source count does not match registry")
        catalog=root/'docs'/'SKILL-CATALOG.md'
        catalog_text=catalog.read_text(encoding='utf-8') if catalog.is_file() else ''
        for path in skill_files:
            if f"`{path.parent.name}`" not in text+catalog_text:
                errors.append(f"README missing skill {path.parent.name}")
    audit=skill_content_audit(root)
    for name in audit['empty_procedures']:
        errors.append('Empty operational procedure: '+name)
    for names in audit['duplicate_procedures']:
        errors.append('Duplicate operational procedures: '+', '.join(names))
    return errors, len(entries), len(skill_files)


if __name__ == "__main__":
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--content-report',action='store_true',help='Emit duplicate/padding diagnostics as JSON')
    args=parser.parse_args()
    if args.content_report:
        print(json.dumps(skill_content_audit(ROOT),indent=2));raise SystemExit(0)
    errors, n_sources, n_skills = validate()
    if errors:
        for error in errors:
            print("FAIL:", error)
        raise SystemExit(1)
    print(f"PASS: {n_sources} sources, {n_skills} skills, local structural checks passed")
