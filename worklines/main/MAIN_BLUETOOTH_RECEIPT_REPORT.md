# 来宾等待态与请求关联｜2026-10-30

已复现并修复旧快照/无关错误提前解除来宾等待的消费者问题。[草稿PR21](https://github.com/aaaycc931-droid/jieqi-engine/pull/21)，代码`96fa7394f0371ab966b8b3572bf3f21b9bfe0da3`，父版PR20，未合并。

完整生产applyBluetoothView、行动/消息处理和sendBluetoothChat在VM中执行，实际BluetoothHostRoom负责规则；native send和最后DOM渲染函数为记录端。两种新离线调度严格保持各方向FIFO：房主已产生的周期快照延迟到来宾发行动后到达时，权威还未看行动，旧版已解锁；真实聊天客户端10000/12001跨2秒冷却，两请求延迟至房主20001收到，第二条真实CHAT_COOLDOWN及其快照能解锁仍排队的游戏行动。没有随意重排同向消息，也不冒充原110棋谱刺激。

先明确兼容设计，后最小修改web/app.ts：来宾行动后发送同编号的既有v2 ping，只在当前pong到达后解除等待并刷新控制。任意snapshot/error/旧pong不解锁；原聊天错误静默/规则提示、快照与错误payload/编号、PR20拒绝后最新已提交视图保持。旧v2房主已有pong回路，离线新来宾/PR20房主及旧来宾/新房主实际通过；旧房主原错误后不推快照的问题不被追溯修复。没有新增规则接受/duplicate ACK、新协议字段、中间阶段公开或自动重放未知行动。

原CH06/PR14 H15/H11 seed476和合法招募0/1在A实测截止65000的-1/0/+1共6组父版/本版：完整权威/随机抽数、原snapshot/error字节及最终授权视图一致。迟到拒绝仍先原error、后PR20最新红方/无A视图、再pong；客户端等待持续至相应pong。另有明确的旧/重复帧控制和精确载荷重放，不能算原自然刺激。

**边界实际被故障注入证实：**若记录桥吞弃action却发送ping，pong仍会到达并解除等待，而权威没有收到该行动。真实Java send捕获IOException后异步transport-error、无发送成功返回，当前并无按请求核对的原生结果。故pong仅能表正常有序链路中已送消息的处理顺序，不能作为接受/拒绝/去重或真机投递证明。此故障是明确注入的控制，不宣称实际Java故障已跑。下一`MAIN-BLUETOOTH-SEND-FAILURE-ACCOUNTING-20261030`先恢复真实桥调用/错误/连接生命周期并设计兼容结果核算，不自动重发未知行动。

验证19新/59相关文件914串行通过、另2个Web静态文件50通过，37代码模块按生产方式转换。首轮4并发913/914通过，旧评分策略隔离进程invalid_policy_execution；未改评分代码/预算，完整串行复核通过，根因未独立实测。4个未改二进制素材检查/全资产包/全类型/完整DOM/Java/radio/设备/独立QA未验。15引擎路径逐内容/blob复读，611个其他既有blob保持；src游戏权威、门禁、英雄、素材未改。

公开研究文件只含调度/类型/编号/等待态与比较哈希，不公开私密权威；旧owner包身份保持，没有重复ZIP。半混乱/普通蓝牙门禁、原56完整义务与64正式验收及客户端送达仍0或未验。普通NG11/暗子来源/三态消费者等原缺口保持。

主线实际读HC54完整caller审计并针对05/08/10和当前PR20六文件字节身份及限定函数核对；未新读其余三线最新采用，不代填接收回执。三线TASK仅追加本轮共享输入，实际PR21采用待其线。评分/原账本冻结、NET暂停，山风/UI/H03/旧成果保护，无合并/部署/重复APK，本阶段不自动关闭对话。

[引擎说明](https://github.com/aaaycc931-droid/jieqi-engine/blob/96fa7394f0371ab966b8b3572bf3f21b9bfe0da3/docs/BLUETOOTH_RECEIPT_CORRELATION_20261030.md) · [研究结果](https://github.com/aaaycc931-droid/jieqi-engine/blob/96fa7394f0371ab966b8b3572bf3f21b9bfe0da3/review/bluetooth-receipt-correlation/RESULTS_20261030.json) · [进度](BLUETOOTH_RECEIPT_PROGRESS.json) · [发布复读](BLUETOOTH_RECEIPT_PUBLICATION_VERIFICATION.json)
