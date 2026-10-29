# 普通象棋线｜主线PR19 HC56共享观察失败隔离的限定接收（2026-10-29）

**任务**：`STD-MAIN-PR19-HC56-SHARED-OBSERVATION-RECEIVER-20261029`。交接核验HEAD `825dcb42aab686096e3a7111b9e4ac7c72f1d9b9`。PR19为草稿、未合并，精确源`760caf57d454af0db3be92d5b52ffc3cc9078d06`，父提交PR18 `099eca44dbaab39bdedb02a9986f7d54e9761121`。普通线**只接收共享观察器的源级/半混乱研究证据**，不接收半混乱56槽位作为普通象棋已实跑，也不代替主线声明产品输出可用。

## 本线实际复读的工程依据
- 主线 `worklines/main/MAIN_HC56_STAGE_VIEW_REPORT.md`、`HC56_STAGE_VIEW_PROGRESS.json`，主线下发 `TASK_FROM_MAIN.json#main_hc56_stage_view_increment`。
- 固定PR19 `src/mechanism-observer.ts`、`scripts/research/original-half-chaos.ts`、`scripts/research/half-chaos-stage-views.ts`、`half-chaos-stage-differential.ts`、`tests/half-chaos-stage-views.test.ts`，以及 `src/remote-room.ts` / `src/game.ts` 的公开/本人投影来源。
- 实际 `RESULTS_20261029.json` 六个汇总与原56比较行、`DIFFERENTIAL_20261029.json` 110比较行、`SOURCE_AUDIT_20261029.json`、`BASELINE_INTEGRITY_20261029.json`、`COMMAND_20261029.json`和TAP结果。项目代码变更14条路径，涉及共享`src/mechanism-observer.ts`；没有批准新玩法、产品中间房间推送或游戏模式开启。
- 普通原信息权限设计参照 `../specs/ORDINARY_PRIVATE_PUBLIC_OBSERVABILITY_MAP_20261029.json`；本轮新增12项共享/普通应用区分矩阵见 `../specs/STD_PR19_SHARED_OBSERVATION_ISOLATION_MATRIX_20261029.json`。

## 可在普通线引用的共享技术边界（不是普通运行PASS）
1. `captureMechanismEvents`可选同步`projectCheckpoint`，仅在真实`main_action_atom_closed`、`formal_turn_settled`事件到来时对冻结的副本投影；结果再复制冻结。**未启用时不额外构造投影**；`checkpointProjection`是研究事件附属字段，非生产游戏状态或玩家包。
2. `withoutMechanismEvents`让只读查询屏蔽观察；候选行动失败丢弃其临时观察事件。投影函数抛错、企图修改冻结副本、返回Promise或不可复制对象，只令研究`evidenceValid=false`且观察证据清空；**已成功行动的权威结算不因此改变**。后续正常观察捕获栈可恢复。递归从投影回调发出的事件也被抑制。
3. 精确棋局时点发生在下一`begin`、当前请求返回前；但研究驱动用的是**真实当前请求入口**的房间外壳，只把其`game.state/secret`替换为当时准确的快照，序列化输出带`ACTUAL_REQUEST_ENTRY_METADATA_NOT_COMMITTED_ROOM_DELIVERY`。这不是整条消息历史/updatedAt在阶段中已提交，也不是客户端收到中间帧。
4. 主线作者在半混乱12真实序列/110请求中保存100个主原子＋100个正式结束检查点，200份公开JSON与400份红黑玩家JSON。原56配对槽位对应112份玩家JSON，窄映射后56项可见字段相同；两个私密世界各有2个不同初始暗身份槽。**完整56义务0、客户端送达0、HC原64正式验收0**。不能把这组HC反例当普通32明棋隐私结论。
5. 独立复读`DIFFERENTIAL`行：110个原父源/默认、110个投影开启/默认、110个无观察/默认请求，逐项相等标记全部为真；仅事件新`checkpointProjection`另判，实际环境`Math.random`和`Date.now`调用为0。`related-final-20261029.tap`共873条成功、0失败，主线同作者执行；本线**未重新运行引擎**、未取回仅owner原始秘密JSONL，不声称独立QA。

## 对普通象棋的实际限制与后续检查门
- 共享观察器的`evidenceValid=false`是**研究证据失效**，不等于玩家普通行动的失败/回滚/退款，也不得产生用户可见的独立错误提示。本身不证明所有普通来源都已有真实时点观察。
- 原本的H10秘密宿主、H15受训棋即使拥有者也不知、D01普通开局五兵卒锚点的公开资格、H21锁形态直到入场、H14夜/M07混乱普通池排除仍按原确认；不能把HC`faceDown`隔离测试偷换为这些普通英雄秘密的端到端防泄露。共计18条本线静态权限/12个未运行反泄露检查仍待对应真实刺激、room/player/wire与UI检查。
- 普通PR15/18的真实32棋研究和R8窗口已有独立来源回执，**PR19没有新增普通NP32自然序列**。普通NG12限定部分完成，NG11、多防护/H10/控制/空间、普通正式验收、PR17三态消费者迁移、完整类型检查、设备/蓝牙/独立QA仍未完成。
- 主线`MAIN-ROOM-COMMITTED-OUTPUT-CHANNEL-20261029`目前只在PR19报告登记为下一计划，尚无本任务实际发布的新可验产品通道证据。应由主线串行负责共享room/客户端接口、阶段包/重复/错误回执的真实实现与验证。
- 普通线下一可独立推进：`NEXT-STD-NG11-COMPLEX-GUARD-STIMULUS-SOURCE-AUDIT-20261029`，将旧NG11及复杂例外拆成可来源支持的最小证明/未决刺激目录；不擅自实现或宣布测试通过。

**回执边界**：接收与采用仅限共享观察器的源级/半混乱限定证据；不认定HC模式、普通模式或产品已接受，主线是否实际读取/采用此回传未知。普通31/本线发起共享13、玩法Δ0、评分冻结、NET暂停、`xiangqi.featuresReady=false`。没有更改三线旧源、业务源码、评分账本和旧回执。
