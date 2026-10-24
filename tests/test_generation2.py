import importlib.util,json,subprocess,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
import media_ingest,mcp_server,skill_eval
class Generation2(unittest.TestCase):
 def test_mcp_discovery_and_route(self):
  def req(method,params=None):return mcp_server.respond({'jsonrpc':'2.0','id':1,'method':method,'params':params or {}})
  self.assertEqual(req('initialize')['result']['serverInfo']['version'],'2.0.0')
  self.assertEqual(len(req('tools/list')['result']['tools']),3)
  out=req('tools/call',{'name':'route_task','arguments':{'query':'debate-intelligence'}})
  data=json.loads(out['result']['content'][0]['text'])
  self.assertEqual(data['recommendations'][0]['skill'],'debate-intelligence')
 def test_mcp_blocks_unknown_argument_and_tool(self):
  with self.assertRaises(ValueError):mcp_server.call('validate',{'root':'/etc'})
  with self.assertRaises(ValueError):mcp_server.call('shell',{'command':'ls'})
  self.assertIsNone(mcp_server.respond({'jsonrpc':'2.0','method':'notifications/initialized'}))
 def test_mcp_transport_is_json_only(self):
  result=subprocess.run([sys.executable,str(ROOT/'tools/mcp_server.py')],input='bad\n'+json.dumps({'jsonrpc':'2.0','id':2,'method':'ping'})+'\n',capture_output=True,text=True,check=True)
  rows=[json.loads(x) for x in result.stdout.splitlines()]
  self.assertEqual(rows[0]['error']['code'],-32700);self.assertEqual(rows[1]['result'],{})
 def test_each_skill_has_behavior_spec_not_claimed_pass(self):
  rows=json.loads((ROOT/'benchmarks/skill-golden-specs.json').read_text())['cases']
  self.assertEqual({x['skill'] for x in rows},{p.parent.name for p in (ROOT/'skills').glob('*/SKILL.md')})
  self.assertTrue(all(x['input'] and x['expected_behavior'] and x['negative_trap'] and x['model_run'] is False for x in rows))
 def test_media_preflight_rejects_missing_or_existing_output(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'source.mp4';p.write_bytes(b'not real')
   with self.assertRaises(ValueError):media_ingest.prepare(p,Path(d),interval=5)
   with self.assertRaises(ValueError):media_ingest.prepare(p,Path(d)/'new',interval=float('nan'))
 def test_eval_rejects_unpaired_and_mislabelled_ablation(self):
  with self.assertRaises(ValueError):skill_eval.assess({'provenance':'observed','skill':'a','pairs':[]})
  row={'task_id':'x','split':'holdout','model':'m','settings_hash':'s','tools_hash':'t','input_hash':'i','judge_version':'j','baseline_skills':[],'candidate_skills':['wrong']}
  with self.assertRaises(ValueError):skill_eval.assess({'provenance':'observed','skill':'a','pairs':[row]})
 def test_lower_latency_is_improvement(self):
  from paired_stats import paired_summary
  out=paired_summary([100]*20,[80]*20,higher_is_better=False)
  self.assertTrue(out['improvement_supported']);self.assertLess(out['mean_delta'],0)
 def test_eval_rejects_nonobject_row(self):
  with self.assertRaises(ValueError):skill_eval.assess({'provenance':'observed','skill':'a','pairs':[None]})
 def test_mcp_invalid_params_preserves_id(self):
  r=mcp_server.respond({'jsonrpc':'2.0','id':42,'method':'tools/call','params':[]})
  self.assertEqual(r['id'],42);self.assertEqual(r['error']['code'],-32602)
 def test_eval_fixture_never_promotes(self):
  rows=[]
  for i in range(20):
   rows.append({'task_id':str(i),'split':'holdout','model':'m','settings_hash':'s','tools_hash':'t','input_hash':'i'+str(i),'judge_version':'j','baseline_skills':[],'candidate_skills':['a'],'baseline':{'score':0,'tokens':20,'latency_ms':2,'critical_failure':False},'candidate':{'score':1,'tokens':10,'latency_ms':1,'critical_failure':False}})
  out=skill_eval.assess({'provenance':'fixture','skill':'a','pairs':rows})
  self.assertTrue(out['quality']['improvement_supported']);self.assertFalse(out['eligible_for_review']);self.assertFalse(out['auto_promoted'])
  rows[0]['candidate']['tokens']=1000000
  over=skill_eval.assess({'provenance':'observed','skill':'a','pairs':rows})
  self.assertFalse(over['budgets_pass']);self.assertFalse(over['eligible_for_review']);self.assertIn('latency_delta',over)
if __name__=='__main__':unittest.main()
