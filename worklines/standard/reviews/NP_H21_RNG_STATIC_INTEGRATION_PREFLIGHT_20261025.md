# 普通模式｜NP × H21 随机授鳞与 H02/M04 真实动作接口静态预检（2026-10-25）

- ID：STD-NP-H21-RNG-STATIC-INTEGRATION-PREFLIGHT-20261025
- 来源：交接仓库 `a0c617910821583f4dc52df4f357b715c5aca48e`，最新收束 `STD-SESSION-CLOSEOUT-20261024-H21-RNG-REPLAY-CONTRACT`；引擎 **PR #13 未合并**定点 `aaaycc931-droid/jieqi-engine@3f98bc9fb89a2a209209c424c4bf1bbd2cf6aca7`。截至检查时，引擎 main `c25749d4f21d394c3d94486cfba1d786864083b6` 为不同指针；**本报告不声称 PR13 已进入 main 或线上版本**。
- 任务：`NEXT-STD-NP-H21-RNG-STATIC-INTEGRATION-PREFLIGHT`；只读源码/现行已确认设计核验，不运行 Deno/游戏引擎、不修改产品代码、不开放模式。
- 证据层级：V2 原规则/已确认原件与定点源码；V1 静态调用链推理；正式引擎测试、自然棋谱回放、独立 QA：**UNRUN**。
- 本线普通确认31、本线发起直接共享13、Δ规则0；评分冻结、NET暂停；主线接收/采用本报告**未知**。

## 一、实际准入、真实身份与前缀映射

1. `src/modes.ts:5-22`：`xiangqi.featuresReady=false`；`requireModeAdaptationReady` 拒绝尚未资格化的英雄/畸变组合（研究专用房间上下文例外不等于普通模式正式开放）；`src/game.ts:52-73` 配置英雄/唯一畸变调用 `requireModeFeatureAdaptation`。所以“从真实普通局运行此 NP”目前**准入受阻**。不得切换门禁或借研究豁免作为验收。
2. `src/slots.ts:13-49` 固定黑方15个非将帅槽位在前、红方15个在后；`src/setup.ts:72-100` 生成 `covered-00..covered-29`，普通模式虽保留 covered-* ID，全部为 `faceDown:false`；将帅为 `black-general`、`red-general`，总数32。名称中的 covered 不代表普通模式仍是暗棋。
3. B5 前黑棋未减员、均受黑方控制且未离盘、黑方15个非将帅的相对数组顺序未被额外机制改写时：黑马 `black_horse_1=covered-01`、路径黑卒 `black_pawn_0=covered-10`、黑象 `covered-02`、黑士 `covered-03`、黑车 `covered-07`。普通移动在 `src/game.ts:489-495` 把**移动棋子**放至数组末尾；R1—R5只移动红棋，黑方合格对象排序在这份候选前缀中不变。不能把逻辑别名直接当稳定游戏 ID。
4. 原 NP 合同 `specs/NP_H02_M04_H21_AS_AP_ES_CONTRACT_20261020.json`：R1红兵0,6→0,5；B1祈求；R2红兵0,5→0,4；B2祈求；R3红兵0,4→1,4；B3祈求；R4红车0,9→0,5；B4祈求并产生预兆；R5红兵2,6→2,5；B5开始应降临并允许黑马1,0→0,2；AS于R6发动，AP/ES于R6发动、B6黑卒8,3→8,4、R7使用后续刺杀。此为**待执行的完整候选前缀**，当前不能宣称已走通。

## 二、H21正式回合与随机调用：发现关键计数不符合规则

- 已确认 `rules/shared/02_CURRENT_HEROES.md#H21`：**每次祈求是占步主行动并结束本次正式回合**，第四次祈求先产生公开预兆，对方完整行动之后，己方下一个正式回合开始才降临。
- 源码 `src/hero-actions.ts:104-129` 将 `invoke` 从 `isMain` 列表遗漏：其 ActionClassification 成为 `opportunity:"before_main", countsAsFormalTurn:false`，但在 `case "invoke"` 中又设置 `endsTurn=true`。在 `src/hero-actions.ts:316-329` 生成 `lastMove.countsAsFormalTurn:false`，调用 `endSkillTurn`。
- `src/hero-actions.ts:68-81` 的 `endSkillTurn` 调用 `finishFormalTurn`，而 `src/settlement.ts:369-372` 因 `lastMove?.countsAsFormalTurn === false` **提前返回**，因此此源码路径不能按批准规则为黑方祈求增长 `formalTurns.black`。随后可能继续将轮流推进至红方，造成行动次数和**正式回合计数**分离。不能仅由这一调用链断言必定抛 `INVALID_TURN_PHASE`：该早退恰好避免立即走到阶段末尾校验；真实运行尚未复现。此缺陷是 **P0 规则/实现差异候选，交主线源码修正和实际复验**，不是新玩法候选。
- `src/settlement.ts:301-340` 的 `beginFormalTurn` 由 `turnLifecycle.side/number` 门控，每一真正的新正式回合内部调用 `ascendGalakrond`；`src/hero-descent.ts:20-36` 才在已具 omen、未 descended 时执行授鳞。当前祈求计数错位时，B1—B5正式编号、生命周期幂等和预兆后对手完整一回合这三项都不能宣称实测通过。
- 源码 `choose(pool,4,randomInt)` 是当前实现的 `min(4,N)` 无放回抽法，而规则正文只有“随机选择最多4枚”；不把实现事实自行上升为新增已批规则。N=0/1/3/4/15 的原合同、AS/ES的 `[1,1,1,4]` 与AP的 `[10,2,2,5]` 均只是输入合法且身份/顺序满足前提时的条件性抽签带，历史正式测例保持 UNRUN。

