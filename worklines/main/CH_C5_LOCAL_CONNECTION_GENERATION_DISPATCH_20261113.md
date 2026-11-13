# 混乱C5已采用并派发

2026-11-13。主线实际采用以下来源审查结论和任务范围；专属分支 `codex/ch-local-generation-draft-20261113` 已从 `5cb3df526e1d41d60332b2b1f5c946f41126a720` 创建。当前任务的完整约束以 `worklines/chaos/TASK_FROM_MAIN.json#local_connection_generation_20261113` 为准，状态READY。执行者读取/采用/运行UNKNOWN，由本线自行登记。

这项工作首次实施native本机代次及最终Web消费者隔离，和主线src结果适配互不抢写；旧C4仅做内存保存，不能替代它。两阶段均在明确隔离代码/测试授权内，无需等待主线回执才开始下一段。下方为子代理实际来源核查记录；其中“未派发/待root采用”是准备时状态，由本段实际派发覆盖。

# C5分发前来源核查

本文件由临时子代理为主线准备，未提交GitHub、未给混乱线登记已读/已执行。

## 读取与结论

固定engine PR22 `71145df45ad17215a3731e53150b6728e079e375`：

- BluetoothGameSession.java全文，blob `48e02db86e4f1dce1f6cc42e10da3b329b4f22c5`。
- GameWebBridge.java全文，blob `fddf464605fd2ce3d017eb705069afcde0da5101`。
- MainActivity.java全文，blob `7173bec7fdd07bd25671a36e74e4cb7fc1368024`。
- web/app.ts 353—410、1248—1412、3626—3793相关入口全文，blob `3e5db425a6104b207070330b6709305bc678431a`；未审全文件。
- C4 `5cb3df526e1d41d60332b2b1f5c946f41126a720` 的ch-lifecycle-pending.ts与PENDING_RESULTS全文；C1—C3方法/SOURCE_AUDIT全文，ch-lifecycle-probe.py队列、socket、门闩、真实join/延迟任务相关实现锚点；驱动未重跑。实际读取的ch-lifecycle-web.ts/旧测试已取得，但不计全文语义审计。

现有Listener没有session/连接代次。Session.emit在排队lambda中读取可变role；readLoop把message直接排到Handler，Bridge.emit再排一次runOnUiThread/evaluateJavascript；Web最后不核任何代次就更新nativeState、清pending并可能调用hostRoom或处理action。只在第一次Java回调处加guard，不能覆盖已提交WebView但JS未执行的窗口。

sendChecked的返回只有本机not_sent/written/unknown，实际writer身份保护只阻止旧失败writer关闭新writer，不能让Web识别旧返回。C4的instance token是PendingMemory自身实例，不是native来源；lifecycle函数明确返回no_trusted_native_generation。当前资料足以开展一个真实有价值的本机代次隔离草稿。

旧C2模型使用单io、真实BufferedWriter和受控socket.close；旧写可晚回在其流模型下成立，真实Bluetooth/JNI未证。C1/C3已证完整EOF尾帧可达、两种权威结果都清UI；这些不要重做报告，也不能擅自改变。旧MainActivity替身总是排队，不能把它当真实Android队列证明。新测试需把inline/排队模型分别写明，并保留真机缺口。

## 主线可直接采用的工程安排

建议采用TASK_C5.json，给混乱线隔离草稿代码权限：基于保留5cb3df5的专属新分支，在实际native/bridge及Web蓝牙局部实现本机上下文和可选scoped send，分C5A来源/发送与C5B最终消费者两段。两段无需等主线确认收到。主线正在修改src/bluetooth-host-room.ts；C5明确不写它，避免抢写。

技术局部选择可以由主线在本次任务中明确：本机instance/generation字符串、不可变回调快照、作用于特定writer的compare-and-send、能力缺失降级、只读本机context查询及旧wire保持。不需让用户逐项审核工程命名或锁实现。具体锁顺序/接口细节由执行者在约束内实现并验证。任务是隔离草稿，不是已采用生产协议。

仍留主线的事项：远端actor连续性、authority/match身份、结果记录+内容规范化、hello协商、新旧对端安全降级；这些不能由本机generation证明。本机标签不可上传当远端认证，也不能把unknown改accepted。Android/JNI/无线自然时序、真实WebView与独立QA仍未完成，不能以离线模型核销。

## 未采取行动

未修改任何生产代码、未运行测试、未写GitHub/派发/回执。TASK_C5的READY采用与仓库写入需root实际执行；混乱线的读取/执行继续由它自己登记。
