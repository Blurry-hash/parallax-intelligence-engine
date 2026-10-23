"""Deterministic archive verification including failed integrity cases."""
import importlib.util, tempfile, unittest, zipfile, json, shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('parallax_archive',ROOT/'tools'/'build_release.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class ReleaseIntegrityTests(unittest.TestCase):
    def test_build_and_verify(self):
        with tempfile.TemporaryDirectory() as d:
            out=Path(d)/'release.zip';m.pack(ROOT,out)
            self.assertGreater(m.verify(out)['files'],60)
    def test_repack_extracted_archive(self):
        with tempfile.TemporaryDirectory() as d:
            out=Path(d)/'first.zip';m.pack(ROOT,out)
            extract=Path(d)/'extracted'
            with zipfile.ZipFile(out) as z:z.extractall(extract)
            repeated=Path(d)/'second.zip'
            m.pack(extract/'parallax-intelligence-engine',repeated)
            self.assertEqual(m.verify(out)['sha256_zip'],m.verify(repeated)['sha256_zip'])
    def test_zip_path_guard(self):
        with tempfile.TemporaryDirectory() as d:
            z=Path(d)/'evil.zip'
            with zipfile.ZipFile(z,'w') as f:
                f.writestr('../outside.txt','bad')
                f.writestr('parallax-intelligence-engine/RELEASE_MANIFEST.json',json.dumps({'sha256':{},'file_count':0}))
            with self.assertRaises(ValueError):m.verify(z)
    def test_destination_inside_repo_rejected(self):
        with self.assertRaises(ValueError):m.pack(ROOT,ROOT/'test.zip')
    def test_corrupted_member_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            a=Path(d)/'a.zip';m.pack(ROOT,a)
            names=zipfile.ZipFile(a).namelist()
            corrupt=Path(d)/'corrupt.zip'
            with zipfile.ZipFile(a) as old, zipfile.ZipFile(corrupt,'w') as new:
                for name in names:
                    content=old.read(name)
                    if name.endswith('README.md'):content+=b' changed!'
                    new.writestr(name,content)
            with self.assertRaises(ValueError):m.verify(corrupt)
if __name__=='__main__':unittest.main()
