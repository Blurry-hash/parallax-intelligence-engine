"""Offline structural, regression and deliberately failing-case tests."""

import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("aiontrix_validate", ROOT / "tools" / "validate.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class PackageTests(unittest.TestCase):
    def test_registry_and_structure(self):
        errors, sources, skills = module.validate()
        self.assertEqual(errors, [])
        self.assertGreaterEqual(sources, 74)
        self.assertGreaterEqual(skills, 23)

    def test_master_prompt_covers_systems(self):
        text = (ROOT / "MASTER_PROMPT.md").read_text(encoding="utf-8").lower()
        for concept in ("coding", "physical", "performance", "image", "distillation", "humor", "security", "source", "mcp", "holdout", "latency", "video", "ffmpeg"):
            with self.subTest(concept=concept):
                self.assertIn(concept, text)

    def test_untrusted_prompt_archive_label(self):
        sources = json.loads((ROOT / "sources" / "sources.json").read_text(encoding="utf-8"))["sources"]
        for source in sources:
            if source["topic"] == "prompt-archives":
                self.assertEqual(source["trust"], "unverified")
                self.assertTrue(source["notes"])

    def test_all_skills_contain_check_and_procedure(self):
        for path in (ROOT / "skills").glob("*/SKILL.md"):
            body = path.read_text(encoding="utf-8")
            with self.subTest(skill=path.parent.name):
                self.assertIn("**Check:**", body)
                self.assertIn("## Source access", body)
                self.assertIn("## Operational procedure", body)

    def test_video_storyboard_validation(self):
        from copy import deepcopy
        import importlib.util
        script = ROOT / "tools" / "render_video.py"
        module_spec = importlib.util.spec_from_file_location("aiontrix_video", script)
        video = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(video)
        sample = json.loads((ROOT / "examples/video-storyboard.json").read_text(encoding="utf-8"))
        self.assertEqual(video.checked_storyboard(sample)["fps"], 24)
        with self.assertRaises(video.StoryboardError):
            x = deepcopy(sample)
            x["width"] = 641
            video.checked_storyboard(x)
        with self.assertRaises(video.StoryboardError):
            x = deepcopy(sample)
            x["scenes"][0]["background"] = "#000000;rm -rf /"
            video.checked_storyboard(x)
        with self.assertRaises(video.StoryboardError):
            x = deepcopy(sample)
            x["scenes"][0]["seconds"] = float("nan")
            video.checked_storyboard(x)

    def _temporary_repo(self):
        tmp = tempfile.TemporaryDirectory()
        dest = Path(tmp.name) / "repo"
        shutil.copytree(ROOT, dest, ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"))
        self.addCleanup(tmp.cleanup)
        return dest

    def test_reject_duplicate_source(self):
        root = self._temporary_repo()
        path = root / "sources/sources.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["sources"].append(data["sources"][0].copy())
        path.write_text(json.dumps(data), encoding="utf-8")
        errors, _, _ = module.validate(root)
        self.assertTrue(any("Duplicate URL" in error for error in errors))

    def test_reject_untrusted_source_without_caveat(self):
        root = self._temporary_repo()
        path = root / "sources/sources.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        target = next(s for s in data["sources"] if s["trust"] == "unverified")
        target["notes"] = ""
        path.write_text(json.dumps(data), encoding="utf-8")
        errors, _, _ = module.validate(root)
        self.assertTrue(any("provenance caveat" in error for error in errors))

    def test_reject_broken_local_link(self):
        root = self._temporary_repo()
        path = root / "README.md"
        path.write_text(path.read_text(encoding="utf-8") + "\n[broken](missing-file.md)\n", encoding="utf-8")
        errors, _, _ = module.validate(root)
        self.assertTrue(any("Broken local link" in error for error in errors))

    def test_reject_misnamed_skill(self):
        root = self._temporary_repo()
        path = root / "skills/deep-reasoning/SKILL.md"
        body = path.read_text(encoding="utf-8").replace("name: deep-reasoning", "name: something-else", 1)
        path.write_text(body, encoding="utf-8")
        errors, _, _ = module.validate(root)
        self.assertTrue(any("Invalid skill name" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
