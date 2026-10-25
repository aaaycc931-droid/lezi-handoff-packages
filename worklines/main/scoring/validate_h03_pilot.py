"""Check source identities and fixture integrity, without importing a game engine.

This deliberately does not implement chess legality, execute requests, or score games.
Run: python validate_h03_pilot.py --engine-root /path/to/jieqi-engine
"""
from collections import Counter
from copy import deepcopy
from pathlib import Path
import argparse
import hashlib
import json

HERE = Path(__file__).resolve().parent


def require(condition, label):
    if not condition:
        raise ValueError(label)


def read(name):
    return json.loads((HERE / name).read_text())


def git_blob(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def validate(opening, spec):
    require(opening['mode'] == 'jieqi', 'wrong_mode')
    require(opening['natural_authority_prefix_verified'] is False, 'unearned_runtime_claim')
    ids = [f'covered-{i:02d}' for i in range(30)]
    kinds = [('rook', 2), ('horse', 2), ('elephant', 2), ('advisor', 2), ('cannon', 2), ('pawn', 5)]
    pool = [{'color': s, 'type': k} for s in ['red', 'black'] for k, n in kinds for _ in range(n)]
    desired = opening['desired_authority_identities']
    require(set(desired) == set(ids), 'identity_inventory_ids')
    require(Counter((p['color'], p['type']) for p in pool) ==
            Counter((p['color'], p['type']) for p in desired.values()), 'identity_inventory_multiset')
    tape = opening['initial_random_tape']
    require(len(tape) == 29, 'initial_draw_count')
    for i, draw in zip(range(29, 0, -1), tape):
        j = draw['value']
        require(type(j) is int and 0 <= j <= i and draw['max_exclusive'] == i + 1 and
                draw['event_key'] == f'initial:fisher_yates:{i}', 'random_draw_domain_or_order')
        pool[i], pool[j] = pool[j], pool[i]
    require(pool == [desired[id_] for id_ in ids], 'random_draw_realization')
    # Input construction only: exact slot order from pinned slots.ts, no legality oracle.
    slots = []
    for side in ['black', 'red']:
        by, cy, py = (0, 2, 3) if side == 'black' else (9, 7, 6)
        slots += [(x, by) for x in range(9) if x != 4]
        slots += [(x, cy) for x in [1, 7]]
        slots += [(x, py) for x in [0, 2, 4, 6, 8]]
    public = opening['public_pieces']
    require(len(public) == 32 and len({p['id'] for p in public}) == 32, 'public_piece_inventory')
    require(public[:2] == [
        {'id': 'black-general', 'color': 'black', 'type': 'general', 'faceDown': False, 'x': 4, 'y': 0},
        {'id': 'red-general', 'color': 'red', 'type': 'general', 'faceDown': False, 'x': 4, 'y': 9},
    ], 'general_opening')
    require(public[2:] == [{'id': id_, 'x': x, 'y': y, 'faceDown': True}
                           for id_, (x, y) in zip(ids, slots)], 'public_slot_layout')
    require(spec['arms_share_opening_and_random_tape'] is True and
            spec['post_initialization_state_overrides'] == [], 'unfair_state_override')
    require(spec['opening_file'] == 'H03_OPENING_WITNESS.json', 'opening_reference')
    require(spec['release'] == {'global_candidate': False, 'formal_adoption': False, 'new_hero_score': None}, 'unearned_release')
    require(spec['heldout_source_families'] == [] and spec['independent_samples'] == 0, 'false_independence')
    cases = spec['cases']
    require(len(cases) == 4 and len({c['id'] for c in cases}) == 4, 'case_ids')
    require({c['category'] for c in cases} == {'immediate_attack', 'wait_until_expiry',
            'alternative_target_and_reentry', 'public_adaptive_exchange'}, 'behavior_coverage')
    action_ids = []
    request_count = 0
    for case in cases:
        require(case['source_family'] == opening['id'] and case['split'] == 'development_only', 'family_or_split')
        require(case['status'] == 'STATIC_SPEC_NOT_RUN' and case['engine_legality'] == 'UNVERIFIED', 'false_execution_claim')
        require(case['with']['initialization'] == {'api': 'initializeFeatureGameState', 'heroes': {'red': 'warrior'}, 'mutation': None}
                and case['without']['initialization'] == {'api': 'initializeFeatureGameState', 'heroes': None, 'mutation': None}, 'counterfactual_initialization')
        require(case['paired_policy']['reads_private_identities'] is False, 'private_policy_input')
        require(all(v is None for v in case['observation'].values()), 'unearned_observation')
        require(case['stop']['nonterminal_classification'] == 'censored', 'false_draw_at_cutoff')
        require(len(case['with']['requests']) == len(case['without']['requests']) == case['stop']['budget'], 'unequal_action_budget')
        for arm in ['with', 'without']:
            require(set(case[arm]) == {'initialization', 'requests'}, 'unexpected_arm_override')
            for i, action in enumerate(case[arm]['requests']):
                cmd = action['command']
                require(set(cmd) == {'actionId', 'expectedRevision', 'pieceId', 'from', 'to'}, 'unexpected_command_permission')
                require(action['side'] == ('red' if i % 2 == 0 else 'black') and
                        action['kind'] == 'ordinary_move', 'turn_or_action_taxonomy')
                require(action['piece_id'] in ids and cmd['pieceId'] == action['piece_id'] and
                        cmd['expectedRevision'] == i, 'id_or_revision')
                for label in ['from', 'to']:
                    xy = action[f'{label}_xy']
                    require(len(xy) == 2 and all(type(v) is int for v in xy) and
                            0 <= xy[0] <= 8 and 0 <= xy[1] <= 9 and cmd[label] == dict(zip(['x', 'y'], xy)), 'coordinate_integrity')
                require(action['from_xy'] != action['to_xy'], 'zero_length_request')
                require(cmd['actionId'] == f"{case['id']}:{arm}:a{i+1:02d}", 'stable_action_id')
                action_ids.append(cmd['actionId'])
                request_count += 1
        for i, (left, right) in enumerate(zip(case['with']['requests'], case['without']['requests'])):
            if case['category'] == 'public_adaptive_exchange' and i == case['stop']['budget'] - 1:
                require(left['policy_branch'] == 'own_rook_present' and right['policy_branch'] == 'own_rook_absent', 'adaptive_policy_branch')
            else:
                normalize = lambda x: {k: v for k, v in x.items() if k != 'command'}
                require(normalize(left) == normalize(right), 'unfair_fixed_requests')
    require(len(set(action_ids)) == len(action_ids), 'duplicate_action_id')
    return request_count


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--engine-root', type=Path, required=True)
    args = parser.parse_args()
    binding = read('H03_SOURCE_BINDING.json')
    opening, spec = read('H03_OPENING_WITNESS.json'), read('H03_PAIRED_CASES.json')
    require(spec['engine_commit'] == binding['engine_commit'] == '3f98bc9fb89a2a209209c424c4bf1bbd2cf6aca7', 'source_pin')
    matched = []
    for item in binding['engine_files']:
        path = args.engine_root / item['path']
        require(path.is_file() and git_blob(path.read_bytes()) == item['git_blob_sha'], f"source_blob_mismatch:{item['path']}")
        matched.append(item['path'])
    requests = validate(opening, spec)
    rejected = []
    mutations = [
        ('invalid_draw', lambda o, s: o['initial_random_tape'][0].update(value=30)),
        ('wrong_realization', lambda o, s: o['initial_random_tape'][0].update(value=(o['initial_random_tape'][0]['value'] + 1) % 30)),
        ('state_override', lambda o, s: s['post_initialization_state_overrides'].append('delete barrier')),
        ('wrong_counterfactual', lambda o, s: s['cases'][0]['without']['initialization'].update(heroes={'red': 'warrior'})),
        ('private_oracle', lambda o, s: s['cases'][0]['paired_policy'].update(reads_private_identities=True)),
        ('fake_draw', lambda o, s: s['cases'][0]['stop'].update(nonterminal_classification='draw')),
        ('fake_observation', lambda o, s: s['cases'][0]['observation'].update(material_delta=9)),
        ('false_holdout', lambda o, s: s['heldout_source_families'].append(o['id'])),
        ('false_release', lambda o, s: s['release'].update(global_candidate=True)),
    ]
    for name, mutate in mutations:
        o, s = deepcopy(opening), deepcopy(spec)
        mutate(o, s)
        try:
            validate(o, s)
        except (ValueError, KeyError, TypeError):
            rejected.append(name)
        else:
            raise ValueError(f'negative_validation_failed:{name}')
    probes = read('H03_GUARD_PROBES.json')
    require(probes['engine_commit'] == binding['engine_commit'] and probes['engine_runs'] == 0 and
            probes['status'] == 'PLANNED_RUNTIME_UNRUN' and probes['source_legality_or_strength_claim'] is False,
            'false_probe_execution_claim')
    require([p['id'] for p in probes['probes']] == ['H03-S01', 'H03-S02', 'H03-S03'] and
            all(p['actual'] is None for p in probes['probes']), 'guard_probe_inventory')
    artifacts = ['validate_h03_pilot.py', 'H03_SOURCE_BINDING.json', 'H03_OPENING_WITNESS.json', 'H03_PAIRED_CASES.json', 'H03_GUARD_PROBES.json']
    result = {
        'id': 'SCORE-H03-PREP-01', 'date_local': '2026-10-25', 'status': 'STATIC_INTEGRITY_PASS_RUNTIME_UNRUN',
        'engine_commit': binding['engine_commit'], 'engine_blob_matches': len(matched), 'matched_paths': matched,
        'initialization_draws_checked': 29, 'opening_pieces_checked': 32,
        'paired_behavior_specs': 4, 'planned_requests_across_both_arms': requests,
        'unrun_guard_probes': 3,
        'negative_integrity_checks_passed': len(rejected), 'negative_checks': rejected,
        'limitations': ['No chess rules reimplemented', 'No authority requests executed', 'No legal-prefix proof',
                        'One conditioned source family; no independent samples/holdout', 'Not engine, mode or strength acceptance'],
        'engine_imports': 0, 'engine_runs': 0, 'natural_replays': 0, 'observed_terminals': 0,
        'new_hero_global_scores': 0, 'publication_gate': False,
        'inputs_sha256': {name: hashlib.sha256((HERE / name).read_bytes()).hexdigest() for name in artifacts},
    }
    (HERE / 'H03_STATIC_VALIDATION.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: result[k] for k in ['status', 'engine_blob_matches', 'paired_behavior_specs',
          'planned_requests_across_both_arms', 'negative_integrity_checks_passed', 'engine_runs', 'publication_gate']}, ensure_ascii=False))


if __name__ == '__main__':
    main()
