from pathlib import Path
import copy
import hashlib
import json
import re
import sys
import zipfile

ROOT = Path(__file__).resolve().parent
CHECKS = []

def read(name):
    return json.loads((ROOT / name).read_text(encoding='utf-8-sig'))

def sha(data):
    return hashlib.sha256(data).hexdigest()

def check(name, condition, scope='document_state_and_source_check'):
    CHECKS.append({'check': name, 'passed': bool(condition), 'scope': scope})
    if not condition:
        raise AssertionError(name)

def section(text, ident):
    m = re.search(r'^## ' + re.escape(ident) + r'\b.*?(?=^## |\Z)', text, re.M | re.S)
    return m.group() if m else ''

def source_member(archive, member):
    with zipfile.ZipFile(ROOT / archive) as z:
        return z.read(member)

state = read('CURRENT_STATE.json')
sync = read('MODE_SYNC.json')
pending = read('PENDING_ITEMS.json')
current = read('rules/lezi-adjudication-reference-decision-2026-10-12.json')
old = read('history/ADJUDICATION_v1.21_READONLY.json')
check('round_closed_not_project_complete', state['status'] == 'round_closed_by_user' and state['closure_is_not_project_completion'])
check('no_automatic_work_or_messages', state['no_tasks_auto_started'] and state['no_messages_sent_to_other_dialogues'])
check('formal_scoring_frozen', state['scoring']['formal_status'] == 'frozen' and all(state['scoring'][k] is None for k in ['q','H','I','B','J']) and state['scoring']['independent_empirical_n'] == 0)
check('no_new_engine_execution_or_full_acceptance', state['verification_this_closeout']['new_engine_reexecution'] is False and state['verification_this_closeout']['independent_V3'] is False and state['scoring']['P1_qualified'] is False)
check('same_confirmed_adjudication_rule_objects', current['unified_adjudication_core'] == old['unified_adjudication_core'] and current['project_specific_confirmations'] == old['project_specific_confirmations'] and current['game_chase_base_review'] == old['game_chase_base_review'])
a = copy.deepcopy(current)
b = copy.deepcopy(old)
for item in [a,b]:
    for key in ['record_version','updated_at','session_closure']:
        item.pop(key, None)
    item['three_mode_adjudication_draft'].pop('session_status',None)
check('only_adjudication_closure_bookkeeping_changed', a == b)
check('GC01_to_GC04_preserved_as_confirmed', [x['id'] for x in current['game_chase_base_review']['cases']] == ['GC-01','GC-02','GC-03','GC-04'] and all(x['status'] == 'user_confirmed' for x in current['game_chase_base_review']['cases']))
check('dark_boundary_not_auto_approved', current['three_mode_adjudication_draft']['next_decision']['status'] == 'pending')
check('current_draft_session_closed', current['three_mode_adjudication_draft']['session_status'] == 'closed_by_user_total_closeout')

for mode, fields in sync['modes'].items():
    check('shared_scope_and_consumer:' + mode, fields['design_confirmed'] and fields['main_received'] and fields['mode_consumer_written_in_this_package'])
    check('external_delivery_and_engine_not_falsely_claimed:' + mode, not fields['sent_to_other_existing_dialogue_this_closeout'] and not fields['external_dialogue_read_or_adopt_verified'] and not fields['engine_implemented_or_synced_this_closeout'] and not fields['new_runtime_verified'])
check('single_shared_source_for_three_modes', len(sync['modes']) == 3 and len({x['shared_source'] for x in sync['modes'].values()}) == 1)

heroes = (ROOT/'rules/shared/02_CURRENT_HEROES.md').read_text()
base_heroes = (ROOT/'audit/integrity/current/02_CURRENT_HEROES.md').read_text()
h10 = section(heroes,'H10')
h15 = section(heroes,'H15')
check('F1_first_own_turn_optional_and_no_bypass', all(x in h10 for x in ['第一个己方正式回合','正常主行动前','玩家可以不发动','第二次不能绕过第一次','原揭棋、普通象棋、半混乱揭棋']))
check('F1_preserves_existing_Flow', h10[h10.index('### 【流】'):] == section(base_heroes,'H10')[section(base_heroes,'H10').index('### 【流】'):])
check('H15_training_core_and_M07_history_present', all(x in h15 for x in ['每局最多启动一次','原始真实红/黑阵营','不读取M07当前秘密阵营','控制权变化本身不取消培养','不自动重征','回溯及其他棋盘重置不恢复','保留稳定棋子本体绑定']))
check('H15_costs_and_privacy_boundaries_preserved', all(x in h15 for x in ['兵2／士2／象3／马5／炮6／车6','天空上将本人和对手','历史稿允许培养进度','第一次培养计数点']))
for i in range(1,22):
    ident=f'H{i:02d}'
    if ident not in ['H10','H15']:
        check('other_hero_section_unchanged:' + ident, section(heroes,ident) == section(base_heroes,ident))
