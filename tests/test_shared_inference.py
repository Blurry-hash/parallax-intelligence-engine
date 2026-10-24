import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from paired_stats import paired_summary
from dag import topological_layers
import quality_gate
import evolve_gate
import perf_gate

class SharedInference(unittest.TestCase):
    def test_small_sample_cannot_support_improvement(self):
        self.assertFalse(paired_summary([0]*5,[1]*5)['improvement_supported'])
    def test_clear_gain_and_deterministic_interval(self):
        result=paired_summary([0]*20,[1]*20)
        self.assertTrue(result['improvement_supported'])
        self.assertEqual(result['mean_delta_bootstrap_ci'],[1,1])
        self.assertEqual(result,paired_summary([0]*20,[1]*20))
    def test_ties_are_not_significant(self):
        result=paired_summary([1]*20,[1]*20)
        self.assertEqual(result['p_value'],1)
        self.assertFalse(result['improvement_supported'])
    def test_input_rejection(self):
        for b,c in [([],[]),([1],[1,2]),([float('nan')],[1]),([True],[1])]:
            with self.assertRaises(ValueError): paired_summary(b,c)
    def test_quality_requires_sufficient_untuned_holdouts(self):
        data={'provenance':'observed','minimum_improvement':.05,'cases':[
            {'name':str(i),'split':'holdout','baseline':.5,'candidate':.6,'critical':True} for i in range(20)]}
        self.assertEqual(quality_gate.assess(data)['decision'],'PROMOTE_CANDIDATE')
        data['cases'][0]['candidate']=.49
        self.assertEqual(quality_gate.assess(data)['decision'],'REJECT_CANDIDATE')
    def test_no_quality_gain_cannot_promote(self):
        data={'provenance':'observed','minimum_improvement':0,'cases':[
            {'name':str(i),'split':'holdout','baseline':.5,'candidate':.5,'critical':False} for i in range(20)]}
        self.assertEqual(quality_gate.assess(data)['decision'],'REJECT_CANDIDATE')
    def test_performance_minimum_shared_policy(self):
        data={'cases':[{'id':str(i),'baseline':{'correct':True,'latency_ms':100},
                       'candidate':{'correct':True,'latency_ms':80}} for i in range(20)]}
        result=perf_gate.compare(data)
        self.assertTrue(result['accepted'])
        self.assertLess(result['latency_inference']['mean_delta_bootstrap_ci'][1],0)
    def test_dag_contract(self):
        self.assertEqual(topological_layers({'first-task':[],'next':['first-task']}),[['first-task'],['next']])
        for g in [{'a':['b'],'b':['a']},{'a':['missing']},{'Bad':[]},{'a':['a']}]:
            with self.assertRaises(ValueError):topological_layers(g)
