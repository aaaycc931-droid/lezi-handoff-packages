# 混乱线：离线生命周期验证回传

日期：2026-11-13（Asia/Shanghai）。任务：MAIN-CH-OFFLINE-LIFECYCLE-VALIDATION-20261113。
主线委派源：`d5d05f92df1be0b3fef43b22245c0a0c5cc25fbf`。本轮 C1/C2/C3 有界离线阶段均完成，7 个 JVM 用例、8 个 Web 用例通过；不是设备验证或正式 CH07 验收。

## 实际交付

引擎专属研究分支 `codex/ch-lifecycle-verification-20261113` 已发布提交 [09af8bf](https://github.com/aaaycc931-droid/jieqi-engine/commit/09af8bf1dae274e180d123370b86d444aafad4c9)，6 文件逐内容读回一致；仅新增研究脚本、结果和说明。641 个原有文件逐 Git blob 校验未变。

- [详细方法、限制与复现命令](https://github.com/aaaycc931-droid/jieqi-engine/blob/09af8bf1dae274e180d123370b86d444aafad4c9/docs/research/CH_LIFECYCLE_VALIDATION.md)
- [JVM 原始回调和线程轨迹](https://github.com/aaaycc931-droid/jieqi-engine/blob/09af8bf1dae274e180d123370b86d444aafad4c9/review/ch-lifecycle-validation/JVM_RESULTS.json)
- [真实 Web／房间结果](https://github.com/aaaycc931-droid/jieqi-engine/blob/09af8bf1dae274e180d123370b86d444aafad4c9/review/ch-lifecycle-validation/WEB_RESULTS.json)
- [源哈希、环境与失败记录](https://github.com/aaaycc931-droid/jieqi-engine/blob/09af8bf1dae274e180d123370b86d444aafad4c9/review/ch-lifecycle-validation/SOURCE_AUDIT.json)

## 主线可采用的新增证据

| 阶段 | 实际运行 | 结论及边界 |
|---|---|---|
| C1 | 5 个生产 host→attach→readLoop 用例 | 完整无换行 JSON+EOF 确实投递 1 条消息；同字节+IOException、partial+EOF 不投递；正常换行正控和错误协议版本负控符合预期。保留真实 JDK BufferedReader，Android/JSON 是限定替身 |
| C2 | 2 个生产 join/单 io/真实 BufferedWriter 用例 | 控制旧写异常分别在新 attach 前／后发生，两次新连接均保持 CONNECTED。无反射换 writer；只证明“关闭输入但不立即释放输出”的明确流模型可达，不证明真实 RFCOMM/JNI 自然竞态 |
| C3 | 4 种流 × 2 个跨端回放顺序，共 8 例 | 完整无换行 EOF 和完整换行均使真实房间选择 shuffler；IOException/partial 均无选择。所有发送均仅一次 action、无重发或 ping；断连清掉 pending、unknown 和瞬时请求 ID，两种权威结果都能产生相同 UI 清等待 |

C1 推进了原 W1 的生产接收路径证据；C2 仅为 W2 的条件化离线可达性；C3 是 W3 的生产回调记录回放，真实 Android 队列与跨连接陈旧事件顺序仍未证明。不要把“阶段完成”理解为三个 W 规格全部设备验收。

旧转接器曾丢弃无换行尾段，其 null 仍是那个转接器的真实结果；本次经真实 readLoop 接收后能进入房间，不删除或改写旧实验。发送方 unknown 记录仍复用旧精确输入结果，不把接收 IOException 宣称为已证明的发送异常原因。

## 环境、失败和范围

实际环境：Node v24.22.1、Python 3.12.14、OpenJDK/JDK compiler 21.0.13。命令为 `python3 scripts/research/ch-lifecycle-probe.py` 与 `node scripts/research/ch-lifecycle-web.ts`。
初次研究驱动编译退出 1、尚未运行用例；当时未输出编译器 stderr。补研究 BluetoothServerSocket.close 的 IOException 声明、改进诊断输出后成功。原诊断未保留，不声称已确认唯一根因。未改生产逻辑来使测试通过。

Handler 是显式 FIFO，延迟执行为虚拟推进 1000ms 后调用生产 runnable；MainActivity 仍总入队。JSON 替身只适用此次精确 fixture 的括号、v/type 边界，非完整语法一致性证明；C3 用生产 TypeScript parser 校验有效请求。旧 16/3/8/3 与 935 套件未重跑，评分未运行；没有 Android/JNI/无线、完整 DOM、独立 QA、合并或部署。

半混乱候选合同本轮已读身份/兼容及失败边界，作为输入约束，未采用 A/B 或实现账本。主线已按 RESULT_RECONCILIATION_REVIEW 实际接收本线上一份来源报告；本轮新执行结果是否接收仍 UNKNOWN。

## 下一步

当前三段有价值离线队列耗尽。主线可用此结果收敛身份保留／结果合同与实施范围；后续需实际方案、生产差分或真实设备条件再定向验证，不通过重复报告制造进展。本线长期 main 文档写入授权仍有效；评分冻结、NET 暂停、模式门禁与其他支线并发成果保留。
