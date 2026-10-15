from pathlib import Path
import hashlib,json,re,subprocess,sys,zipfile
root=Path(__file__).resolve().parent
manifest=json.loads((root/'MANIFEST.json').read_text())
files={p.relative_to(root).as_posix():p for p in root.rglob('*') if p.is_file() and p!=root/'MANIFEST.json'}
assert set(files)==set(manifest['files']), 'package member mismatch'
for name,p in files.items():
 data=p.read_bytes();record=manifest['files'][name]
 assert len(data)==record['size_bytes'] and hashlib.sha256(data).hexdigest()==record['sha256'], name
s=json.loads((root/'CURRENT_STATE.json').read_text());c=json.loads((root/'CONFIRMATIONS.json').read_text())
assert s['status']=='round_closed_design_work_partial_adaptation_engine_unrun'
assert s['new_user_rule_confirmations']==c['new_user_rule_confirmations']==5
assert len(c['local_confirmations'])==3 and len(c['direct_shared_confirmations'])==2
assert s['engine_tests_run']==0 and s['engine_tests_passed'] is None and s['code_changes']==0
assert not s['full_mode_verified'] and not s['main_sent'] and not s['main_received_verified'] and not s['main_adopted_verified']
assert s['scoring']['frozen'] and s['scoring']['n']==0 and not s['scoring']['featuresReady']
assert all(s['scoring'][k] is None for k in ['q','H','I','B','J'])
md=(root/s['working_document']).read_text();working=json.loads(re.search('```json'+chr(10)+'(.*?)'+chr(10)+'```',md,re.S).group(1))
assert working['revision']==s['working_document_revision']
assert working['local_confirmation_records']==c['local_confirmations']
assert working['direct_shared_confirmation_records']==c['direct_shared_confirmations']
subprocess.run([sys.executable,str(root/'input_dispatch/validate_dispatch.py')],check=True)
archive=root.parent/(root.name+'.zip')
if archive.exists():
 with zipfile.ZipFile(archive) as z:
  expected=set(files)|{'MANIFEST.json'}
  assert set(z.namelist())==expected and len(z.namelist())==len(expected)
  for name in expected: assert z.read(name)==(root/name).read_bytes(),name
print(f'Validated {len(files)} hashed package files; JSON and read-only input invariants hold. Archive bytes match when present. Product/engine tests: 0.')
