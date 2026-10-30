import pathlib,sys,copy,json,unittest
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
import layout_support
class Object:
 path_id=1
 def __init__(self,tree):self.tree=tree
 def read_typetree(self):return copy.deepcopy(self.tree)
 def save_typetree(self,tree):self.saved=copy.deepcopy(tree);return b'serialized'
class LayoutTests(unittest.TestCase):
 def test_binary_sprite_data_decodes_to_bytes(self):
  o=Object({'mesh':{'data':b'old'}});layout_support.apply_layout({1:o},[{'id':1,'set':[{'field':'mesh.data','value':'0000ff','encoding':'hex'}]}]);self.assertEqual(o.saved['mesh']['data'],b'\0\0\xff')
 def test_binary_operation_rejects_nonbinary_target(self):
  o=Object({'data':10})
  with self.assertRaisesRegex(ValueError,'Binary layout field'):layout_support.apply_layout({1:o},[{'id':1,'set':[{'field':'data','value':'00','encoding':'hex'}]}])
 def test_translated_tree_retained_when_font_changes(self):
  o=Object({'m_Text':'original','font':1});layout_support.apply_layout({1:o},[{'id':1,'set':[{'field':'font','value':2}]}],{1:{'m_Text':'English','font':1}});self.assertEqual(o.saved,{'m_Text':'English','font':2})
