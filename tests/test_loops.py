"""Adversarial tests for deterministic five-mode loop controller (no model calls)."""
import importlib.util
import json
import math
import unittest
from copy import deepcopy
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('loop_controller',ROOT/'tools/loop_controller.py')
ctrl=importlib.util.module_from_spec(spec);spec.loader.exec_module(ctrl)

def load(name):
    return json.loads((ROOT/'examples'/f'loop-{name.replace("_","-")}.json').read_text())

class LoopEngineTests(unittest.TestCase):
    def test_all_five_modes_have_real_fixture(self):
        for mode in ctrl.MODES:
            with self.subTest(mode=mode):
                out=ctrl.evaluate(load(mode))
                self.assertEqual(out['mode'],mode)
                self.assertTrue(out['eligible_for_human_review'])
                self.assertFalse(out['auto_deployed'])
                self.assertFalse(out['code_executed'])
                self.assertEqual(out['model_calls_performed'],0)

    def test_self_review_is_not_external_evidence(self):
        p=load('verification')
        p['candidates'][0]['evidence']['kind']='self_review'
        out=ctrl.evaluate(p)
        self.assertEqual(out['best_candidate'],'baseline')
        self.assertFalse(out['eligible_for_human_review'])
        self.assertIn('no passed external evidence',out['rejected_candidates']['candidate-v1'])

    def test_critical_failure_vetoes_high_score(self):
        p=load('verification');p['candidates'][0]['score']=.99;p['candidates'][0]['critical_failure']=True
        self.assertEqual(ctrl.evaluate(p)['best_candidate'],'baseline')

    def test_negative_and_nonfinite_scores_rejected(self):
        for bad in [-1,1.1,float('nan'),float('inf'),True,'0.5']:
            with self.subTest(bad=repr(bad)):
                p=load('verification');p['candidates'][0]['score']=bad
                with self.assertRaises(ValueError):ctrl.evaluate(p)

    def test_duplicate_evidence_or_candidate_forbidden(self):
        p=load('verification');p['candidates'][0]['evidence']['id']='baseline-test'
        with self.assertRaises(ValueError):ctrl.evaluate(p)
        p=load('verification');p['candidates'][0]['id']='baseline'
        with self.assertRaises(ValueError):ctrl.evaluate(p)

    def test_parent_and_sequence_contracts(self):
        for change in [('parent','nonexistent'),('iteration',4)]:
            p=load('verification');p['candidates'][0][change[0]]=change[1]
            with self.subTest(change=change),self.assertRaises(ValueError):ctrl.evaluate(p)

    def test_zero_progress_keeps_baseline_and_uses_patience(self):
        p=load('verification')
        p['config']['max_iterations']=2;p['config']['patience']=2
        p['candidates'][0]['score']=.50
        another=deepcopy(p['candidates'][0]);another.update(id='v2',iteration=2,score=.51)
        another['evidence']['id']='test-v2'
        p['candidates'].append(another)
        out=ctrl.evaluate(p)
        self.assertEqual(out['status'],'stop')
        self.assertEqual(out['best_candidate'],'baseline')

    def test_budget_cannot_claim_executed_calls(self):
        p=load('verification');p['config']['max_cost_usd']=.001
        out=ctrl.evaluate(p)
        self.assertEqual(out['status'],'stop')
        self.assertFalse(out['code_executed'])

    def test_strict_iteration_cap(self):
        p=load('verification');p['config']['max_iterations']=1
        p['candidates'].append(deepcopy(p['candidates'][0]))
        with self.assertRaises(ValueError):ctrl.evaluate(p)

    def test_adversarial_missing_and_failing_stress_rejected(self):
        p=load('adversarial');p['candidates'][0]['stress_tests']=[]
        self.assertEqual(ctrl.evaluate(p)['best_candidate'],'baseline')
        p=load('adversarial');p['candidates'][0]['stress_tests'][0]['passed']=False
        self.assertEqual(ctrl.evaluate(p)['best_candidate'],'baseline')

    def test_adversarial_duplicate_stress_test_rejected(self):
        p=load('adversarial');p['candidates'][0]['stress_tests'][1]['id']='boundary-case'
        with self.assertRaises(ValueError):ctrl.evaluate(p)

    def test_multipath_requires_two_distinct_verified_strategies(self):
        p=load('multipath');p['candidates'][1]['strategy']='symbolic'
        out=ctrl.evaluate(p)
        self.assertFalse(out['eligible_for_human_review'])
        self.assertTrue(out['warnings'])
        p=load('multipath');p['candidates'][1]['evidence']['passed']=False
        out=ctrl.evaluate(p)
        self.assertFalse(out['eligible_for_human_review'])

    def test_prompt_opt_requires_one_unseen_holdout(self):
        p=load('prompt_opt');p.pop('holdout_audit')
        out=ctrl.evaluate(p)
        self.assertEqual(out['status'],'needs_holdout')
        self.assertFalse(out['eligible_for_human_review'])

    def test_prompt_opt_prevents_contamination(self):
        p=load('prompt_opt');p['holdout_audit']['used_to_tune']=True
        out=ctrl.evaluate(p)
        self.assertEqual(out['status'],'reject')
        self.assertFalse(out['eligible_for_human_review'])
        p=load('prompt_opt');p['candidates'][0]['holdout_score']=.9
        self.assertEqual(ctrl.evaluate(p)['best_candidate'],'baseline')

    def test_prompt_opt_rejects_holdout_regression(self):
        p=load('prompt_opt');p['holdout_audit']['candidate_score']=.51
        self.assertFalse(ctrl.evaluate(p)['eligible_for_human_review'])

    def test_regression_missing_or_failed_baseline_case_rejected(self):
        p=load('regression');p['candidates'][0]['regressions'].pop('unit-2')
        self.assertEqual(ctrl.evaluate(p)['best_candidate'],'baseline')
        p=load('regression');p['candidates'][0]['regressions']['unit-1']=False
        self.assertEqual(ctrl.evaluate(p)['best_candidate'],'baseline')

    def test_regression_capsule_never_saved_automatically(self):
        p=load('regression');out=ctrl.evaluate(p)
        self.assertEqual(len(out['memory_capsule']),1)
        self.assertTrue(out['memory_capsule'][0]['not_persisted'])
        self.assertEqual(out['memory_capsule'][0]['provenance'],'test-candidate-v1')
        p['candidates'][0]['lessons']=['x'*181]
        with self.assertRaises(ValueError):ctrl.evaluate(p)

    def test_skill_files_and_docs(self):
        for skill in ['adaptive-verification-loop','counterexample-discovery-loop','parallel-hypothesis-loop','holdout-prompt-optimization-loop','regression-reflection-loop']:
            text=(ROOT/'skills'/skill/'SKILL.md').read_text()
            self.assertTrue(text.startswith('---\n'))
            self.assertIn('## Operational procedure',text)
            self.assertIn('external',text.lower())
        self.assertTrue((ROOT/'docs/LOOP-ENGINEERING.md').is_file())

if __name__=='__main__':unittest.main()