check('H15_only_provenance_path_adjusted_from_recovery', section(heroes,'H15') == section(base_heroes,'H15').replace('evidence/historical/2026-10-05/09_CONFIRMED_DESIGN_SKY_GENERAL.md','../../audit/integrity/evidence/historical/2026-10-05/09_CONFIRMED_DESIGN_SKY_GENERAL.md'))
check('mutations_no_unapproved_delta', (ROOT/'rules/shared/03_CURRENT_MUTATIONS.md').read_bytes() == (ROOT/'audit/integrity/current/03_CURRENT_MUTATIONS.md').read_bytes())
original09 = (ROOT/'audit/integrity/evidence/historical/2026-10-05/09_CONFIRMED_DESIGN_SKY_GENERAL.md').read_bytes()
check('H15_complete_original_exact_bytes', sha(original09) == 'dd0405e911bf822b6f99af06ad967a338c63ebfe17068934378ff258b4c2676e', 'historical_source_byte_integrity')

std = read('modes/standard/CONFIRMED_DECISIONS.json')
raw_std = json.loads(source_member('inputs/lezi-standard-design-closeout-2026-10-13.zip','WORKING_DECISIONS_20261013.json'))
raw_active = [x for x in raw_std['decisions'] if not x.get('historical_only')]
check('all_current_standard_confirmations_carried', {x['id'] for x in std['decisions']} == {x['id'] for x in raw_active})
check('superseded_H10_S1_not_active', not any(x['id'] == 'H10-standard-host-S1' for x in std['decisions']))
for item in std['decisions']:
    if item['id'] != 'H10-standard-current-20261013':
        check('standard_confirmed_details_unchanged:' + item['id'], item == next(x for x in raw_active if x['id'] == item['id']))
    else:
        original = next(x for x in raw_active if x['id'] == item['id'])
        check('standard_H10_mechanics_unchanged', item['current_design'] == original['current_design'] and item['open_edges'] == original['open_edges'])
matrix = read('modes/standard/ADAPTATION_MATRIX.json')
rows = {x['id']:x for x in matrix['rows']}
check('standard_H15_shared_confirmed_mode_edges_pending', rows['H15']['adaptation_status'] == 'shared_core_confirmed_standard_specific_edges_pending')
check('standard_F1_current_receipt_consistent', '主线尚未收到' not in rows['H10']['standard_issue'] and rows['H10']['mainline_sync'] == 'main_bundle_source_synced')
hc = read('modes/half_chaos/CURRENT_STATE.json')
hc_interaction = (ROOT/'modes/half_chaos/HC_H11_H15_DESIGN.md').read_text()
check('HC_approved_B_and_stable_binding_preserved', all(x in hc_interaction for x in ['清除飞行并恢复为地面暗棋','同一稳定本体身份及全部累计培养进度保留','洗牌本身不产生一次额外培养回合','原候选A1','已否决']))
check('HC_progress_privacy_not_silently_changed', '累计进度/剩余回合历史允许公开' in hc_interaction and old.get('record_version') == '1.21' and 'H15-PROGRESS-VISIBILITY' in {x['id'] for x in pending['items']})
check('HC_stale_GC_not_current', hc['limits']['GC01_GC04'].startswith('confirmed_normal_revealed'))
check('unresolved_sources_not_auto_fixed', {'H15-START-EDGES','H20-HISTORY-COVERAGE','H10-F1-HISTORY','STATIC-H15-H20'}.issubset({x['id'] for x in pending['items']}))

