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
        for path in skill_files:
            if f"`{path.parent.name}`" not in text:
                errors.append(f"README missing skill {path.parent.name}")
    return errors, len(entries), len(skill_files)


if __name__ == "__main__":
    errors, n_sources, n_skills = validate()
    if errors:
        for error in errors:
            print("FAIL:", error)
        raise SystemExit(1)
    print(f"PASS: {n_sources} sources, {n_skills} skills, local structural checks passed")
