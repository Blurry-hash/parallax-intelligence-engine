"""Tests: no fake duration, no arbitrary execution, failed steps and truthful reporting."""
import importlib.util
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('parallax_work_budget', ROOT/'tools/work_budget.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def plan(minutes=50, action='validate'):
    return {'requested_minutes': minutes, 'work_items':[{'id':'review','action':action,'purpose':'Run an explicitly authorized validation for quality.'}]}


class Clock:
    def __init__(self): self.n = 100.0
    def __call__(self): return self.n
    def increment(self, delta): self.n += delta


class TimeBudgetTests(unittest.TestCase):
    def test_valid_spec(self):
        self.assertEqual(mod.parse_plan(plan())[0],50)
        self.assertEqual(mod.parse_plan(plan())[1][0]['action'],'validate')

    def test_invalid_time(self):
        for val in (0,-1,1441,float('nan'),float('inf'),True,'50'):
            with self.subTest(val=val),self.assertRaises(ValueError):mod.parse_plan(plan(val))

    def test_unknown_command_rejected(self):
        for val in ('shell','curl','../../evil.py',['validate'],None):
            with self.subTest(val=val),self.assertRaises(ValueError):mod.parse_plan(plan(action=val))

    def test_duplicate_ids(self):
        x=plan();x['work_items'].append(x['work_items'][0])
        with self.assertRaisesRegex(ValueError,'duplicate'):mod.parse_plan(x)

    def test_invalid_purpose(self):
        x=plan();x['work_items'][0]['purpose']='bad'
        with self.assertRaisesRegex(ValueError,'purpose'):mod.parse_plan(x)

    def test_invalid_id(self):
        x=plan();x['work_items'][0]['id']='../../a'
        with self.assertRaisesRegex(ValueError,'id'):mod.parse_plan(x)

    def test_more_than_hundred_items(self):
        x=plan();x['work_items']=[{'id':str(i),'action':'validate','purpose':'Meaningful offline structural inspection'} for i in range(101)]
        with self.assertRaises(ValueError):mod.parse_plan(x)

    def test_short_work_does_not_fake_minutes(self):
        clock=Clock()
        def good(*a,**kw):
            clock.increment(.4)
            return SimpleNamespace(returncode=0,stdout='PASS',stderr='')
        r=mod.run_plan(plan(50),clock=clock,runner=good)
        self.assertEqual(r['status'],'work_exhausted')
        self.assertAlmostEqual(r['actual_wall_seconds'],.4,places=5)
        self.assertLess(r['actual_wall_seconds'],3000)
        self.assertEqual(r['steps'][0]['status'],'passed')

    def test_failed_step_stops(self):
        clock=Clock()
        def bad(*a,**kw):
            clock.increment(.25)
            return SimpleNamespace(returncode=1,stdout='',stderr='failure')
        x=plan();x['work_items'].append({'id':'next','action':'unit_tests','purpose':'Inspect all regression tests for failures'})
        r=mod.run_plan(x,clock=clock,runner=bad)
        self.assertEqual(r['status'],'failed')
        self.assertEqual(len(r['steps']),1)

    def test_expired_budget_skips_remaining(self):
        clock=Clock()
        def slow(*a,**kw):
            clock.increment(2.1)
            return SimpleNamespace(returncode=0,stdout='',stderr='')
        x=plan(0.03)
        x['work_items'].append({'id':'next','action':'unit_tests','purpose':'Analyze nontrivial edge cases in regression tests'})
        r=mod.run_plan(x,clock=clock,runner=slow)
        self.assertEqual(r['status'],'budget_exhausted')
        self.assertEqual(len(r['steps']),1)

    def test_checkpoint_written(self):
        clock=Clock()
        def good(*a,**kw):
            clock.increment(.1)
            return SimpleNamespace(returncode=0,stdout='PASS',stderr='')
        with tempfile.TemporaryDirectory() as tmp:
            output=Path(tmp)/'ledger.json'
            r=mod.run_plan(plan(10),clock=clock,runner=good,output=output)
            self.assertTrue(output.exists())
            self.assertEqual(__import__('json').loads(output.read_text())['status'],r['status'])

if __name__=='__main__':unittest.main()