## 三、H02＋M04入口与AS/AP/ES逐支源代码差异

动作入口为 `src/game.ts:556-741 applyAuthoritativeAssassination`，合法性先经 `src/rules.ts:335-405 validatePublicMove`；`src/rules.ts:129-133` 给M04车“隔一棋且有终点对象”几何，`src/game.ts:115-143` 枚举路径棋，`src/game.ts:634-644` 先路径 `captureByCrush`；终点由龙鳞/普通攻击/刺杀单独处理。已批准的限制不扩张到其他模式、双防护、影武者、河道等。

| 分支 | 已确认/合同要求（完整guard成立时） | 定点PR13静态对照 | 状态 |
|---|---|---|---|
| AS R6，**发动回合**、无鳞路径卒、终点马单龙鳞 | 卒实际被M04碾碎；马耗鳞留位；车弹回0,5；本手耗掉，**H02英雄来源不耗、无新无形/后续机会**（2026-10-19明确限定A） | `src/game.ts:670-671` **先** `consumeAssassinationCharge` 再 `consumeDragonScale`；`709-724` 在车存活时仍可能 `entersStealth=true` 并创建潜行/活跃来源。路径死亡、鳞耗与车返回的基础路径可定位。 | **P0 规则与实现差异**；未运行 |
| AP R7，已有有效后续刺杀、路径卒一鳞、终点马无盾 | 路径卒耗鳞留原格；终点马死；车落0,2；机会消耗、无退款（2026-10-18限定A） | `destroyPiece`/ `consumeDragonScale` 使路径原子不实际死亡，后续终点按刺杀来源处理；`continuing` 时 `endStealth`。组合方向与此限定一致，但缺少引擎/王安全完整验证。 | **静态条件一致，不是PASS** |
| ES R7，已有后续刺杀、路径卒无鳞、终点马一鳞 | 路径卒死、马耗鳞；车弹回0,4，使用后的刺杀机会**不退款** | `src/game.ts:671-700` 的 `scaleBounced` 返回、`709-710` 的 `continuing` 结束潜行与此条件结果方向一致。 | **静态条件一致，不是PASS** |

AS原确认 `rules/confirmed/H02_M04_ACTIVATION_ENDPOINT_DRAGON_SCALE_CONFIRMATION_20261019.json` 的来源未用/无无形要求是明确既有用户批准，不应提新用户玩法审批来“解决”代码不一致；由主线修实现。AP限定见 `rules/confirmed/H02_M04_PATH_DRAGON_SCALE_CONTINUATION_CONFIRMATION_20261018.json`。

## 四、王安全、原子闭合和事件字段

