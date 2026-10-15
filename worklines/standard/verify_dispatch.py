from pathlib import Path
import hashlib,json
r=Path(__file__).resolve().parent
m=json.loads((r/'PUBLISHED_FILES.json').read_text())
for x in m['files']:
 p=r/x['path'];assert p.is_file(),x['path'];b=p.read_bytes();assert len(b)==x['size'] and hashlib.sha256(b).hexdigest()==x['sha256'],x['path']
s=json.loads((r/'CURRENT_STATE.json').read_text());assert s['scoring']['frozen'] and s['new_game_engine_tests']==0
assert json.loads((r/'PENDING_DECISION.json').read_text())['status']=='pending'
for p in s['required_files']:assert (r/p).is_file(),p
assert (r/s['source_root']).is_dir()
print(json.dumps({'status':'passed','files':len(m['files']),'game_engine_tests':0,'scope':'published_project_file_integrity'}))
