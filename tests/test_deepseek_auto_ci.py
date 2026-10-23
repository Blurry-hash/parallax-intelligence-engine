"""Checks that a GET-only AI can inspect genuine, not fabricated, CI evidence."""
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def verified(run,sha):
    return bool(sha) and run.get('head_sha')==sha and run.get('status')=='completed' and run.get('conclusion')=='success'

class DeepSeekCIEvidenceTests(unittest.TestCase):
    def test_scheduled_full_suite_is_readonly(self):
        w=(ROOT/'.github/workflows/deepseek-test-bench.yml').read_text(encoding='utf-8')
        self.assertIn("cron: '17 3 * * *'",w)
        self.assertIn("permissions:\n  contents: read",w)
        self.assertIn('persist-credentials: false',w)
        self.assertIn("github.event_name == 'workflow_dispatch' && inputs.suite || 'full'",w)
        self.assertIn('python -m unittest discover -s tests -q',w)
        self.assertNotIn('contents: write',w)

    def test_readonly_catalog_exposes_public_evidence_and_provenance(self):
        index=json.loads((ROOT/'bridge/v1/index.json').read_text(encoding='utf-8'))
        self.assertEqual(index['counts'],{'skills':142,'sources':157})
        self.assertEqual(index['source_status_counts'],{'unconfirmed':46,'verified-page':111})
        ci=index['ci_get_only']
        self.assertTrue(ci['latest_commit'].startswith('https://api.github.com/repos/'))
        self.assertIn('event=schedule',ci['scheduled_test_runs'])
        self.assertIn('/actions/runs?per_page=3',ci['runs_fallback'])
        self.assertIn('run_id',ci['run_jobs_template'])

    def test_in_progress_failed_stale_and_missing_are_not_verified(self):
        good={'head_sha':'now','status':'completed','conclusion':'success'}
        self.assertTrue(verified(good,'now'))
        for run in [dict(good,head_sha='old'),dict(good,status='in_progress'),
                    dict(good,conclusion='failure'),dict(good,conclusion=None)]:
            self.assertFalse(verified(run,'now'))
        self.assertFalse(verified(good,''))

    def test_committed_generated_pages_match(self):
        r=subprocess.run([sys.executable,str(ROOT/'tools/deepseek_catalog.py'),'--check'],cwd=ROOT,capture_output=True,text=True)
        self.assertEqual(r.returncode,0,r.stdout+r.stderr)

if __name__=='__main__':unittest.main()