1. `src/rules.ts:310-334` 的 `simulatePublicMove` 遇终点龙鳞直接返回原 `state`，且其普通移棋模拟**没有应用M04路径碾碎的死亡/耗鳞**；`validatePublicMove:400-402` 的 SELF_CHECK 因而并非对AS/AP/ES**完整结算后盘面**的证明。后续 `src/game.ts:433-435,638-642` 路径死亡，再于 `finishDirectDeaths:146-150` 进行落点、返回、死亡闭合。NP三个指定棋谱末态另有此前V1几何检查，但本次不能据此扩写全部前后王安全或独立验收。**P1：主线建立前置模拟与闭合后最终王安全对应矩阵**，先不擅改代码。
2. 真实可定位字段：`state.gameMode`、`revision`、`pieces[].id/x/y/faceDown/color/type`、`effectsByPieceId[id].dragonScale/dragonClaw/stealth`、`heroRuntime[side].invokeCount/omen/descended`、`formalTurns`、`turnLifecycle(side,number,phase,mainActionId)`、`lastMove(actionId,pieceId,from,to,pathCrushed,bouncedAgainstPieceId,captured,landed,classification)`、`automaticEvents`、`destructionBatches`、`landingEvents`；`secret.processedActions` 为去重证据（`src/types.ts`、`game.ts`、`settlement.ts`）。
3. `src/hero-descent.ts:25-35` 创建内部 `atom` 文本标识和 `automaticEvents` 中 `galakrond:invincible` 标记；未定位附有候选有序ID、每抽上界/返回值、被选ID或可验证随机种子的**专用权威日志**。原合同中的 `atomic_close_id`、`state_hash_or_snapshot_reference`、`rng_draw_indices`、`public/private_projection_diff` 属于建议观测字段，**不是已经可用的引擎API**。
4. `src/game.ts:403-404,572-573` 普通走子/刺杀调用 `beginFormalTurn` 时不传随机函数；`src/room.ts` 的这两类转发也不提供随机注入；`src/settlement.ts:302` 默认 `Math.random`。技能入口可传 `randomInt`（`hero-actions.ts`），`startFormalClock`亦可传；不同入口随机源不保证一致。 `hero-descent.ts:11-14` 的 `choose` 未验证索引是合法范围整数，坏输入可能误选或循环停滞，**不可直接向未隔离的现有choose注入恒非法返回做引擎测试**。
5. 观测必须使用权威服务器/合适私有权限、稳定ID有序池、每次最大上界和索引、抽中ID、动作/时序与代码版本。公开投影仅提供玩法允许的信息，不把秘密身份或可改随机索引能力给玩家；普通模式全明不意味着三模式公私授权相同。

## 五、可复验条件与责任归属

| 优先 | 主线需处理的真实阻断/差异 | 最小验收及注意事项 |
|---|---|---|
| P0 | H21祈求 `before_main` 计数错位 | 以明确已确认“每次占步”修正行动分类/正式回合推进；复验B1—B4及B5先后/计数/幂等，无额外回合或提前授鳞 |
| P0 | AS终点龙鳞拦截仍先扣H02来源且可能建潜行 | AS限guard下断言 charge保留、无 stealth/activePieceId，路径死亡/鳞耗/弹回/本手消耗不回滚；不得改AP/ES已使用后续机会行为 |
| P1 | M04路径改变棋盘后王安全未纳入预检模拟 | 对比**完整原子后的**王安全/落位与预检；添加应拒/应允对照，验证具体合法前缀与否，防止未审的路径分支扩张 |
| P1 | RNG索引边界、权威抽签凭证、同一局面重放 | 先安全隔离/校验非法随机输入，再注入合法索引；登记有序池/边界/索引/输出与可授权回放标识，严格区分测试输入与自然对局 |
| Gate | `xiangqi.featuresReady=false`，PR13未合并 | 模式资格化、独立QA及权限另由主线决定；不利用研究豁免冒充正式验收 |

**普通线本次已完成**：静态映射与接口差异报告，以上P0/P1被登记为需主线检查的**工程候选问题**；未擅改英雄/畸变规则或共享引擎。**未完成**：真实 NP 自然开局、H21祈求修正、AS实现修正、权威重放、正式AS/AP/ES/NP/RE规格、独立QA。以上统一 **UNRUN**；不写PASS、不替主线填写已收到或已采用回执。

**独立下一断点**：`NEXT-STD-NP-AS-AP-ES-OBSERVATION-GUARD-MATRIX`；在不运行引擎、不改共享代码的条件下，把AS/AP/ES已批准guard映射为最小字段/负例观察矩阵。共享修复/正式测试依赖主线对本报告**实际读取并作技术分配**；本次GitHub发布≠主线接收。

---

## 2026-10-26重要更正｜撤回H21「祈求不占步」源码P0判断（后续补录，优先于上方旧结论）

本报告此前称`src/hero-actions.ts:104-129`的`isMain`遗漏`invoke`，从而得出祈求`before_main/countsAsFormalTurn:false`。**复读同一引擎commit `3f98bc9fb89a2a209209c424c4bf1bbd2cf6aca7`，`src/hero-actions.ts:108-115`实际把`invoke`写在`isMain`列表中**；生成的是`opportunity:main/countsAsFormalTurn:true`。原“P0-H21-invoke-classified-before_main-formal-count-skipped”作为**错误的静态诊断已撤回**，不能再作为主线已证阻断。这里是源事实纠正而非程序变更，历史旧段仅供错误链追溯；B1—B5从未做引擎实测，仍UNRUN。AS首次发动H02来源过早消耗的另一个独立P0未撤回。后续以`worklines/standard/reviews/M04_PATH_CRUSH_ROYAL_SAFETY_SYMBOLIC_WITNESSES_20261026.md`及最新CURRENT_STATE / RETURN_TO_MAIN纠正记录为准。
