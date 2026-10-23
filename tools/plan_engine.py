#!/usr/bin/env python3
"""Offline, side-effect-free planning compiler for bounded multi-agent projects.

Compiles a user-provided goal/task graph into deterministic parallel waves. No
model invocation, network, command execution, permission escalation, or timer.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import re
from pathlib import Path

KINDS = frozenset({'research', 'design', 'implementation', 'verification', 'review', 'delivery'})
RISKS = frozenset({'low', 'medium', 'high'})
ID_RE = re.compile(r'^[a-z][a-z0-9_-]{0,47}$')
MAX_TASKS = 80


class PlanError(ValueError):
    """Invalid or unsafe plan specification."""


def _text(value, label, *, minimum=1, maximum=320):
    if not isinstance(value, str) or not minimum <= len(value.strip()) <= maximum:
        raise PlanError(f'{label}: expected {minimum}-{maximum} characters')
    if '\x00' in value:
        raise PlanError(f'{label}: NUL not allowed')
    return value.strip()


def validate_plan(data: dict):
    if not isinstance(data, dict) or set(data) != {'version', 'goal', 'requested_minutes', 'max_workers', 'tasks'}:
        raise PlanError('plan requires exactly version, goal, requested_minutes, max_workers, tasks')
    if data['version'] != '1':
        raise PlanError('unsupported plan version')
    _text(data['goal'], 'goal', minimum=12, maximum=800)
    requested = data['requested_minutes']
    if type(requested) not in (int, float) or not math.isfinite(requested) or not 0 < requested <= 1440:
        raise PlanError('requested_minutes must be finite and in (0, 1440]')
    workers = data['max_workers']
    if type(workers) is not int or not 1 <= workers <= 4:
        raise PlanError('max_workers must be integer 1..4')
    tasks = data['tasks']
    if not isinstance(tasks, list) or not 1 <= len(tasks) <= MAX_TASKS:
        raise PlanError(f'tasks must contain 1..{MAX_TASKS} entries')
    by_id = {}
    required = {'id', 'title', 'kind', 'depends_on', 'estimated_minutes', 'impact', 'risk', 'approval_required', 'acceptance'}
    for index, item in enumerate(tasks):
        if not isinstance(item, dict) or set(item) != required:
            raise PlanError(f'task[{index}] has incorrect fields')
        ident = item['id']
        if not isinstance(ident, str) or not ID_RE.fullmatch(ident):
            raise PlanError(f'task[{index}] invalid id')
        if ident in by_id:
            raise PlanError(f'duplicate task id: {ident}')
        _text(item['title'], ident + '.title', minimum=6, maximum=180)
        if not isinstance(item['kind'], str) or item['kind'] not in KINDS:
            raise PlanError(f'{ident}: unknown kind')
        if not isinstance(item['risk'], str) or item['risk'] not in RISKS:
            raise PlanError(f'{ident}: unknown risk')
        if type(item['approval_required']) is not bool:
            raise PlanError(f'{ident}: approval_required must be boolean')
        if (item['risk'] == 'high' or item['kind'] == 'delivery') and not item['approval_required']:
            raise PlanError(f'{ident}: high-risk/delivery task requires explicit approval gate')
        estimate = item['estimated_minutes']
        if type(estimate) not in (int, float) or not math.isfinite(estimate) or not 0 < estimate <= 1440:
            raise PlanError(f'{ident}: invalid estimated_minutes')
        if type(item['impact']) is not int or not 1 <= item['impact'] <= 5:
            raise PlanError(f'{ident}: impact must be integer 1..5')
        deps = item['depends_on']
        if not isinstance(deps, list) or any(not isinstance(d, str) for d in deps) or len(deps) != len(set(deps)):
            raise PlanError(f'{ident}: invalid or duplicate dependencies')
        acceptance = item['acceptance']
        if not isinstance(acceptance, list) or not 1 <= len(acceptance) <= 8:
            raise PlanError(f'{ident}: expected 1..8 acceptance criteria')
        for criterion in acceptance:
            _text(criterion, ident + '.acceptance', minimum=12, maximum=260)
        by_id[ident] = item
    for ident, item in by_id.items():
        for dep in item['depends_on']:
            if dep not in by_id:
                raise PlanError(f'{ident}: unknown dependency {dep}')
            if dep == ident:
                raise PlanError(f'{ident}: self dependency')

    # Deterministic topological sorting with explicit bounded worker waves.
    remaining = set(by_id)
    complete = set()
    waves = []
    while remaining:
        ready = [by_id[k] for k in sorted(remaining) if set(by_id[k]['depends_on']) <= complete]
        if not ready:
            raise PlanError('dependency cycle detected')
        # Approval gates are not automatically satisfied. Scheduling is advisory.
        ready.sort(key=lambda t: (-t['impact'], t['estimated_minutes'], t['id']))
        chosen = ready[:workers]
        ids = [t['id'] for t in chosen]
        waves.append(ids)
        complete.update(ids)
        remaining.difference_update(ids)
    return by_id, waves


def compile_plan(data: dict) -> dict:
    by_id, waves = validate_plan(data)
    order = [t for wave in waves for t in wave]
    ends = {}
    for task_id in order:
        task = by_id[task_id]
        ends[task_id] = float(task['estimated_minutes']) + max([ends[d] for d in task['depends_on']], default=0)
    total = sum(float(t['estimated_minutes']) for t in by_id.values())
    critical = max(ends.values())
    payload = json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False)
    approvals = sorted(i for i, t in by_id.items() if t['approval_required'])
    return {
        'plan_sha256': hashlib.sha256(payload.encode('utf-8')).hexdigest(),
        'status': 'ADVISORY_ONLY_NOT_EXECUTED',
        'goal': data['goal'],
        'task_count': len(by_id),
        'worker_limit': data['max_workers'],
        'parallel_waves': waves,
        'estimated_work_minutes_sum': round(total, 3),
        'estimated_critical_path_minutes': round(critical, 3),
        'requested_minutes': data['requested_minutes'],
        'approval_gates': approvals,
        'work_estimate_exceeds_budget': total > data['requested_minutes'] * data['max_workers'],
        'note': 'Estimates are user-supplied. Critical path ignores resource contention, and waves are priorities, not a wall-clock execution schedule. No agents or models were run.',
    }


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('plan', type=Path, help='Local JSON plan. Never executed by this tool.')
    p.add_argument('--output', type=Path)
    args = p.parse_args()
    try:
        compiled = compile_plan(json.loads(args.plan.read_text(encoding='utf-8')))
    except (OSError, ValueError) as exc:
        p.error(str(exc))
    output = json.dumps(compiled, indent=2, ensure_ascii=False) + '\n'
    if args.output:
        args.output.write_text(output, encoding='utf-8')
    print(output, end='')


if __name__ == '__main__':
    main()
