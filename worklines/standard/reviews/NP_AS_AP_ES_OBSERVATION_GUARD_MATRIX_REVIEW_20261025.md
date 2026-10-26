# 普通象棋｜NP AS／AP／ES 观测门禁与反例矩阵（2026-10-25）

**任务**：`NEXT-STD-NP-AS-AP-ES-OBSERVATION-GUARD-MATRIX`；交接仓库读取基准 `bab2ac020ff508d4e33accf9178a21a2d355d45b`；引擎静态参考 `aaaycc931-droid/jieqi-engine@3f98bc9fb89a2a209209c424c4bf1bbd2cf6aca7`（PR13仍为未合并草稿）。实际产物：[`specs/NP_AS_AP_ES_OBSERVATION_GUARD_MATRIX_20261025.json`](../specs/NP_AS_AP_ES_OBSERVATION_GUARD_MATRIX_20261025.json)。

**边界**：只读整理测试规范与已确认限定，没有运行游戏引擎、没有修改共享代码、没有解开普通象棋模式门禁；正式 NP、AS、AP、ES、RE 和其他原测例一律 **UNRUN**。普通确认31、由普通线发起直接共享13、Δ规则0，评分冻结，NET暂停。主线实际接收／采用另行核实，不以本文件发布代替回执。

## 1. 为什么要分三种结果

既有原审批：H02＋M04后续刺杀的合法车进攻几何（2026-10-17）；**AP路径龙鳞**限定A（2026-10-18）；**AS发动终点龙鳞**限定A（2026-10-19）。ES沿原终点龙鳞拦截与后续刺杀来源作受限组合，不是另一次新审批。三者不可混淆：

| 分支与行动 | 路径黑卒 `covered-10` | 终点黑马 `covered-01` | 红车 `covered-15` | 红H02技能／机会 |
|---|---|---|---|---|
| **AS R6**：首次发动的普通M04进攻，终点一鳞 | 单独碾碎并记死亡 | 耗一鳞后留原格 | 从(0,5)返回(0,5)；不获得潜行 | **heroChargeAvailable=true**，无 activePieceId／无后续机会；本手已耗 |
| **AP R7**：已发动且正在持有一次后续刺杀，路径一鳞 | 消耗龙鳞、存活(0,3)，**没有死亡记录** | 无盾，由H02终点刺杀消灭 | 从(0,4)落位(0,2)，结束潜行 | heroChargeAvailable=false，activePieceId清除，已用机会**不得补回** |
| **ES R7**：已有后续刺杀，终点一鳞 | 单独碾碎并记死亡 | 耗一鳞后留原格 | 从(0,4)弹回(0,4)，结束潜行 | heroChargeAvailable=false，activePieceId清除，已用机会**不得补回** |

**关键区分**：AS的“未成功发动因此英雄次数没花”与ES的“已持有后续机会、尝试后被挡仍然花掉”不是同一机制。三个分支均只花本回合主行动，不加行动、不退款、不延长期限。

## 2. 真正的棋局前提（所有分支共用）

