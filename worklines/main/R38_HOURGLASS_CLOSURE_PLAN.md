# R38 沙漏完整闭合与一次提交方案

当前实施状态：2026-10-21后续限定补丁已完成，独立[草稿PR10](https://github.com/aaaycc931-droid/jieqi-engine/pull/10)、提交`7ece1fdda7837d4f14433f3f74c6f6be8eef4cc9`尚未合并。31项新组件、61项针对性及41文件560项相关检查通过；实际范围/命令/残留见[R38报告](R38_ENGINEERING_REVIEW.json)。以下“本轮0代码/NOT_RUN”属于固定提交`564924478f64250ecd1e65a3d153f49d1a0f944e`的原设计阶段记录，不能作为当前实施状态。原自然12/64、完整威胁/终局及研究适配器消费evidenceValid=false仍未验收。


本轮编号：MAIN-R38-HOURGLASS-CLOSURE-PLAN-20261021。状态：具体工程设计完成，尚未实施或运行。主线负责共用引擎与闭合接口，半混乱负责其准入、自然案例和接收采用；UI、普通工作稿不改。

接续源为主线交接 `13dcdad643008263c3663df1702e5f0926e4082e`，引擎采用 PR9 固定源 `74edf370acf76a377b3f74e69f252d0b7de2169d`，继承 PR8 投弹修复，不向默认 main 拆搬代码。用户本轮“进行下一步”指向已说明的沙漏具体设计；本轮代码修改、引擎导入与运行均为 0。此前 529 项通过仍是铁马/投弹组件与相关回归证据。

## 1. 规则依据与适用边界

实际重读本提交的三份原确认：`D01_HOURGLASS_CORE_CONFIRMATION_20261016.json`、`D01_HOURGLASS_ZERO_APPEARED_CONFIRMATION_20261016.json`、`D01_HOURGLASS_CHECK_SAFETY_CONFIRMATION_20261016.json`，以及 `worklines/standard/rules/shared/03_CURRENT_MUTATIONS.md` 的完整 D01 段。本轮不新增玩法批准。半混乱 `SAFETY_REPAIR_CONTRACT_PROPOSAL.json` 的 HC-SAFE-01、隔离/提交合同、七组拒绝不变量和 Q01—Q03 为工程输入，其原候选身份保留。

仅在 D01 合法可用、原房间/成员/side/版本/截止/正式主行动前窗口与剩余次数成立时处理。普通受将可进入沙漏试算；双方真将帅在完整闭合结果仍存活、无独立终局来源时，以本次完整结果判断己王安全。安全不得依靠下一次沙漏或随后的普通主行动。

零现身、零成功回归均不是自行新增的拒绝条件；有效使用扣 1 次，五次上限，第五次仍完整净化/装填。逐次自愿使用每次重新冻结候选，不自动连发。未现身身份/锚点不补入公开候选或玩家错误信息。产品 `featuresReady=false`、研究三 tuple、原 12/64 门禁均保持。

## 2. 此轮确认的源码依赖

| 位置 | 实际行为 | 对补丁的约束 |
|---|---|---|
| `remote-room.ts#submitRemoteHeroAbility` | phase/保留 ID 检查→expiry→actor/turn→`gameWithPrivateTraps`→技能；辅助函数复制整个 RoomGame | 新请求必须在第一次复制前检查原 `room.game.state` 的批次；只在技能副本检查会漏掉原 WeakMap 关联 |
| `hero-actions.ts#applyHeroAbility` | 形式校验/duplicate/特殊窗口分流→revision/phase→复制→初始化/begin→before_main→记录→沙漏→revision/死亡尾部→processed ID | 直接权威 API 也须在复制前检查原 state；不得只修远端入口。保留既有 duplicate、expiry 和其他错误优先级 |
| `settlement-context.ts` | 开放消灭批次存于 `WeakMap<GameState,...>` | 不序列化、不复制开放批次；原对象闭合才允许新候选，候选内部仍沿用同一闭合屏障 |
| `hero-actions.ts#hourglass` | 已冻结锚点、整组移置后落位、净化、装填；所有成功对象的 effects 都被覆盖 | 冻结和整组先移动保持；死亡复活清临时状态与存活对象的状态处理必须分开 |
| `settlement.ts#settleLandings` | 消耗陷阱、亡魂入格感染/死亡、崩坏；`queueLanding` 可记录来源格与原控制方 | 不能只模拟坐标；回归的落位须保留真实起点/控制信息，避免漏感染或重复叠层 |
| `settlement.ts#closeDirectDeaths` | 风归位→降临早退→死亡资源→培养死亡重选→真王存活/终局 | 只调用一次完整原尾部，不在王安全前跳过死亡后续，也不为试算加正式回合结束 |
| 同函数→`hero-progress.ts` | 培养重选使用直接包装的 `Math.random`，不是技能参数 RNG；死亡资源改 runtime/events | 副本没有隔离随机源；不能预检后重跑、换固定随机值，或把无 H15 当通用纯函数证明 |
| `mechanism-observer.ts` / `beginFormalTurn` | collector 在模块栈中，启用时 clone/freeze 可抛错；初始化型 begin 可发事件 | rejected 候选事件不得进入外层真实事件列表；不能假定所有调用都已 begin，或吞业务异常 |
| `rules.ts#isGeneralInCheck` | 使用公开攻击判定，不是完整来源闭合/全部技能应将搜索 | 只能作覆盖分支的己王受将判定，不能据一次 false 宣布完整安全、无应对或模式验收 |

另核 `turns.ts` 的 before_main 记录不推进主行动，`hero-forms.ts` 的完整包锁，`modes.ts` 的既有门禁，以及 `ghosts.ts`、`spaces.ts` 的权限/空间限制。86 份本地 src/tests 文件已逐字节计算 Git blob 并与 PR9 完整树比对，全部一致；这是依赖身份核对，不是运行证明。

## 3. 选定的执行结构

采用**同一候选只执行一次，检查后直接返回该候选**。不新增另一套沙漏模拟器，不调用现有技能函数两遍，不将整局先实写再退款。

1. 原远端 phase、ID、expiry、成员/turn 顺序保持。新的 hourglass 非 duplicate 请求，在 `gameWithPrivateTraps` 复制前执行 `requireClosedDestructionBatch(room.game.state)`。duplicate 仍按原分流，不凭本方案补载荷绑定。直接技能 API 在其原 revision/phase 检查后、首次 copy 前，对传入 state 做同样检查；原特殊窗口分派不搬迁。
2. 建立仅同步、函数栈内的候选作用域，冻结 command 的本次字段，并捕获原 state/secret 引用、revision、side、正式 number/phase、原 deadline；远端 actor/room 绑定由外层已验证调用携带。不开 `await`，不调用外部回调，不导出可序列化或客户端可伪造的 plan token。保留唯一规则执行主体，初始化/begin、分类/记录、沙漏正文及适用尾部都只在其副本中执行。
3. 初始化及 begin 仍沿原入口；已完成的开始阶段不得重复授益。候选未完成原开始条件时不能伪造 before_main；精确开始源序依照原源，不在本轮重新定义。将候选内部发出的现有机制事件暂存，接受后才交给原 collector。
4. 六步及原死亡尾部全闭合后分类：`ordinary_royal_safety` / `source_terminal` / `unsupported`。这些是工程内部诊断类别，不新增玩家字段或错误协议。普通分支检查己王；确定仍受将使用现有 `RuleError` 的 `IN_CHECK` 类别和通用文本，不附候选、锚点或秘密详情。其他原资格错误及先后关系保持。
5. 普通分支通过后，发布的是同一份完整 s/k 结果。revision 增量、action record、processedActions 只随这份结果成为真实输出；其候选内写入不是真实提交。尾部不得重跑，远端只安装返回结果一次，featureSecret.traps 随该结果更新。非终局 turn 未变则不启动时钟，原主行动和 deadline 保持。
6. 拒绝或业务抛错时丢弃副本与暂存事件；原 state、secret、room/featureSecret、自动事件/批次/库存/历史、次数/弹药、阶段/截止和 processed ID 均不因技能提交改变。墙钟自然流逝不要求 remainingMs 相同。下一次新 ID 自愿使用基于最新实际状态重检；原样重传和同 ID 冲突另按原协议，不声称已经修好。

此处“一次提交”指同步函数返回的权威结果和房间替换，不宣称数据库/网络事务、跨线程并发或幂等协议已完成。未来若 plan 逃出栈、加入异步或可重入外部调用，须先扩展真实身份/epoch/上下文绑定与失效处理，不能直接复用本设计。

## 4. 六步与状态保留的具体实现映射

| 源步骤 | 候选内执行内容 | 必须保留的边界 |
|---|---|---|
| 1 锁定现身勇士 | 一次取 `destinyIdentities` 中 time_warrior 且 shown 的适用对象，含已死现身者 | 未现身不补选；现有河道/来源权限限制不因修复扩大 |
| 2 冻结锚点资格 | 在移置前一次计算所有占据/污染/来源落位资格并记录成功 ID | 被其他将要回归对象占据也按发动瞬间失败；净化后不补试；自己已在锚点也不偷改“任意棋子占据”的原义 |
| 3 群体回归/复活 | 先完成全部成功对象移置/复活，再统一处理落位 | 无循环中的逐棋重算；复活用原公开身份、移除当前 captured 库存条目，不回滚敌方历史或秘密知识 |
| 4 落位后续 | 活棋保留原对象和未被本来源明确清除的 effects；保存原位置和控制方后 queueLanding。死棋新建明棋、仅恢复 destiny，临时状态不继承。调用同一 settleLandings 一次 | 不把活棋当复活清空全部状态；此保留是依据“只移置/复活、非完整回溯”和死棋独立清除条款作出的最小实现解释，非新增通用免疫或状态政策。空中/河道/特殊控制组合须有原来源覆盖，否则不登记为已支持 |
| 5 净化 | 全部清除扭曲及其关联、尚未结算的崩坏 | 落位死亡不撤销；不复活死龙；不延期原崩坏；不同来源状态不借净化清空 |
| 6 装填 | 此时仍存活、在本来源适用空间且 shown 的无限龙补到 1 | 不累加、不暗示未现身龙、不恢复已死龙 |
| 原尾部 | 原 revision 语义、closeDirectDeaths 完成适用死亡派生；之后才作本次安全判断 | 不调用 finishFormalTurn/advanceToFormalTurn/generateGhosts 来补造沙漏原本没有的结束链；若实际来源另要求新后续，单列差分，不混入本次批准 |

现代码活棋 effects 全量覆盖及 queueLanding 未传真实起点是额外来源风险；后续补丁要分别给差异用例，不能把旧回归通过当成它们获准。涉及特殊空间或终局未决时保持来源缺口，不通过清状态把分支变成“可安全处理”。

## 5. 外部副作用的具体接口选择

**批次。** 复用现有 `requireClosedDestructionBatch`，无需复制 WeakMap 或制造 closed 标记。原权威检查是入口屏障，副本检查是候选内部屏障，职责不同。添加原对象开放批次、复制后关联丢失的负例，以证明检查位置。

**随机。** 为 `closeDirectDeaths` 增加可选 `RandomInt` 参数，默认表达式保留旧 `Math.random` 行为，所有旧三参数调用不变；培养死亡统一使用收到的参数。hourglass 候选的 begin/死亡尾部传入同一“禁止抽样”函数，调用即在触碰生产随机源前抛出内部不覆盖诊断。合法固定 D01 双包不含 H15、风、降临等随机英雄，但 secret.training 等残留并不由英雄枚举自动排除，须源核及负例覆盖。不得改写全局 Math.random，不调用外部 RNG 再尝试回卷，不使用 0/随机重播/假结果作为安全依据。

这选择只适用于已证明零抽样的沙漏范围，不宣称通用随机事务已实现；未来真实合法来源若需抽样，须提供可 fork/提交/丢弃的生产 RNG 接口及来源确认后再开放该分支。未知分支停在内部设计/开发验证，不能把内部“不覆盖”直接变成新的产品统一拒绝政策。

**死亡资源。** 同一个候选内调用一次原 settleHeroDeathResources/settleTrainingDeaths；原资源标记、捕获库存和自动事件随候选同进同退。不得省略这些结算以满足零抽样断言。不能顺便恢复 H15 旧成本/失败策略。

**观察。** 在 `mechanism-observer.ts` 加候选作用域缓冲；未启用 collector 时不增加快照，启用时暂存既有事件，拒绝丢弃、接受按原顺序移交一次，不重放执行器或重新 clone 一遍。作用域使用 finally 复原，嵌套不把副本事件漏入父列表。候选内观测 clone/freeze 失败只使该段研究证据无效，不能改变业务是否提交；业务异常原样传播。此为候选隔离所需的窄接口，不新增 D01 六阶段事件、不重定义旧 formal_* 事件，也不宣布 WP02 所有观察完成。

## 6. 终局与安全判定的未决处置

先核真王引用/存活，再按 guard 调公开受将函数，避免用 findGeneral 抛错冒充不安全裁决。`source_terminal` 仅标注原独立终局路径，由既有源控制，不能改名“沙漏安全通过”；来源尚未裁定的独立终局继续未决。`unsupported` 不提供 safe/no-response 结论；不得吞异常、返回 false、跳安全检查或通过复制后丢上下文来“解决”。

现 `isGeneralInCheck` 不证明全技能合法应对空间，且铁马/战车等是互斥畸变，不从 PR9 的坐标修复推到 D01 全搜索。后续实施可验证明确普通攻击组件与完整候选一致，但在威胁覆盖、特殊空间和终局源不足时不得据此开放原 12/64。D01 的不安全错误复用 IN_CHECK 不新增秘密提示；实际按钮/错误封装、双玩家投影与 wire 证据仍由相应通道另验。

## 7. 后续补丁路径与验证顺序

| 路径 | 拟改范围 |
|---|---|
| `src/hero-actions.ts` | 复制前批次屏障；沙漏候选隔离/同结果提交；六步活死状态区分/真实落位上下文；完整死亡后王安全 |
| `src/remote-room.ts` | 只在新的沙漏请求、复制 RoomGame 前补原 authority 批次屏障；其余入口/timeout/duplicate 顺序保持 |
| `src/settlement.ts` | closeDirectDeaths 可选 RNG；旧调用的默认行为保持 |
| `src/mechanism-observer.ts` | 候选缓冲、丢弃/移交及观测失败隔离的窄作用域 |
| `tests/hourglass-safety-boundaries.test.ts`（拟新增） | 以下公开合成组件与原上下文的拒绝/成功/副作用差异 |
| 现有相关测试 | 复用 confirmed-runtime、action-turn-contracts、cross-rule-contracts、exception-contracts、remote-room、hero-transfer-r5、river-space、scoring-mechanism 等；仅必要直接依赖变更时调整 |

只读依赖：rules、settlement-context、hero-progress、turns、hero-forms、ghosts、spaces、modes。若补丁需要改它们的业务语义，先记录新增具体差分；不顺带路径安全、research capability、WP02 新事件、客户端或全部终局重写。分支从实时复核仍匹配的 PR9 固定 head 派生，不动 PR8/9 或默认 main。

验证按下列顺序，所有条目当前均 **NOT_RUN**：

- HG01/02：原受将可由回归挡线/复活自身解将；原安全因回归开线则整次拒绝。每例先确认原代码差异，再核完整输出和原输入深相等。
- HG03：中间看似安全、落位陷阱/感染使勇士死亡后又受将，必须以闭合结果拒绝。它是闭合 helper 合成例，不能冒充合法 D01 三 tuple 自然前缀。
- HG04：锚点冻结、交叉占据、污染第一用失败而下一次独立重检；一次内不净化后补回。
- HG05：空候选、零成功、第五次、无第六次；装填限 1、死龙不回、未现身不公开。
- HG06：活棋保留无关临时 effects、死棋清临时 effects；从/到同亡魂区域不重复入格，实际新入格仍结算。特殊空间无来源则标未覆盖。
- HG07：原 authority 开放 WeakMap 批次时，直接/远端入口均在复制前拒绝且不碰 RNG/collector；原 duplicate 分流保留。
- HG08：拒绝保留 SAFE-INV01—07 全组；下一新 ID 同状态仍独立拒绝，正常主行动机会和原截止不刷新，拒绝 ID 不被登记成功。
- HG09：生产 RNG 和 Math.random 设置计数/抛错哨兵，合法支持分支零抽样；带培养残留的内部负例在触碰真实 RNG 前停止。其他旧 closeDirectDeaths 默认路径及显式 RNG 各自只消费一次。
- HG10：collector 开关、候选拒绝/接受、clone/freeze 失败、业务异常和作用域恢复；业务 state/secret/返回/截止/RNG 等价，观测故障明确证据无效。
- HG11：错误版本、错 actor/turn、过期、主行动后、已终局按原外层优先级；没有 room/wire 证据的 duplicate 载荷冲突继续未验。
- HG12：source_terminal/王缺失/未知分支明确分类，不假造 safe/no-response；分支绑定不跨请求或 await。

先做上述最窄回归，随后相关测试一次；有实际共享依赖修改再按必要范围扩展，不运行评分采样、不合并、不构建 APK。合成案例全部通过也不能写成半混乱原自然回放或 64 项验收通过。

## 8. 本轮结果与下一断点

方案已把入口 WeakMap 屏障、六步和活死状态、死亡资源/RNG、候选 observer、同一结果提交及验证项目细化到具体函数。仍需真实补丁及测试证明，普通威胁完整性/特殊空间/独立终局缺口继续单列；没有因此新开产品或研究组合。

下一项 `NEXT-MAIN-R38-HOURGLASS-BOUNDED-PATCH`：按本方案从 PR9 继承创建独立补丁，先完成批次/候选/RNG/observer 隔离与明确普通分支差异用例，再接入完整闭合的王安全；遇来源不足只阻断依赖分支，不扩成通用安全重写。范围执行依据届时当前用户指令和工作约定记录，不把本设计发布当成新玩法批准、代码已运行或其他线已经采用。

主线 55 项玩法确认、H15 毕业跨越待决、投弹/铁马草稿 PR、其他线文件/资产、协作工作稿 v0.14 均保留。原 12 执行 0、64 项 UNRUN、评分冻结、NET 暂停。
