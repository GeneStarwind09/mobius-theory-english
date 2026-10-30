"""Retrieve the immutable, hash-verified v1.0.0 artwork payload for source builds."""
import hashlib,pathlib,urllib.request,zipfile
ROOT=pathlib.Path(__file__).resolve().parents[1]
URL='https://github.com/GeneStarwind09/mobius-theory-english/releases/download/v1.0.0/Mobius-Theory-English-Artwork-v1.0.0.zip'
EXPECTED='2c8754ee31b70520a941c2ff09d904bf1d30ecb67eeb1f93fc3b4d0c801fffb4'
dest=ROOT/'.build/release-artwork.zip';dest.parent.mkdir(parents=True,exist_ok=True)
if not dest.exists():urllib.request.urlretrieve(URL,dest)
if hashlib.sha256(dest.read_bytes()).hexdigest()!=EXPECTED:raise ValueError('Release artwork archive hash mismatch.')
with zipfile.ZipFile(dest) as z:
    for entry in z.infolist():
        p=pathlib.PurePosixPath(entry.filename)
        if p.is_absolute() or '..' in p.parts or not p.parts or p.parts[0]!='artwork':raise ValueError('Unsafe artwork archive path.')
        if entry.is_dir() or p.name=='README.md':continue
        path=ROOT.joinpath(*p.parts);path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(z.read(entry))
print('Verified release artwork downloaded and extracted.')
