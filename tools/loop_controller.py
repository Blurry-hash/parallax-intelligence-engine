#!/usr/bin/env python3
"""Deterministic, offline evaluation controller for five bounded feedback-loop designs.

This is not a model API, Python code runner, scheduler or automatic deployment system.
Scores must come from externally observed evaluation records; it never fabricates scores.
"""
from __future__ import annotations
import argparse
import json
import math
import re
from pathlib import Path

MODES = ('verification', 'adversarial', 'multipath', 'prompt_opt', 'regression')
ID = re.compile(r'^[a-zA-Z0-9][a-zA-Z0-9_.:-]{0,95}$')


def number(value, field, minimum=0, maximum=None):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f'{field}: finite number required')
    if value < minimum or (maximum is not None and value > maximum):
        raise ValueError(f'{field}: out of range')
    return float(value)


def ident(value, field):
    if not isinstance(value, str) or not ID.fullmatch(value):
        raise ValueError(f'{field}: simple nonempty identifier required')
    return value


def evidence(item, field):
    if not isinstance(item, dict) or item.get('kind') not in ('external', 'self_review'):
        raise ValueError(f'{field}: kind external or self_review required')
    ident(item.get('id'), field+'.id')
    if not isinstance(item.get('passed'), bool):
        raise ValueError(f'{field}: passed must be a boolean')
    return item['kind'] == 'external' and item['passed'] is True


def tests_pass(tests, field):
    if not isinstance(tests, list) or not tests:
        return False
    ids=set()
    for t in tests:
        if not isinstance(t, dict):
            raise ValueError(f'{field}: test object required')
        t_id=ident(t.get('id'),field+'.id')
        if t_id in ids:
            raise ValueError(f'{field}: duplicate test id')
        ids.add(t_id)
        if not isinstance(t.get('passed'), bool):
            raise ValueError(f'{field}: test.passed must be bool')
    return all(t['passed'] for t in tests)


def regression_gate(baseline, item):
    old=baseline.get('regressions')
    new=item.get('regressions')
    if not isinstance(old,dict) or not old or not isinstance(new,dict):
        return False
    if len(old)>1000 or len(new)>1000:
        raise ValueError('regression cases capped at 1000')
    for key, passed in old.items():
        ident(key,'baseline.regressions key')
        if not isinstance(passed,bool):raise ValueError('baseline regression outcome must be bool')
        if passed and new.get(key) is not True: return False
    for key,passed in new.items():
        ident(key,'candidate.regressions key')
        if not isinstance(passed,bool): raise ValueError('candidate regression outcome must be bool')
        if not passed: return False
    return True


