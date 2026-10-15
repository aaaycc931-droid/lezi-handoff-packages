from pathlib import Path
import json,hashlib
p=Path(__file__).resolve().parent
m=json.loads((p/'SHA256_MANIFEST.json').read_text())
for name,digest in m.items():
 assert hashlib.sha256((p/name).read_bytes()).hexdigest()==digest,name
s=json.loads((p/'CURRENT_STATE.json').read_text())
d=json.loads((p/'CONFIRMED_DELTA.json').read_text())
assert s['new_rule_confirmations']==d['count']==len(d['decisions'])==21
assert s['new_engine_tests']==s['new_code_changes']==0
assert s['M04_status']=='proposal_pending_user_confirmation'
print(json.dumps({'passed':True,'hashes_checked':len(m),'scope':'document_and_source_integrity_only','new_engine_tests':0}))
