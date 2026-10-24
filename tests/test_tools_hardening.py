"""Regression cases for evidence binding, release metadata and media contracts."""
import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import goal_trace
import plan_engine
import build_release
import privacy_scan
import render_video

class HardeningTests(unittest.TestCase):
    def ledger(self, evidence):
        plan = json.loads((ROOT/'examples/planning-v10.3.json').read_text(encoding='utf-8'))
        ledger = {'plan_sha256': plan_engine.compile_plan(plan)['plan_sha256'], 'tasks': [
            {'id': t['id'], 'state': 'verified', 'approved': True, 'evidence': evidence} for t in plan['tasks']]}
        return plan, ledger

    def test_arbitrary_string_is_not_evidence(self):
        with self.assertRaises(ValueError):
            goal_trace.audit_ledger(*self.ledger(['xxxxxxxxxxxx']))

    def test_hash_binding_and_tamper(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/'report.json'; path.write_text('{"passed": true}', encoding='utf-8')
            evidence = [{'path': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                         'kind': 'test_report', 'outcome': 'pass'}]
            self.assertTrue(goal_trace.audit_ledger(*self.ledger(evidence))['complete'])
            path.write_text('{"passed": false}', encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'hash mismatch'):
                goal_trace.audit_ledger(*self.ledger(evidence))

    def test_release_uses_version_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)/'src'; root.mkdir()
            for name, text in [('README.md','project'), ('MASTER_PROMPT.md','prompt'), ('VERSION','2.0')]:
                (root/name).write_text(text, encoding='utf-8')
            self.assertEqual(build_release.pack(root, Path(tmp)/'out.zip')['release'], 'PARALLAX v2.0')

    def test_secret_families_redacted(self):
        with tempfile.TemporaryDirectory() as tmp:
            values = ['sk-ant-'+ 'A'*35, 'sk-proj-'+ 'B'*40, 'xoxb-'+ 'C'*30, 'sk_live_'+ 'D'*25]
            (Path(tmp)/'.env.local').write_text('\n'.join(values), encoding='utf-8')
            result = privacy_scan.inspect(Path(tmp))
            self.assertTrue({'anthropic_token','openai_project_token','slack_token','stripe_secret'} <= {x['pattern'] for x in result['issues']})
            for value in values: self.assertNotIn(value, json.dumps(result))

    def test_render_rejects_wrong_fps_even_with_valid_geometry(self):
        with tempfile.TemporaryDirectory() as tmp:
            story=Path(tmp)/'story.json'; out=Path(tmp)/'out.mp4'
            story.write_text(json.dumps({'width':128,'height':128,'fps':24,'scenes':[{'seconds':1,'background':'#000000'}]}), encoding='utf-8')
            out.write_bytes(b'0'*2048)
            metadata={'streams':[{'codec_type':'video','codec_name':'h264','width':128,'height':128,'r_frame_rate':'30/1'}], 'format':{'duration':'1'}}
            with patch.object(render_video,'require_program',return_value='ffmpeg'), patch.object(render_video.subprocess,'run'), patch.object(render_video,'probe_file',return_value=metadata):
                with self.assertRaisesRegex(RuntimeError, 'fps'):
                    render_video.render(story,out)

    def test_render_rejects_wrong_duration(self):
        with tempfile.TemporaryDirectory() as tmp:
            story=Path(tmp)/'story.json'; out=Path(tmp)/'out.mp4'
            story.write_text(json.dumps({'width':128,'height':128,'fps':24,'scenes':[{'seconds':1,'background':'#000000'}]}), encoding='utf-8')
            out.write_bytes(b'0'*2048)
            metadata={'streams':[{'codec_type':'video','codec_name':'h264','width':128,'height':128,'r_frame_rate':'24/1'}], 'format':{'duration':'2'}}
            with patch.object(render_video,'require_program',return_value='ffmpeg'), patch.object(render_video.subprocess,'run'), patch.object(render_video,'probe_file',return_value=metadata):
                with self.assertRaisesRegex(RuntimeError, 'duration'):
                    render_video.render(story,out)

if __name__ == '__main__': unittest.main()

