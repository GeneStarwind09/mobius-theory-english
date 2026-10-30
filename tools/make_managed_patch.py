"""Generate a portable delta from original and approved Windows output assemblies.

No full game assembly is distributed. Regenerate after assembly translation changes.
"""
import argparse,base64,hashlib,json,pathlib


def sha(data):return hashlib.sha256(data).hexdigest()


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--original',required=True);parser.add_argument('--english',required=True)
    parser.add_argument('--root',default=str(pathlib.Path(__file__).resolve().parents[1]));args=parser.parse_args()
    import bsdiff4
    root=pathlib.Path(args.root);manifest=json.loads((root/'manifest.json').read_text(encoding='utf-8'))
    original=pathlib.Path(args.original).read_bytes();english=pathlib.Path(args.english).read_bytes()
    if sha(original)!=manifest['managed']['original_sha256']:raise ValueError('Unsupported original assembly.')
    patch=bsdiff4.diff(original,english)
    assert bsdiff4.patch(original,patch)==english
    recipe={'schema':1,'format':'BSDIFF40','original_sha256':sha(original),'english_sha256':sha(english),
        'english_size':len(english),'patch_sha256':sha(patch),'patch_base64':base64.b64encode(patch).decode('ascii'),
        'generated_by':'tools/make_managed_patch.py; bsdiff4 1.4.0',
        'translation_sha256':sha((root/'translations.json').read_bytes()),
        'TextPatch_cs_sha256':sha((root/'TextPatch.cs').read_bytes()),'EnglishWrap_cs_sha256':sha((root/'EnglishWrap.cs').read_bytes())}
    raw=(json.dumps(recipe,indent=2)+'\n').encode('utf-8');(root/'managed-patch.json').write_bytes(raw)
    manifest['managed']['portable_patch_sha256']=sha(raw)
    (root/'manifest.json').write_bytes((json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
    print('Verified portable assembly delta:',len(patch),'bytes; English SHA256',sha(english))


if __name__=='__main__':main()
