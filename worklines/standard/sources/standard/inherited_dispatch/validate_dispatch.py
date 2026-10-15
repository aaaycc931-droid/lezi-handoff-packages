from pathlib import Path
import json,hashlib,zipfile
r=Path(__file__).resolve().parent
m=json.loads((r/'MANIFEST.json').read_text())
actual={p.relative_to(r).as_posix() for p in r.rglob('*') if p.is_file()}
assert actual==set(m['files'])|{'MANIFEST.json'}
for n,h in m['files'].items(): assert hashlib.sha256((r/n).read_bytes()).hexdigest()==h,n
s=json.loads((r/'RESUME_STATE.json').read_text())
assert s['new_engine_tests_run']==0 and s['scoring']['frozen']
assert s['external_dialogue_received'] is False
assert (r/'collaboration/X_Collaboration_Integrated_Candidate_2026-10-13-1.md').read_text().find('2026-10-14.v0.8')>=0
assert hashlib.sha256((r/'baseline/audit/integrity/evidence/historical/2026-10-05/09_CONFIRMED_DESIGN_SKY_GENERAL.md').read_bytes()).hexdigest()=='dd0405e911bf822b6f99af06ad967a338c63ebfe17068934378ff258b4c2676e'
for n in ['baseline/inputs/lezi-standard-design-closeout-2026-10-13.zip','baseline/inputs/lezi-half-chaos-design-closeout-2026-10-13.zip']:
 with zipfile.ZipFile(r/n) as z: assert z.testzip() is None
print(json.dumps({'passed':True,'file_hashes_checked':len(m['files']),'scope':'dispatch_document_and_source_integrity_only','new_engine_tests':0}))