- 普通象棋32棋固定开局、全部明置，红英雄H02、黑英雄H21预锁**无敌**形态，全场仅一个M04“战车”畸变；不能引用揭棋额外暗置/反转机制，亦不可把另一英雄或畸变叠加进来。
- NP固定前缀从 R1 红兵(0,6)→(0,5)开始；B1—B4各祈求一次，**四次都是占步主行动并完成正式回合**。B4仅建立公开预兆；R5必须给红方一个完整合法反制回合；B5开始、未终局且对应状态成立才降临，不提前在B4取签，也不能消耗B5主行动。B5黑马(1,0)→(0,2)后才到分支R6。
- AS终点鳞 / ES终点鳞使用条件序列 `[1,1,1,4]`（对应已确认候选ID `covered-01/02/03/07`；`covered-10` 未被选）。AP路径鳞使用 `[10,2,2,5]`（选 `covered-10/02/03/07`；`covered-01` 未选）。两组均要求抽样前按 `covered-00..covered-14` 排列15个当前实际合格黑棋，每次上界为15、14、13、12，合法索引/无放回；**这只是限定测试输入/静态推算，不是玩家实战随机结果**。源代码的`min(4,N)`并不把规则正文“最多四枚”提升成新的确认。
- R6 AP/ES先通过H02首次普通移动从(0,5)到(0,4)，红车仍存活且获得后续两个己方正式回合窗口；B6黑卒(8,3)→(8,4)；R7才允许使用首个后续刺杀机会。不得将AS“失败保留英雄来源”套入R7已经使用的刺杀机会。
- 所有断言仅当路径敌方明地面棋恰一枚、独立M04碾碎权/防护、终点的原合法权限与龙鳞、车返回格可用、双方王安全/空间/控制/来源窗口/落位及原子闭合条件**全部证实**时成立；缺条件则标`NOT_APPLICABLE`或`BLOCKED`，不能硬判FAIL或PASS。

## 3. 观测字段分级（避免伪造可用API）

**定点源码中真实存在**：`GameState` 的 `gameMode/status/turn/revision`、`pieces` 稳定ID与空间/公开身份、`effectsByPieceId` 中龙鳞/龙爪/stealth、`assassination.red.heroChargeAvailable/activePieceId`、`heroRuntime.black.invokeCount/omen/descended`、`formalTurns`、`turnLifecycle`、`lastCompletedFormalTurn`、`lastMove.pathCrushed/bouncedAgainstPieceId/landed/captured/classification`、`captured`、`automaticEvents`、`destructionBatches`、`landingEvents`、`turnDeadlineAt`。还有仅在权威秘密态的`secret.processedActions`及`secret.formalStart`。以是否能在恰当原子边界真实读到为准，字段存在**不保证全部入口有完整历史快照**。

**必须组合推导而非单字段**：存活与坐标的对象ID匹配；路径鳞“未死亡”需要同时看原始对象、`captured`及死亡事件，不能用未出现在`lastMove.pathCrushed`单独得出；原子完整后双方将帅生存和合法受将；同回合只有一次主行动与不额外延长技能时窗。

**尚未证明存在的接口**：权威抽签时有序候选列表、每抽上界/索引/选中稳定ID、种子或防篡改回放身份、完整前后原子快照哈希、权限过滤过的公私差异。不把 JSON 合同建议字段当作源码已落地能力；数据隔离、回放与RNG错误防护由主线设计实现并验收。

## 4. 负例／拒绝规则（15例，全部未运行）

| ID | 最小反例 | 必须验证的结果 |
|---|---|---|
| NG-01—03 | 受将祈求；B4立即降临；R5已终局 | 祈求禁止／B4不抽／已终局不执行B5 |
| NG-04—06 | B5重复begin；非法RNG值或池顺序变动；N=0/1/3/4/15大小与河道／空层差异 | 幂等无多抽；非法输入阻断且**绝不能**向现有choose裸注入会卡死的假随机；只按真实合格池及已记录抽签断言 |
| NG-07—08 | 零/二路径、将帅/空终点；AS发动使用强击或AP重复带source | 按原权限拒绝，不跨流程偷用H02来源 |
| NG-09—11 | AS路径卒已有鳞；AP终点也有鳞；多重盾/H10/飞行/返回占格 | 原限定guard失效，不能套用AS/AP/ES预期 |
| NG-12 | 后续两己方正式回合窗口结束后再刺杀 | 机会失效；第二次尚未用的机会只在仍合法的原时窗有效 |
| NG-13—14 | M04碾碎打开王线；龙鳞阻死却错误制造死亡日志 | 将帅安全必须在实际路径/返回完整原子后判；鳞耗≠死亡 |
| NG-15 | 子行动／强迫应将／重复开始／计时刷新 | 不增正式回合或另开期限，无未经授权的时间延长 |

