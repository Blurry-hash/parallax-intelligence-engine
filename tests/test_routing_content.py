import sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from route_task import candidates
from routing_eval import evaluate
from validate import skill_content_audit

class RetrievalCoverage(unittest.TestCase):
    def test_every_skill_reachable_by_exact_name(self):
        for path in (ROOT/'skills').glob('*/SKILL.md'):
            with self.subTest(skill=path.parent.name):
                self.assertEqual(candidates(path.parent.name,limit=1)[0]['skill'],path.parent.name)
    def test_new_skill_reachable_without_router_edit(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);p=root/'skills'/'specialized-optics';p.mkdir(parents=True)
            (p/'SKILL.md').write_text('description: calibrate interferometer coherence\n## Operational procedure\nMeasure fringe visibility.',encoding='utf-8')
            self.assertEqual(candidates('interferometer',root=root)[0]['skill'],'specialized-optics')
    def test_eval_rejects_unknown_label(self):
        with self.assertRaises(ValueError):evaluate([{'query':'x','relevant':['not-installed']}])
    def test_duplicate_procedures_detected(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            for name in ('one','two'):
                p=root/'skills'/name;p.mkdir(parents=True)
                (p/'SKILL.md').write_text('## Operational procedure\n1. The same substantial instruction copied between two skills.\n',encoding='utf-8')
            report=skill_content_audit(root)
            self.assertEqual(report['duplicate_procedures'],[['one','two']])
            self.assertEqual(len(report['warnings']),2)
