#!/usr/bin/env python3
"""Offline acceptance/evidence ledger: reject false 'verified' task completions."""
import argparse
import hashlib
import json
from pathlib import Path
from plan_engine import compile_plan, PlanError

STATES = frozenset({'pending', 'in_progress', 'blocked', 'verified'})


def audit_ledger(plan, ledger):
    summary = compile_plan(plan)
    task_ids = {item['id'] for item in plan['tasks']}
    if not isinstance(ledger, dict) or set(ledger) != {'plan_sha256', 'tasks'}:
        raise ValueError('ledger requires exactly plan_sha256, tasks')
    if ledger['plan_sha256'] != summary['plan_sha256']:
        raise ValueError('plan hash mismatch: stale or unrelated evidence')
    records = ledger['tasks']
    if not isinstance(records, list) or len(records) != len(task_ids):
        raise ValueError('ledger must include exactly one record per planned task')
    found = {}
    for item in records:
        if not isinstance(item, dict) or set(item) != {'id', 'state', 'evidence', 'approved'}:
            raise ValueError('malformed record')
        ident = item['id']
        if not isinstance(ident, str) or ident not in task_ids or ident in found:
            raise ValueError('unknown or duplicate ledger id')
        if not isinstance(item['state'], str) or item['state'] not in STATES or type(item['approved']) is not bool:
            raise ValueError('invalid ledger state or approval')
        evidence = item['evidence']
        if not isinstance(evidence, list) or any(not isinstance(e, str) or len(e.strip()) < 12 or len(e) > 500 for e in evidence):
            raise ValueError('invalid evidence entry')
        if item['state'] == 'verified' and not evidence:
            raise ValueError('cannot verify without evidence')
        found[ident] = item
    task_map = {item['id']: item for item in plan['tasks']}
    for ident, record in found.items():
        if record['state'] == 'verified':
            if task_map[ident]['approval_required'] and not record['approved']:
                raise ValueError(f'{ident}: approval gate not satisfied')
            if any(found[dependency]['state'] != 'verified' for dependency in task_map[ident]['depends_on']):
                raise ValueError(f'{ident}: dependencies not verified')
    return {
        'plan_sha256': summary['plan_sha256'],
        'verified': sorted(i for i, v in found.items() if v['state'] == 'verified'),
        'blocked': sorted(i for i, v in found.items() if v['state'] == 'blocked'),
        'complete': all(item['state'] == 'verified' for item in found.values()),
        'note': 'Self-reported evidence is a trace, not independently authenticated proof. Review evidence before deployment.'
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('plan', type=Path)
    p.add_argument('ledger', type=Path)
    args = p.parse_args()
    try:
        plan = json.loads(args.plan.read_text(encoding='utf-8'))
        ledger = json.loads(args.ledger.read_text(encoding='utf-8'))
        result = audit_ledger(plan, ledger)
    except (OSError, ValueError, PlanError) as exc:
        p.error(str(exc))
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
