"""Offline audio and self-evolution regression tests with negative cases."""
from __future__ import annotations
import copy
import importlib.util
import json
import math
import tempfile
import unittest
import wave
from array import array
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load(name):
    spec=importlib.util.spec_from_file_location(name,ROOT/'tools'/f'{name}.py')
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

audio = load('audio_lab')
evolve = load('evolve_gate')
voice = load('voice_route')

class AudioTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.src=Path(self.tmp.name)/'source.wav'
        sr=16000
        samples=array('h',[int(6000*math.sin(2*math.pi*440*i/sr)) for i in range(sr)])
        with wave.open(str(self.src),'wb') as w:
            w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes(samples.tobytes())

    def test_wav_statistics(self):
        result=audio.analyze(self.src)
        self.assertEqual(result['channels'],1)
        self.assertEqual(result['duration_sec'],1.0)
        self.assertEqual(result['sample_rate'],16000)
        self.assertAlmostEqual(result['sample_peak_dbfs'],-14.75,delta=.5)
        self.assertEqual(result['clipped_sample_ratio'],0)

    def test_normalize_and_fade(self):
        dest=Path(self.tmp.name)/'out.wav'
        report=audio.normalize(self.src,dest,-3,5)
        self.assertTrue(dest.is_file())
        self.assertGreater(report['after']['sample_peak_dbfs'],report['before']['sample_peak_dbfs'])
        self.assertLessEqual(report['after']['sample_peak_dbfs'],-2.99)
        self.assertEqual(audio._load(dest)[0][0],0)
        with self.assertRaises(ValueError):audio.normalize(self.src,dest)
        with self.assertRaises(ValueError):audio.normalize(self.src,self.src)

    def test_reject_non_pcm(self):
        p=Path(self.tmp.name)/'corrupt.wav';p.write_bytes(b'not a wave')
        with self.assertRaises((ValueError,EOFError,wave.Error)):audio.analyze(p)
        with self.assertRaises(ValueError):audio.normalize(self.src,Path(self.tmp.name)/'unsafe.wav',1)

    def test_voice_routing_default_no_provider(self):
        t=json.loads((ROOT/'examples/voice-task.json').read_text())
        self.assertEqual(voice.route(t,[])['status'],'not_executed')

    def test_voice_blocks_unauthorized_reference(self):
        t=json.loads((ROOT/'examples/voice-task.json').read_text())
        t['speaker_reference']='someone.wav'
        self.assertEqual(voice.route(t,[])['status'],'blocked')

    def test_voice_requires_actual_availability_and_license(self):
        t=json.loads((ROOT/'examples/voice-task.json').read_text())
        t['commercial']=True
        backend={'id':'fake','tasks':['tts'],'languages':['sv-SE'],'verified_available':True,'commercial_licensed':False}
        self.assertEqual(voice.route(t,[backend])['status'],'not_executed')
        backend['commercial_licensed']=True
        self.assertEqual(voice.route(t,[backend])['status'],'planned_only')

class EvolutionTests(unittest.TestCase):
    def setUp(self):
        self.data=json.loads((ROOT/'examples/evolution-fixture.json').read_text())

    def test_eligible_not_autodeployed(self):
        result=evolve.evaluate(self.data)
        self.assertEqual(result['decision'],'eligible_for_human_review')
        self.assertFalse(result['safe_to_auto_deploy'])

    def test_quality_regression_rejected(self):
        d=copy.deepcopy(self.data)
        d['cases'][1]['candidate']['quality']=.1
        self.assertEqual(evolve.evaluate(d)['decision'],'reject')

    def test_critical_failure_rejected(self):
        d=copy.deepcopy(self.data)
        d['cases'][2]['candidate']['critical_failure']=True
        self.assertEqual(evolve.evaluate(d)['decision'],'reject')

    def test_latency_regression_rejected(self):
        d=copy.deepcopy(self.data)
        for c in d['cases']:c['candidate']['latency_ms']=1200
        self.assertEqual(evolve.evaluate(d)['decision'],'reject')

    def test_missing_holdout_or_contamination(self):
        d=copy.deepcopy(self.data);d['holdout_was_used_to_tune']=True
        with self.assertRaises(ValueError):evolve.evaluate(d)
        d=copy.deepcopy(self.data)
        for c in d['cases']:c['split']='holdout'
        with self.assertRaises(ValueError):evolve.evaluate(d)

    def test_nonfinite_and_duplicate(self):
        d=copy.deepcopy(self.data);d['cases'][1]['candidate']['quality']=float('nan')
        with self.assertRaises(ValueError):evolve.evaluate(d)
        d=copy.deepcopy(self.data);d['cases'][1]['id']=d['cases'][2]['id']
        with self.assertRaises(ValueError):evolve.evaluate(d)

    def test_sample_count_and_domain(self):
        d=copy.deepcopy(self.data);d['cases']=d['cases'][:4]
        with self.assertRaises(ValueError):evolve.evaluate(d)
        d=copy.deepcopy(self.data)
        for c in d['cases']:c['domain']='only-one'
        with self.assertRaises(ValueError):evolve.evaluate(d)

if __name__=='__main__':unittest.main()
