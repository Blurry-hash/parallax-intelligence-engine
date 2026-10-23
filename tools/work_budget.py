#!/usr/bin/env python3
"""Auditable, bounded actual-work runner; no sleeps, no arbitrary shell commands.

Only allows configured local offline PARALLAX checks. A long session requires
*independent useful work items* supplied in a plan; it cannot invent work or
simulate thinking, run after the model stops, or claim timed mental effort.
"""
import argparse
import json
import math
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALLOWED = {
    'validate': ('tools/validate.py',),
    'unit_tests': ('-m', 'unittest', 'discover', '-s', 'tests', '-q'),
    'source_audit': ('tools/source_audit.py',),
    'skill_route': ('tools/route_task.py', 'Design an accessible, secure application'),
    'capability_audit': ('tools/capability_audit.py',),
    'perf_gate': ('tools/perf_gate.py', 'examples/perf-pairs.json'),
    'critical_path': ('tools/critical_path.py', 'examples/workflow-dag.json'),
}


def parse_plan(data):
    if not isinstance(data, dict):
        raise ValueError('plan must be an object')
    mins = data.get('requested_minutes')
    if type(mins) not in (float, int) or not math.isfinite(mins) or not 0 < mins <= 1440:
        raise ValueError('requested_minutes must be finite positive number <= 1440')
    items = data.get('work_items')
    if not isinstance(items, list) or not items:
        raise ValueError('work_items must be a nonempty list')
    if len(items) > 100:
        raise ValueError('at most 100 work items')
    names = set()
    for item in items:
        if not isinstance(item, dict) or set(item) != {'id', 'action', 'purpose'}:
            raise ValueError('each item needs exactly id, action, purpose')
        ident, action, purpose = (item[k] for k in ('id','action','purpose'))
        if not isinstance(ident,str) or not (1 <= len(ident) <= 64) or not ident.isascii() or not ident.replace('_','').replace('-','').isalnum():
            raise ValueError('invalid item id')
        if ident in names:
            raise ValueError('duplicate item id')
        names.add(ident)
        if not isinstance(action,str) or action not in ALLOWED:
            raise ValueError('action not allowlisted')
        if not isinstance(purpose,str) or not (10 <= len(purpose) <= 250):
            raise ValueError('purpose must describe useful work')
    return mins, items


def atomic_write(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + '.tmp')
    tmp.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n', encoding='utf-8')
    os.replace(tmp, path)


def run_plan(data, *, root=ROOT, output=None, clock=time.monotonic, runner=subprocess.run, time_limit=300.0):
    mins, items = parse_plan(data)
    start = clock()
    deadline = start + mins * 60.0
    report = {
        'requested_minutes': mins, 'started_at_utc': datetime.now(timezone.utc).isoformat(),
        'steps': [], 'status': 'work_exhausted', 'actual_wall_seconds': 0.0,
        'actual_execution_seconds': 0.0, 'reason': '',
        'note': 'This ledger measures local allowed command execution, not AI reasoning time or increased intelligence.',
    }
    for item in items:
        remaining = deadline - clock()
        if remaining <= 0:
            report['status'] = 'budget_exhausted'
            report['reason'] = 'wall-time budget reached before remaining steps'
            break
        cmd = [sys.executable] + list(ALLOWED[item['action']])
        step_start = clock()
        try:
            result = runner(cmd, cwd=str(root), capture_output=True, text=True, timeout=max(0.001, min(time_limit, remaining)), check=False)
            elapsed = max(0.0, clock() - step_start)
            status = 'passed' if result.returncode == 0 else 'failed'
            err = (result.stderr or '')[-1000:]
            out = (result.stdout or '')[-1200:]
            record = {'id':item['id'], 'action':item['action'], 'purpose':item['purpose'],
                      'elapsed_seconds':round(elapsed,6), 'status':status, 'exit_code':result.returncode,
                      'stdout_tail':out, 'stderr_tail':err}
        except OSError as exc:
            elapsed = max(0.0, clock() - step_start)
            record = {'id':item['id'],'action':item['action'],'purpose':item['purpose'],
                      'elapsed_seconds':round(elapsed,6),'status':'failed',
                      'stderr_tail':str(exc)[:600]}
        except subprocess.TimeoutExpired:
            elapsed = max(0.0, clock() - step_start)
            record = {'id':item['id'],'action':item['action'],'purpose':item['purpose'],
                      'elapsed_seconds':round(elapsed,6),'status':'timed_out'}
        report['steps'].append(record)
        if output:
            report['actual_wall_seconds'] = round(max(0.0, clock() - start),6)
            report['actual_execution_seconds'] = round(sum(x['elapsed_seconds'] for x in report['steps']),6)
            atomic_write(Path(output),report)
        if record['status'] != 'passed':
            report['status'] = 'failed'
            report['reason'] = 'a step failed or timed out; inspect ledger'
            break
    else:
        report['reason'] = 'all distinct planned work completed before the requested time budget; no artificial waiting or rework'
    report['actual_wall_seconds'] = round(max(0.0, clock()-start),6)
    report['actual_execution_seconds'] = round(sum(x['elapsed_seconds'] for x in report['steps']),6)
    report['finished_at_utc'] = datetime.now(timezone.utc).isoformat()
    if output:
        atomic_write(Path(output),report)
    return report


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('plan',help='JSON work plan; no arbitrary commands allowed')
    ap.add_argument('--output',default='work-session-ledger.json')
    ap.add_argument('--step-timeout',type=float,default=300.0)
    args=ap.parse_args()
    if not 0 < args.step_timeout <= 3600 or not math.isfinite(args.step_timeout):
        ap.error('step-timeout must be a finite positive number <= 3600')
    try:
        plan=json.loads(Path(args.plan).read_text(encoding='utf-8'))
        report=run_plan(plan,output=Path(args.output),time_limit=args.step_timeout)
    except (OSError,UnicodeError,ValueError) as exc:
        ap.error(str(exc))
    print(json.dumps(report,indent=2,ensure_ascii=False))
    if report['status']=='failed':
        raise SystemExit(1)

if __name__=='__main__':main()
