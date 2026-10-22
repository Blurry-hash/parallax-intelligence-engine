"""Browser-runtime claims must remain capability gated and testable."""
import json
from pathlib import Path
import unittest
from tools.validate import validate

ROOT = Path(__file__).resolve().parents[1]

class BrowserComputeTests(unittest.TestCase):
    def test_runtime_docs_and_routing(self):
        skill = (ROOT/'skills/browser-compute-bridge/SKILL.md').read_text()
        docs = (ROOT/'docs/execution-backends.md').read_text()
        self.assertIn('read-only web fetch is NOT a runtime', skill)
        self.assertIn('NOT EXECUTED', skill)
        self.assertIn('Pyodide', docs)
        self.assertIn('JupyterLite', docs)
        self.assertIn('ffmpeg.wasm', docs)
        self.assertIn('permission', docs.lower())

    def test_sources_and_registry(self):
        data = json.loads((ROOT/'sources/sources.json').read_text())
        urls = {s['url'] for s in data['sources']}
        for url in ('https://github.com/pyodide/pyodide', 'https://github.com/jupyterlite/jupyterlite',
                    'https://github.com/ffmpegwasm/ffmpeg.wasm', 'https://github.com/e2b-dev/e2b',
                    'https://github.com/openai/openai-agents-python'):
            self.assertIn(url, urls)
        self.assertFalse(validate()[0])

    def test_example_evidence_is_not_faked(self):
        data = json.loads((ROOT/'examples/evidence-ledger.json').read_text())
        self.assertEqual(data['records'][0]['status'], 'PREPARED')
        self.assertIsNone(data['records'][0]['result'])

if __name__ == '__main__':
    unittest.main()
