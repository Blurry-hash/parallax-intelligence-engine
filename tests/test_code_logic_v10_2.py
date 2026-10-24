"""Deliberate negative tests for new logic/performance tools."""
import ast
import importlib.util
import json
import math
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def load(name):
    p=ROOT/'tools'/f'{name}.py'
    spec=importlib.util.spec_from_file_location(name,p)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

class LogicToolsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dag=load('critical_path');cls.perf=load('perf_gate');cls.ast=load('complexity_guard')

    def test_critical_path_reference(self):
        v=self.dag.schedule(json.loads((ROOT/'examples/workflow-dag.json').read_text()))
        self.assertEqual(v['estimated_critical_path'],20)
        self.assertEqual(v['total_serial_work'],23)
        self.assertEqual(v['parallel_frontiers'][0],['inspect'])
        self.assertIn('review',v['critical_tasks'])

    def test_task_graph_order_independent(self):
        a=json.loads((ROOT/'examples/workflow-dag.json').read_text())
        b={'tasks':list(reversed(a['tasks']))}
        self.assertEqual(self.dag.schedule(a)['estimated_critical_path'],self.dag.schedule(b)['estimated_critical_path'])

    def test_missing_dependency(self):
        with self.assertRaisesRegex(ValueError,'unknown dependency'):
            self.dag.schedule({'tasks':[{'id':'a','duration':1,'depends_on':['z']}]})

    def test_cycle(self):
        with self.assertRaisesRegex(ValueError,'cycle'):
            self.dag.schedule({'tasks':[{'id':'a','duration':1,'depends_on':['b']},{'id':'b','duration':1,'depends_on':['a']}]})

    def test_duplicate_task(self):
        with self.assertRaisesRegex(ValueError,'duplicate task'):
            self.dag.schedule({'tasks':[{'id':'a','duration':1},{'id':'a','duration':2}]})

    def test_invalid_duration(self):
        for d in (-1,0,float('nan'),True):
            with self.subTest(d=d),self.assertRaises(ValueError):
                self.dag.schedule({'tasks':[{'id':'x','duration':d}]})

    def test_parallel_frontiers(self):
        v=self.dag.schedule({'tasks':[{'id':'a','duration':2},{'id':'b','duration':3},{'id':'c','duration':1,'depends_on':['a','b']}]})
        self.assertEqual(v['parallel_frontiers'],[['a','b'],['c']])
        self.assertEqual(v['estimated_critical_path'],4)

    def test_perf_fixture(self):
        out=self.perf.compare(json.loads((ROOT/'examples/perf-pairs.json').read_text()))
        self.assertFalse(out['accepted'])
        self.assertTrue(out['numeric_gates_pass'])
        self.assertFalse(out['latency_inference']['sample_sufficient'])
        self.assertEqual(out['sample_count'],5)

    def test_correctness_regression_reject(self):
        obj=json.loads((ROOT/'examples/perf-pairs.json').read_text())
        obj['cases'][2]['candidate']['correct']=False
        self.assertFalse(self.perf.compare(obj)['accepted'])
        self.assertEqual(self.perf.compare(obj)['reason'],'correctness regression')

    def test_tail_regression_reject(self):
        obj=json.loads((ROOT/'examples/perf-pairs.json').read_text())
        obj['cases'][-1]['candidate']['latency_ms']=700
        self.assertFalse(self.perf.compare(obj)['accepted'])

    def test_perf_duplicate_reject(self):
        obj=json.loads((ROOT/'examples/perf-pairs.json').read_text())
        obj['cases'][1]['id']=obj['cases'][0]['id']
        with self.assertRaises(ValueError):self.perf.compare(obj)

    def test_nonfinite_latency_reject(self):
        obj=json.loads((ROOT/'examples/perf-pairs.json').read_text())
        for invalid in (0,-1,float('inf'),float('nan'),True):
            obj['cases'][0]['candidate']['latency_ms']=invalid
            with self.subTest(invalid=invalid),self.assertRaises(ValueError):self.perf.compare(obj)

    def test_ast_heuristic(self):
        simple='def f(x):\n    return x+1\n'
        nested='def f(x):\n    for n in x:\n        if n > 0 and n != 2:\n            pass\n'
        self.assertGreater(self.ast.function_metrics(nested)[0]['score'],self.ast.function_metrics(simple)[0]['score'])

    def test_ast_does_not_double_count_nested_functions(self):
        nested='def outer():\n    def inner():\n        if 1: pass\n    return 1\n'
        scores={x['function']:x['score'] for x in self.ast.function_metrics(nested)}
        self.assertEqual(scores['outer'],1)
        self.assertGreater(scores['inner'],1)

    def test_ast_invalid_code(self):
        with self.assertRaises(SyntaxError):self.ast.function_metrics('def foo(: pass')

    def test_all_new_skills_have_checks(self):
        for name in ('formal-invariants','cache-invalidation-design','video-encoding-efficiency','property-based-testing-lab'):
            x=(ROOT/'skills'/name/'SKILL.md').read_text()
            self.assertIn('**Check:**',x)
            self.assertIn('## Operational procedure',x)

if __name__=='__main__':unittest.main()
