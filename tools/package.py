"""Build a standalone Windows folder and ZIP from this checkout."""
import hashlib,json,os,pathlib,shutil,site,sys,zipfile
ROOT=pathlib.Path(__file__).resolve().parents[1];os.chdir(ROOT)
# Keep build caches in the checkout and avoid inaccessible user-site paths.
os.environ['PYINSTALLER_CONFIG_DIR']=str(ROOT/'.build/pyinstaller-cache')
site.USER_SITE=str(ROOT/'.build/user-site');site.getusersitepackages=lambda:site.USER_SITE
from PyInstaller.__main__ import run
run(['--noconfirm','--windowed','--onedir','--name','Mobius-English-Patcher','--distpath','.build/frozen','--workpath','.build/pyinstaller','--specpath','.build','--collect-all','UnityPy','--collect-all','texture2ddecoder','--collect-all','etcpak','--collect-all','astc_encoder','--collect-all','archspec','patcher.py'])
out=ROOT/'dist/Mobius-Theory-English';out.mkdir(parents=True,exist_ok=True)
shutil.copytree(ROOT/'.build/frozen/Mobius-English-Patcher',out,dirs_exist_ok=True)
for filename in ['patcher.py','artwork_support.py','TextPatch.cs','manifest.json','translations.json','Translation-Review.csv','README.md','LICENSE','CONTRIBUTING.md','requirements.txt','THIRD-PARTY-NOTICES.txt']:
    shutil.copy2(ROOT/filename,out/filename)
for folder in ['subtitles','licenses','docs','tools','artwork']:
    shutil.copytree(ROOT/folder,out/folder,dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
for filename in ['TextPatch.exe','Mono.Cecil.dll']:shutil.copy2(ROOT/'.build'/filename,out/filename)
archive=ROOT/'dist/Mobius-Theory-English.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for file in sorted(out.rglob('*')):
        if file.is_file() and '__pycache__' not in file.parts:z.write(file,pathlib.Path(out.name)/file.relative_to(out))
with zipfile.ZipFile(archive) as z:
    if z.testzip() is not None:raise RuntimeError('ZIP verification failed.')
checksum=hashlib.sha256(archive.read_bytes()).hexdigest()
(ROOT/'dist/SHA256SUMS.txt').write_text(checksum+'  '+archive.name+'\n',encoding='ascii')
(ROOT/'dist/build-info.json').write_text(json.dumps({'python':sys.version,'version':json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))['version'],'sha256':checksum},indent=2),encoding='utf-8')
print('Built',archive)
