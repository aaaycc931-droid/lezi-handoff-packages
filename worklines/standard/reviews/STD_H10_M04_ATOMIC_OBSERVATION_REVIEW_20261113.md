# H10／M04原子观察合同与源码风险｜2026-11-13

基准 `6979552f76ec0a8866510306891eee9137b3ab7c`，固定引擎 `71145df45ad17215a3731e53150b6728e079e375`。本轮完成 `NEXT-STD-H10-M04-ATOMIC-OBSERVATION-CONTRACT`：10项来源证据义务、8项未运行反例规格、2项具体源码风险。机读正文见 `../specs/STD_H10_M04_ATOMIC_OBSERVATION_CONTRACT_20261113.json`。不重跑上阶段8手几何，不改共享代码、不运行引擎。

## 当前协调与真实接收

实际读取主线新并行安排 `MODE_DISPATCH.json#parallel_execution_20261113`、`SHARED_COORDINATION.json`同对象、`READ_RECEIPTS.json#parallel_dispatch_precheck_20261113`及docs/COORDINATION_SETUP新段。主线已全文读上一阶段前缀报告及NEXT元数据，但未重跑几何、未读全部合同；本线按该范围记录已接收，不写成完整验收。普通任务仍归本线，可继续已授权独立静态工作，不必等待新成果接收。其他线的传输生命周期/结果候选研究不接管、不重复。

英雄线新提交涉及H02暗影步的H05导航更正；本轮只核变更路径，未全文重审新设计。这里持续使用旧刺杀合同，既有规则及该独立设计不混用。

## 所需关系，而非新增内部时序

规则原文 `01_CURRENT_RULES.md#1.1A/2.4` 区分路径独立碾碎与终点进攻本体，并要求“候选终局→原子闭合→正式终结”。本合同只记录必要偏序：合法提交在来源处理前；路径在终点前；已承诺终点、落位、死亡记录与必要收尾在正式终结前；终结后无新的正常回合/动作。没有新定义候选终局字段、H02清理的统一总顺序或中间帧协议。

R5仍依赖此前条件前缀的合法准备、完整真帅安全和准入。世界A路径卒是宿主，世界B宿主在另一卒；两者不能共享错误的真帅死亡结论。真实H10准备未跑，所以所有O0—O9运行状态均UNRUN，不能把本合同当自然运行轨迹。

## 现有观察点能证明什么

`mechanism-observer.ts`全文已读：事件种类包含main_action_atom_closed、formal_turn_settled，但没有独立的路径死亡/候选终局类型；投影仅接这两个闭合点。路径对象可查lastMove.pathCrushed、captured及automaticEvents，但这不是已捕获该中间瞬间的不可变状态。

`game.ts#finishDirectDeaths`先落位收尾、resolveWindReturn、closeMainActionAtom，再调用closeDirectDeaths；若终局，随后emitMainActionAtomClosed(sourceTerminal=true)。`closeDirectDeaths`已经能把status设为finished。因此不能把“atom_closed”名称理解为“正式终结之前”。`turns.ts#closeMainActionAtom`本身只是生命周期phase变更，不是独立行为验收证明。

A如在本原子终结，不应为了凑齐formal_turn_settled样本继续执行回合末或下一begin。结果持久化/日志允许，继续游戏不允许。B是否正常完成回合仍要依实际最终裁判；不因宿主未被这次路径杀死就保证没有其他终局。

## 两个新增的具体风险

**R1：终局提前返回与H02清理。**固定`game.ts#applyFreshAuthoritativeAssassination`在路径、终点与queueLanding之后调用finishDirectDeaths；terminal=true即登记processedActions并返回。后面的`if (continuing) endStealth(...)`不在该分支执行，而终局观察点已在finishDirectDeaths内发出。这是已读代码的控制流事实。若合法H02/H10真的到达这里，需核使用后机会/无形和activePieceId是否残留、终局快照与最终返回是否完整；不能将既有窗口消耗遗漏忽略为“结束就没关系”。但是本线未执行来源，未证明候选自然可达、外层处理或下游实际影响，故记录静态风险，不称已复现bug/P0，不改引擎。

**R2：宿主记录表示差异。**`destroyPiece`创建captured并在destroy事件中保存copy(record)；`closeDirectDeaths`在宿主实际死亡时可能把captured对应项type改为general。最终表、旧事件副本及lastMove引用可能不完全同形。核验必须先按稳定pieceId/cause/position串联，再审公开身份/死亡来源语义；不能因pawn/general文字不同凭空计两次死亡，也不能仅凭差异断言泄密或错误。这是需要真实取证的表示风险，不是预设修复方案。

## 已完成的规格与明确未做

O0准备准入；O1行动身份；O2路径死亡；O3宿主/候选；O4终点落位；O5H02来源收尾；O6正式终结/停止推进；O7记录身份；O8观察失败隔离；O9已提交投影/重复请求。八个反例覆盖提前截断、用影武者替代真帅、两世界错绑、误用观察点、费用清理混用、重复计死亡、秘密广播及终局后补结算。

实际只做源文本/控制流阅读和合同结构、引用检查；运行0、独立QA0、新玩法0。PR19研究副本的失败隔离边界仍可引用，但不是本H10运行通过。PR20—22的written/pong/重连不是接受ACK，普通蓝牙门禁不变。本轮不公开私密权威原包，不把研究快照变玩家数据。

来源复用：同对话已读且未变的H02/H10、M04及10月17日确认与旧普通M04/H10审查；本轮复读01相关段、02 H02范围；完整读取固定mechanism-observer.ts、settlement-context.ts，定向读取game.ts刺杀入口/路径/终点/finishDirectDeaths/finishAfterPlayerAction，settlement.ts destroyPiece/settleLandings/closeDirectDeaths与turns.ts recordAction/closeMainActionAtom。不是全引擎历史审计。

## 下一步与依赖

下一独立静态任务是**H10准备期入口与候选生成链的定向来源追踪**：把已确认T0三选一、具体候选身份/去重、私有选择及真实研究准入分别映射到实际房间入口，找出缺的是代码、接口或尚未发布的证据；不重复原几何，不通过注入hostId绕过准备，不运行引擎。当前合同可供主线审O5/R1与O7/R2，不要求主线先读完才开始该来源追踪。

保持NG11 OPEN、NG12既有有限证据、普通31/共享13、评分冻结、NET暂停、featuresReady=false。此阶段发布≠主线已读；主线本轮实际接收由其自行记录。
