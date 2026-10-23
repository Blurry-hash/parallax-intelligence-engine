#!/usr/bin/env python3
"""Four concurrent, independent deterministic specialist workers (NOT LLM agents).

This is a useful non-model sub-agent mode: scoped read-only functions and a
single orchestrator. No provider keys, arbitrary plugins, shell, or writes.
For reasoning agents via LLMs, integrate an authorized SDK separately.
"""
import argparse
import concurrent.futures
import json
import time
from pathlib import Path
from plan_engine import compile_plan

ROOT = Path(__file__).resolve().parents[1]


def structure_worker(root, plan):
    from validate import validate
    problems, sources, skills = validate(root)
    return {'pass': not problems, 'findings': problems[:30], 'metrics': {'sources': sources, 'skills': skills}}


def planning_worker(root, plan):
    result = compile_plan(plan)
    alerts = []
    if result['work_estimate_exceeds_budget']:
        alerts.append('Estimated sum of work exceeds requested_minutes multiplied by workers')
    if result['estimated_critical_path_minutes'] > result['requested_minutes']:
        alerts.append('Critical-path minimum exceeds the requested time budget')
    return {'pass': not alerts, 'findings': alerts, 'metrics': {'waves': len(result['parallel_waves']), 'critical_minutes': result['estimated_critical_path_minutes']}}


def provenance_worker(root, plan):
    data = json.loads((root / 'sources/sources.json').read_text(encoding='utf-8'))
    sources = data['sources']
    unconfirmed = sum(s.get('status') == 'unconfirmed' for s in sources)
    unsafe = [s.get('name', '?') for s in sources if s.get('trust') == 'unverified' and not s.get('notes')]
    return {'pass': not unsafe, 'findings': ['unverified source missing caveat: ' + x for x in unsafe], 'metrics': {'unconfirmed_sources': unconfirmed}}


def permission_worker(root, plan):
    missing = [t['id'] for t in plan['tasks'] if (t['risk'] == 'high' or t['kind'] == 'delivery') and not t['approval_required']]
    return {'pass': not missing, 'findings': ['approval required: ' + x for x in missing], 'metrics': {'approval_gates': sum(t['approval_required'] for t in plan['tasks'])}}


WORKERS = {
    'structure': structure_worker,
    'planning': planning_worker,
    'source_provenance': provenance_worker,
    'permissions': permission_worker,
}


def run_audits(plan, root=ROOT, *, clock=time.perf_counter, executor_factory=concurrent.futures.ThreadPoolExecutor):
    # Validate before parallel dispatch: guard against malformed plans.
    summary = compile_plan(plan)
    start = clock()
    with executor_factory(max_workers=min(4, len(WORKERS))) as pool:
        futures = {name: pool.submit(worker, root, plan) for name, worker in WORKERS.items()}
        reports = {}
        for name in sorted(futures):
            try:
                reports[name] = futures[name].result()
            except Exception as exc:
                reports[name] = {'pass': False, 'findings': [type(exc).__name__ + ': ' + str(exc)[:250]], 'metrics': {}}
    return {
        'execution': '4 real read-only parallel deterministic audit workers; no separate LLMs were invoked',
        'plan_sha256': summary['plan_sha256'],
        'worker_count': len(WORKERS),
        'elapsed_seconds': round(max(0, clock()-start), 6),
        'pass': all(item['pass'] for item in reports.values()),
        'workers': reports,
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('plan', type=Path)
    p.add_argument('--root', type=Path, default=ROOT)
    p.add_argument('--out', type=Path)
    args = p.parse_args()
    try:
        data = json.loads(args.plan.read_text(encoding='utf-8'))
        report = run_audits(data, args.root)
    except (OSError, ValueError) as exc:
        p.error(str(exc))
    output = json.dumps(report, indent=2) + '\n'
    if args.out:
        args.out.write_text(output, encoding='utf-8')
    print(output, end='')
    if not report['pass']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
