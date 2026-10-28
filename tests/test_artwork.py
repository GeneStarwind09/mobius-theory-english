import contextlib,hashlib,importlib.util,io,json,pathlib,sys,tempfile,unittest
from PIL import Image
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
import artwork_support
spec=importlib.util.spec_from_file_location('artwork_tool',ROOT/'tools/artwork.py');tool=importlib.util.module_from_spec(spec);spec.loader.exec_module(tool)

class ArtworkValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=pathlib.Path(self.temp.name)
        self.pack=self.root/'pack';self.edited=self.root/'edited';self.out=self.root/'prepared'
        (self.pack/'originals/labels').mkdir(parents=True);(self.edited/'labels').mkdir(parents=True)
        self.original=self.pack/'originals/labels/button__123.png';self.edit=self.edited/'labels/button__123.png'
        image=Image.new('RGBA',(8,8),(0,0,0,0));image.paste((255,255,255,255),(2,2,6,6));image.save(self.original)
        self.bundle=tool.read(ROOT/'manifest.json')['bundle']['original_sha256']
        self.asset={'id':'123','path':'assets/gamebundle/textures/languages/button.png','name':'button','width':8,'height':8,'mip_count':1,'file':'originals/labels/button__123.png','replacement':'replacements/labels/button__123.png','png_sha256':tool.sha(self.original),'pixels_sha256':tool.pixels(image)}
        tool.write(self.pack/'assets.json',{'original_bundle_sha256':self.bundle,'assets':[self.asset]})
        image.putpixel((3,3),(10,20,30,255));image.save(self.edit)
    def tearDown(self):self.temp.cleanup()
    def prepare(self):
        with contextlib.redirect_stdout(io.StringIO()):tool.prepare(self.pack,self.edited,self.out)
    def test_valid_batch_retains_identity_and_hash(self):
        self.prepare();data=tool.read(self.out/'manifest.json');row=data['assets'][0]
        self.assertEqual(row['id'],'123');self.assertEqual(row['file'],'labels/button__123.png')
        self.assertEqual(row['replacement_sha256'],tool.sha(self.edit))
        base=self.root/'base';(base/'artwork').mkdir(parents=True)
        import shutil;shutil.copytree(self.out,base/'artwork',dirs_exist_ok=True)
        self.assertEqual(len(artwork_support.load_replacements(base,tool.read(ROOT/'manifest.json'))),1)
    def test_resized_png_rejected_before_output(self):
        Image.new('RGBA',(9,8)).save(self.edit)
        with self.assertRaisesRegex(ValueError,'Canvas size'):self.prepare()
        self.assertFalse(self.out.exists())
    def test_flattened_transparency_rejected_before_output(self):
        Image.new('RGB',(8,8),'white').save(self.edit)
        with self.assertRaisesRegex(ValueError,'flattened'):self.prepare()
        self.assertFalse(self.out.exists())
    def test_unknown_filename_rejected(self):
        self.edit.rename(self.edited/'labels/wrong.png')
        with self.assertRaisesRegex(ValueError,'Unknown replacement'):self.prepare()
    def test_original_export_modification_rejected(self):
        self.original.write_bytes(self.edit.read_bytes())
        with self.assertRaisesRegex(ValueError,'Original export was changed'):self.prepare()
    def test_unchanged_copy_is_not_an_edit(self):
        self.edit.write_bytes(self.original.read_bytes())
        with self.assertRaisesRegex(ValueError,'No changed PNG'):self.prepare()
    def test_path_escape_rejected(self):
        self.prepare();data=tool.read(self.out/'manifest.json');data['assets'][0]['file']='../outside.png'
        base=self.root/'base';(base/'artwork').mkdir(parents=True);tool.write(base/'artwork/manifest.json',data)
        with self.assertRaisesRegex(ValueError,'escapes'):artwork_support.load_replacements(base,tool.read(ROOT/'manifest.json'))
    def test_duplicate_texture_ids_rejected(self):
        self.prepare();data=tool.read(self.out/'manifest.json');data['assets'].append(data['assets'][0])
        tool.write(self.out/'manifest.json',data)
        import shutil;base=self.root/'base';shutil.copytree(self.out,base/'artwork')
        with self.assertRaisesRegex(ValueError,'Duplicate'):artwork_support.load_replacements(base,tool.read(ROOT/'manifest.json'))
    def test_payload_identity_changes_when_art_batch_added(self):
        base=self.root/'base';base.mkdir();(base/'manifest.json').write_text('{}');(base/'translations.json').write_text('{}')
        before=artwork_support.payload_id(base);(base/'artwork').mkdir();(base/'artwork/manifest.json').write_text('{}')
        self.assertNotEqual(before,artwork_support.payload_id(base))

if __name__=='__main__':unittest.main()
