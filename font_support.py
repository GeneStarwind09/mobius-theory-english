"""Keep Mind Palace English glyphs on its animated primary text renderer.

Font data is reused from the player's own Unity resources, never distributed.
The existing custom fill shader, component references and puzzle code stay intact.
"""
import copy,hashlib,pathlib


def sha(data):return hashlib.sha256(data).hexdigest()


def primary_font(original, latin, required_text):
    characters={x['m_Unicode'] for x in latin['m_CharacterTable']}
    missing={ord(c) for text in required_text for c in text}-characters
    if missing:raise ValueError('Mind Palace primary font lacks glyphs: '+str(sorted(missing)))
    result=copy.deepcopy(latin)
    # All references must belong to the destination bundle, not resources.assets.
    for key in ('m_GameObject','m_Enabled','m_Script','m_Name','hashCode','material',
                'materialHashCode','m_AtlasTextures','atlas'):
        result[key]=copy.deepcopy(original[key])
    result['m_SourceFontFile']={'m_FileID':0,'m_PathID':0}
    result['m_AtlasPopulationMode']=0
    result['m_FallbackFontAssetTable']=[];result['fallbackFontAssets']=[]
    result['m_FontWeightTable']=copy.deepcopy(original['m_FontWeightTable'])
    result['fontWeights']=copy.deepcopy(original['fontWeights'])
    return result


def apply_mind_palace_font(env, game_root, manifest, mapping, log=print):
    plan=manifest.get('mind_palace_font')
    if not plan:return {}
    import UnityPy
    root=pathlib.Path(game_root).resolve()
    def checked(rel,expected):
        path=(root/rel).resolve()
        if root not in path.parents:raise ValueError('Font source escapes game folder.')
        data=path.read_bytes()
        if sha(data)!=expected:raise ValueError('Unsupported font source: '+rel)
        return data
    resource_bytes=checked(plan['resources_path'],plan['resources_sha256'])
    atlas_stream=checked(plan['stream_path'],plan['stream_sha256'])
    resources=UnityPy.load(resource_bytes);source={o.path_id:o for o in resources.objects}
    objects={o.path_id:o for o in env.objects}
    for row in plan['targets']:
        if sha(objects[row['id']].get_raw_data())!=row['sha256']:
            raise ValueError('Mind Palace font object identity mismatch.')
    font_obj=objects[plan['font_id']];texture_obj=objects[plan['texture_id']]
    original=font_obj.read_typetree()
    # resources.assets strips type trees; use the same game's bundled TMP schema.
    latin=source[plan['source_font_id']].read_typetree(nodes=font_obj.serialized_type.node)
    source_texture=source[plan['source_texture_id']].read_typetree(nodes=texture_obj.serialized_type.node)
    required=[mapping[x] for x in plan['clue_keys']]
    font=primary_font(original,latin,required)
    stream=source_texture['m_StreamData']
    if stream['path']!=pathlib.PurePosixPath(plan['stream_path']).name:
        raise ValueError('Unexpected English font atlas stream.')
    start,size=stream['offset'],stream['size'];pixels=atlas_stream[start:start+size]
    width,height=latin['m_AtlasWidth'],latin['m_AtlasHeight']
    if source_texture['m_TextureFormat']!=1 or len(pixels)!=width*height or size!=len(pixels):
        raise ValueError('Expected a complete Alpha8 English font atlas.')
    texture=texture_obj.read_typetree()
    for key in ('m_Width','m_Height','m_CompleteImageSize','m_TextureFormat','m_MipCount'):
        texture[key]=source_texture[key]
    texture['image data']=pixels
    texture['m_StreamData']={'offset':0,'size':0,'path':''}
    material_obj=objects[plan['material_id']];material=material_obj.read_typetree()
    floats=material['m_SavedProperties']['m_Floats']
    values={'_TextureWidth':float(width),'_TextureHeight':float(height),
            '_GradientScale':float(latin['m_AtlasPadding']+1),
            '_WeightNormal':latin['normalStyle'],'_WeightBold':latin['boldStyle']}
    material['m_SavedProperties']['m_Floats']=[(k,values.pop(k,v)) for k,v in floats]
    if values:raise ValueError('Missing primary font shader metrics: '+str(values))
    expected={}
    for obj,tree in ((font_obj,font),(texture_obj,texture),(material_obj,material)):
        expected[obj.path_id]=obj.save_typetree(tree)
    log('Mind Palace: all 10 English labels use the primary font and original fill shader.')
    return expected
