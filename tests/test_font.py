import copy,pathlib,sys,unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
from font_support import primary_font


class PrimaryFontTests(unittest.TestCase):
    def setUp(self):
        self.original={k: {'m_FileID':0,'m_PathID':123} for k in
            ('m_GameObject','m_Script','material','atlas')}
        self.original.update(m_Enabled=1,m_Name='Original',hashCode=12,materialHashCode=34,
            m_AtlasTextures=[{'m_FileID':0,'m_PathID':456}],m_FontWeightTable=[],fontWeights=[])
        self.latin={'m_CharacterTable':[{'m_Unicode':ord(c)} for c in 'Me'],
            'm_FallbackFontAssetTable':[{'m_FileID':0,'m_PathID':29}],
            'fallbackFontAssets':[29],'m_AtlasTextures':[{'m_FileID':0,'m_PathID':12}]}

    def test_primary_font_retains_destination_references(self):
        font=primary_font(self.original,self.latin,['Me'])
        for k in ('m_Script','material','m_AtlasTextures'):
            self.assertEqual(font[k],self.original[k])
        self.assertEqual(font['m_FallbackFontAssetTable'],[])
        self.assertEqual(font['m_AtlasPopulationMode'],0)

    def test_missing_glyph_rejected(self):
        with self.assertRaisesRegex(ValueError,'lacks glyphs'):
            primary_font(self.original,self.latin,['Mood'])

    def test_source_tables_are_not_modified(self):
        before=copy.deepcopy((self.original,self.latin))
        primary_font(self.original,self.latin,['Me'])
        self.assertEqual((self.original,self.latin),before)
