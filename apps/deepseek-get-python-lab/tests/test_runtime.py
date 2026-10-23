"""Offline tests: mock Worker HTTP response, actual local Python for computations."""
import asyncio
import importlib.util
import sys
import types
import unittest
from pathlib import Path

class Response:
    @staticmethod
    def json(data,status=200):
        return data,status

sys.modules.setdefault("workers",types.SimpleNamespace(Response=Response,WorkerEntrypoint=object))
spec=importlib.util.spec_from_file_location("deepseek_lab_entry",Path(__file__).resolve().parents[1]/"src"/"entry.py")
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class Request:
    def __init__(self,url):
        self.url=url

class Tests(unittest.TestCase):
    def test_calculations(self):
        self.assertEqual(mod.stats()["mean"],5)
        self.assertAlmostEqual(mod.stats()["sample_stdev"],2.138089935299395,places=14)
        self.assertEqual(mod.determinants(),{"det2":-2,"checksum":385,"det3":0})

    def test_valid_routes(self):
        for case in ("stats","determinants","all"):
            body,code=asyncio.run(mod.Default().fetch(Request("https://example.com/run?case="+case)))
            self.assertEqual(code,200)
            self.assertFalse(body["supports_arbitrary_code"])

    def test_invalid_cases_are_rejected(self):
        body,code=asyncio.run(mod.Default().fetch(Request("https://example.com/run?case=__import__")))
        self.assertEqual(code,400)
        self.assertEqual(body["error"],"unknown case")

    def test_health_and_404(self):
        self.assertEqual(asyncio.run(mod.Default().fetch(Request("https://example.com/health")))[1],200)
        self.assertEqual(asyncio.run(mod.Default().fetch(Request("https://example.com/nope")))[1],404)

if __name__=="__main__":unittest.main()
