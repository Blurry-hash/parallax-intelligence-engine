"""Differential, adversarial, deterministic regressions for PARALLAX v10.4."""
from __future__ import annotations
import copy, json, sys, tempfile, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'tools'))
import resource_scheduler, quality_gate, skill_dispatch, artifact_proof, mission_review, plan_engine
PLAN=json.loads((ROOT/'examples/planning-v10.3.json').read_text(encoding='utf8'))

def minimal_plan():
    p=copy.deepcopy(PLAN);p['requested_minutes']=80;p['max_workers']=2
    p['tasks']=[p['tasks'][0],p['tasks'][1],p['tasks'][2],p['tasks'][3]]
    return p

def metric():
    return {'provenance':'observed','minimum_improvement':0.02,'cases':[
      {'name':'code','split':'development','baseline':0.6,'candidate':0.8,'critical':True},
      {'name':'research','split':'holdout','baseline':0.7,'candidate':0.72,'critical':True}]}

class Scheduling(unittest.TestCase):
    def test_deterministic(self):self.assertEqual(resource_scheduler.schedule(minimal_plan()),resource_scheduler.schedule(minimal_plan()))
    def test_approvals_block_deps(self):
        p=copy.deepcopy(PLAN);x=resource_scheduler.schedule(p)
        self.assertEqual(x['blocked'],['publish_release']);self.assertTrue(resource_scheduler.check_schedule(p,x))
        self.assertNotIn('publish_release',[x['id'] for x in x['scheduled']])
    def test_explicit_approval_schedules(self):
        p=copy.deepcopy(PLAN);x=resource_scheduler.schedule(p,approvals=['publish_release'])
        self.assertFalse(x['blocked']);self.assertEqual(len(x['scheduled']),6)
        self.assertTrue(resource_scheduler.check_schedule(p,x,approvals=['publish_release']))
    def test_approval_does_not_fake_authority(self):
        self.assertIn('external authorization',resource_scheduler.schedule(PLAN,approvals=['publish_release'])['note'])
    def test_unknown_approval_rejected(self):
        with self.assertRaisesRegex(ValueError,'unknown'):resource_scheduler.schedule(PLAN,approvals=['not_a_task'])
    def test_worker_parallelism_changes_makespan(self):
        p=minimal_plan();p['max_workers']=1;single=resource_scheduler.schedule(p)['estimated_makespan_minutes']
        p['max_workers']=2;parallel=resource_scheduler.schedule(p)['estimated_makespan_minutes']
        self.assertLess(parallel,single)
    def test_independent_verifier_rejects_overlap(self):
        p=minimal_plan();s=resource_scheduler.schedule(p);s['scheduled'][-1]['worker']=s['scheduled'][0]['worker']
        s['scheduled'][-1]['start_minute']=0
        with self.assertRaises(ValueError):resource_scheduler.check_schedule(p,s)
    def test_deadline_flagged(self):
        p=minimal_plan();p['requested_minutes']=5
        self.assertFalse(resource_scheduler.schedule(p)['within_requested_budget'])
    def test_bogus_approval_type(self):
        with self.assertRaises(ValueError):resource_scheduler.schedule(PLAN,approvals=['not_a_task'])

class Integrity(unittest.TestCase):
    def setUp(self):self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name);(self.root/'result.txt').write_text('original')
    def test_roundtrip(self):
        m=artifact_proof.manifest(self.root,['result.txt']);self.assertEqual(artifact_proof.verify(self.root,m)['verified_files'],1)
    def test_tampering_rejected(self):
        m=artifact_proof.manifest(self.root,['result.txt']);(self.root/'result.txt').write_text('replaced')
        with self.assertRaisesRegex(ValueError,'mismatch'):artifact_proof.verify(self.root,m)
    def test_traversal_rejected(self):
        for n in ('../parent','/etc/passwd','folder/../result.txt','C:secret','result.txt\\bad'):
            with self.subTest(name=n), self.assertRaises(ValueError):artifact_proof.manifest(self.root,[n])
    def test_symlink_rejected(self):
        (self.root/'linked').symlink_to(self.root/'result.txt')
        with self.assertRaisesRegex(ValueError,'symlink'):artifact_proof.manifest(self.root,['linked'])
    def test_symlink_parent_rejected(self):
        (self.root/'folder').symlink_to(self.root,target_is_directory=True)
        with self.assertRaisesRegex(ValueError,'symlink'):artifact_proof.manifest(self.root,['folder/result.txt'])
    def test_duplicate_rejected(self):
        with self.assertRaisesRegex(ValueError,'duplicate'):artifact_proof.manifest(self.root,['result.txt','result.txt'])
    def test_boolean_size_rejected(self):
        m=artifact_proof.manifest(self.root,['result.txt']);m['artifacts']['result.txt']['bytes']=True
        with self.assertRaises(ValueError):artifact_proof.verify(self.root,m)
    def test_bad_hash_rejected(self):
        m=artifact_proof.manifest(self.root,['result.txt']);m['artifacts']['result.txt']['sha256']='hello'
        with self.assertRaises(ValueError):artifact_proof.verify(self.root,m)

