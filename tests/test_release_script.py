"""Regression checks for the ZIP-driven visibility-preserving release script (static)."""
from pathlib import Path
import unittest

SOURCE = Path(__file__).resolve().parents[1] / "scripts" / "private-release.ps1"

class PrivateReleaseScriptTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.script = SOURCE.read_text(encoding="utf-8")

    def test_no_case_insensitive_function_recursion(self):
        self.assertNotRegex(self.script, r"(?im)^\s*function\s+(?:gh|git)\b")
        self.assertIn('& $script:GhExecutable @Arguments', self.script)
        self.assertIn('& $script:GitExecutable @Arguments', self.script)

    def test_actual_executable_resolution(self):
        self.assertIn('Get-Command -Name "$Name.exe" -CommandType Application', self.script)
        self.assertIn("Get-Executable 'gh'", self.script)
        self.assertIn("Get-Executable 'git'", self.script)

    def test_auto_find_and_extract_zip(self):
        self.assertIn('function Find-ReleaseZip', self.script)
        self.assertIn('function Expand-VerifiedRelease', self.script)
        self.assertIn("'Downloads'", self.script)
        self.assertIn("'parallax-intelligence-engine*.zip'", self.script)
        self.assertIn('Expand-Archive -LiteralPath', self.script)
        self.assertIn('docs/execution-backends.md', self.script)
        self.assertIn('skills/browser-compute-bridge/SKILL.md', self.script)

    def test_zip_path_traversal_guard(self):
        self.assertIn("$entry.FullName.Replace", self.script)
        self.assertIn('Unsafe ZIP entry', self.script)
        self.assertIn('No GitHub changes made', self.script)

    def test_preflight_before_remote_writes(self):
        self.assertLess(self.script.index('Expand-VerifiedRelease -Path'), self.script.index("if (-not $Apply)"))
        self.assertIn('[string]$ZipPath', self.script)
        self.assertIn('[switch]$SkipPush', self.script)

    def test_dry_run_guard(self):
        self.assertIn('if (-not $Apply)', self.script)
        self.assertIn('DRY RUN ONLY:', self.script)

    def test_clone_before_nonforce_push(self):
        self.assertIn("'clone'", self.script)
        self.assertIn("'ls-remote'", self.script)
        self.assertNotIn("'--force'", self.script)
        self.assertNotIn("'push','--force'", self.script)

    def test_visibility_unchanged(self):
        self.assertNotIn("'--visibility','private'", self.script)
        self.assertNotIn('repo edit', self.script)
        self.assertIn('Repository visibility will NOT be changed.', self.script)
        self.assertIn('Repository visibility unexpectedly changed.', self.script)

if __name__ == '__main__':
    unittest.main()