def evaluate(data):
    if not isinstance(data, dict):raise ValueError('Expected JSON object')
    mode=data.get('mode')
    if mode not in MODES:raise ValueError(f'mode must be one of {MODES}')
    conf=data.get('config',{})
    if not isinstance(conf,dict):raise ValueError('config must be object')
    limit=conf.get('max_iterations',4)
    patience=conf.get('patience',2)
    if type(limit) is not int or not 1<=limit<=20:raise ValueError('max_iterations: integer 1..20')
    if type(patience) is not int or not 1<=patience<=limit:raise ValueError('patience: integer 1..max_iterations')
    min_gain=number(conf.get('min_gain',0.01),'min_gain',0,1)
    cost_cap=number(conf.get('max_cost_usd',1),'max_cost_usd',0,100000)
    tokens_cap=number(conf.get('max_tokens',10000),'max_tokens',0,10000000)
    base=data.get('baseline')
    if not isinstance(base,dict):raise ValueError('baseline object required')
    baseid=ident(base.get('id'),'baseline.id')
    base_score=number(base.get('score'),'baseline.score',0,1)
    if not evidence(base.get('evidence'),'baseline.evidence'):
        raise ValueError('baseline requires passed external evidence')
    if base.get('critical_failure') is not False:
        raise ValueError('baseline must explicitly have no critical_failure')
    candidates=data.get('candidates')
    if not isinstance(candidates,list) or len(candidates)>limit:
        raise ValueError('candidates must be list within iteration limit')
    ids={baseid}; evid_ids={base['evidence']['id']}; candidates_checked=[]; spent_cost=0.;spent_tokens=0.
    for i,row in enumerate(candidates,1):
        if not isinstance(row,dict):raise ValueError('candidate must be object')
        name=ident(row.get('id'),'candidate.id')
        if name in ids:raise ValueError('duplicate candidate id')
        ids.add(name)
        if row.get('iteration')!=i or type(row.get('iteration')) is not int:
            raise ValueError('iterations must be sequential integers starting at 1')
        ident(row.get('parent'),'candidate.parent')
        if row['parent'] not in ids-{name}:
            raise ValueError('candidate parent must be an earlier known revision')
        score=number(row.get('score'),'candidate.score',0,1)
        ev=row.get('evidence')
        is_external=evidence(ev,'candidate.evidence')
        if ev['id'] in evid_ids:raise ValueError('evidence id reused: independence impossible to assess')
        evid_ids.add(ev['id'])
        if not isinstance(row.get('critical_failure'),bool):raise ValueError('critical_failure must be boolean')
        spent_cost+=number(row.get('cost_usd',0),'cost_usd',0)
        spent_tokens+=number(row.get('tokens',0),'tokens',0)
        candidates_checked.append({'item':row,'valid_evidence':is_external,'score':score,'reject':[]})
    reasons=[]
    best=baseid;best_score=base_score
    for entry in candidates_checked:
        row=entry['item'];reject=entry['reject']
        if not entry['valid_evidence']: reject.append('no passed external evidence')
        if row['critical_failure']: reject.append('critical failure')
        if mode=='adversarial':
            stress=row.get('stress_tests')
            if not tests_pass(stress,'stress_tests') or len(stress)<2:
                reject.append('at least two distinct passing adversarial checks required')
        elif mode=='regression':
            if not regression_gate(base,row): reject.append('protected regression tests failed or absent')
        elif mode=='multipath':
            ident(row.get('strategy'),'candidate.strategy')
        elif mode=='prompt_opt':
            # Development-only selection. Holdout must be a separate, one-time final gate.
            if row.get('holdout_score') is not None: reject.append('holdout result cannot tune candidate selection')
            if row.get('holdout_used_to_tune') is not False:reject.append('holdout use must explicitly be false')
        if not reject and entry['score']>=best_score+min_gain:
            best=row['id'];best_score=entry['score']
    if mode=='multipath':
        strategies={e['item']['strategy'] for e in candidates_checked if not e['reject']}
        if len(strategies)<2:reasons.append('Need at least two distinct externally evaluated strategies')
    if mode=='prompt_opt':
        audit=data.get('holdout_audit')
        if audit is not None:
            if not isinstance(audit,dict):raise ValueError('holdout_audit must be object')
            if audit.get('candidate')!=best:reasons.append('Holdout evaluated a non-selected candidate')
            if audit.get('used_to_tune') is not False:reasons.append('Holdout leakage or unknown selection provenance')
            if not evidence(audit.get('evidence'),'holdout_audit.evidence'):
                reasons.append('No passed external holdout proof')
            if audit['evidence']['id'] in evid_ids:reasons.append('Holdout evidence reused')
            holdout_base=number(audit.get('baseline_score'),'holdout baseline',0,1)
            holdout_candidate=number(audit.get('candidate_score'),'holdout candidate',0,1)
            if holdout_candidate < holdout_base+min_gain:reasons.append('Holdout did not improve over baseline')
    exhausted=len(candidates)>=limit or spent_cost>=cost_cap or spent_tokens>=tokens_cap
    eligible=[e for e in candidates_checked if not e['reject']]
    # Stop after the last `patience` eligible attempts fail to improve the champion,
    # but never conflate the absence of evidence with a successful iteration.
    stagnant=False
    if len(eligible)>=patience:
        recently=eligible[-patience:]
        prior=[base_score]+[e['score'] for e in eligible[:-patience]]
        stagnant=all(e['score']<max(prior)+min_gain for e in recently)
    no_gain=(best==baseid)
    if mode=='prompt_opt' and best!=baseid and data.get('holdout_audit') is None:
        status='needs_holdout'
    elif mode=='prompt_opt' and reasons:
        status='reject'
    elif mode=='multipath' and reasons:
        status='stop' if exhausted else 'continue'
    elif exhausted or stagnant:
        status='stop'
    else:status='continue'
    if mode=='prompt_opt' and no_gain and exhausted:status='stop'
    accepted=(best!=baseid and not reasons and (mode!='prompt_opt' or status!='needs_holdout'))
    capsule=[]
    if mode=='regression':
        for e in candidates_checked:
            if e['item']['id']!=best or e['reject']:continue
            lessons=e['item'].get('lessons',[])
            if not isinstance(lessons,list) or len(lessons)>5:raise ValueError('lessons capped at 5 strings')
            for note in lessons:
                if not isinstance(note,str) or not 1<=len(note)<=180:
                    raise ValueError('lesson must be short text')
                capsule.append({'candidate':best,'lesson':note,'provenance':e['item']['evidence']['id'],'not_persisted':True})
    return {'mode':mode,'status':status,'best_candidate':best,'best_score':round(best_score,6),
            'eligible_for_human_review':bool(accepted),'auto_deployed':False,
            'code_executed':False,'model_calls_performed':0,
            'evaluated_candidates':len(candidates),'budgets_declared':{'cost_usd':round(spent_cost,6),'tokens':int(spent_tokens)},
            'remaining_iterations':max(0,limit-len(candidates)), 'warnings':reasons,
            'rejected_candidates':{e['item']['id']:e['reject'] for e in candidates_checked if e['reject']},
            'memory_capsule':capsule,
            'note':'Controller checks user-supplied evidence; it does not run LLMs, tests, CI, deployments, or authenticate their provenance.'}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('file',type=Path,help='Offline JSON loop evidence')
    args=p.parse_args()
    try: print(json.dumps(evaluate(json.loads(args.file.read_text(encoding='utf-8'))),ensure_ascii=False,indent=2))
    except (ValueError,OSError,KeyError) as exc:p.exit(2,'Invalid loop evidence: '+str(exc)+'\n')
