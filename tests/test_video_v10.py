"""V10 video timebase, safety and actual-media contracts."""
import copy,importlib.util,json,shutil,subprocess,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(name):
    spec=importlib.util.spec_from_file_location(name,ROOT/'tools'/f'{name}.py')
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod
T=load('video_timeline');Q=load('video_qc')
BASE=json.loads((ROOT/'examples/v10-timeline.json').read_text())
class TimelineTests(unittest.TestCase):
    def test_compile_deterministic(self):
        a=T.compile_timeline(BASE);b=T.compile_timeline(BASE)
        self.assertEqual(a,b);self.assertEqual(a['duration_frames'],108)
        self.assertEqual(a['duration_seconds'],4.5)
        self.assertEqual(a['edl'][0]['start_frame'],0)
        self.assertEqual(a['edl'][-1]['end_frame_exclusive'],108)
        self.assertEqual(a['edl'][-1]['end'],'00:00:04,500')
        self.assertEqual(a['srt'].count('-->'),3)
        self.assertFalse(a['checks']['rendered'])
    def test_bad_fps_rejected(self):
        for bad in (0,121,23.5,True,None):
            x=copy.deepcopy(BASE);x['fps']=bad
            with self.subTest(value=bad),self.assertRaises(T.TimelineError):T.compile_timeline(x)
    def test_bad_dimension_rejected(self):
        for bad in (641,100,'640',False):
            x=copy.deepcopy(BASE);x['width']=bad
            with self.subTest(value=bad),self.assertRaises(T.TimelineError):T.compile_timeline(x)
    def test_identity_metadata_lock_guard(self):
        x=copy.deepcopy(BASE);x['shots'][1]['state']['identity']='different'
        with self.assertRaises(T.TimelineError):T.compile_timeline(x)
    def test_locked_state_cannot_verify_pixels(self):
        x=T.compile_timeline(BASE)
        self.assertIn('not_visual_identity_verified',x['checks']['locked_state'])
    def test_bad_shot_rejected(self):
        for k,v in [('frames',0),('frames',True),('background','red'),('id','discover')]:
            x=copy.deepcopy(BASE);x['shots'][1][k]=v
            with self.subTest(key=k),self.assertRaises(T.TimelineError):T.compile_timeline(x)
    def test_duration_limit(self):
        x=copy.deepcopy(BASE);x['shots']=x['shots']*8
        with self.assertRaises(T.TimelineError):T.compile_timeline(x)
    def test_caption_text_with_special_characters(self):
        x=copy.deepcopy(BASE);x['shots'][0]['caption']='Speaker: [rain] & 100% safe'
        self.assertIn('Speaker: [rain] & 100% safe',T.compile_timeline(x)['srt'])
    def test_exact_srt_frame_clock(self):
        self.assertEqual(T.srt_clock(24,24),'00:00:01,000')
        self.assertEqual(T.srt_clock(25,24),'00:00:01,042')
        with self.assertRaises(T.TimelineError):T.srt_clock(-1,24)
class QCTests(unittest.TestCase):
    def test_contract_pass_fixture(self):
        probe={'streams':[{'codec_type':'video','codec_name':'h264','width':640,'height':360,'r_frame_rate':'24/1','nb_frames':'108'}],'format':{'duration':'4.5'}}
        spec={'width':640,'height':360,'fps':24,'codec_name':'h264','has_audio':False,'duration_seconds':4.5}
        r=Q.assess(probe,spec)
        self.assertEqual(r['status'],'pass');self.assertEqual(r['observed']['nb_frames'],108)
    def test_wrong_codec_and_missing_audio(self):
        probe={'streams':[{'codec_type':'video','codec_name':'vp9','width':640,'height':360,'avg_frame_rate':'24/1'}],'format':{'duration':'4.5'}}
        result=Q.assess(probe,{'codec_name':'h264','has_audio':True})
        self.assertEqual(result['status'],'fail');self.assertEqual(len(result['failures']),2)
    def test_missing_video_fails(self):
        self.assertEqual(Q.assess({'streams':[],'format':{}},{})['status'],'fail')
    def test_invalid_fraction_rejected(self):
        for val in ('0/0','invalid','-25/1','NaN'):
            with self.subTest(value=val),self.assertRaises(Q.VideoQualityError):Q.rational(val)
    def test_output_does_not_claim_semantic_identity(self):
        r=Q.assess({'streams':[{'codec_type':'video','r_frame_rate':'30/1'}],'format':{'duration':'1.0'}},{})
        self.assertTrue(any('visual quality' in x for x in r['limitations']))
    @unittest.skipUnless(shutil.which('ffmpeg') and shutil.which('ffprobe'),'FFmpeg/FFprobe required')
    def test_real_render_and_probe(self):
        renderer=load('render_video')
        with tempfile.TemporaryDirectory() as d:
            target=Path(d)/'actual.mp4'
            story=Path(d)/'story.json'
            story.write_text(json.dumps(T.compile_timeline(BASE)['storyboard']),encoding='utf8')
            renderer.render(story,target)
            result=Q.assess(Q.probe_file(target),json.loads((ROOT/'examples/v10-video-contract.json').read_text()))
            self.assertEqual(result['status'],'pass',result)
            self.assertEqual(result['observed']['nb_frames'],108)
if __name__=='__main__':unittest.main()
