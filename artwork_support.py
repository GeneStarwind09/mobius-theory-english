"""Optional, verified PNG replacements. Contains no original game artwork."""
import hashlib,json,pathlib
from PIL import Image

def sha(path):return hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()
def pixel_hash(image):return hashlib.sha256(image.convert('RGBA').tobytes()).hexdigest()

def payload_id(base):
    h=hashlib.sha256()
    for rel in ('manifest.json','translations.json','artwork/manifest.json','layout.json'):
        path=pathlib.Path(base)/rel
        h.update(rel.encode());h.update(path.read_bytes() if path.is_file() else b'absent')
    return h.hexdigest()

def load_replacements(base,manifest):
    root=pathlib.Path(base)/'artwork';path=root/'manifest.json'
    if not path.exists():return []
    data=json.loads(path.read_text(encoding='utf-8'))
    if data.get('schema')!=1 or data.get('original_bundle_sha256')!=manifest['bundle']['original_sha256']:raise ValueError('Artwork manifest is for an unsupported original bundle.')
    rows=data.get('assets',[]);seen=set()
    for row in rows:
        ident=int(row['id'])
        if ident in seen:raise ValueError('Duplicate texture ID in artwork manifest.')
        seen.add(ident);file=(root/row['file']).resolve()
        if root.resolve() not in file.parents:raise ValueError('Artwork path escapes its folder.')
        if sha(file)!=row['replacement_sha256']:raise ValueError('Artwork hash mismatch: '+row['file'])
        with Image.open(file) as image:
            image.load()
            if image.format!='PNG' or image.size!=(row['width'],row['height']):raise ValueError('Artwork dimensions or format changed: '+row['file'])
    return rows

def apply_replacements(env,base,rows,log):
    index={obj.path_id:obj for obj in env.objects};expected={}
    for row in rows:
        ident=int(row['id']);obj=index.get(ident)
        if obj is None or obj.type.name!='Texture2D':raise ValueError('Artwork texture ID not found: '+str(ident))
        texture=obj.read()
        if texture.m_Name!=row['name'] or (texture.m_Width,texture.m_Height)!=(row['width'],row['height']):raise ValueError('Original artwork identity mismatch: '+row['file'])
        original=texture.image.convert('RGBA')
        if pixel_hash(original)!=row['pixels_sha256']:raise ValueError('Original artwork pixels mismatch: '+row['file'])
        with Image.open(pathlib.Path(base)/'artwork'/row['file']) as image:
            image=image.convert('RGBA')
            old_alpha=original.getchannel('A');new_alpha=image.getchannel('A')
            if old_alpha.getextrema()[0]==0 and new_alpha.getextrema()[0]!=0:raise ValueError('Transparent artwork background was flattened: '+row['file'])
            texture.set_image(image,target_format=4,mipmap_count=max(1,int(getattr(texture,'m_MipCount',1) or 1)))
            texture.save()
            expected[ident]=pixel_hash(image)
        log('Artwork replaced: '+row['path'])
    return expected

def verify_replacements(objects,expected):
    for ident,expected_hash in expected.items():
        texture=objects[ident].read()
        if int(texture.m_TextureFormat)!=4 or pixel_hash(texture.image)!=expected_hash:raise ValueError('Rebuilt artwork failed pixel verification: '+str(ident))
