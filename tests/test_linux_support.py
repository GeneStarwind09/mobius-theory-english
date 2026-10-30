import base64,hashlib,json,pathlib,sys,tempfile,unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
from platform_support import linux_game_running,linux_steam_roots,steam_game_candidates
from managed_support import apply_managed_delta
import bsdiff4


class LinuxSupportTests(unittest.TestCase):
 def setUp(self):self.temp=tempfile.TemporaryDirectory();self.root=pathlib.Path(self.temp.name)
 def tearDown(self):self.temp.cleanup()
 def test_running_proton_game_detected_from_windows_argument(self):
  p=self.root/'987654321';p.mkdir();(p/'cmdline').write_bytes('wine\0Z:\\Games\\轮回之理.exe\0'.encode())
  self.assertTrue(linux_game_running(self.root))
 def test_patcher_folder_argument_does_not_count_as_running_game(self):
  p=self.root/'987654321';p.mkdir();(p/'cmdline').write_bytes('patcher\0--game\0/home/user/轮回之理\0'.encode())
  self.assertFalse(linux_game_running(self.root))
 def test_flatpak_and_external_library_discovery(self):
  home=self.root/'user';client=linux_steam_roots(home,{})[-1];(client/'steamapps').mkdir(parents=True)
  external=self.root/'External Library';(external/'steamapps').mkdir(parents=True)
  (client/'steamapps/libraryfolders.vdf').write_text('"path" "'+str(external)+'"',encoding='utf-8')
  (external/'steamapps/appmanifest_1925830.acf').write_text('"installdir" "轮回之理"',encoding='utf-8')
  self.assertEqual(list(steam_game_candidates([client])),[external/'steamapps/common/轮回之理'])
 def recipe(self):
  original=b'original binary fixture'+bytes(range(256));english=b'English binary fixture'+bytes(range(256))
  sha=lambda x:hashlib.sha256(x).hexdigest();delta=bsdiff4.diff(original,english)
  r={'schema':1,'format':'BSDIFF40','original_sha256':sha(original),'english_sha256':sha(english),
     'english_size':len(english),'patch_sha256':sha(delta),'patch_base64':base64.b64encode(delta).decode()}
  raw=json.dumps(r).encode();(self.root/'managed-patch.json').write_bytes(raw)
  source=self.root/'original.dll';source.write_bytes(original)
  return source,self.root/'english.dll',english,{'managed':{'original_sha256':sha(original),'portable_patch_sha256':sha(raw)}}
 def test_portable_patch_output_exact(self):
  source,dest,english,m=self.recipe();apply_managed_delta(source,dest,self.root,m);self.assertEqual(dest.read_bytes(),english)
 def test_wrong_original_rejected_without_destination_write(self):
  source,dest,english,m=self.recipe();source.write_bytes(b'another game build')
  with self.assertRaisesRegex(ValueError,'original managed'):apply_managed_delta(source,dest,self.root,m)
  self.assertFalse(dest.exists())
 def test_recipe_tampering_rejected_without_destination_write(self):
  source,dest,english,m=self.recipe();(self.root/'managed-patch.json').write_text('{}')
  with self.assertRaisesRegex(ValueError,'patch hash'):apply_managed_delta(source,dest,self.root,m)
  self.assertFalse(dest.exists())
