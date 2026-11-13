# C4：原请求内存保存原型

2026-11-13（Asia/Shanghai）。任务 MAIN-CH-PENDING-REQUEST-PRESERVATION-PROTOTYPE-20261113；输入交接 `e7a581d1208479e5ab48d67dd96a77bc969cc0a5`。

已在本线研究分支基于 09af8bf 增量发布 [5cb3df5](https://github.com/aaaycc931-droid/jieqi-engine/commit/5cb3df526e1d41d60332b2b1f5c946f41126a720)，新增4文件逐内容读回一致，原成果和生产代码未改。

## 实际结果

Node v24.22.1，`node --test --test-reporter=tap tests/research/ch-lifecycle-pending.test.ts`：16通过、0失败。初次16通过；补每实例本地 token 及重建后重新捕获的反例后，再跑相关16项通过。未重跑原15例或主线29例。

- 2个真实出站边界／已记录C3接收用例：EOF使真实房间选择shuffler，IOException不选择；两者发送方断连回调均清UI，研究内存仍保留原完整raw、传输ID和本机unknown，权威结果继续unknown。均只发送一次action，无重发。
- 3种本机状态：not_sent、written、unknown都不自动变成权威结果。仅在显式研究证据入口给出正确绑定的测试结果；not_sent与accepted矛盾时保留conflict/unknown。
- 5种错绑：actor、authority、room、match、完整raw不符拒绝关联；原记录不被改写。
- 其余6项：原始scope缺失、旧结果/无代次回调与新请求、FIFO淘汰/重建后重捕获、外部变更隔离、接受/拒绝矛盾、原传输ID缺失。

## 保存点与语义

研究包装在实际 Web 调用 sendChecked 的记录边界捕获原字符串，再保存记录返回的本机状态。不是生产应用已经在发送前持久保存。精确字节绑定比规范化JSON更保守：仅对象键重排也不认相同；没有声称跨Java/JS规范化互通。

实际旧帧没有authority/局次/可信连接代次。真实C3输入中这些字段保留null，provenance=production_missing；不能被后来的回复补写成历史事实。测试中fixture-authority/fixture-match显式标研究标签，fixtureAnswer只是合成结果证据入口，参考PR24语义，不连接主线owner、不解析线上回复，也不证明远端身份认证。

每个内存实例有独立本地token，防止旧实例编号与重建后新记录碰撞；它不是native代次，不上传、不证明连接身份。旧无标签回调一律标未覆盖；生产UI对旧回调的处理没有被本原型修复。

存储为最多256条FIFO内存，没有磁盘恢复、TTL或字节/堆预算承诺；测试用容量1验证淘汰。丢失的记录返回unknown。没有send能力，不能自动重发。跨进程、可信代次、协商和生产结果绑定均留主线。

## 来源和复现

- [存储助手](https://github.com/aaaycc931-droid/jieqi-engine/blob/5cb3df526e1d41d60332b2b1f5c946f41126a720/scripts/research/ch-lifecycle-pending.ts)
- [16项测试](https://github.com/aaaycc931-droid/jieqi-engine/blob/5cb3df526e1d41d60332b2b1f5c946f41126a720/tests/research/ch-lifecycle-pending.test.ts)
- [TAP输出](https://github.com/aaaycc931-droid/jieqi-engine/blob/5cb3df526e1d41d60332b2b1f5c946f41126a720/review/ch-lifecycle-validation/PENDING_TESTS.tap)
- [结果／哈希](https://github.com/aaaycc931-droid/jieqi-engine/blob/5cb3df526e1d41d60332b2b1f5c946f41126a720/review/ch-lifecycle-validation/PENDING_RESULTS.json)

实际读取PR24固定f30f1f5的main-authority-result-prototype.ts及方法说明全文，作为scope/内容绑定、unknown、内存保留的语义参考；未将其导入本分支、重跑或声称生产采用。复用09af8bf的JVM回调与旧发送记录，只测试新增存储关系。实际房间观察只用已公开hero fixture，不公开私有权威包。

本线C4有界任务完成；下一需主线生产接入／可信代次或具体新任务。C1—C3已被主线按范围接收，本C4接收尚UNKNOWN。Android/JNI/无线、独立QA、CH07正式验收不增加；评分冻结、NET暂停及其他支线保护不变。
