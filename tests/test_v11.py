"""V11 PARALLAX offline regressions; do not require model or media rendering."""
import importlib.util,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(path):
    spec=importlib.util.spec_from_file_location('v11_'+path.replace('.','_'),ROOT/'tools'/path)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
image=load('image_contract.py');wf=load('workflow_risk_audit.py');style=load('response_style_lint.py');cats=load('capability_catalog.py')
class V11Tests(unittest.TestCase):
    def test_150_catalog(self):
        rows=json.loads((ROOT/'catalog/150-capability-contracts.json').read_text(encoding='utf-8'))['capabilities']
        self.assertEqual(len(rows),150);self.assertEqual(len(set(x['slug'] for x in rows)),150)
        self.assertTrue(all((ROOT/x['integration_target']).exists() and x['status']=='documented-protocol' for x in rows))
    def test_130_skill_extensions(self):
        paths=list((ROOT/'skills').glob('*/SKILL.md'));self.assertEqual(len(paths),142)
        applied=[p for p in paths if '## v11.0 — Three targeted extensions' in p.read_text(encoding='utf-8')]
        self.assertEqual(len(applied),130)
        self.assertTrue(all('3. **Lean evidence and fallback:**' in p.read_text(encoding='utf-8') for p in applied))
    def test_no_render_for_text(self):
        obj=json.loads((ROOT/'examples/image-intent-v11.json').read_text(encoding='utf-8'));self.assertFalse(image.validate(obj)['render_required'])
        obj['render_required']=True
        with self.assertRaises(image.ContractError):image.validate(obj)
    def test_identity_conflicts(self):
        with self.assertRaises(image.ContractError):image.validate({'mode':'generate','requested_output':'portrait','locked':['face'],'editable':['FACE']})
    def test_generating_cannot_lock_pixels(self):
        with self.assertRaises(image.ContractError):image.validate({'mode':'generate','requested_output':'portrait','pixel_exact':True})
    def test_edit_requires_reference(self):
        with self.assertRaises(image.ContractError):image.validate({'mode':'edit','requested_output':'change background'})
    def test_workflow_audit_never_runs(self):
        data=json.loads((ROOT/'examples/automation-audit-v11.json').read_text(encoding='utf-8'))
        self.assertFalse(wf.audit(data)['executed'])
        self.assertTrue(wf.audit({'nodes':[{'name':'script','type':'n8n-nodes-base.executeCommand'}]})['requires_review'])
    def test_bad_workflow_rejected(self):
        with self.assertRaises(wf.WorkflowError):wf.audit({'nodes':{}})
    def test_natural_output(self):
        self.assertFalse(style.check('[ESTABLISHED] done')['passes'])
        self.assertTrue(style.check('I checked the code. The output is correct.')['passes'])
        self.assertTrue(style.check('[APPROVED] requested',True)['passes'])
    def test_search(self):
        self.assertTrue(cats.search('image'))
        with self.assertRaises(ValueError):cats.search(' ')
    def test_tiktok_provenance(self):
        d=json.loads((ROOT/'sources/tiktok-sourced-v11.json').read_text(encoding='utf-8'))
        self.assertEqual(len(d['entries']),5)
        self.assertTrue(all('tiktok.com' in x['post_url'] and 'github.com' in x['repo'] for x in d['entries']))
