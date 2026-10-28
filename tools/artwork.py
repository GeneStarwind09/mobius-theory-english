"""Export original Unity textures and prepare verified PNG replacements.

Original artwork is for the owner's local editing workflow, not this repository.
No game file is changed by this tool.
"""
from __future__ import annotations
import argparse,collections,hashlib,html,json,pathlib,re,shutil,sys
from PIL import Image,ImageDraw,ImageFont
import UnityPy

BUNDLE_REL='轮回之理_Data/StreamingAssets/Bundles/gamebundle'
REPO=pathlib.Path(__file__).resolve().parents[1]

def sha(path):return hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()
def pixels(image):return hashlib.sha256(image.convert('RGBA').tobytes()).hexdigest()
def read(path):return json.loads(pathlib.Path(path).read_text(encoding='utf-8'))
def write(path,value):pathlib.Path(path).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def within(root,rel):
    path=(root/rel).resolve()
    if root.resolve() not in path.parents:raise ValueError('Path escapes its root: '+rel)
    return path

def original_bundle(game):
    game=pathlib.Path(game).resolve();backup=game/'.mobius-english/original'/BUNDLE_REL
    source=backup if backup.is_file() else game/BUNDLE_REL
    expected=read(REPO/'manifest.json')['bundle']['original_sha256']
    if sha(source)!=expected:raise ValueError('Unsupported original Unity bundle.')
    return source

def export(game,out,include_effects=False):
    source=original_bundle(game);out=pathlib.Path(out).resolve()
    if (out/'assets.json').exists():raise ValueError('An asset pack already exists here. Choose a new output folder.')
    out.mkdir(parents=True,exist_ok=True)
    env=UnityPy.load(source.read_bytes());paths=collections.defaultdict(list)
    for path,obj in env.container.items():
        if obj.type.name=='Texture2D':paths[obj.path_id].append(path)
    assets=[];skipped=[];empty=[];technical=[]
    for obj in env.objects:
        if obj.type.name!='Texture2D':continue
        path=sorted(paths.get(obj.path_id,[f'unlisted/{obj.path_id}']))[0]
        if '/fonts/' in path or obj.path_id not in paths:
            technical.append({'id':str(obj.path_id),'path':path});continue
        animation='/effects/' in path or '/turnsplaysprite/' in path
        if animation and not include_effects:
            skipped.append({'id':str(obj.path_id),'path':path});continue
        texture=obj.read()
        stream=getattr(texture,'m_StreamData',None)
        if texture.m_Width<=0 or texture.m_Height<=0 or (not texture.image_data and (stream is None or not stream.size)):
            empty.append({'id':str(obj.path_id),'path':path,'name':texture.m_Name});continue
        try:image=texture.image.convert('RGBA')
        except Exception as exc:raise RuntimeError(f'Cannot decode texture {obj.path_id} {path}: {exc}') from exc
        short=path.split('/textures/')[-1] if '/textures/' in path else path
        short_path=pathlib.PurePosixPath(short)
        filename=short_path.stem+'__'+str(obj.path_id)+'.png'
        relative=str(short_path.parent/filename)
        original=within(out,'originals/'+relative);original.parent.mkdir(parents=True,exist_ok=True)
        image.save(original)
        preview=within(out,'previews/'+relative);preview.parent.mkdir(parents=True,exist_ok=True)
        thumb=image.copy();thumb.thumbnail((360,220));thumb.save(preview)
        category=str(short_path.parent)
        priority='high' if category.startswith(('languages','commons','buttons','goods','stories','games/computerinvestigation','backgrounds/helps','unlisted')) else 'review'
        assets.append({'id':str(obj.path_id),'path':path,'name':texture.m_Name,'category':category,'priority':priority,'width':image.width,'height':image.height,'texture_format':int(texture.m_TextureFormat),'mip_count':getattr(texture,'m_MipCount',1),'file':'originals/'+relative,'preview':'previews/'+relative,'replacement':'replacements/'+relative,'png_sha256':sha(original),'pixels_sha256':pixels(image),'has_transparency':image.getextrema()[3][0]<255})
        if len(assets)%50==0:print('Exported',len(assets),'textures',flush=True)
    assets.sort(key=lambda a:(a['priority']!='high',a['category'],a['path']))
    manifest={'schema':1,'app_id':1925830,'bundle':BUNDLE_REL,'original_bundle_sha256':sha(source),'assets':assets,'excluded_animation_textures':skipped,'empty_texture_placeholders':empty,'excluded_technical_textures':technical}
    write(out/'assets.json',manifest);(out/'replacements').mkdir(exist_ok=True)
    make_index(out,assets);make_sheets(out,assets)
    (out/'START-HERE.md').write_text('''# Mobius Theory artwork editing pack

Open **index.html** to browse the full-resolution artwork by category. The default “High priority” view concentrates on labels, documents and likely text artwork. This is a candidate inventory, not an OCR-certified list: some images contain no text, and Chinese may also occur in other categories.

## Editing and returning

1. Open a full-resolution PNG from `originals/`. Do not edit a preview or contact sheet.
2. Ask your image editor to replace only the Chinese writing with English, preserve the design, and keep the exact canvas size and transparency. Avoid changing numbers, dates, diagrams, highlighted clue symbols, or puzzle answers. Some images are sprite sheets: keep every element in its original position.
3. Save edited PNGs under `replacements/`, retaining the same category folder and filename. For example, `originals/languages/name__ID.png` becomes `replacements/languages/name__ID.png`.
4. Return just the `replacements` folder (ZIP is fine) plus `assets.json`. You do not need to return the unchanged originals. A subset is fine; we can incorporate batches.
5. Include any intended wording in a text note if an AI image editor has mangled letters. Translations can be checked against the story glossary before release.

Each filename includes the actual Unity texture ID. `assets.json` records the asset path, dimensions and original hashes, so replacements can be verified and reinserted into the right texture. Pixel data must match the original dimensions; do not upscale, crop, rotate, or flatten transparent artwork onto a solid background. The importer rejects obviously flattened transparent backgrounds and changed transparent corners; partial transparency still needs visual review.

The source repository includes `tools/artwork.py prepare` to convert a returned batch into the patcher's optional artwork package. The PNGs are encoded into Unity textures losslessly as RGBA32; unchanged game textures and sprite positions remain untouched. Mip levels are regenerated when the original used them.

This pack contains original game artwork and story spoilers. It is a local working pack; it is excluded from the public source repository. Video frames and baked text within the movies are outside this pack. Animation/effect textures are omitted by default; the export tool can include them with `--include-effects` if a later inspection finds relevant text there.
''',encoding='utf-8')
    print(json.dumps({'textures':len(assets),'high_priority':sum(a['priority']=='high' for a in assets),'excluded_animation_textures':len(skipped),'categories':dict(collections.Counter(a['category'] for a in assets))},indent=2))

