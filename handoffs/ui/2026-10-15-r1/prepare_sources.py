from pathlib import Path
import json,hashlib
r=Path(__file__).resolve().parent
s=json.loads((r/'CURRENT_STATE.json').read_text());d=r/s['source_root'];assert d.is_dir()
for x in json.loads((r/'LARGE_SOURCE_PARTS.json').read_text())['items']:
 p=r/x['path']
 if p.exists():continue
 data=b''
 for part in x['parts']:
  b=(r/part['path']).read_bytes();assert len(b)==part['size'] and hashlib.sha256(b).hexdigest()==part['sha256'];data+=b
 assert len(data)==x['size'] and hashlib.sha256(data).hexdigest()==x['sha256']
 p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
print(json.dumps({'status':'sources_ready','source_root':str(d),'game_engine_run':False}))
