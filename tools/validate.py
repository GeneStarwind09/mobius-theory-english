"""Validate distributed translation payloads; no game or network access needed."""
import argparse,hashlib,json,pathlib,re
ROOT=pathlib.Path(__file__).resolve().parents[1]
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def run(refresh=False):
    path=ROOT/'manifest.json';manifest=json.loads(path.read_text(encoding='utf-8'));mapping=json.loads((ROOT/'translations.json').read_text(encoding='utf-8'))
    if refresh:
        manifest['translations_sha256']=sha(ROOT/'translations.json')
        for name,row in manifest['subtitles'].items():row['english_sha256']=sha(ROOT/'subtitles'/name)
        path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    assert sha(ROOT/'translations.json')==manifest['translations_sha256'],'Translation dictionary hash mismatch.'
    if manifest['managed'].get('portable_patch_sha256'):
        recipe_path=ROOT/'managed-patch.json'
        assert sha(recipe_path)==manifest['managed']['portable_patch_sha256'],'Portable assembly patch hash mismatch.'
        recipe=json.loads(recipe_path.read_text(encoding='utf-8'))
        assert recipe['original_sha256']==manifest['managed']['original_sha256']
        assert recipe['translation_sha256']==sha(ROOT/'translations.json'),'Regenerate the portable assembly patch after translation changes.'
    for source,english in mapping.items():
        assert sorted(re.findall(r'\{\d+\}',source))==sorted(re.findall(r'\{\d+\}',english)),source
        assert sorted(re.findall(r'</?color[^>]*>',source))==sorted(re.findall(r'</?color[^>]*>',english)),source
        if re.match(r'^\d+\|\d+\|',source):assert source.split('|')[:2]==english.split('|')[:2],source
    total=0
    for name,row in manifest['subtitles'].items():
        file=ROOT/'subtitles'/name;assert sha(file)==row['english_sha256'],name
        text=file.read_text(encoding='utf-8-sig');assert not re.search('[\u3400-\u9fff]',text),name
        blocks=re.split(r'\n\s*\n',text.strip());assert len(blocks)==row['english_cues'],name
        last=0
        for i,block in enumerate(blocks,1):
            lines=block.splitlines();assert int(lines[0])==i
            a,b=lines[1].split(' --> ')
            def ms(value):
                h,m,s,z=map(int,re.split('[:,]',value));return ((h*60+m)*60+s)*1000+z
            start,end=ms(a),ms(b);assert start>=last and end>start;last=end
            assert 1<=len(lines[2:])<=2 and all(len(x)<=42 for x in lines[2:]),(name,i)
            assert len(' '.join(lines[2:]))/((end-start)/1000)<=25,(name,i)
        total+=len(blocks)
    from importlib.util import spec_from_file_location,module_from_spec
    spec=spec_from_file_location('artwork_support',ROOT/'artwork_support.py');module=module_from_spec(spec);spec.loader.exec_module(module)
    artwork=module.load_replacements(ROOT,manifest)
    print(f'Validated {total} subtitle cues, {len(mapping)} dictionary entries and {len(artwork)} artwork replacements.')
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--refresh-hashes',action='store_true');args=parser.parse_args();run(args.refresh_hashes)
