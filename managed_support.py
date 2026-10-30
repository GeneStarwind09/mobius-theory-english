"""Apply a verified BSDIFF delta to the owner's original managed assembly."""
import base64,hashlib,json,pathlib


def sha(data):return hashlib.sha256(data).hexdigest()


def apply_managed_delta(source,destination,base,manifest):
    path=pathlib.Path(base)/'managed-patch.json';raw=path.read_bytes()
    if sha(raw)!=manifest['managed'].get('portable_patch_sha256'):
        raise ValueError('Portable assembly patch hash mismatch.')
    recipe=json.loads(raw.decode('utf-8'))
    if recipe.get('schema')!=1 or recipe.get('format')!='BSDIFF40':raise ValueError('Unsupported portable assembly patch.')
    original=pathlib.Path(source).read_bytes()
    if sha(original)!=manifest['managed']['original_sha256'] or sha(original)!=recipe['original_sha256']:
        raise ValueError('Unsupported original managed assembly.')
    patch=base64.b64decode(recipe['patch_base64'],validate=True)
    if sha(patch)!=recipe['patch_sha256']:raise ValueError('Portable patch data is corrupt.')
    import bsdiff4
    english=bsdiff4.patch(original,patch)
    if len(english)!=recipe['english_size'] or sha(english)!=recipe['english_sha256']:
        raise ValueError('Portable assembly output failed verification.')
    pathlib.Path(destination).write_bytes(english)
