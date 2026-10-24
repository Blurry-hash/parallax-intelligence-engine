"""Adversarial and positive tests for bounded planning, evidence and workers."""
from __future__ import annotations
import copy
import hashlib
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'tools'))
import plan_engine
import goal_trace
import agent_audit

BASE = json.loads((ROOT/'examples/planning-v10.3.json').read_text(encoding='utf-8'))


def modify(fn):
    obj=copy.deepcopy(BASE)
    fn(obj)
    return obj


def valid_ledger(data=BASE):
    digest = plan_engine.compile_plan(data)['plan_sha256']
    return {'plan_sha256':digest,'tasks':[{'id':t['id'],'state':'verified','evidence':[{'path':str(Path(__file__)), 'sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), 'kind':'test_report', 'outcome':'pass'}],'approved':t['approval_required']} for t in data['tasks']]}


class PlanningTests(unittest.TestCase):
    def test_baseline_compiles_reproducibly(self):
        a=plan_engine.compile_plan(BASE)
        b=plan_engine.compile_plan(copy.deepcopy(BASE))
        self.assertEqual(a,b)
        self.assertEqual(a['task_count'],6)
        self.assertEqual(a['estimated_critical_path_minutes'],102)
        self.assertIn('publish_release',a['approval_gates'])
        self.assertEqual(a['status'],'ADVISORY_ONLY_NOT_EXECUTED')

    def test_independent_tasks_appear_together(self):
        waves=plan_engine.compile_plan(BASE)['parallel_waves']
        self.assertEqual(set(waves[2]),{'build_engine','test_negative'})

    def test_dependency_cycle_rejected(self):
        x=modify(lambda o:o['tasks'][0]['depends_on'].append('publish_release'))
        with self.assertRaisesRegex(plan_engine.PlanError,'cycle'):
            plan_engine.compile_plan(x)

    def test_unknown_dependency_rejected(self):
        x=modify(lambda o:o['tasks'][1]['depends_on'].append('ghost'))
        with self.assertRaisesRegex(plan_engine.PlanError,'unknown dependency'):
            plan_engine.compile_plan(x)

    def test_self_dependency_rejected(self):
        x=modify(lambda o:o['tasks'][0]['depends_on'].append('inspect_baseline'))
        with self.assertRaisesRegex(plan_engine.PlanError,'self dependency'):
            plan_engine.compile_plan(x)

    def test_duplicate_tasks_rejected(self):
        x=modify(lambda o:o['tasks'].append(copy.deepcopy(o['tasks'][0])))
        with self.assertRaisesRegex(plan_engine.PlanError,'duplicate task id'):
            plan_engine.compile_plan(x)

    def test_undocumented_risk_or_delivery_rejected(self):
        for setter in [
            lambda o:o['tasks'][-1].update(approval_required=False),
            lambda o:o['tasks'][1].update(kind='delivery',approval_required=False),
        ]:
            with self.subTest(setter=setter), self.assertRaisesRegex(plan_engine.PlanError,'approval gate'):
                plan_engine.compile_plan(modify(setter))

    def test_boolean_or_nonfinite_numeric_rejected(self):
        cases = [
            lambda o:o.update(requested_minutes=True),
            lambda o:o.update(requested_minutes=float('nan')),
            lambda o:o['tasks'][0].update(estimated_minutes=float('inf')),
            lambda o:o['tasks'][0].update(estimated_minutes=False),
            lambda o:o['tasks'][0].update(impact=True),
        ]
        for case in cases:
            with self.subTest(case=case), self.assertRaises(plan_engine.PlanError):
                plan_engine.compile_plan(modify(case))

    def test_workers_bound(self):
        for n in (0,5,True,'4',4.0):
            with self.subTest(n=n),self.assertRaises(plan_engine.PlanError):
                plan_engine.compile_plan(modify(lambda o:o.update(max_workers=n)))

    def test_illegal_task_type_rejected(self):
        for value in ([],None,{},7):
            with self.subTest(value=value),self.assertRaises( (plan_engine.PlanError,TypeError) ):
                plan_engine.compile_plan(modify(lambda o:o['tasks'][0].update(kind=value)))

    def test_empty_or_vague_criteria_rejected(self):
        for criteria in ([],['OK'],['']):
            with self.subTest(criteria=criteria),self.assertRaises(plan_engine.PlanError):
                plan_engine.compile_plan(modify(lambda o:o['tasks'][0].update(acceptance=criteria)))

    def test_no_arbitrary_commands(self):
        x=modify(lambda o:o['tasks'][0].update(command='curl https://example.net'))
        with self.assertRaisesRegex(plan_engine.PlanError,'incorrect fields'):
            plan_engine.compile_plan(x)

    def test_estimate_mismatch_flagged(self):
        x=modify(lambda o:o.update(requested_minutes=5))
        r=plan_engine.compile_plan(x)
        self.assertTrue(r['work_estimate_exceeds_budget'])

    def test_valid_complete_evidence(self):
        r=goal_trace.audit_ledger(BASE,valid_ledger())
        self.assertTrue(r['complete'])
        self.assertEqual(len(r['verified']),6)

    def test_false_verified_without_evidence_rejected(self):
        x=valid_ledger(); x['tasks'][0]['evidence']=[]
        with self.assertRaisesRegex(ValueError,'without evidence'):
            goal_trace.audit_ledger(BASE,x)

    def test_approval_not_granted_rejected(self):
        x=valid_ledger(); x['tasks'][-1]['approved']=False
        with self.assertRaisesRegex(ValueError,'approval gate'):
            goal_trace.audit_ledger(BASE,x)

    def test_dependency_not_verified_rejected(self):
        x=valid_ledger(); x['tasks'][0]['state']='pending'
        with self.assertRaisesRegex(ValueError,'dependencies not verified'):
            goal_trace.audit_ledger(BASE,x)

    def test_stale_hash_rejected(self):
        x=valid_ledger();x['plan_sha256']='0'*64
        with self.assertRaisesRegex(ValueError,'plan hash mismatch'):
            goal_trace.audit_ledger(BASE,x)

    def test_duplicate_ledger_entry_rejected(self):
        x=valid_ledger(); x['tasks'][-1]['id']=x['tasks'][0]['id']
        with self.assertRaisesRegex(ValueError,'duplicate'):
            goal_trace.audit_ledger(BASE,x)

    def test_worker_set_runs_independently(self):
        result=agent_audit.run_audits(BASE,ROOT)
        self.assertEqual(set(result['workers']),{'structure','planning','source_provenance','permissions'})
        self.assertEqual(result['worker_count'],4)
        self.assertTrue(result['pass'])
        self.assertIn('no separate LLMs',result['execution'])

    def test_worker_isolation_failure_is_reported(self):
        original=agent_audit.WORKERS.copy()
        def bad(root,plan):raise RuntimeError('worker failed')
        try:
            agent_audit.WORKERS['planning']=bad
            result=agent_audit.run_audits(BASE,ROOT)
            self.assertFalse(result['pass'])
            self.assertIn('RuntimeError',result['workers']['planning']['findings'][0])
            self.assertTrue(result['workers']['structure']['pass'])
        finally:
            agent_audit.WORKERS.clear()
            agent_audit.WORKERS.update(original)

if __name__ == '__main__':
    unittest.main()
