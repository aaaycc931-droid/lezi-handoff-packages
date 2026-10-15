from pathlib import Path
import json,re,hashlib
ROOT=Path(__file__).resolve().parent
index=json.loads((ROOT/'MECHANISM_SOURCE_INDEX.json').read_text())
results=[]
def check(name,condition,scope='document_and_source_verification'):
    results.append({'check':name,'passed':bool(condition),'scope':scope})
for sid,s in index['sources'].items():
    p=ROOT/s['path']
    check('accessible:'+sid,p.is_file())
    check('sha256:'+sid,p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest()==s['sha256'])
for row in index['mechanisms']:
    src=index['sources'][row['primary_source']['source_id']]
    lines=(ROOT/src['path']).read_text().splitlines()
    check('range:'+row['mechanism_id'],1<=row['primary_source']['start_line']<=row['primary_source']['end_line']<=len(lines))
    for sid in row.get('authority_chain',[]):check('chain:'+row['mechanism_id']+':'+sid,sid in index['sources'])
check('30_primary_mechanisms', {r['mechanism_id'] for r in index['mechanisms'] if re.fullmatch(r'H\d\d|M\d\d|D01',r['mechanism_id'])}=={f'H{i:02d}' for i in range(1,22)}|{f'M{i:02d}' for i in range(1,9)}|{'D01'})
check('5_H21_forms',sum(r['mechanism_id'].startswith('H21.') for r in index['mechanisms'])==5)
old=(ROOT/'evidence/dispatched_reference/02_CURRENT_HEROES.md').read_text()
new=(ROOT/'current/02_CURRENT_HEROES.md').read_text()
def blocks(text):return {m.group(1):m.group(0) for m in re.finditer(r'^## (H\d\d) .*?(?=^## H\d\d |^## 形态与实现|\Z)',text,re.M|re.S)}
ob,nb=blocks(old),blocks(new)
for hid,txt in ob.items():
    if hid!='H15':check('unchanged_nonH15:'+hid,nb[hid]==txt)
h=nb['H15']
for phrase in ['每局最多启动一次','原始真实红/黑阵营','不读取M07当前秘密阵营','天空上将本人和对手','控制权变化本身不取消培养','成为对手控制','不自动重征','回溯及其他棋盘重置不恢复','半混乱H11×H15','保留稳定棋子本体绑定','同兵种重新绑定','第一次培养计数点','仍待明确']:
    check('H15_semantic_anchor:'+phrase,phrase in h)
check('cost_preserved','兵2／士2／象3／马5／炮6／车6' in h)
check('no_blanket_history_reactivation','不将整份旧稿无条件恢复为当前规则' in h)
for n in ['01_CURRENT_RULES.md','03_CURRENT_MUTATIONS.md','09_CURRENT_GAME_MODES.md']:
    check('unchanged_shared:'+n,(ROOT/'current'/n).read_bytes()==(ROOT/'evidence/dispatched_reference'/n).read_bytes())
m=json.loads((ROOT/'MODE_CONSUMPTION.json').read_text())
check('all_three_mode_core',{*m['modes']}=={'original_jieqi','standard_xiangqi','half_chaos'} and all(r['design_confirmed'] and not r['engine_synced'] and not r['sent_to_dialogue'] for r in m['modes'].values()))
e=json.loads((ROOT/'ERROR_RECOVERY_RECORD.json').read_text())
check('scoring_frozen_and_no_code_change',e['formal_scoring']=='frozen' and e['empirical_n']==0 and not e['repository_or_runtime_modified'] and not e['runtime_tests_run'])
check('original09_exact_hash', index['sources']['H15:ORIGINAL-20261005']['sha256']=='dd0405e911bf822b6f99af06ad967a338c63ebfe17068934378ff258b4c2676e')
check('full_history_not_falsely_proven',all(not r.get('full_historical_completeness_proven',True) for r in index['mechanisms']))
v={'status':'passed' if all(r['passed'] for r in results) else 'failed','checks':len(results),'failed':[r for r in results if not r['passed']],'verification_type':'source_and_document_only; no gameplay runtime or independent model verification','results':results}
(ROOT/'VERIFICATION_RESULTS.json').write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v[k] for k in ['status','checks','failed','verification_type']},ensure_ascii=False))
if v['status']!='passed':raise SystemExit(1)
