#!/usr/bin/env python3
"""Read-only accounting of the original HC evidence. Never emits authority values.

Run with the owner-only authority-trace.json and pinned handoff files. This is an
offline artifact audit: it neither imports the engine nor executes a game. Exact
authority checkpoints, returned views, and real client delivery are distinct.
"""
import argparse
import collections
import hashlib
import json
from pathlib import Path

RAW_SHA = 'ccea6579108af5f2547d8b4f8bc1179239967784411de135028e85277cc59259'
ENGINE = '570fdf189867ec93355f0eca66362deb72cca53c'
HANDOFF = '4af533233920a6ebbc818c466365673aa21a18ee'
SOURCE_HASHES = {
    'INITIALIZATION_WITNESS_DATA.json': 'ba8f0a40e19230176df732e267d14b6070778d74886f4c007ea0ff1be4084836',
    'REPLAY_ACTION_DATA.json': '1e213fe2c6db48ab54d15a599023f57ab50f1ecda50e30601ae555fbf88fda68',
}
SOURCE_BLOBS = {
    'INITIALIZATION_WITNESS_DATA.json':'83b1e80eea254d17d3c3f9fee1e978c4aa284965',
    'REPLAY_ACTION_DATA.json':'d8453df0104ffdef95fd22f705cf355d53b8d027',
    'ASSERTION_EVIDENCE_MATRIX.json':'e46a29f3e69cc2b005dd7633a60c888a5882b8ce',
    'OBSERVATION_FIELD_MAPPING.json':'be63d62bf94e029042e49089455af41b2b81b5a4',
    'HC49_ALL_REPLAYS_API_BINDING.json':'9f91119b17354d91c94ac443cbbe2733902d9002',
    'HC50_ORIGINAL_210_EVIDENCE_PRIVACY_AUDIT.json':'d801ef23325beea568b6d2f9e5074cfcfada8320',
    'HC51_PAIR_VIEW_MISSING_STIMULUS_CONTRACT.json':'22abe23c22ab0032aa014e6a4afbf6f3f128b66f',
}

def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()

