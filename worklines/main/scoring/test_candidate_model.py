import copy
from fractions import Fraction as F
import itertools
import unittest
from candidate_model import evaluate, paired_value, allocate_consequences, publication_gate
from validation_cases import cases, leaf, decision, chance, sensitivity, historical_wind_schedule


class CandidateTests(unittest.TestCase):
    def test_cross_type_conditional_oracles(self):
        for case in cases():
            with self.subTest(case=case['id']):
                result=paired_value(case['without'],case['with'])
                self.assertEqual(F(result['delta']),F(case['expected_delta']))
                self.assertIsNone(result['whole_hero_score'])

    def test_no_skill_zero(self):
        for v in (-9,0,9):self.assertEqual(paired_value(leaf(v),leaf(v))['delta'],'0')

    def test_extra_optional_actions_never_reduce_value(self):
        for a,b,c in itertools.product((-9,0,9),repeat=3):
            self.assertGreaterEqual(evaluate(decision('max',old=leaf(a),extra1=leaf(b),extra2=leaf(c)))[1],F(a))

    def test_costly_mandatory_change_can_be_negative(self):
        self.assertEqual(paired_value(leaf(1),leaf(-4))['delta'],'-5')

    def test_shorter_window_is_action_subset_not_fixed_discount(self):
        for a,b,c in itertools.product((-2,0,3),repeat=3):
            shorter=decision('max',normal=leaf(a),turn1=leaf(b))
            longer=decision('max',normal=leaf(a),turn1=leaf(b),turn2=leaf(c))
            self.assertGreaterEqual(evaluate(longer)[1],evaluate(shorter)[1])

    def test_fewer_uses_preserves_option_inclusion(self):
        def value(uses,opportunities):
            if not opportunities:return leaf(0)
            skip=value(uses,opportunities[1:])
            return decision('max',skip=skip,use=leaf(opportunities[0]+evaluate(value(uses-1,opportunities[1:]))[1])) if uses else skip
        for opp in itertools.product((-3,0,4),repeat=3):
            self.assertGreaterEqual(evaluate(value(2,opp))[1],evaluate(value(1,opp))[1])

    def test_eliminating_intervening_defense_does_not_hurt_in_same_toy_game(self):
        for a,b,c,d in itertools.product((-1,0,1),repeat=4):
            interrupted=max(min(a,b),min(c,d));uninterrupted=max(a,b,c,d)
            self.assertGreaterEqual(uninterrupted,interrupted)

    def test_information_obeys_non_anticipation(self):
        baseline=decision('max',left=chance(('1/2',leaf(9)),('1/2',leaf(1))),right=chance(('1/2',leaf(1)),('1/2',leaf(9))))
        after=chance(('1/2',decision('max',left=leaf(9),right=leaf(1))),('1/2',decision('max',left=leaf(1),right=leaf(9))))
        self.assertEqual(evaluate(baseline)[1],5)
        self.assertEqual(evaluate(after)[1],9)
        self.assertEqual(paired_value(baseline,after)['delta'],'4')

    def test_random_target_is_expectation_not_best(self):
        self.assertEqual(evaluate(chance(('1/2',leaf(9)),('1/2',leaf(1))))[1],5)

    def test_relabeling_channels_cannot_change_total(self):
        for dim in ('terminal','material','action','mobility','information'):
            self.assertEqual(allocate_consequences([{'id':'gain','delta':4,'shares':{dim:1}}],4)['total'],'4')

    def test_shared_consequence_split_reconciles(self):
        result=allocate_consequences([{'id':'saved-rook','delta':9,'shares':{'material':'2/3','action':'1/3'}}],9)
        self.assertEqual(result['dimensions'],{'material':'6','action':'3'})

    def test_duplicate_consequence_rejected(self):
        one={'id':'rook','delta':9,'shares':{'material':1}}
        with self.assertRaises(ValueError):allocate_consequences([one,one],18)

    def test_full_credit_in_multiple_dimensions_rejected(self):
        with self.assertRaises(ValueError):allocate_consequences([{'id':'rook','delta':9,'shares':{'material':1,'action':1}}],9)

    def test_renamed_duplicate_cannot_exceed_paired_total(self):
        with self.assertRaises(ValueError):allocate_consequences([{'id':'rook','delta':9,'shares':{'material':1}},{'id':'tempo-same-rook','delta':9,'shares':{'action':1}}],9)

    def test_direct_and_avoidance_are_exclusive(self):
        self.assertEqual(evaluate(chance(('1/4',leaf(9)),('3/4',leaf(2))))[1],F(15,4))

    def test_non_normalized_or_negative_chance_rejected(self):
        for ps in [('1/3','1/3'),('-1/2','3/2')]:
            with self.assertRaises(ValueError):evaluate(chance((ps[0],leaf(1)),(ps[1],leaf(0))))

    def test_unknown_or_float_probability_rejected(self):
        for p in ('unknown',0.5,True):
            with self.assertRaises((ValueError,ZeroDivisionError)):evaluate(chance((p,leaf(1)),('1/2',leaf(0))))

    def test_terminal_and_material_cannot_be_summed(self):
        with self.assertRaises(ValueError):evaluate(chance(('1/2',leaf(1,'outcome')),('1/2',leaf(9))))
        with self.assertRaises(ValueError):paired_value(leaf(9),leaf(1,'outcome'))

    def test_terminal_anchor_range(self):
        for value in (2,-1,'3/4'):
            with self.assertRaises(ValueError):evaluate(leaf(value,'outcome'))

    def test_terminal_absorbs_no_material_bonus(self):
        self.assertEqual(paired_value(leaf(1,'outcome'),leaf(1,'outcome'))['conditional_impact_index'],'0')
        self.assertEqual(paired_value(leaf(0,'outcome'),leaf('1/2','outcome'))['conditional_impact_index'],'50')
        self.assertEqual(paired_value(leaf(0,'outcome'),leaf(1,'outcome'))['conditional_impact_index'],'100')
        self.assertEqual(paired_value(leaf(1,'outcome'),leaf(0,'outcome'))['conditional_impact_index'],'-100')

    def test_all_toy_cases_block_global_publication(self):
        for case in cases():
            self.assertFalse(publication_gate({'kind':case['evidence_kind'],'utility':'outcome'})['global_numeric_publishable'])

    def test_even_asserted_checkboxes_cannot_promote_toy(self):
        flags={k:True for k in publication_gate({})['missing'] if k not in ('common_outcome_utility','not_a_toy_or_partial_position')}
        flags.update(kind='toy',utility='outcome')
        self.assertFalse(publication_gate(flags)['global_numeric_publishable'])

    def test_rule_version_and_precision_are_required(self):
        missing=publication_gate({'kind':'paired_full_game_data','utility':'outcome'})['missing']
        self.assertIn('current_rule_snapshot',missing);self.assertIn('precision_justified',missing)

    def test_candidate_ready_is_separate_from_formal_adoption(self):
        flags={k:True for k in publication_gate({})['missing'] if k not in ('common_outcome_utility','not_a_toy_or_partial_position')}
        flags.update(kind='paired_full_game_data',utility='outcome')
        self.assertTrue(publication_gate(flags)['global_numeric_publishable'])
        self.assertFalse(publication_gate(flags)['formal_numeric_publishable'])
        flags.update(method_adopted=True,release_reviewed=True)
        self.assertTrue(publication_gate(flags)['formal_numeric_publishable'])

    def test_historical_wind_opening_milestone_schedule(self):
        self.assertEqual([historical_wind_schedule(n)['minimum_own_formal_turns_in_restricted_schedule'] for n in (0,1,2)],[4,3,2])

    def test_local_material_has_no_global_conversion(self):
        self.assertIsNone(paired_value(leaf(0),leaf(9))['conditional_impact_index'])

    def test_lifespan_resource_sensitivity_is_not_strength(self):
        rows=sensitivity()
        self.assertEqual([r['H14_ordinary_resource_only_ceiling'] for r in rows],[5,6,6])
        self.assertEqual([r['historical_wind_max_uses'] for r in rows],[2,2,2])
        self.assertTrue(all(r['whole_game_value'] is None for r in rows))

    def test_source_flame_material_accounting(self):
        self.assertEqual(F(9)+F('9/2')-F(4)-F(1),F('17/2'))
        self.assertEqual(F('17/2')-F('9/2'),4)

    def test_opportunity_cost_is_not_subtracted_twice(self):
        self.assertEqual(paired_value(leaf('9/2'),leaf('17/2'))['delta'],'4')
        self.assertNotEqual(paired_value(leaf('9/2'),leaf('17/2'))['delta'],str(F(4)-F('9/2')))

    def test_empty_and_duplicate_action_catalog_rejected(self):
        with self.assertRaises(ValueError):evaluate({'kind':'max','branches':[]})
        with self.assertRaises(ValueError):evaluate({'kind':'max','branches':[{'action':'x','node':leaf(1)},{'action':'x','node':leaf(2)}]})


if __name__=='__main__':unittest.main(verbosity=2)
