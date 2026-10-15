from PIL import Image
import pathlib,json,hashlib
p=pathlib.Path(__file__).resolve().parent
for name in ['old-text-mask.png','allowed-mask.png']:Image.open(p/'evidence'/name).convert('L').save(p/'evidence'/name)
def chunks(data):
 off=8
 while off<len(data):
  length=int.from_bytes(data[off:off+4],'big');yield data[off+4:off+8],data[off:off+length+12];off+=length+12
types=[b'cHRM',b'gAMA',b'sRGB',b'iCCP',b'pHYs'];keep=[c for t,c in chunks((p/'source/approved-B3-v1.png').read_bytes()) if t in types]
f=p/'preview/lezi-bluetooth-B4-v1.png';data=f.read_bytes();out=data[:8]
for t,c in chunks(data):
 if t in types:continue
 out+=c
 if t==b'IHDR':out+=b''.join(keep)
f.write_bytes(out);ev=p/'evidence/revision.json';d=json.loads(ev.read_text());d['output_sha256']=hashlib.sha256(out).hexdigest();ev.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
