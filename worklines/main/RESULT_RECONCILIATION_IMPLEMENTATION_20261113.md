# 主线技术取舍与实际工程增量

2026-11-13。读源起点d5d05f9；并发接收源fc70084及7d86ae4。原未知结果断点保留，本轮完成“兼容方向收敛＋有界权威结果原型”，不是完整联机恢复。

## 明确取舍

选择A作为后续技术草稿方向：保留v2外壳和旧消息类型，用hello的显式命名空间/版本协商只读结果核对；B（v3新type并升级双端验证）本轮不实施。A仍改变协议语义，不能把“v2没变”当作已经上线或自动批准所有消息。当前没有新增wire实现。

共同最小边界已经具体化：先保存原传输ID/actor/完整内容/authority/局次，再在可证明的命令提交点记结果，输出另做；查询不进入handle/submit/views、不推进时钟/RNG。未覆盖或缺记录保持unknown。无游戏actionId的英雄选择不能靠再次选英雄来查旧结果，ID-only去重不认证同actor/内容。

研究阶段选择内存256记录＋1MiB UTF-8内容绑定、FIFO、无查询续期/TTL；这是可测默认值，不承诺精确堆上限、重启恢复或永久保留。同局同权威才可核既存记录；旧局/旧authority必须明确指定，未知实例不从roomId重建。重复结果语义只有真实原始记录关联后才覆盖，首批不发duplicate凭据。

A生产接入前还必须落实可信native session/attach代次、Web实例、双方当前协商和actor连续性。Java现行回调无代次、旧Web忽略hello；因此“可穿过旧parser”不等于“旧桥可安全跨重连核对”。缺能力时只保留旧对局路径与unknown，不用sendChecked/CONNECTED顶替。将来跨重连若不能证明同一actor，仅能降级，不能靠对方自报playerId或低熵载荷hash认证。原请求私密内容不广播/不上传公开日志。

## 已实际完成

[草稿PR24](https://github.com/aaaycc931-droid/jieqi-engine/pull/24)，引擎`f30f1f5541fd84ebbf6aa298a4bcc3e446adeb80`，分支`codex/main-result-ledger-prototype-20261113`，父版PR22/71145df。仅新增6个research/test/报告文件，生产src/web/android/package均不改；发布后6文件逐内容读回一致。

代码是独立离线owner，调用真实未改的英雄选择和认输函数，把结果与room在一个同步引用中发布，再生成输出。首批覆盖hero与resign；实现对原attempt的内容/actor/scope绑定、查询隔离、淘汰和未知降级。不是已接入BluetoothHostRoom/客户端的结果服务，也不是持久事务。

实际Node v24.22.1，21新检查＋原host8项=29通过/0失败；36基线blob一致。英雄选择和认输两条输出与现行host比较一致；原接受/后来拒绝、终局、投影故障、到期、无记录/重启、错actor/内容、查询不改状态/RNG/投影均有有界证据。注入故障和真实来源分别标记。首轮原型默认模式识别错误导致16失败已修，过程及命令见[原型报告](https://github.com/aaaycc931-droid/jieqi-engine/blob/f30f1f5541fd84ebbf6aa298a4bcc3e446adeb80/docs/research/MAIN_RESULT_RECONCILIATION_PROTOTYPE.md)。未跑全部935/56/64、无独立QA/Android/无线。

## 并发接收的混乱新证据

实际读取混乱CH_OFFLINE_LIFECYCLE_VALIDATION_20261113全文、引擎09af8bf1dae274e180d123370b86d444aafad4c9方法说明全文/SOURCE_AUDIT全文，JVM结果各例输入/状态/脚本及Web8例观察/最终输出；未重跑，也未全文独立审计两个驱动的实现。按其明确替身边界采用为新增来源证据：
- 7JVM/8Web由支线实际跑过；完整JSON无换行＋EOF在生产readLoop路径可进权威，同字节＋IOException不等价。
- C2旧写晚于新attach只在“关闭输入不释放阻塞输出”的条件模型成立；不能外推真实Bluetooth/JNI。
- C3两种结果均清UI等待和瞬时ID，强化“原请求应独立于UI字段保留”；W3真实Android代次/越序未闭合。
本批完成的是有界队列，不将W1—W3记成全部真机验收。旧源报告头部的NOT_RUN按本新正文范围更新，不能覆盖新运行。

## 接续与分工

主线下一实施目标：把原型证实的提交/结果边界形成可选内部生产适配草稿，先不接线上查询；再按明确代次/协商来源落实A。普通H10成功路径/精确研究另见H10_PREPARATION_IMPLEMENTATION_SCOPE.md，不依赖这个协议。不能等所有支线测试后才开始主线自身工作。

混乱原C1—C3已完成，追加C4仅做“客户端未决原请求保存”的离线研究原型：消费它自己已跑出的精确回调/出站输入，与本PR24结果语义对齐，禁止把存档当游戏成功、禁止重放action。范围见本线TASK_FROM_MAIN.main_result_increment_20261113；不重做15例、不改生产Web/native。

半混乱发布前已完成H1/H2/H3（engine9f0b14c），主线全文读其回传/引擎方法及结果计数/范围元信息，13例按支线自测层级接收；未全文审计驱动/逐例原JSON或重跑。相同最终英雄也可能来自到期随机、认输与forfeit重复语义不同、Web可在已提交后发拒绝措辞error，是内部适配必须保留的约束。本次改派对PR24真实代码的一次有界反例审查，不重复H1/H2/H3、13或29。它线对新PR24任务实际读取/采用由自身回执证明。

英雄设计并发新增路径已观察，未全文接收；单英雄试点RETURN_TO_MAIN已读工程候选元信息（PR23/7a1dfbc、浏览器QA缺口），未审其20文件/设计/结果正文、未批准集成。保留独立分支及成果，不让本研究覆盖它。

## 明确未完成

客户端原请求持久保存、native代次与actor连续性、协商与线上只读查询、全部动作结果分类、跨重启持久化、原普通/半混乱门禁和正式验收、独立英雄正式集成均未完成。评分原账本冻结、NET暂停、不合并/部署/APK。