def blob_sha(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()

def load(path):
    return json.loads(path.read_text())

def normalize(value, binding):
    if isinstance(value, str):
        if value == binding['players']['red']: return '<red-player>'
        if value == binding['players']['black']: return '<black-player>'
        if value == binding['roomId']: return '<room>'
        if any(value.startswith(prefix + binding['roomId'] + ':') for prefix in ['', 'system:', 'server:']):
            return value.replace(binding['roomId'], '<room>').replace(binding['replayId'], '<replay>')
        return value
    if isinstance(value, list): return [normalize(x, binding) for x in value]
    if isinstance(value, dict): return {normalize(k, binding): normalize(v, binding) for k, v in value.items()}
    return value

def forbidden_paths(value, path=''):
    forbidden = {'secret', 'identities', 'destinyIdentities', 'processedActions', 'trueGenerals',
                 'trainingOriginalSides', 'shuffleOpening', 'true_type_by_stable_piece_id', 'all_initial_pieces_original_side'}
    found = []
    if isinstance(value, dict):
        for k, v in value.items():
            if k in forbidden: found.append(path + '/' + k)
            found.extend(forbidden_paths(v, path + '/' + k))
    elif isinstance(value, list):
        for i, v in enumerate(value): found.extend(forbidden_paths(v, path + '/' + str(i)))
    return found

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--authority', required=True, type=Path)
    parser.add_argument('--handoff', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    raw_bytes = args.authority.read_bytes()
    assert hashlib.sha256(raw_bytes).hexdigest() == RAW_SHA, 'wrong owner authority artifact'
    raw = json.loads(raw_bytes)
    folder = args.handoff / 'worklines/half_chaos'
    sources = {name: load(folder / name) for name in [
        'INITIALIZATION_WITNESS_DATA.json', 'REPLAY_ACTION_DATA.json', 'ASSERTION_EVIDENCE_MATRIX.json',
        'OBSERVATION_FIELD_MAPPING.json', 'HC49_ALL_REPLAYS_API_BINDING.json',
        'HC50_ORIGINAL_210_EVIDENCE_PRIVACY_AUDIT.json', 'HC51_PAIR_VIEW_MISSING_STIMULUS_CONTRACT.json']}
    for name, sha in SOURCE_HASHES.items():
        assert hashlib.sha256((folder / name).read_bytes()).hexdigest() == sha, 'source bytes differ: ' + name
    for name, sha in SOURCE_BLOBS.items():
        assert blob_sha((folder / name).read_bytes()) == sha, 'pinned source blob differs: ' + name
    matrix = sources['ASSERTION_EVIDENCE_MATRIX.json']
    original = sources['REPLAY_ACTION_DATA.json']
    readiness = sources['HC50_ORIGINAL_210_EVIDENCE_PRIVACY_AUDIT.json']
    r51 = sources['HC51_PAIR_VIEW_MISSING_STIMULUS_CONTRACT.json']
    replay_data = {r['replay_id']: r for r in original['replays']}
    replays = {r['binding']['replayId']: r for r in raw}
    worlds = {w['id']: w for w in sources['INITIALIZATION_WITNESS_DATA.json']['worlds']}
    assert len(raw) == len(replays) == 12 and set(replays) == set(replay_data)
    requests, declarations, replay_rows = {}, {}, []
    checks = []

    def check(id_, ok):
        checks.append({'id': id_, 'passed': bool(ok)})
        return bool(ok)

    for ri, r in enumerate(raw):
        rid = r['binding']['replayId']; source = replay_data[rid]
        world = worlds[r['binding']['worldId']]
        check(rid + ':binding', r['binding']['worldId'] == source['world_id'] and r['binding']['engineParent'] == 'b28535780a7c7427c0d715b46b0362d35a696d8f')
        initial = r['initial']; pieces = initial['game']['state']['pieces']; secret = initial['game']['secret']
        check(rid + ':initial32', len(pieces) == 32 and len({p['id'] for p in pieces}) == 32)
        check(rid + ':initial_identity_world', all(secret['identities'][id_]['type'] == typ and secret['identities'][id_]['color'] == world['all_initial_pieces_original_side'][id_] for id_, typ in world['true_type_by_stable_piece_id'].items()))
        check(rid + ':original_draw_witness', r['draws'][:28] == [{'bound': d['bound'], 'value': d['value']} for d in world['fisher_yates_draw_witness']])
        check(rid + ':real_actors', initial['game']['players'] == r['binding']['players'] == initial['rps']['assignments'])
        expected = []
        for turn in source['source_prescribed_turns']:
            for decl in [*turn['pre_main_requests'], turn['normal_main']]:
                declarations[decl['declaration_id']] = (rid, turn, decl)
                expected.append(decl['declaration_id'])
        check(rid + ':exact_sequence', [x['declarationId'] for x in r['results']] == expected)
        for xi, x in enumerate(r['results']):
            id_ = x['declarationId']; _, turn, decl = declarations[id_]
            requests[id_] = (r, x, f'/{ri}/results/{xi}')
            before = x['before']['game']['state']; after = x['after']['game']['state']; actor = turn['actor']
            check(id_ + ':actor', x['playerId'] == r['binding']['players'][actor] and before['turn'] == actor)
            check(id_ + ':deadline', x['now'] < before['turnDeadlineAt'])
            check(id_ + ':disposition', x['disposition'] == decl.get('expected_disposition', 'accepted') and not x.get('duplicate', False) and x['evidenceValid'] and not x['outcomeIssues'])
            check(id_ + ':view_sensitive_keys', not forbidden_paths(x['views']))
            if id_.endswith(':main'):
                ev = x['events']; kinds = [e['kind'] for e in ev]
                check(id_ + ':exact_event_multiplicity', all(kinds.count(k) == 1 for k in ['formal_main_action', 'main_action_atom_closed', 'formal_turn_end', 'formal_turn_settled', 'formal_turn_begin', 'formal_clock_start']))
                closed = next(e['state'] for e in ev if e['kind'] == 'main_action_atom_closed')
                settled = next(e['state'] for e in ev if e['kind'] == 'formal_turn_settled')
                check(id_ + ':event_order', kinds.index('formal_main_action') < kinds.index('main_action_atom_closed') < kinds.index('formal_turn_end') < kinds.index('formal_turn_settled') < kinds.index('formal_turn_begin') < kinds.index('formal_clock_start'))
                check(id_ + ':counter_boundary', closed['formalTurns'] == before['formalTurns'] and settled['formalTurns'][actor] == before['formalTurns'][actor] + 1 and settled['formalTurns'][{'red':'black','black':'red'}[actor]] == before['formalTurns'][{'red':'black','black':'red'}[actor]])
                check(id_ + ':original_clock_at_internal_stages', all(s.get(k) == before.get(k) for s in [closed, settled] for k in ['formalClock', 'turnStartedAt', 'turnDeadlineAt']))
                check(id_ + ':closed_phase', closed['turnLifecycle']['phase'] == 'atom_closure' and settled['turnLifecycle']['phase'] == 'turn_end')
                lm = closed['lastMove']; exp = decl['expected_result']; source_id = decl['authority_only_expected_initial_source_id']
                p = next((p for p in closed['pieces'] if p['id'] == source_id), None)
                check(id_ + ':source_request_and_identity', lm['actionId'] == x['command']['actionId'] and lm['pieceId'] == source_id and lm['actingSide'] == actor and [x['command']['from']['x'], x['command']['from']['y']] == decl['semantic_request']['semantic_from'] and [x['command']['to']['x'], x['command']['to']['y']] == decl['semantic_request']['semantic_to'])
                check(id_ + ':position_and_reveal', p is not None and [p['x'], p['y']] == exp['source_position_after_full_atom'] and p['faceDown'] == exp['source_face_down_after_full_atom'])
                actual_path = sorted(p['id'] for p in lm.get('pathCrushed', [])); expected_path = sorted(p['initial_piece_id'] for p in exp['path_deaths'])
                endpoint = (exp.get('endpoint_death') or {}).get('initial_piece_id')
                check(id_ + ':path_endpoint_and_rebound', actual_path == expected_path and (lm.get('captured') or {}).get('id') == endpoint and bool(lm.get('bouncedAgainstPieceId')) == exp['ordinary_defense_rebound'])
                for victim in [*expected_path, *([endpoint] if endpoint else [])]:
                    deaths = [a for a in closed.get('automaticEvents', []) if a.get('pieceId') == victim and a.get('deathRecord')]
                    check(id_ + ':destruction_record:' + victim, victim not in {p['id'] for p in closed['pieces']} and len(deaths) == 1 and deaths[0]['deathRecord']['id'] == victim)
            else:
                check(id_ + ':nonmain_preserves_opportunity_and_clock', all(after.get(k) == before.get(k) for k in ['turn', 'turnLifecycle', 'formalTurns', 'formalClock', 'turnStartedAt', 'turnDeadlineAt']) and not x['events'])
                if x['disposition'] == 'rejected':
                    check(id_ + ':refusal_full_authority_unchanged', x['before'] == x['after'] and x['error']['code'] == 'IN_CHECK')
        expected_alive = sorted(source['authority_only_expected_terminal_ledger']['living_initial_ids'])
        check(rid + ':final_living_ledger', sorted(p['id'] for p in r['results'][-1]['after']['game']['state']['pieces']) == expected_alive)
        replay_rows.append({'replay_id': rid, 'world_id': r['binding']['worldId'], 'raw_pointer': '/' + str(ri), 'requests': len(r['results']), 'source_sequence_reconciled': True, 'bounded_ledger_recomputed': True})

    # Select the actual required boundary. A returned room after next begin is
    # deliberately never used in place of main_atom_closed or formal_settled.
    checkpoint_rows = []
    for cp in readiness['original_all_210_checkpoint_readiness']:
        id_ = cp['request_id']; r, x, pointer = requests[id_]
        boundary = cp['semantic_boundary']
        event_kind = {'after_main_atom': 'main_action_atom_closed', 'after_normal_end_effects': 'formal_turn_settled'}.get(boundary)
        if event_kind:
            candidates = [(i, e) for i, e in enumerate(x['events']) if e['kind'] == event_kind]
            assert len(candidates) == 1
            ei, event = candidates[0]; state, secret = event['state'], event['secret']
            selector = pointer + '/events/' + str(ei)
            view_status = 'NOT_CAPTURED_AT_THIS_SEMANTIC_STAGE'
        else:
            state, secret = x['after']['game']['state'], x['after']['game']['secret']
            selector = pointer + '/after/game'
            view_status = 'ACTUAL_RETURNED_PLAYER_AND_PUBLIC_VIEWS_CAPTURED'
        groups = []
        for fm in cp['field_group_ids']:
            status = 'TRACE_AVAILABLE_BOUNDED_ASSERTIONS_SEPARATE'
            limitation = None
            if fm == 'FM02': limitation = 'Fixed opening body binding only; no general H06/H11 lifecycle acceptance.'
            elif fm == 'FM05': limitation = 'Earlier operation death witnesses retained offline; no production append-only adjudication ledger proved.'
            elif fm == 'FM15': limitation = 'Original requests and error source captured; real wire retransmission/actor-payload conflicts absent.'
            elif fm == 'FM16':
                status = view_status
                limitation = 'Actual browser/client delivery and rendering not captured.'
            elif fm == 'FM17':
                status = 'RETURNED_SERVER_MESSAGES_OR_THROWN_ERROR_ONLY'
                limitation = 'No exact-stage room message projection or actual client error serialization/delivery.'
            elif fm == 'FM20':
                status = 'AUTHORITATIVE_ACCEPTANCE_AND_STATUS_ONLY'
                limitation = 'No independent complete royal-threat/legal-response/terminal oracle.'
            elif fm == 'FM21': limitation = 'Pinned three-tuple research admission only; product featuresReady remains false.'
            elif fm == 'FM22': limitation = 'Whole accepted/refused result only; six internal phases not separately observed.'
            groups.append({'field_group_id': fm, 'evidence_status': status, **({'remaining': limitation} if limitation else {})})
        checkpoint_rows.append({
            'checkpoint_id': cp['checkpoint_id'], 'request_id': id_, 'replay_id': cp['replay_id'],
            'semantic_boundary': boundary, 'raw_pointer': selector,
            'snapshot_canonical_sha256': digest({'state': state, 'secret': secret}),
            'authority_boundary': 'CAPTURED_AND_RECONCILED', 'request_disposition': x['disposition'],
            'linked_specs': cp['linked_specs'], 'field_groups': groups, 'exact_stage_player_views': view_status,
            'returned_view_pointer': pointer + '/views', 'client_delivery': 'NOT_CAPTURED',
            'full_observation_obligation_discharged': False,
        })
    cp_index = {x['checkpoint_id']: x for x in checkpoint_rows}
    assert len(cp_index) == 210
    # Store shared FM policies once. Each checkpoint retains its actual group
    # membership and the stage-specific view status; no 210-fold prose copies.
    field_group_policies = {}
    for row in checkpoint_rows:
        row['field_group_ids'] = []
        for policy in row.pop('field_groups'):
            fm = policy.pop('field_group_id')
            if fm == 'FM16': policy['evidence_status'] = 'SEE_EACH_ROW_EXACT_STAGE_PLAYER_VIEWS'
            assert fm not in field_group_policies or field_group_policies[fm] == policy
            field_group_policies[fm] = policy
            row['field_group_ids'].append(fm)

    # Explicit specification-specific predicates, in addition to the recomputed
    # source outcome for every declared main request. No hidden values are output.
    def request(rid, suffix): return requests[rid + ':' + suffix][1]
    def st(rid, suffix, stage='closed'):
        x = request(rid, suffix)
        if stage in ['before', 'after']: return x[stage]['game']['state']
        kind = {'closed':'main_action_atom_closed','end':'formal_turn_settled'}[stage]
        return next(e['state'] for e in x['events'] if e['kind'] == kind)
    def pc(s, id_): return next((p for p in s['pieces'] if p['id'] == id_), None)
    def barrier(s, id_): return s.get('effectsByPieceId', {}).get(id_, {}).get('barrier', {}).get('enemyTurnsRemaining')
    def quota(s): return len(s.get('warrior', {}).get('black', {}).get('barrierPieceIds', []))
    def effects(s, id_): return s.get('effectsByPieceId', {}).get(id_, {})
    def no_refund(x): return x['before'] == x['after']
    explicit = collections.defaultdict(list)
    def spec(id_, label, ok):
        explicit[id_].append({'assertion': label, 'passed': bool(ok)})
    for rid, pre, grant, terminal in [
        ('MA-PD01','B1:main','B2:main','R3:main'),('MA-PD02',None,'B4:main','R5:main'),
        ('MA-PD03',None,'B4:main','R7:main'),('MA-PD04',None,'B3:main','R5:main'),
        ('MA-PD05-A',None,'B2:main','R4:main'),('MA-PD05-B',None,'B2:main','R4:main'),
        ('MA-PD06-A','B2:main','B3:main','R4:main'),('MA-PD06-B','B2:main','B3:main','R4:main')]:
        g = st(rid, grant); t = st(rid, terminal)
        target = g['lastMove']['pieceId']
        ids = {'MA-PD01':['PD-S01'], 'MA-PD02':['PD-S07','PD-S10'], 'MA-PD03':['PD-S13'], 'MA-PD04':['PD-S18'], 'MA-PD05-A':['PD-S23'], 'MA-PD05-B':['PD-S23'], 'MA-PD06-A':['PD-S26'], 'MA-PD06-B':['PD-S26']}[rid]
        for id_ in ids:
            spec(id_, rid + ':departure_grants_three_and_one_lifetime_member', barrier(g, target) == 3 and quota(g) == 1)
        if pre:
            spec(ids[0], rid + ':palace_reveal_no_barrier', not st(rid, pre).get('effectsByPieceId', {}).get(target, {}).get('barrier'))
        spec('PD-S31', rid + ':no_extra_main_begin_end', all(sum(e['kind'] == kind for e in request(rid, terminal)['events']) == 1 for kind in ['formal_main_action','formal_turn_begin','formal_turn_settled']))
        if rid != 'MA-PD04':
            spec({'MA-PD01':'PD-S04','MA-PD02':'PD-S09','MA-PD03':'PD-S14','MA-PD05-A':'PD-S23','MA-PD05-B':'PD-S23','MA-PD06-A':'PD-S28','MA-PD06-B':'PD-S28'}[rid], rid + ':barrier_exhaustion_keeps_lifetime_member', barrier(t, target) is None and target in t['warrior']['black']['barrierPieceIds'])
    spec('PD-S13','three_two_one_lifetime', barrier(st('MA-PD03','B4:main'),'covered-03') == 3 and barrier(st('MA-PD03','R5:main','end'),'covered-03') == 2 and barrier(st('MA-PD03','R6:main','end'),'covered-03') == 1)
    spec('PD-S18','PD04_end_decay_and_palace_advisor_no_new_member', barrier(st('MA-PD04','R4:main','end'),'covered-04') == 2 and quota(st('MA-PD04','B4:main')) == 1)
    spec('PD-S25','no_free_replay_no_representation_approval', all(request(rid,'R4:main')['after']['game']['state']['formalTurns']['red'] == 4 for rid in ['MA-PD05-A','MA-PD05-B']))
    spec('PD-S34','attack_keyword_only_not_tier_adoption', all('进攻' in st(rid, turn)['lastMove'].get('keywords', []) for rid, turn in [('MA-PD01','R3:main'),('MA-PD02','R2:main'),('MA-PD02','R5:main'),('MA-PD03','R7:main'),('MA-PD04','R5:main'),('MA-PD05-A','R4:main'),('MA-PD06-A','R4:main')]))

    hg = request('MA-DS01-02','R3:pre-1'); a=hg['after']['game']['state']; b=hg['before']['game']['state']
    spec('DS-S03','appeared_warrior_returns_to_original_anchor', pc(a,'covered-18') is not None and [pc(a,'covered-18')[k] for k in ['x','y']] == [3,9])
    spec('DS-S04','one_hourglass_clear_pollution_rearm_living_dragon', b['hourglasses'] == 5 and a['hourglasses'] == 4 and b['warps'] == [{'x':0,'y':5}] and a['warps'] == [] and effects(b,'covered-10').get('ammunition') == 0 and effects(a,'covered-10').get('ammunition') == 1)
    spec('DS-S05','cleansed_landing_has_no_time_collapse', not effects(st('MA-DS01-02','R3:main'),'covered-25').get('timeCollapse'))
    spec('DS-S06','hourglass_not_whole_game_snapshot', pc(a,'covered-08') is not None and [pc(a,'covered-08')[k] for k in ['x','y']] == [1,9] and pc(a,'covered-16') is None)
    for id_ in ['DS-S07','DS-S08','DS-S09','DS-S10','DS-S12']:
        spec(id_,'DS02_whole_authority_refusal_unchanged', all(no_refund(request('MA-DS01-02',t)) for t in ['R4:pre-1','R4:pre-2']))
    spec('DS-S11','collapse_at_R4_end_not_main_atom', pc(st('MA-DS01-02','R4:main'),'covered-25') is not None and pc(st('MA-DS01-02','R4:main','end'),'covered-25') is None and effects(st('MA-DS01-02','R4:main'),'covered-25')['timeCollapse']['expiresAtOwnerTurnEnd'] == 4)
    for id_ in ['DS-S14','DS-S15','DS-S16']:
        spec(id_,'DS03_newly_exposed_safety_refusal_is_atomic', no_refund(request('MA-DS03','R4:pre-1')) and request('MA-DS03','R4:pre-1')['error']['code'] == 'IN_CHECK' and request('MA-DS03','R4:main')['disposition'] == 'accepted')
    bad=request('MA-DS04','B3:pre-1'); good=request('MA-DS04','B4:pre-1'); caster=bad['command']['pieceId']
    for id_ in ['DS-S17','DS-S18','DS-S19','DS-S20','DS-S21','DS-S22']:
        spec(id_,'DS04_refusal_unchanged_then_real_main_and_new_safe_window', no_refund(bad) and bad['error']['code'] == 'IN_CHECK' and request('MA-DS04','B3:main')['disposition'] == 'accepted' and good['disposition'] == 'accepted')
    spec('DS-S18','other_bomb_gates_geometrically_present', effects(bad['before']['game']['state'],caster).get('ammunition') == 1 and max(abs(pc(bad['before']['game']['state'],caster)[k] - bad['command']['to'][k]) for k in ['x','y']) == 1 and bad['command']['to'] not in bad['before']['game']['state']['warps'])
    spec('DS-S21','safe_bomb_spends_one_ammo_and_one_army_quota', effects(good['before']['game']['state'],caster).get('ammunition') == 1 and effects(good['after']['game']['state'],caster).get('ammunition') == 0 and good['after']['game']['secret']['processedActions'].get('bomb:turn:black:3') == good['after']['game']['state']['revision'])
    spec('DS-S23','dead_dragon_not_alive_or_rearmed', pc(st('MA-DS05','B2:main'),'covered-12') is None and not effects(st('MA-DS05','B2:main'),'covered-12').get('ammunition'))
    spec('DS-S24','collapse_survives_evasion_until_original_R6_end', pc(st('MA-DS05','R6:main'),'covered-18') is not None and pc(st('MA-DS05','R6:main','end'),'covered-18') is None and effects(st('MA-DS05','R6:main'),'covered-18')['timeCollapse']['expiresAtOwnerTurnEnd'] == 6)
    revive=request('MA-DS05','R7:pre-1'); rs=revive['after']['game']['state']
    spec('DS-S25','dead_warrior_revives_at_anchor', pc(revive['before']['game']['state'],'covered-18') is None and pc(rs,'covered-18') is not None and [pc(rs,'covered-18')[k] for k in ['x','y']] == [3,9])
    spec('DS-S26','revival_is_not_snapshot_rollback', rs['hourglasses'] == 4 and rs['warps'] == [] and effects(rs,'covered-09').get('ammunition') == 1 and not effects(rs,'covered-18').get('timeCollapse') and all(pc(rs,id_) is None for id_ in ['covered-12','covered-16','covered-17']))
    spec('DS-S27','unappeared_central_pawn_stays_covered_in_original_position', pc(rs,'covered-27')['faceDown'] and [pc(rs,'covered-27')[k] for k in ['x','y']] == [4,6])
    spec('DS-S28','all_original_D01_requests_within_original_deadline', all(x['now'] < x['before']['game']['state']['turnDeadlineAt'] and x['after']['phase'] == 'playing' for r in raw if r['binding']['replayId'].startswith('MA-DS') for x in r['results']))
    spec('PD-S33','all_PD_source_tuples_remain_fixed', all(r['initial']['features']['mutation'] in ['iron_steed','war_chariot'] and r['initial']['features']['heroes'] == {'red':'qin_long','black':'warrior'} for r in raw if r['binding']['replayId'].startswith('MA-PD')))

    paired_rows=[]
    for pair in r51['pair_source_readiness']['pairs']:
        left, right = [replays[id_] for id_ in pair['replay_ids']]
        assert left['initial']['game']['secret']['identities'] != right['initial']['game']['secret']['identities']
        for i, (x,y) in enumerate(zip(left['results'],right['results'])):
            for side in ['red','black','public']:
                equal = normalize(x['views'][side],left['binding']) == normalize(y['views'][side],right['binding'])
                check(pair['id'] + ':' + str(i) + ':' + side + ':returned_view_equal', equal)
                paired_rows.append({'pair_id': pair['id'], 'left_request_id': x['declarationId'], 'right_request_id': y['declarationId'], 'viewer': side, 'actual_stage': 'AFTER_REQUEST_RETURN_AFTER_NEXT_BEGIN', 'equal_after_transport_identity_normalization': equal, 'fulfills_original_exact_stage_slot': False})
        spec('PD-S24' if pair['id']=='PAIR-PD05' else 'PD-S29', 'actual_returned_two_player_and_public_view_pair_equal', all(x['equal_after_transport_identity_normalization'] for x in paired_rows if x['pair_id']==pair['id']))
    original_pair_slots = [{
        'comparison_id': s['comparison_id'], 'left_checkpoint': s['original_left_checkpoint'], 'right_checkpoint': s['original_right_checkpoint'],
        'status': 'MISSING_EXACT_STAGE_RAW_PLAYER_VIEWS_AND_CLIENT_DELIVERY', 'authority_stages_available': True,
        'related_returned_comparisons_available': True, 'discharged': False,
    } for s in r51['pair_source_readiness']['comparison_slots']]
    assert len(original_pair_slots) == 56

    # Every row receives actual source outcome checks. Those checks prove the
    # named scalar/action facts only, never all obligations merely by linkage.
    spec_rows=[]
    for row in matrix['rows']:
        sid=row['spec_id']; cps=row['direct_checkpoint_ids']
        related=sorted({cp_index[cp]['request_id'] for cp in cps})
        outcome_checks=[c for c in checks if any(c['id'].startswith(id_ + ':') for id_ in related)]
        missing=list(row['missing_stimuli_or_natural_cases']); remaining=list(row['preserved_remaining_obligations'])
        explicit_assertions=explicit[sid]
        status='BOUNDED_TRACE_ASSERTIONS_RECONCILED_FULL_SPEC_OPEN'
        if not cps: status='MISSING_NATURAL_POSITIVE_NO_DIRECT_CHECKPOINT'
        elif missing: status='PARTIAL_MISSING_ORIGINAL_STIMULUS'
        elif remaining or sid in ['PD-S24','PD-S29','DS-S27']: status='PARTIAL_SEMANTIC_OR_EVIDENCE_BOUNDARY'
        if any(not c['passed'] for c in outcome_checks+explicit_assertions): status='TRACE_ASSERTION_MISMATCH_REQUIRES_REVIEW'
        spec_rows.append({
            'spec_id': sid, 'original_obligation': row['original_obligation'], 'source': row['original_source'],
            'direct_checkpoint_ids': cps, 'reconciled_request_ids': related,
            'source_declared_action_outcomes_rechecked': len({id_ for id_ in related if id_.endswith(':main')}),
            'explicit_bounded_assertions': explicit_assertions,
            'linked_request_checks_passed': sum(c['passed'] for c in outcome_checks),
            'linked_request_checks_failed': sum(not c['passed'] for c in outcome_checks),
            'status': status, 'missing_original_stimuli': missing, 'preserved_semantic_or_scope_limits': remaining,
            'common_remaining_evidence': ['Exact-stage player projections and actual client channels not fully captured.', 'Independent specification QA not performed; complete royal-response/terminal oracles remain outside this audit.'],
            'next_validation': ('Construct a lawful source positive without position injection.' if not cps else 'Supply the listed original missing stimulus; keep current trace facts.' if missing else 'Resolve the listed semantic/evidence limits against actual source; retain measured action facts.' if remaining else 'Receiver independently reviews the linked authority facts and any applicable exact-stage fields; this accounting is not formal acceptance.'),
            'formal_original_spec_accepted': False,
        })
    failures=[c for c in checks if not c['passed']]
    explicit_failures=[{'spec_id':sid,**c} for sid, cs in explicit.items() for c in cs if not c['passed']]
    args.output.mkdir(parents=True,exist_ok=True)
    summary={
        'schema':'lezi.main.hc_evidence_accounting.v1', 'id':'MAIN-HC-EVIDENCE-ACCOUNTING-20261027', 'date_local':'2026-10-28',
        'read_handoff_head':HANDOFF, 'engine_commit':ENGINE,
        'method':'OFFLINE_RECONCILIATION_OF_EXISTING_OWNER_AUTHORITY_ARTIFACT_NO_ENGINE_IMPORT_OR_RUN',
        'authority_raw_sha256':RAW_SHA, 'authority_bytes':len(raw_bytes),
        'authority_visibility':'Owner-only artifact; no raw state/secret/view payload published by this audit.',
        'source_files':[{'path':'worklines/half_chaos/'+name,'git_blob_sha':blob_sha((folder/name).read_bytes()),'sha256':hashlib.sha256((folder/name).read_bytes()).hexdigest()} for name in sources],
        'replays':12, 'requests':len(requests), 'authority_checkpoints':len(checkpoint_rows),
        'boundary_counts':dict(collections.Counter(x['semantic_boundary'] for x in checkpoint_rows)),
        'offline_request_checks':len(checks), 'offline_request_check_failures':len(failures),
        'explicit_spec_assertions':sum(len(x) for x in explicit.values()), 'explicit_spec_assertion_failures':len(explicit_failures),
        'original_specs':len(spec_rows),'spec_status_counts':dict(collections.Counter(x['status'] for x in spec_rows)),
        'formal_specs_accepted':0, 'fully_discharged_observation_rows':0,
        'returned_view_pair_comparisons':len(paired_rows),'returned_view_pair_equal':sum(x['equal_after_transport_identity_normalization'] for x in paired_rows),
        'original_exact_stage_player_view_slots':56,'original_exact_stage_player_view_slots_discharged':0,
        'new_engine_runs':0,'engine_code_changes':0,'new_gameplay_confirmations':0,'independent_QA':False,
        'failures':failures,'explicit_failures':explicit_failures,
        'outputs':{'checkpoints':'HC_EVIDENCE_210.json','specifications':'HC_EVIDENCE_64.json','pairs':'HC_EVIDENCE_PAIRS.json'},
        'protected':{'scoring':'frozen','NET':'paused','featuresReady':False,'hero_design_unchanged':True,'H03_pilot':'preserved_unrun','receiver_adoption':'not asserted'},
    }
    for name,obj in [('HC_EVIDENCE_ACCOUNTING.json',summary),('HC_EVIDENCE_210.json',{'schema':'lezi.main.hc_checkpoints.v1','authority_raw_sha256':RAW_SHA,'field_group_policies':field_group_policies,'rows':checkpoint_rows}),('HC_EVIDENCE_64.json',{'schema':'lezi.main.hc_spec_accounting.v1','rows':spec_rows}),('HC_EVIDENCE_PAIRS.json',{'schema':'lezi.main.hc_pair_accounting.v1','returned_comparisons':paired_rows,'original_exact_stage_slots':original_pair_slots})]:
        (args.output/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:summary[k] for k in ['replays','requests','authority_checkpoints','boundary_counts','offline_request_checks','offline_request_check_failures','explicit_spec_assertions','explicit_spec_assertion_failures','spec_status_counts','formal_specs_accepted','returned_view_pair_comparisons','original_exact_stage_player_view_slots_discharged','failures','explicit_failures']},ensure_ascii=False,indent=2))
    return 1 if failures or explicit_failures else 0

if __name__=='__main__': raise SystemExit(main())
