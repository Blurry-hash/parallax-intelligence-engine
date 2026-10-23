"""Regression cases for repository refresh, DeepSeek GET scope, and visual contract."""
import datetime as dt
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock

ROOT = Path(__file__).resolve().parents[1]
def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT/'tools'/f'{name}.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod
freshness=load('freshness_gate')
probe=load('deepseek_get_probe')
design=load('design_contract')
SHA1='a'*40
SHA2='b'*40

class RefreshTests(unittest.TestCase):
    def setUp(self):
        self.t=tempfile.TemporaryDirectory();self.addCleanup(self.t.cleanup)
        self.state=Path(self.t.name)/'nested'/'state.json'
        self.now=dt.datetime(2026,10,23,tzinfo=dt.timezone.utc)
    def test_first_fetch_and_change(self):
        out=freshness.inspect('a/b',self.state,now=self.now,fetcher=lambda u:{'sha':SHA1})
        self.assertEqual(out['status'],'changed')
        second=freshness.inspect('a/b',self.state,now=self.now+dt.timedelta(hours=25),fetcher=lambda u:{'sha':SHA2})
        self.assertEqual(second['status'],'changed')
    def test_unmodified_sha(self):
        freshness.inspect('a/b',self.state,now=self.now,fetcher=lambda u:{'sha':SHA1})
        out=freshness.inspect('a/b',self.state,now=self.now+dt.timedelta(hours=25),fetcher=lambda u:{'sha':SHA1})
        self.assertEqual(out['status'],'unchanged')
    def test_cache_avoids_calls(self):
        freshness.inspect('a/b',self.state,now=self.now,fetcher=lambda u:{'sha':SHA1})
        m=Mock(side_effect=AssertionError('should not fetch'))
        out=freshness.inspect('a/b',self.state,now=self.now+dt.timedelta(hours=2),fetcher=m)
        self.assertEqual(out['status'],'cached');m.assert_not_called()
    def test_force_bypasses_cache(self):
        freshness.inspect('a/b',self.state,now=self.now,fetcher=lambda u:{'sha':SHA1})
        out=freshness.inspect('a/b',self.state,now=self.now,force=True,fetcher=lambda u:{'sha':SHA2})
        self.assertEqual(out['sha'],SHA2)
    def test_network_failure_does_not_corrupt_checkpoint(self):
        freshness.inspect('a/b',self.state,now=self.now,fetcher=lambda u:{'sha':SHA1})
        bad=freshness.inspect('a/b',self.state,now=self.now,force=True,fetcher=lambda u:1/0)
        self.assertEqual(bad['status'],'unverified')
        self.assertEqual(json.loads(self.state.read_text())['sha'],SHA1)
    def test_bad_repo_and_ttl(self):
        for name in ('https://evil.com','a/b/c','a/b?token=1','../etc'):
            with self.subTest(name=name),self.assertRaises(ValueError):freshness.inspect(name,self.state)
        with self.assertRaises(ValueError):freshness.inspect('a/b',self.state,ttl_hours=-1)
    def test_bad_sha_is_not_saved(self):
        out=freshness.inspect('a/b',self.state,now=self.now,fetcher=lambda u:{'sha':'not_sha'})
        self.assertEqual(out['status'],'unverified');self.assertFalse(self.state.exists())

class DeepSeekTests(unittest.TestCase):
    def test_math_url(self):self.assertEqual(probe.url_for('7*6'),'https://api.mathjs.org/v4/?expr=7%2A6')
    def test_simulated_get_distinct_from_live(self):
        out=probe.probe('7*6',fetcher=lambda url:'42')
        self.assertEqual(out['response'],'42');self.assertIn('not a Python',out['warning'])
    def test_network_failure_no_fake_pass(self):
        out=probe.probe('7*6',fetcher=lambda url: (_ for _ in ()).throw(OSError('blocked')))
        self.assertEqual(out['status'],'blocked');self.assertNotIn('response',out)
    def test_reject_code_and_tokens(self):
        bad=['import os','print(1)','process.exit(0)','1;2','https://foo','api_key=abc','x=1','2**3','2//3','', '9'*100]
        for val in bad:
            with self.subTest(val=val),self.assertRaises(ValueError):probe.url_for(val)

class DesignTests(unittest.TestCase):
    def test_example(self):
        c=json.loads((ROOT/'examples/design-contract-v10.5.json').read_text());self.assertEqual(design.check_contract(c),[])
    def test_bad_colors(self):
        self.assertTrue(design.check_contract({'colors':{'text':'#fffff'},'contrast_pairs':[{'foreground':'text','background':'text'}]}))
    def test_low_contrast(self):
        c={'colors':{'text':'#cccccc','surface':'#cccccd'},'contrast_pairs':[{'foreground':'text','background':'surface'}]}
        self.assertTrue(any('contrast' in x.lower() for x in design.check_contract(c)))
    def test_bad_pair(self):
        c={'colors':{'text':'#ffffff'},'contrast_pairs':[{'foreground':'missing','background':'text'}]}
        self.assertTrue(any('Unknown' in x for x in design.check_contract(c)))
    def test_no_pairs(self):self.assertIn('Missing contrast pairs',design.check_contract({'colors':{'text':'#ffffff'}}))

class DocsTests(unittest.TestCase):
    def test_all_activation_links_exist(self):
        s=(ROOT/'docs/UNIVERSAL-ACTIVATION.md').read_text()
        for marker in ('CONTINUITY.md','DEEPSEEK-WEB-ONLY.md','MASTER_PROMPT.md','SKILL.md'):
            self.assertIn(marker,s)
    def test_documented_limits(self):
        s=(ROOT/'docs/DEEPSEEK-WEB-ONLY.md').read_text()
        for marker in ('GET','JupyterLite','Pyodide','POST','NOT EXECUTED'):
            self.assertIn(marker,s)
    def test_skills_have_source_sections(self):
        for key in ('repo-refresh-protocol','deepseek-web-only-lab','design-taste-direction','image-to-code-fidelity','cross-model-activation'):
            with self.subTest(key=key):
                s=(ROOT/'skills'/key/'SKILL.md').read_text()
                self.assertIn('## Source access',s);self.assertIn('## Verification criteria',s)

if __name__=='__main__':unittest.main()
