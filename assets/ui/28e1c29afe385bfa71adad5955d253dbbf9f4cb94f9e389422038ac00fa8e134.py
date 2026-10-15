import pathlib,json,hashlib,sys
root=pathlib.Path(__file__).resolve().parent.parent
manifest=json.loads((root/'PACKAGE_MANIFEST.json').read_text());bad=[]
for e in manifest['files']:
 p=root/e['path']
 if not p.is_file() or p.stat().st_size!=e['bytes'] or hashlib.sha256(p.read_bytes()).hexdigest()!=e['sha256']:bad.append(e['path'])
print(json.dumps({'checked':len(manifest['files']),'bad':bad,'passed':not bad}))
sys.exit(1 if bad else 0)