class Quality(unittest.TestCase):
    def test_tiny_observed_sample_cannot_promote(self):self.assertEqual(quality_gate.assess(metric())['decision'],'REJECT_CANDIDATE')
    def test_fixture_not_real(self):
        m=metric();m['provenance']='fixture'
        self.assertEqual(quality_gate.assess(m)['decision'],'FIXTURE_ONLY')
    def test_aggregate_cannot_mask_regression(self):
        m=metric();m['cases'][0]['candidate']=1;m['cases'][1]['candidate']=0.69
        self.assertFalse(quality_gate.assess(m)['candidate_passes_numeric_gates'])
    def test_critical_regression_rejected(self):
        m=metric();m['cases'][0]['candidate']=0.59;m['cases'][1]['candidate']=1
        self.assertIn('code',quality_gate.assess(m)['regressed_cases'])
    def test_no_holdout_rejected(self):
        m=metric();m['cases'][1]['split']='development'
        with self.assertRaisesRegex(ValueError,'holdout'):quality_gate.assess(m)
    def test_nan_and_bool_rejected(self):
        for val in (float('nan'),float('inf'),True,None):
            m=metric();m['cases'][0]['candidate']=val
            with self.subTest(val=val),self.assertRaises(ValueError):quality_gate.assess(m)
    def test_duplicate_case_rejected(self):
        m=metric();m['cases'][1]['name']='code'
        with self.assertRaisesRegex(ValueError,'duplicate'):quality_gate.assess(m)
    def test_missing_threshold_rejected(self):
        m=metric();m.pop('minimum_improvement')
        with self.assertRaises(ValueError):quality_gate.assess(m)

class Routing(unittest.TestCase):
    def test_image_route(self):
        names=[x['skill'] for x in skill_dispatch.choose('image generation preserve composition',ROOT)['selected']]
        self.assertIn('image-generation',names)
    def test_coding_route(self):
        names=[x['skill'] for x in skill_dispatch.choose('code debugging',ROOT)['selected']]
        self.assertIn('coding-engineering',names)
    def test_small_context_budget(self):
        r=skill_dispatch.choose('research source quality',ROOT,max_chars=2000)
        self.assertLessEqual(r['chars_used'],2000)
        self.assertLessEqual(len(r['selected']),3)
    def test_no_false_execution(self):self.assertIn('no embeddings',skill_dispatch.choose('planning',ROOT)['method'])
    def test_bad_inputs(self):
        for q in ('',123,'x'*2001):
            with self.subTest(q=q),self.assertRaises(ValueError):skill_dispatch.choose(q,ROOT)
    def test_out_of_bounds(self):
        for budget in (0,999,30001,True):
            with self.subTest(budget=budget),self.assertRaises(ValueError):skill_dispatch.choose('audio',ROOT,max_chars=budget)

class Integration(unittest.TestCase):
    def test_fail_closed_without_proof(self):
        r=mission_review.review(minimal_plan(),root=ROOT)
        self.assertEqual(r['status'],'BLOCKED');self.assertIn('no content manifest supplied',r['findings'])
    def test_invalid_metrics_blocked(self):
        r=mission_review.review(minimal_plan(),root=ROOT,metrics={'bad':'data'})
        self.assertTrue(any('benchmark invalid' in f for f in r['findings']))
    def test_no_false_approval(self):
        r=mission_review.review(PLAN,root=ROOT)
        self.assertTrue(any('approval gates' in f for f in r['findings']))

if __name__=='__main__':unittest.main()
