"""Offline voice, audio and self-evolution regression tests."""
import copy,importlib.util,json,math,tempfile,unittest,wave
from array import array
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(name):
    spec=importlib.util.spec_from_file_location(name,ROOT/"tools"/(name+".py"))
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
audio=load("audio_lab");voice=load("voice_route");evolve=load("evolve_gate")

class AudioEvolutionTests(unittest.TestCase):
    def make_wav(self,root):
        path=root/"sound.wav";rate=16000
        wave_data=array("h",(int(6000*math.sin(2*math.pi*440*i/rate)) for i in range(rate)))
        with wave.open(str(path),"wb") as f:
            f.setnchannels(1);f.setsampwidth(2);f.setframerate(rate);f.writeframes(wave_data.tobytes())
        return path
    def test_measure_and_normalize(self):
        with tempfile.TemporaryDirectory() as tmp:
            src=self.make_wav(Path(tmp));out=Path(tmp)/"out.wav"
            self.assertEqual(audio.analyze(src)["duration_sec"],1)
            result=audio.normalize(src,out)
            self.assertGreater(result["after"]["sample_peak_dbfs"],result["before"]["sample_peak_dbfs"])
            self.assertLessEqual(result["after"]["sample_peak_dbfs"],-2.99)
            with self.assertRaises(ValueError):audio.normalize(src,out)
    def test_voice_requires_real_provider(self):
        task=json.loads((ROOT/"examples/voice-task.json").read_text())
        self.assertEqual(voice.route(task,[])["status"],"not_executed")
        task["speaker_reference"]="person.wav"
        self.assertEqual(voice.route(task,[])["status"],"blocked")
    def test_voice_commercial_license(self):
        task=json.loads((ROOT/"examples/voice-task.json").read_text())
        task["commercial"]=True
        model={"id":"dummy","verified_available":True,"tasks":["tts"],"languages":["sv-SE"],"commercial_licensed":False}
        self.assertEqual(voice.route(task,[model])["status"],"not_executed")
        model["commercial_licensed"]=True
        self.assertEqual(voice.route(task,[model])["status"],"planned_only")
    def test_evolution_gate(self):
        data=json.loads((ROOT/"examples/evolution-fixture.json").read_text())
        result=evolve.evaluate(data)
        self.assertEqual(result["decision"],"eligible_for_human_review")
        self.assertFalse(result["safe_to_auto_deploy"])
        broken=copy.deepcopy(data);broken["cases"][2]["candidate"]["critical_failure"]=True
        self.assertEqual(evolve.evaluate(broken)["decision"],"reject")
    def test_evolution_unsafe_evidence_rejected(self):
        data=json.loads((ROOT/"examples/evolution-fixture.json").read_text())
        data["holdout_was_used_to_tune"]=True
        with self.assertRaises(ValueError):evolve.evaluate(data)
        data["holdout_was_used_to_tune"]=False
        data["cases"][2]["candidate"]["quality"]=float("nan")
        with self.assertRaises(ValueError):evolve.evaluate(data)