负例不是新增玩法禁止项；触及此前明确排除的新交互时只作为“当前分支不适用／需要专项复核”，不凭空决定其新结果。

## 5. 主线工程阻断与正式测试执行条件

1. **P0｜H21祈求正式回合**：`src/hero-actions.ts` 把invoke遗漏于`isMain`，分类为before_main，却又endsTurn；`src/settlement.ts` 对 `lastMove.countsAsFormalTurn=false` 提前返回。先按原用户批准修复“每祈求占步”的动作分类/结束/计数链，再真实核 B1—B5、窗口及幂等；当前不得称NP已实际可走。
2. **P0｜AS首次发动遇单龙鳞**：`src/game.ts` 在终点耗鳞之前扣英雄来源，车弹回存活后还可能建stealth。主线修复应精确守AS限定；**不得顺便给AP/ES已经使用的后续刺杀返还机会**。
3. **P1｜王安全与原子**：`src/rules.ts` 的简化`simulatePublicMove`未纳入独立M04路径碾碎后盘面，遇龙鳞还直接返回旧态；须以完整路径、终点、返回、落位及死亡派生闭合后的实际盘面核正式合法性/将军。**中途候选死亡不得等于最终终局**。
4. **P1｜随机与证据接口**：共享H21 `choose` 未对注入`RandomInt`作整数范围验证，异常值可能导致不终止；普通走棋/刺杀`beginFormalTurn`存在默认`Math.random`路径，缺权威自然抽签日志。应由主线安全地处理拒绝测试/同一局复播并保护隐私，普通线只提交条件测试合同。
5. **正式门禁**：`src/modes.ts` 仍有 `xiangqi.featuresReady=false`；研究入口不是正式授权或产品资格化。PR13尚未合并，此处不是线上版本表现。待主线**实际读回**、安排共享修复/必要资格化并真实运行完整前缀、负例、独立QA之后，才可逐个按版本/条件记PASS/FAIL。

**自检**：结构化合同已按三个分支、15个负例、原确认来源、真实字段与拟议字段区别作同一AI一致性检查；验证等级V2来源及V1构造，**无任何项目测试执行证据**。保留2026-10-24随机合同与2026-10-25静态预检原字节。无新增H02/H21/M04机制、无正式评分、无NET恢复、无跨工作线回执。

**独立下一断点**：`NEXT-STD-NP-PATH-CRUSH-ROYAL-SAFETY-SYMBOLIC-WITNESSES`，仅准备能使M04路径碾碎前后王线出现变化的最小**符号反例**及其守卫（区分假设摆盘和合法自然开局）；主线负责引擎修复和运行验证。该下一项本轮未开始。

---

## 2026-10-26重要更正｜撤回H21「祈求不占步」源码P0判断（后续补录，优先于上方旧结论）

本报告此前称`src/hero-actions.ts:104-129`的`isMain`遗漏`invoke`，从而得出祈求`before_main/countsAsFormalTurn:false`。**复读同一引擎commit `3f98bc9fb89a2a209209c424c4bf1bbd2cf6aca7`，`src/hero-actions.ts:108-115`实际把`invoke`写在`isMain`列表中**；生成的是`opportunity:main/countsAsFormalTurn:true`。原“P0-H21-invoke-classified-before_main-formal-count-skipped”作为**错误的静态诊断已撤回**，不能再作为主线已证阻断。这里是源事实纠正而非程序变更，历史旧段仅供错误链追溯；B1—B5从未做引擎实测，仍UNRUN。AS首次发动H02来源过早消耗的另一个独立P0未撤回。后续以`worklines/standard/reviews/M04_PATH_CRUSH_ROYAL_SAFETY_SYMBOLIC_WITNESSES_20261026.md`及最新CURRENT_STATE / RETURN_TO_MAIN纠正记录为准。
