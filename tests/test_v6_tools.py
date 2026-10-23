"""Executable security and correctness cases for PARALLAX v6 offline helpers."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def load(name):
    spec=importlib.util.spec_from_file_location(name,ROOT/'tools'/f'{name}.py')
    mod=importlib.util.module_from_spec(spec)
    # Avoid forward-ref dataclass setup; modules intentionally do not execute on import.
    spec.loader.exec_module(mod)
    return mod

route=load('route_task')
cap=load('capability_audit')
bench=load('bench_compare')
source=load('source_audit')

class RouteTests(unittest.TestCase):
    def test_multidomain_routing(self):
        results=route.candidates('Build an accessible UI and API dashboard',limit=4)
        self.assertIn('interface-design',[x['skill'] for x in results])
        self.assertIn('api-contract-engineering',[x['skill'] for x in results])
    def test_empty_and_non_matching(self):
        self.assertEqual(route.candidates(''),[])
        self.assertEqual(route.candidates('saffron'),[])
    def test_word_boundary(self):
        self.assertNotIn('video-intelligence',[x['skill'] for x in route.candidates('videoscope')])
    def test_input_limits(self):
        with self.assertRaises(ValueError):route.candidates('a'*10001)
        with self.assertRaises(ValueError):route.candidates('valid',limit=11)
    def test_no_phantom_skill(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(route.candidates('UI',root=Path(d)),[])

class CapabilityTests(unittest.TestCase):
    def test_does_not_assume_unauthorized_tools(self):
        result=cap.inspect(('ffmpeg','gh'),which=lambda x: '/bin/'+x if x=='ffmpeg' else None)
        self.assertTrue(result['local_executables']['ffmpeg'])
        self.assertFalse(result['local_executables']['gh'])
        self.assertFalse(result['private_data_upload_authorized'])
        self.assertFalse(result['consequential_writes_authorized'])
        self.assertIn('unknown',result['browser_automation'])

class BenchTests(unittest.TestCase):
    def setUp(self):
        self.rows=json.loads((ROOT/'examples/paired-evaluation.json').read_text())
    def test_paired_accuracy_vs_latency(self):
        r=bench.compare(self.rows)
        self.assertEqual(r['n_paired'],3)
        self.assertEqual(r['baseline_only_correct'],1)
        self.assertEqual(r['candidate_only_correct'],1)
        self.assertEqual(r['accuracy_delta_pp'],0.0)
        self.assertLess(r['candidate_p95_ms'],r['baseline_p95_ms'])
    def test_percentile_single(self):
        self.assertEqual(bench.percentile([123],.95),123)
    def test_duplicate_ids_rejected(self):
        with self.assertRaises(ValueError):bench.compare(self.rows+[self.rows[0]])
    def test_no_fabricated_benchmark(self):
        with self.assertRaises(ValueError):bench.compare([])
    def test_nan_and_zero_rejected(self):
        for v in (float('nan'),float('inf'),0,-1,True,'5'):
            with self.subTest(value=v):
                row=dict(self.rows[0],baseline_ms=v)
                with self.assertRaises(ValueError):bench.compare([row])
    def test_strict_bools(self):
        row=dict(self.rows[0],baseline_correct=1)
        with self.assertRaises(ValueError):bench.compare([row])

class SkillTests(unittest.TestCase):
    def test_25_new_specialties_present(self):
        found=set(p.parent.name for p in (ROOT/'skills').glob('*/SKILL.md'))
        self.assertGreaterEqual(len(found),56)
        for important in ('capability-contract','skill-supply-chain','interface-design',
                          'accessibility-assurance','privacy-by-design','causal-inference',
                          'multimodal-fusion','durable-automation','root-cause-debugging',
                          'retrieval-quality','scientific-computation','structured-output-reliability'):
            self.assertIn(important,found)
    def test_all_new_skills_are_self_contained(self):
        for key in ('capability-contract','interface-design','database-reliability','skill-supply-chain'):
            body=(ROOT/'skills'/key/'SKILL.md').read_text()
            self.assertIn('## Activation',body)
            self.assertIn('## Operational procedure',body)
            self.assertIn('## Failure handling',body)
            self.assertIn('**Check:**',body)
    def test_source_attestations_not_exaggerated(self):
        registry=json.loads((ROOT/'sources'/'sources.json').read_text())
        s=source.summary(registry)
        self.assertGreaterEqual(s['total'],100)
        self.assertGreater(s['unchecked'],0)
        self.assertEqual(s['missing_required_caveats'],[])

if __name__=='__main__':unittest.main()
