#!/usr/bin/env python3
"""Compute dependency-safe schedule, slack and critical path from a deterministic DAG."""
import argparse
import json
import math
from pathlib import Path
try:
    from dag import valid_id, topological_layers
except ModuleNotFoundError:
    from tools.dag import valid_id, topological_layers


def schedule(data: dict) -> dict:
    tasks = data.get('tasks')
    if not isinstance(tasks, list) or not tasks:
        raise ValueError('tasks must be a nonempty list')
    nodes: dict[str, dict] = {}
    for t in tasks:
        if not isinstance(t, dict) or not valid_id(t.get('id')):
            raise ValueError('each task needs a unique nonempty string id')
        tid = t['id']
        d, deps = t.get('duration'), t.get('depends_on', [])
        if tid in nodes: raise ValueError(f'duplicate task id {tid}')
        if type(d) not in (int, float) or not math.isfinite(d) or d <= 0:
            raise ValueError(f'{tid}: duration must be finite positive number')
        if not isinstance(deps, list) or any(not isinstance(p, str) for p in deps):
            raise ValueError(f'{tid}: depends_on must be a string list')
        if len(set(deps)) != len(deps) or tid in deps:
            raise ValueError(f'{tid}: duplicate dependency or self-cycle')
        nodes[tid] = {'duration': float(d), 'deps': deps}
    for tid, v in nodes.items():
        for dep in v['deps']:
            if dep not in nodes: raise ValueError(f'{tid}: unknown dependency {dep}')
    successors = {key: [] for key in nodes}
    for tid, v in nodes.items():
        for dep in v['deps']: successors[dep].append(tid)
    layers=topological_layers({i:v['deps'] for i,v in nodes.items()})
    order=[i for layer in layers for i in layer]
    early_start, early_finish = {}, {}
    for tid in order:
        early_start[tid] = max((early_finish[d] for d in nodes[tid]['deps']), default=0.0)
        early_finish[tid] = early_start[tid] + nodes[tid]['duration']
    total = max(early_finish.values())
    late_start, late_finish = {}, {}
    for tid in reversed(order):
        late_finish[tid] = min((late_start[succ] for succ in successors[tid]), default=total)
        late_start[tid] = late_finish[tid] - nodes[tid]['duration']
    tasks_out = [{'id': tid, 'earliest_start': round(early_start[tid],6),
                  'earliest_finish': round(early_finish[tid],6),
                  'slack': round(max(0,late_start[tid]-early_start[tid]),6)} for tid in order]
    return {'unit': data.get('unit', 'arbitrary duration units'), 'estimated_critical_path':round(total,6),
            'total_serial_work':round(sum(v['duration'] for v in nodes.values()),6),
            'parallel_frontiers':layers, 'critical_tasks': [x['id'] for x in tasks_out if x['slack'] < 1e-6],
            'tasks':tasks_out, 'notes':'Estimates only; no execution or real parallelism occurred.'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('file')
    args=parser.parse_args()
    try:
        result=schedule(json.loads(Path(args.file).read_text(encoding='utf-8')))
    except (ValueError, OSError, UnicodeError) as exc:
        parser.error(str(exc))
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
