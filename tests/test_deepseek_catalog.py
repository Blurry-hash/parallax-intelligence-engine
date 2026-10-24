"""Negative-case tests for DeepSeek's GET-only skill catalog."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('deepseek_catalog',ROOT/'tools/deepseek_catalog.py')
c=importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)


class DeepSeekCatalogTest(unittest.TestCase):
    def test_live_catalog_exact(self):
        saved=c.run(ROOT,check=True)
        ix=json.loads(saved['index.json'])
        self.assertEqual(ix['counts'],{'skills':147,'sources':157})
        self.assertEqual(len(ix['pages']['skills']),13)
        self.assertEqual(len(ix['pages']['sources']),20)
        self.assertTrue(all(len(v)<5500 for v in saved.values()))

    def test_missing_page_is_detected(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t)
            (root/'skills/example').mkdir(parents=True)
            (root/'skills/example/SKILL.md').write_text('example',encoding='utf-8')
            (root/'sources').mkdir()
            (root/'sources/sources.json').write_text(json.dumps({'sources':[{'name':'source','url':'https://github.com/x/y','topic':'t','trust':'official','status':'verified-page'}]}),encoding='utf-8')
            with self.assertRaises(ValueError):c.run(root,check=True)
            c.run(root,check=False)
            self.assertEqual(c.run(root,check=True)['index.json'][:1],b'{')
            (root/'bridge/v1/skills-01.json').write_text('malformed',encoding='utf-8')
            with self.assertRaises(ValueError):c.run(root,check=True)

    def test_large_remote_response_is_not_required(self):
        ix=json.loads((ROOT/'bridge/v1/index.json').read_text())
        self.assertEqual(ix['pages']['skills'][-1],'skills-13.json')
        self.assertIn('cannot execute arbitrary code',ix['execution_rule'])

if __name__=='__main__':unittest.main()