index = read('RULE_SOURCE_INDEX.json')
check('30_subject_entries_not_full_history_proof', len(index['primary_mechanisms']) == 30 and all(not x['full_historical_completeness_proven'] for x in index['primary_mechanisms']))
for item in index['primary_mechanisms']:
    lines=(ROOT/item['current_source']).read_text().splitlines()
    lo,hi=item['lines']
    check('source_range_accessible:' + item['id'], 1 <= lo <= hi <= len(lines) and lines[lo-1].startswith('## '+item['id']))
for ident,item in index['shared_deltas'].items():
    check('shared_confirmation_source_accessible:' + ident, (ROOT/item['current']).is_file() and bool(source_member(item['original_zip'],item['member'])))
manual = read('scoring/MANUAL_CASE_SOURCE_INDEX.json')
for item in manual['sources']:
    data=(ROOT/item['current']).read_bytes()
    check('manual_case_source:' + item['current'], sha(data)==item['sha256'] and data==source_member(item['source_zip'],item['member']), 'historical_source_byte_integrity')
check('actual_12_standard_manual_cases_carried', len(read('scoring/standard/manual/CALIBRATION_CASES_12.json')['cases']) == 12)
check('actual_26_HC_manual_cases_carried', len(read('scoring/half_chaos/manual/CALIBRATION_CASES_26.json')['cases']) == 26)
inputs = read('evidence/INPUT_CHECKS.json')
check('input_manifest_checks_passed', inputs['checks'] and all(x['passed'] for x in inputs['checks']), 'input_byte_integrity')
for item in read('evidence/RETURN_RECEIPT.json')['returns']:
    check('received_zip_still_identical:' + item['workline'], sha((ROOT/item['path']).read_bytes()) == item['sha256'], 'input_byte_integrity')
check('collaboration_working_copy_unchanged', sha((ROOT/'collaboration/X_Collaboration_Integrated_Candidate_2026-10-13.md').read_bytes()) == '620eb651fc77e4e060959c299ceecebf36fac479b6beb0c91b94b39de345f0ab', 'source_byte_integrity')
check('UI_source_path_available', (ROOT/read('UI_NORMALIZED_STATE.json')['source_return']).is_file())
check('UI_and_NET_not_resumed', state['worklines']['UI']['new_return_received_this_closeout'] is False and state['worklines']['NET']['status'] == 'paused_not_resumed')

if '--finalize' in sys.argv:
    report = {
        'scope':'documents_sources_and_package_inputs_only_not_engine_runtime',
        'input_byte_checks':len(inputs['checks']),
        'current_source_and_boundary_checks':len(CHECKS),
        'checks':CHECKS,
        'all_passed':all(x['passed'] for x in CHECKS),
        'new_engine_tests_run':0,
        'independent_model_execution_verified':False,
        'full_mode_acceptance':False,
        'semantic_review_scope':'explicit affected F1/H15/mode deltas and state corrections; not all original historical confirmations'
    }
    (ROOT/'VERIFICATION_RESULTS.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    files=[]
    for path in sorted(ROOT.rglob('*')):
        if path.is_file() and path.name != 'MANIFEST.json' or path.is_file() and path.parent != ROOT:
            if path == ROOT/'MANIFEST.json':
                continue
            data=path.read_bytes()
            files.append({'path':path.relative_to(ROOT).as_posix(),'bytes':len(data),'sha256':sha(data)})
    manifest={'schema':'lezi.total_closeout_manifest.v3','revision':state['revision'],'files':files,'scope':'byte_integrity_does_not_prove_execution'}
    (ROOT/'MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
else:
    manifest=read('MANIFEST.json')
    expected={x['path'] for x in manifest['files']} | {'MANIFEST.json'}
    actual={x.relative_to(ROOT).as_posix() for x in ROOT.rglob('*') if x.is_file()}
    check('exact_file_set', actual==expected,'package_byte_integrity')
    for item in manifest['files']:
        data=(ROOT/item['path']).read_bytes()
        check('package_bytes:' + item['path'], len(data)==item['bytes'] and sha(data)==item['sha256'],'package_byte_integrity')
print(json.dumps({'passed':all(x['passed'] for x in CHECKS),'checks':len(CHECKS),'input_checks':len(inputs['checks']),'new_engine_tests':0},ensure_ascii=False))
