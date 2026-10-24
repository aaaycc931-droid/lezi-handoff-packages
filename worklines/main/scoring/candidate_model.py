"""Exact, offline decision-problem evaluator. Not the game engine or a strength oracle."""
from fractions import Fraction


def number(value):
    if isinstance(value, bool) or isinstance(value, float) or not isinstance(value, (int, str)):
        raise ValueError('Use an exact integer or rational string, never an implicit float')
    return Fraction(value)


def evaluate(node):
    kind = node['kind']
    if kind == 'leaf':
        metric, value = node['metric'], number(node['value'])
        if metric not in ('material_proxy', 'outcome'):
            raise ValueError('Unknown utility metric')
        if metric == 'outcome' and value not in (0, Fraction(1, 2), 1):
            raise ValueError('Terminal anchors are loss=0, draw=1/2, win=1')
        return metric, value
    if kind not in ('max', 'min', 'chance'):
        raise ValueError('Unknown node kind')
    branches = node.get('branches', [])
    if not branches:
        raise ValueError('A decision/chance node needs branches')
    values = [evaluate(b['node']) for b in branches]
    if len({m for m, _ in values}) != 1:
        raise ValueError('Material and terminal outcomes cannot be added or averaged')
    metric = values[0][0]
    if kind == 'chance':
        ps = [number(b['p']) for b in branches]
        if any(p < 0 for p in ps) or sum(ps) != 1:
            raise ValueError('Conditional probabilities must be nonnegative and sum to one')
        return metric, sum(p * v for p, (_, v) in zip(ps, values))
    labels = [b['action'] for b in branches]
    if len(set(labels)) != len(labels):
        raise ValueError('Duplicate action')
    return metric, (max if kind == 'max' else min)(v for _, v in values)


def paired_value(without, with_ability):
    m0, v0 = evaluate(without)
    m1, v1 = evaluate(with_ability)
    if m0 != m1:
        raise ValueError('Counterfactuals must use the same utility')
    return {'metric': m0, 'without': str(v0), 'with': str(v1), 'delta': str(v1-v0),
            'conditional_impact_index': str(100*(v1-v0)) if m0 == 'outcome' else None,
            'whole_hero_score': None}


def allocate_consequences(consequences, expected_delta):
    """Explanatory attribution, not a second source of total value."""
    seen, total, dimensions = set(), Fraction(0), {}
    allowed = {'terminal', 'material', 'action', 'mobility', 'information'}
    for c in consequences:
        if c['id'] in seen:
            raise ValueError('One realized consequence cannot be counted twice')
        seen.add(c['id'])
        value = number(c['delta'])
        if set(c['shares']) - allowed:
            raise ValueError('Unknown explanation dimension')
        weights = {k: number(v) for k, v in c['shares'].items()}
        if not weights or any(w < 0 for w in weights.values()) or sum(weights.values()) != 1:
            raise ValueError('Each consequence must be allocated exactly once')
        total += value
        for key, share in weights.items():
            dimensions[key] = dimensions.get(key, Fraction(0)) + value*share
    if total != number(expected_delta):
        raise ValueError('Explanations must reconcile to the paired total, not create extra value')
    return {'total': str(total), 'dimensions': {k: str(v) for k,v in dimensions.items()}}


def publication_gate(evidence):
    """Checks declared prerequisites only; metadata is not proof that they hold."""
    required = ['current_rule_snapshot', 'source_complete',
                'paired_comparator', 'population_and_opponents_defined',
                'policy_and_information_fair', 'full_trajectory_outcomes',
                'replay_and_evidence_valid', 'uncertainty_estimated',
                'heldout_validation', 'precision_justified']
    missing = [key for key in required if evidence.get(key) is not True]
    if evidence.get('utility') != 'outcome':
        missing.append('common_outcome_utility')
    if evidence.get('kind') not in ('paired_full_game_data', 'complete_exact_game_solution'):
        missing.append('not_a_toy_or_partial_position')
    formal_missing=missing+[k for k in ('method_adopted','release_reviewed') if evidence.get(k) is not True]
    return {'global_numeric_publishable': not missing, 'formal_numeric_publishable':not formal_missing,
            'missing': missing, 'formal_missing':formal_missing,
            'current_level': 'candidate_global_ready_for_review' if not missing else 'conditional_or_qualitative_only'}
