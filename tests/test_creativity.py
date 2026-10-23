"""Offline real execution checks for conceptual-diversity helper and documented creative workflow."""
import importlib.util
import json
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('parallax_ideas',ROOT/'tools/idea_diversity.py')
ideas=importlib.util.module_from_spec(spec)
spec.loader.exec_module(ideas)

class CreativityTests(unittest.TestCase):
    def test_duplicates_identified(self):
        result=ideas.assess(['A blue robot walks in the garden','A blue robot walks in the garden'])
        self.assertEqual(result['lexical_diversity'],0)
        self.assertEqual(len(result['high_overlap_pairs']),1)
    def test_separate_vocabulary(self):
        result=ideas.assess(['graph traversal algorithm','rose petal perfume'])
        self.assertGreater(result['lexical_diversity'],0.9)
    def test_reject_invalid(self):
        for obj in [[],['one'],['one',''],['one',42]]:
            with self.subTest(obj=obj), self.assertRaises(ValueError):ideas.assess(obj)
    def test_sample_and_skill_mechanisms(self):
        sample=json.loads((ROOT/'examples/creative-candidates.json').read_text())
        self.assertEqual(ideas.assess(sample['ideas'])['idea_count'],4)
        for skill in ('creative-discovery','originality-evaluation','concept-laboratory','performance-validation'):
            text=(ROOT/'skills'/skill/'SKILL.md').read_text()
            self.assertIn('## Operational procedure',text)
            self.assertIn('**Check:**',text)
    def test_private_release_guardrails(self):
        helper=(ROOT/'scripts/private-release.ps1').read_text()
        self.assertIn('if (-not $Apply)', helper)
        self.assertNotIn('--visibility', helper)
        self.assertNotIn('repo edit', helper)
        self.assertIn('Repository visibility will NOT be changed.', helper)
        self.assertIn('Repository visibility unexpectedly changed.', helper)

    def test_prompt_and_readme_disclosure(self):
        readme=(ROOT/'README.md').read_text().lower()
        prompt=(ROOT/'MASTER_PROMPT.md').read_text().lower()
        for phrase in ['originality','creativity','holdout','not','evidence']:
            self.assertIn(phrase,readme)
        self.assertIn('constraint inversion',prompt)
        self.assertIn('novelty',prompt)
if __name__=='__main__':unittest.main()