def make_index(out,assets):
    cards=[]
    for a in assets:
        text=html.escape(f"{a['category']} {a['name']} {a['id']} {a['path']}",quote=True)
        cards.append(f'''<article data-search="{text.lower()}" data-priority="{a['priority']}" data-category="{html.escape(a['category'],quote=True)}"><a href="{html.escape(a['file'],quote=True)}" target="_blank"><div class="image"><img loading="lazy" src="{html.escape(a['preview'],quote=True)}"></div></a><strong>{html.escape(a['category'])}/{html.escape(a['name'])}</strong><small>{a['width']} × {a['height']} · {a['priority']} priority</small><code>{a['id']}</code><a href="{html.escape(a['file'],quote=True)}" download>Full-resolution PNG</a></article>''')
    categories=''.join(f'<option>{html.escape(c)}</option>' for c in sorted({a['category'] for a in assets}))
    page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Mobius Theory artwork editing pack</title><style>body{font:16px system-ui;background:#111820;color:#edf1f5;margin:0}header{padding:28px;position:sticky;top:0;background:#17232ff5;z-index:2;border-bottom:1px solid #3d5367}h1{font-size:25px;margin:0 0 10px}p{max-width:1100px;line-height:1.6;margin:7px 0}a{color:#9ed9ff}input,select{font:inherit;padding:9px;border-radius:6px;border:1px solid #61758b;background:#233344;color:white;margin:10px 8px 0 0}input{width:330px}main{padding:24px;display:grid;grid-template-columns:repeat(auto-fill,minmax(270px,1fr));gap:18px}article{background:#1d2b38;padding:13px;border:1px solid #3b5265;border-radius:8px;overflow:hidden}.image{height:190px;display:grid;place-items:center;background:repeating-conic-gradient(#7b8490 0% 25%,#414954 0% 50%) 50%/20px 20px}.image img{max-width:100%;max-height:190px}strong,small,code{display:block;margin:9px 0;overflow-wrap:anywhere}small{color:#bfd0dd}code{font-size:12px}article[hidden]{display:none}#count{display:inline-block;margin:10px}</style><header><h1>Mobius Theory · artwork editing pack</h1><p>Open a full-resolution PNG, replace its Chinese text, and save it into <b>replacements/</b> with the same relative path and filename. Preserve dimensions, transparency, positions and puzzle clues. <a href="START-HERE.md">Editing instructions</a> · <a href="contact-sheets/">Contact sheets</a></p><input id="search" placeholder="Search category, filename or Unity ID"><select id="priority"><option value="high">High priority</option><option value="all">All extracted artwork</option></select><select id="category"><option value="all">All categories</option>'''+categories+'''</select><span id="count"></span></header><main>'''+''.join(cards)+'''</main><script>const cards=[...document.querySelectorAll('article')],search=document.querySelector('#search'),priority=document.querySelector('#priority'),category=document.querySelector('#category');function filter(){let count=0;for(const card of cards){const show=card.dataset.search.includes(search.value.toLowerCase())&&(priority.value==='all'||card.dataset.priority===priority.value)&&(category.value==='all'||card.dataset.category===category.value);card.hidden=!show;if(show)count++}document.querySelector('#count').textContent=count+' images'}[search,priority,category].forEach(x=>x.addEventListener('input',filter));filter()</script></html>'''
    (out/'index.html').write_text(page,encoding='utf-8')

def make_sheets(out,assets):
    folder=out/'contact-sheets';folder.mkdir(exist_ok=True)
    for start in range(0,len(assets),24):
        sheet=Image.new('RGB',(1600,1440),'#dde2e7');draw=ImageDraw.Draw(sheet)
        for i,a in enumerate(assets[start:start+24]):
            x=i%4*400;y=i//4*240
            with Image.open(out/a['preview']) as im:
                thumb=im.copy();thumb.thumbnail((380,175))
                sheet.paste(thumb,(x+(400-thumb.width)//2,y+8),thumb)
            draw.text((x+12,y+188),f"{a['category']}/{a['name']}"[:54],fill='black')
            draw.text((x+12,y+205),f"ID {a['id']}  {a['width']}x{a['height']}",fill='black')
        sheet.save(folder/f'{start//24+1:02}.jpg',quality=90)

def prepare(pack,edited,out):
    pack=pathlib.Path(pack).resolve();edited=pathlib.Path(edited).resolve();out=pathlib.Path(out).resolve()
    manifest=read(pack/'assets.json');bundle_hash=read(REPO/'manifest.json')['bundle']['original_sha256']
    if manifest['original_bundle_sha256']!=bundle_hash:raise ValueError('Artwork pack is for an unsupported game bundle.')
    known={a['replacement'].removeprefix('replacements/'):a for a in manifest['assets']}
    planned=[]
    for file in sorted(edited.rglob('*')):
        if not file.is_file():continue
        rel=file.relative_to(edited).as_posix()
        if file.suffix.lower()!='.png':raise ValueError('Unexpected non-PNG in replacements: '+rel)
        if rel not in known:raise ValueError('Unknown replacement filename: '+rel)
        a=known[rel]
        original=within(pack,a['file'])
        if sha(original)!=a['png_sha256']:raise ValueError('Original export was changed: '+a['file'])
        with Image.open(file) as im,Image.open(original) as source:
            im.load()
            if im.format!='PNG':raise ValueError('Replacement is not a PNG: '+rel)
            if im.size!=(a['width'],a['height']):raise ValueError('Canvas size changed: '+rel)
            if pixels(im)==a['pixels_sha256']:continue
            source_alpha=source.convert('RGBA').getchannel('A');alpha=im.convert('RGBA').getchannel('A')
            # Flattening transparent backgrounds corrupts UI sprites. Partial alpha may change around edited letters.
            if source_alpha.getextrema()[0]==0 and alpha.getextrema()[0]!=0:raise ValueError('Transparent background was flattened: '+rel)
            corners=[(0,0),(im.width-1,0),(0,im.height-1),(im.width-1,im.height-1)]
            if any(source_alpha.getpixel(pt)==0 and alpha.getpixel(pt)!=0 for pt in corners):raise ValueError('Transparent image corners became opaque: '+rel)
        planned.append((file,dict(a,file=rel,replacement_sha256=sha(file))))
    if not planned:raise ValueError('No changed PNG replacements found.')
    if (out/'manifest.json').exists():raise ValueError('An artwork package already exists in the output folder.')
    out.mkdir(parents=True,exist_ok=True)
    for file,a in planned:
        dest=within(out,a['file']);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(file,dest)
    write(out/'manifest.json',{'schema':1,'original_bundle_sha256':bundle_hash,'assets':[a for _,a in planned]})
    print('Prepared',len(planned),'verified artwork replacements.')

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='action',required=True)
    exp=sub.add_parser('export');exp.add_argument('--game',required=True);exp.add_argument('--out',required=True);exp.add_argument('--include-effects',action='store_true')
    pre=sub.add_parser('prepare');pre.add_argument('--pack',required=True);pre.add_argument('--edited',required=True);pre.add_argument('--out',required=True)
    args=parser.parse_args()
    if args.action=='export':export(args.game,args.out,args.include_effects)
    else:prepare(args.pack,args.edited,args.out)
