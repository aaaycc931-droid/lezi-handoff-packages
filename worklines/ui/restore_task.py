from pathlib import Path
import argparse,json,hashlib,urllib.request,os,shutil
from concurrent.futures import ThreadPoolExecutor

def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def safe(root,name):
 p=(root/name).resolve()
 if not p.is_relative_to(root.resolve()):raise ValueError('Unsafe asset path')
 return p
def main():
 root=Path(__file__).resolve().parent;ap=argparse.ArgumentParser()
 ap.add_argument('--task',default='B6');ap.add_argument('--target',type=Path,default=Path('ui-workbench'));ap.add_argument('--cache',type=Path);ap.add_argument('--check-only',action='store_true');ap.add_argument('--prefer-archive',action='store_true')
 a=ap.parse_args();task=json.loads((root/'TASKS.json').read_text())['tasks'][a.task]
 index_path=root/'../../assets/ui/INDEX.json'
 if index_path.is_file():index=json.loads(index_path.read_text())
 else:
  with urllib.request.urlopen('https://raw.githubusercontent.com/aaaycc931-droid/lezi-handoff-packages/main/assets/ui/INDEX.json',timeout=20) as r:index=json.load(r)
 target=a.target.resolve();base=target/'baseline';cache=(a.cache or target.parent/'ui-asset-cache').resolve()
 if a.check_only:
  for f in task['files']:
   p=safe(base,f['path'])
   if not p.is_file() or sha(p)!=f['asset_id']:raise ValueError('Missing or changed dependency '+f['path'])
  print(json.dumps({'status':'verified','files':len(task['files']),'network_asset_bytes':0}));return
 cache.mkdir(parents=True,exist_ok=True)
 def get(d):
  v=index['assets'][d];p=cache/d
  if p.is_file() and p.stat().st_size==v['bytes'] and sha(p)==d:return 0
  tmp=cache/(d+'.download');error=None
  urls=[v['fallback_url'],v['url']] if a.prefer_archive else [v['url'],v['fallback_url']]
  for url in urls:
   try:
    with urllib.request.urlopen(url,timeout=20) as r,tmp.open('wb') as f:shutil.copyfileobj(r,f)
    if tmp.stat().st_size!=v['bytes'] or sha(tmp)!=d:raise ValueError('Asset identity mismatch '+d)
    os.replace(tmp,p);return v['bytes']
   except Exception as e:error=e
  raise RuntimeError('Asset unavailable '+d+': '+str(error))
 with ThreadPoolExecutor(max_workers=4) as pool:transferred=sum(pool.map(get,task['asset_ids']))
 for f in task['files']:
  p=safe(base,f['path']);p.parent.mkdir(parents=True,exist_ok=True)
  if p.exists():
   if p.is_file() and sha(p)==f['asset_id']:continue
   raise ValueError('Preserve modified baseline before restore: '+str(p))
  try:os.link(cache/f['asset_id'],p)
  except OSError:shutil.copyfile(cache/f['asset_id'],p)
 (target/'work').mkdir(exist_ok=True)
 print(json.dumps({'status':'ready','task':a.task,'files':len(task['files']),'unique_assets':len(task['asset_ids']),'network_asset_bytes':transferred,'new_UI_candidate_created':False}))
if __name__=='__main__':main()
