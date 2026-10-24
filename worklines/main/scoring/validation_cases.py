"""Source-linked conditional problems; no observed population or legal game claim."""
from fractions import Fraction as F
from candidate_model import evaluate, paired_value

def leaf(value, metric='material_proxy'):
    return {'kind':'leaf','metric':metric,'value':str(value) if isinstance(value,F) else value}

def decision(kind, **actions):
    return {'kind':kind,'branches':[{'action':k,'node':v} for k,v in actions.items()]}

def chance(*branches):
    return {'kind':'chance','branches':[{'p':str(p) if isinstance(p,F) else p,'node':n} for p,n in branches]}

def cases():
    zero = leaf(0)
    ordinary = decision('max', normal_prepare=decision('min', interrupt_left=zero, interrupt_right=zero))
    wind = decision('max', ordinary=ordinary, paired_prepare=decision('min', defend_left=leaf(4), defend_right=leaf(4)))
    information_before = decision('max', select_left=chance(('1/2',leaf(9)),('1/2',leaf(1))),
                                  select_right=chance(('1/2',leaf(1)),('1/2',leaf(9))))
    information_after = chance(('1/2',decision('max', select_left=leaf(9),select_right=leaf(1))),
                               ('1/2',decision('max', select_left=leaf(1),select_right=leaf(9))))
    catalog = [
      ('WIND-INTERRUPTION','mobility','historical_5T_2USES_oracle',ordinary,wind,'4',
       'Synthetic preparation/interruption game: later normal capture is the only payoff; no legal Xiangqi fork is asserted.'),
      ('WIND-LATE','mobility','historical_5T_2USES_oracle',ordinary,decision('max',ordinary=ordinary,late_prepare=zero),'0',
       'Same move count after the opponent has removed the opportunity; timing is in the response tree, not a per-move price.'),
      ('H03-BARRIER','protection','H03_precondition_barrier_alive',decision('min',capture=leaf(-9),wait=zero),decision('min',bounce=zero,wait=zero),'9',
       'Conditional exposed rook, active barrier, ordinary direct attack, no bypass or landing death. Local saved material only.'),
      ('H03-EXPIRED','protection','H03_after_three_enemy_formal_turns',decision('min',capture=leaf(-9),wait=zero),decision('min',capture=leaf(-9),wait=zero),'0',
       'No persistent insurance after expiry; avoided loss in the prior horizon is not promised as whole-game gain.'),
      ('H14-INFORMATION','information','H14_affordable_first_ordinary_insight',information_before,information_after,'4',
       'Conditional two-world 9/1 pool with assumed equal weights, two legal actions, no intervening response. Resource cost4 is not four material points.'),
      ('H14-NO-DECISION-CHANGE','information','H14_information_without_action_change',leaf(5),chance(('1/2',leaf(5)),('1/2',leaf(5))),'0',
       'Learning a fact has zero local decision value when it cannot change the available action/result.'),
      ('H12-FLAME','direct_destruction','H12_tier3_center_no_royals',decision('max',ordinary_cannon=leaf('9/2'),quiet=zero),decision('max',ordinary_cannon=leaf('9/2'),flame=leaf('17/2')),'4',
       'Own horse4+own pawn1 lost, enemy rook9+cannon4.5 removed =>8.5; subtract available ordinary cannon capture4.5. Restricted menu, not a solved complete board.'),
      ('H12-BAD-OPTION','direct_destruction','H12_unfavorable_optional_flame',decision('max',ordinary=leaf(1)),decision('max',ordinary=leaf(1),bad_flame=leaf(-4)),'0',
       'A bad optional use is declined. Mandatory hero costs would need a different baseline.'),
      ('TERMINAL-ALREADY-WON','terminal','H04_rain_night_conditional_anchor',leaf(1,'outcome'),leaf(1,'outcome'),'0',
       'Oracle says the baseline also wins: direct victory is not additional strength.'),
      ('TERMINAL-RESCUE','terminal','terminal_mathematical_anchor',leaf(0,'outcome'),leaf(1,'outcome'),'1',
       'Exact loss-to-win conditional anchor, not a probability of reaching this state.'),
      ('TERMINAL-DRAW','terminal','terminal_mathematical_anchor',leaf(0,'outcome'),leaf('1/2','outcome'),'1/2',
       'Exact loss-to-draw conditional anchor. No material term added.'),
      ('PRESSURE-EXCLUSIVE','pressure','conditional_assumed_branch_law',zero,chance(('1/4',leaf(9)),('3/4',leaf(2))),'15/4',
       'Direct realization and costly avoidance are exclusive branches;9+2 is not the expected gain.'),
      ('STOP-BEFORE-WINDOW','lifecycle','conditional_survival_gate',zero,chance(('1/2',wind),('1/2',zero)),'2',
       'Half the toy histories end before the opportunity; no benefits after terminal.'),
    ]
    return [{'id':i,'type':t,'rule_snapshot':s,'without':a,'with':b,'expected_delta':d,'scope':note,
             'evidence_kind':'source_linked_conditional_problem_not_game_replay','global_hero_score':None}
            for i,t,s,a,b,d,note in catalog]

def sensitivity():
    # Outcomes/targets and actual survival are deliberately not inferred from resources.
    rows=[]
    for horizon in (25,30,35):
        pupil=uses=0
        for turn in range(1,horizon+1):
            if turn%2==0:pupil+=6
            if pupil>=4+4*uses:
                pupil-=4+4*uses;uses+=1
        rows.append({'complete_rounds':horizon,'historical_wind_max_uses':2,
          'H14_ordinary_resource_only_ceiling':uses,'H14_remaining_pupil':pupil,
          'H12_max_uses':1,'real_target_availability':'unknown','whole_game_value':None,
          'H04_trigger_at_least_once_conditional_on_all_opportunities':str(1-F(17,20)**(horizon-15)),
          'H04_trigger_probability_is_not_win_probability':True})
    return rows


def historical_wind_schedule(uses):
    # Four explicitly named setup milestones, not a chess evaluator.
    # Cannon h2-e2 must precede horse h0-g2; that horse clears rook i0-h0.
    from functools import lru_cache
    predecessors=(set(),set(),{1},{2})
    @lru_cache(None)
    def shortest(done,remaining):
        if done==15:return 0
        options=[]
        def available(i,mask):return not mask&(1<<i) and all(mask&(1<<j) for j in predecessors[i])
        for i in range(4):
            if not available(i,done):continue
            after=done|(1<<i)
            options.append(1+shortest(after,remaining))
            if remaining:
                for j in range(4):
                    if available(j,after):options.append(1+shortest(after|(1<<j),remaining-1))
        return min(options)
    return {'milestones':['left_horse_b0_c2','right_cannon_h2_e2','right_horse_h0_g2','right_rook_i0_h0'],
      'uses_available':uses,'minimum_own_formal_turns_in_restricted_schedule':shortest(0,uses),
      'opponent_interference':'excluded only in this schedule witness; original scripted opponent moves do not touch these squares',
      'board_legality':'source manual ordinary-opening check, not engine/full-history verification',
      'global_hero_score':None}
