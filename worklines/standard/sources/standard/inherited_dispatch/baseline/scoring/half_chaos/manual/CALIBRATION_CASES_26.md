# 半混乱揭棋｜人工校准案例 v0.1

任务：`MODE-SCORE-MODEL-001 / half_chaos_jieqi`；状态：`synthetic_invariants_only`。
**所有输入数字均为纯人工算术检查**，不是英雄/畸变真实触发率、游戏PU、实际胜率、正式分数或运行测试。

| ID | 检查点 | 人工预期 |
|---|---|---|
| HC-T01 | 零效应 | delta_U=0 |
| HC-T02 | 占步净效用和唯一扣减 | net_u=2, decomposition_u=2 |
| HC-T03 | 非负单次收益概率单调 | expected_u=[0.8, 2.0, 3.2] |
| HC-T04 | 不改变行动选择的信息 | net_u=0 |
| HC-T05 | 能改变行动选择的信息 | net_u=4 |
| HC-T06 | 本侧候选池初始概率 | rook=0.13333333333333333, pawn=0.3333333333333333, total=1 |
| HC-T07 | 已确认一枚车后的后验 | rook=0.07142857142857142, pawn=0.35714285714285715, total=1 |
| HC-T08 | 再确认一兵（含死亡揭示） | rook=0.07692307692307693, pawn=0.3076923076923077, total=1 |
| HC-T09 | 红侧揭示不改变黑侧真实池 | black_rook=0.13333333333333333, black_pawn=0.3333333333333333 |
| HC-T10 | 洗牌重建槽位候选池 | postwash_rook=0.13333333333333333, postwash_pawn=0.3333333333333333 |
| HC-T11 | M07逐棋独立刷新 | RR=0.25, RB=0.25, BR=0.25, BB=0.25, total=1 |
| HC-T12 | M07非必翻 | p_same=0.5, p_flip=0.5 |
| HC-T13 | 无M07固定基础阵营 | base_secret_randomization_applies=False, normal_reveal_side=red |
| HC-T14 | M07正常揭示锁定 | public_locked_side=black, remaining_refreshes_on_piece=0 |
| HC-T15 | 洗牌本身不刷新M07 | secret_state=pending_next_normal_turn_refresh, refresh_events=0 |
| HC-T16 | 洗牌后下一正常开始刷新 | red=0.5, black=0.5, refresh_events=1 |
| HC-T17 | 局长截断情景 | opportunities=[10, 15, 20] |
| HC-T18 | 提前终局截断未来机会 | future_opportunities=0 |
| HC-T19 | H11两个窗口互斥 | sum=1, A_and_B_combined=False |
| HC-T20 | 直接兑现与规避互斥 | sum=1, expected_u=2 |
| HC-T21 | 同一消灭事件唯一主要归属 | primary=['material'], duplicated_count=0 |
| HC-T22 | H10流仅一枚实际消灭 | actual_killed_piece_count=1, actual_killed_piece=host |
| HC-T23 | 负效用不能取绝对或截零 | delta_U=-5 |
| HC-T24 | H11×H15未确认 | status=blocked_pending_rule, center=None |
| HC-T25 | 旧洞察失效但H10宿主绑定保留 | old_slot_info_valid=False, H10_host_binding_valid=True |
| HC-T26 | 冻结/上限/空分数 | score_status=frozen, candidate_dimension_sum=80, actual_hero_scores=[], actual_mutation_scores=[] |

## 判定边界

- 参数来源：规则真值来自已确认材料，PU区间是设计假设，局长及技能发挥概率仍缺实测。
- 同一收益只设置一个主归属；信息价值要求改变决策；占步收益采用完整反事实而非再次扣机会成本。
- M07刷新 50/50 是已确认规则中的条件概率，不是触发/胜率。H11 洗牌完成瞬间不产生 M07 刷新。
- H11×H15 待确认；测试只验证“阻断”标记存在，不模拟飞行落位。
- `validate_calibration.py` 验证机器字段、组合概率、代数值、互斥性和冻结状态；不会访问或运行项目引擎。
