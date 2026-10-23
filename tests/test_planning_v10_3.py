"""Offline plan, evidence and independent worker smoke and negative tests."""
import copy,json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
import plan_engine,agent_audit,goal_trace
BASE=json.loads((ROOT/'examples/planning-v10.3.json').read_text(encoding='utf-8'))
class PlanningTests(unittest.TestCase):
    def test_valid(self):
        a=plan_engine.compile_plan(BASE)
        self.assertEqual(a['task_count'],5)
        self.assertEqual(a['status'],'ADVISORY_ONLY_NOT_EXECUTED')
        self.assertEqual(a,plan_engine.compile_plan(copy.deepcopy(BASE)))
    def test_cycles(self):
        x=copy.deepcopy(BASE);x['tasks'][0]['depends_on']=['publish']
        with self.assertRaisesRegex(ValueError,'cycle'):plan_engine.compile_plan(x)
    def test_unknown(self):
        x=copy.deepcopy(BASE);x['tasks'][0]['depends_on']=['ghost']
        with self.assertRaisesRegex(ValueError,'unknown'):plan_engine.compile_plan(x)
    def test_unapproved_delivery(self):
        x=copy.deepcopy(BASE);x['tasks'][-1]['approval_required']=False
        with self.assertRaisesRegex(ValueError,'approval'):plan_engine.compile_plan(x)
    def test_nan(self):
        x=copy.deepcopy(BASE);x['tasks'][0]['estimated_minutes']=float('nan')
        with self.assertRaises(ValueError):plan_engine.compile_plan(x)
    def test_no_arbitrary_commands(self):
        x=copy.deepcopy(BASE);x['tasks'][0]['command']='curl'
        with self.assertRaises(ValueError):plan_engine.compile_plan(x)
    def test_verified_requires_evidence(self):
        h=plan_engine.compile_plan(BASE)['plan_sha256']
        tasks=[{'id':t['id'],'state':'verified','approved':t['approval_required'],'evidence':['Verified test evidence item']} for t in BASE['tasks']]
        self.assertTrue(goal_trace.audit_ledger(BASE,{'plan_sha256':h,'tasks':tasks})['complete'])
        tasks[0]['evidence']=[]
        with self.assertRaisesRegex(ValueError,'evidence'):goal_trace.audit_ledger(BASE,{'plan_sha256':h,'tasks':tasks})
    def test_four_workers(self):
        r=agent_audit.run_audits(BASE,ROOT)
        self.assertTrue(r['pass'])
        self.assertEqual(r['worker_count'],4)
if __name__=='__main__':unittest.main()
