import pathlib,tempfile,unittest,sys,json
from unittest.mock import patch
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
import patcher
class AddedSubtitleTests(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.root=pathlib.Path(self.temp.name);self.game=self.root/'game';self.game.mkdir();(self.game/'轮回之理.exe').write_bytes(b'test')
  self.base=self.root/'payload';self.base.mkdir();self.rel='轮回之理_Data/StreamingAssets/Videos/GameOver.srt';self.file=self.game/self.rel;self.file.parent.mkdir(parents=True)
  self.old=self.game/'existing';self.old.write_bytes(b'english');self.saved=self.game/'.mobius-english/original/existing';self.saved.parent.mkdir(parents=True);self.saved.write_bytes(b'original')
  self.state={'status':'installed','files':{'existing':{'original':patcher.digest(self.saved),'english':patcher.digest(self.old)},self.rel:{'original':None,'english':__import__('hashlib').sha256(b'caption').hexdigest()}}}
  patcher.atomic_json(self.game/'.mobius-english/state.json',self.state)
 def tearDown(self):self.temp.cleanup()
 def restore(self):
  with patch.object(patcher,'game_running',return_value=False):patcher.restore(self.game,lambda s:None)
 def test_restore_removes_only_known_added_file(self):
  self.file.write_bytes(b'caption');self.restore();self.assertFalse(self.file.exists());self.assertEqual(self.old.read_bytes(),b'original')
 def test_interrupted_install_before_new_file_is_safe(self):
  self.state['status']='prepared';patcher.atomic_json(self.game/'.mobius-english/state.json',self.state);self.restore();self.assertEqual(self.old.read_bytes(),b'original')
 def test_modified_added_file_blocks_entire_restore(self):
  self.file.write_bytes(b'user edit')
  with self.assertRaisesRegex(RuntimeError,'File changed'):self.restore()
  self.assertEqual(self.old.read_bytes(),b'english');self.assertEqual(self.file.read_bytes(),b'user edit')
 def test_original_check_rejects_untracked_file(self):
  # Two ordinary target entries use this same known original fixture.
  self.old.write_bytes(b'original');m={'bundle':{'path':'existing','original_sha256':patcher.digest(self.old)},'managed':{'path':'existing','original_sha256':patcher.digest(self.old)},'subtitles':{'GameOver.srt':{'original_sha256':None}}}
  (self.base/'manifest.json').write_text(json.dumps(m),encoding='utf-8');(self.game/'.mobius-english/state.json').unlink()
  with patch.object(patcher,'BASE',self.base):
   self.assertEqual(patcher.check(self.game,lambda s:None),'original');self.file.write_bytes(b'other mod')
   with self.assertRaisesRegex(RuntimeError,'Unsupported'):patcher.check(self.game,lambda s:None)
