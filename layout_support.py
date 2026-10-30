"""Apply narrowly identified English layout changes and verify their full trees."""
import hashlib,json,pathlib

def load_layout(base, manifest):
    path=pathlib.Path(base)/'layout.json'
    if not path.exists():return []
    data=json.loads(path.read_text(encoding='utf-8'))
    if data.get('schema')!=1 or data.get('original_bundle_sha256')!=manifest['bundle']['original_sha256']:
        raise ValueError('Layout manifest is for an unsupported original bundle.')
    rows=data['objects'];ids=[row['id'] for row in rows]
    if len(set(ids))!=len(ids):raise ValueError('Duplicate layout object ID.')
    return rows

def validate_originals(objects, rows):
    for row in rows:
        obj=objects[row['id']]
        if hashlib.sha256(obj.get_raw_data()).hexdigest()!=row['original_sha256']:
            raise ValueError('Original layout identity mismatch: '+row['path'])

def apply_layout(objects, rows, translated_trees=None):
    expected={}
    translated_trees=translated_trees or {}
    for row in rows:
        obj=objects[row['id']]
        tree=translated_trees.get(row['id'])
        if tree is None:tree=obj.read_typetree()
        for operation in row['set']:
            keys=operation['field'].split('.');parent=tree
            for key in keys[:-1]:parent=parent[key]
            if keys[-1] not in parent:raise ValueError('Unknown layout field: '+operation['field'])
            value=operation['value']
            encoding=operation.get('encoding')
            if encoding=='hex':
                if not isinstance(parent[keys[-1]],bytes):raise ValueError('Binary layout field expected: '+operation['field'])
                value=bytes.fromhex(value)
            elif encoding is not None:raise ValueError('Unknown layout value encoding.')
            parent[keys[-1]]=value
        # UnityPy readers retain the original stream after save_typetree.
        # Compare the serialized replacement bytes, including float32 encoding.
        expected[obj.path_id]=obj.save_typetree(tree)
    return expected

def verify_layout(objects, expected):
    for ident,data in expected.items():
        if objects[ident].get_raw_data()!=data:raise ValueError('Rebuilt layout object failed verification: '+str(ident))
