from pathlib import Path
import urllib.request,json,hashlib,zipfile,io
BASE="https://raw.githubusercontent.com/aaaycc931-droid/lezi-handoff-packages/main/"
MANIFEST="packages/lezi-ui-dispatch-2026-10-13.parts/PARTS.json"
def get(path):
    with urllib.request.urlopen(BASE+path,timeout=120) as response:return response.read()
m=json.loads(get(MANIFEST))
chunks=[]
for part in m["parts"]:
    data=get(part["path"])
    if len(data)!=part["bytes"] or hashlib.sha256(data).hexdigest()!=part["sha256"]:raise RuntimeError("Part checksum failed")
    chunks.append(data)
data=b"".join(chunks)
if len(data)!=m["reconstructed_bytes"] or hashlib.sha256(data).hexdigest()!=m["reconstructed_sha256"]:raise RuntimeError("Archive checksum failed")
with zipfile.ZipFile(io.BytesIO(data)) as archive:
    if archive.testzip() is not None:raise RuntimeError("ZIP integrity failed")
target=Path(m["reconstructed_file_name"])
target.write_bytes(data)
print("Restored and verified: "+str(target))
