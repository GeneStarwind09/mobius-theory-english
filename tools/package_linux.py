"""Build a native x86-64 Linux installer with no system Python/.NET dependency."""
import hashlib,json,os,pathlib,platform,shutil,sys,tarfile
ROOT=pathlib.Path(__file__).resolve().parents[1];os.chdir(ROOT)
if not sys.platform.startswith('linux') or platform.machine() not in ('x86_64','AMD64'):
    raise SystemExit('Build this package on x86-64 Linux.')
os.environ['PYINSTALLER_CONFIG_DIR']=str(ROOT/'.build/linux/pyinstaller-cache')
from PyInstaller.__main__ import run
run(['--noconfirm','--onedir','--name','Mobius-English-Patcher','--distpath','.build/linux/frozen',
     '--workpath','.build/linux/pyinstaller','--specpath','.build/linux',
     '--collect-all','UnityPy','--collect-all','fmod_toolkit','--collect-all','texture2ddecoder',
     '--collect-all','etcpak','--collect-all','astc_encoder','--collect-all','archspec','--collect-all','bsdiff4','patcher.py'])
out=ROOT/'dist/Mobius-Theory-English-Linux';out.mkdir(parents=True,exist_ok=True)
shutil.copytree(ROOT/'.build/linux/frozen/Mobius-English-Patcher',out,dirs_exist_ok=True)
for name in ['patcher.py','platform_support.py','managed_support.py','managed-patch.json','artwork_support.py',
             'layout_support.py','font_support.py','layout.json','manifest.json','translations.json','README.md',
             'LICENSE','THIRD-PARTY-NOTICES.txt','requirements.txt','TextPatch.cs','EnglishWrap.cs']:
    shutil.copy2(ROOT/name,out/name)
for folder in ['artwork','subtitles','licenses','docs','tools']:
    shutil.copytree(ROOT/folder,out/folder,dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
shutil.copy2(ROOT/'docs/LINUX.md',out/'START-HERE-LINUX.md')
launcher=out/'Launch-Patcher.sh'
launcher.write_text('#!/bin/sh\nset -eu\ncd -- "$(dirname -- "$0")"\nexec ./Mobius-English-Patcher "$@"\n',encoding='utf-8')
launcher.chmod(0o755);(out/'Mobius-English-Patcher').chmod(0o755)
assert (out/'Mobius-English-Patcher').read_bytes()[:4]==b'\x7fELF'
archive=ROOT/'dist/Mobius-Theory-English-Linux-x86_64-v1.0.0.tar.gz'
with tarfile.open(archive,'w:gz',compresslevel=6) as t:t.add(out,arcname=out.name)
checksum=hashlib.sha256(archive.read_bytes()).hexdigest()
(ROOT/'dist/LINUX-SHA256SUMS.txt').write_text(checksum+'  '+archive.name+'\n',encoding='ascii')
(ROOT/'dist/linux-build-info.json').write_text(json.dumps({'version':'1.0.0','platform':'Linux x86_64',
    'python':sys.version,'build_libc':platform.libc_ver(),'source_commit':os.environ.get('GITHUB_SHA'),
    'artwork_textures':189,'native_gameplay_test':'pending owner Steam Machine test','sha256':checksum},indent=2),encoding='utf-8')
print('Built',archive)
