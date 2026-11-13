# C5 本机连接代次草稿回传

2026-11-13（Asia/Shanghai）。任务 MAIN-CH-C5-LOCAL-CONNECTION-GENERATION-20261113；交接源 `4bd603113914ff8c4fd59cb8fc9c497f347fdb62`。

已完成 C5A native来源／scoped send 与 C5B 最终Web消费隔离，在专属分支 `codex/ch-local-generation-draft-20261113` 发布 [4bd8bf4](https://github.com/aaaycc931-droid/jieqi-engine/commit/4bd8bf4ca79d4a1743d431a55fae2f43e6c37e3c)。父版5cb3df5保留C1—C4全部成果，10文件逐内容读回一致。仅改既定的BluetoothGameSession.java、GameWebBridge.java、web/app.ts三处生产来源草稿，另加研究驱动/测试/证据；其他648个既有文件保持。没有改src、wire v2、其他线或APK。

## 具体实施

- 每native实例独立UUID；generation/sequence为单调十进制字符串。host/join、自动重连attempt、明确disconnect/close失效均换代。每个Attempt拥有自己的socket/server/writer，包括正在connect的socket。
- 旧accept/connect完成、旧readLoop/finally、旧延迟重连只能处置原Attempt；不能安装或关闭新代资源。PR22的旧writer异常保护保留并加入Attempt归属。
- 事件产生时捕获不可变instance/generation/sequence/role，穿过Handler、Bridge、evaluateJavascript不读取新role改贴旧事件。GenerationListener可选，旧Listener签名保留且每事件只通知一种接口一次。
- localTransportContext(v1)只读；sendCheckedScoped在实际writer捕获的同一锁边界比较期望代次。错代/未连接0写且not_sent、attemptedContext=null；旧写晚回携原上下文，仍只有written/unknown本机含义。
- 实际Web最终listener再次查询本机context并核已消费序号；同代合法排队消息不会因native最新序号更大被全部丢弃。页面初始化只采样一次水位，防重建页面重放此前产生的旧事件；序号以字符串比较避免JS整数精度。
- 发送首次边界固定上下文，新路径异常/坏返回不跨路径重发；旧响应和异常不改新pending。无能力旧桥沿原路径，新方法但坏能力保持unknown。C4内存未知不会因此变成accepted。

## 实际验证

| 范围 | 实跑结果 | 覆盖 |
|---|---|---|
| C5A | 16例通过 | 8类各跑inline/queued两模型：EOF/IOException、取消connect、取消accept、旧定时重连、旧发送晚回、scoped/旧send兼容、旧Listener单通知 |
| C5B | 19项通过 | 旧state/message最终JS隔离、同代合法FIFO/重复/倒序、native/Web重建、超2^53序号、正确scoped及异常/错绑/坏返回、晚响应/晚异常、旧桥/坏能力、C4未知保留 |
| 静态 | 通过 | 完整app.ts stripTypeScriptTypes、git diff --check；不是完整TS类型检查 |

使用真实生产Java类/JDK流与执行器、生产Web函数与jieqi房间。原生回调保存后延迟JS执行再切代的窗口已在最终消费处验证；额外ERROR变体和倒序明确是adversarial控制。没有反射替换writer或直接调用attach，没有重跑C1—C4/主线29例全套。

初版native14/Web16通过；补取消accept时测试替身同名变量导致一次编译失败（该轮未跑用例），只修替身命名后native16通过。一次额外转译检查误导入默认Node不提供的SourceTextModule导致命令失败，删无用导入后完整strip通过。补页面重建水位、序号字符串比较及旧异常检查后Web19通过，最终native源哈希重新生成；失败过程未抹除。

## 复现和固定证据

`python3 scripts/research/ch-generation-native.py`

`node --test --test-reporter=tap tests/research/ch-generation-web.test.ts`

[方法与模型边界](https://github.com/aaaycc931-droid/jieqi-engine/blob/4bd8bf4ca79d4a1743d431a55fae2f43e6c37e3c/review/ch-local-generation/README.md) · [native原始回调/轨迹](https://github.com/aaaycc931-droid/jieqi-engine/blob/4bd8bf4ca79d4a1743d431a55fae2f43e6c37e3c/review/ch-local-generation/NATIVE_RESULTS.json) · [Web TAP](https://github.com/aaaycc931-droid/jieqi-engine/blob/4bd8bf4ca79d4a1743d431a55fae2f43e6c37e3c/review/ch-local-generation/WEB_TESTS.tap) · [源哈希/写集](https://github.com/aaaycc931-droid/jieqi-engine/blob/4bd8bf4ca79d4a1743d431a55fae2f43e6c37e3c/review/ch-local-generation/AUDIT.json)

## 主线依赖与未完成

Android/JSON/socket/Handler是明确替身，inline与queued是两个模型，虚拟延迟不是设备定时实测；Web运行于VM，非浏览器/WebView。最终同步context查询后、JS当前处理完成前native若再次切代，未承诺跨运行时原子性；本轮闭合的是排队旧事件到最终消费入口的隔离。页面重建不恢复旧权威/界面，需新的明确连接流程。

本机标签不证明远端身份、actor连续性、authority或matchEpoch。主线仍负责这些身份与结果adapter/协商的接入审查；本分支不接新线上结果协议，不自动重发、不恢复旧记录为成功。完整真机、无线、独立QA与CH07正式验收均未完成。草稿发布不等于生产采用、合并或部署。

C5有限包完成，主线接收本轮结果仍UNKNOWN。下一只接具体新源/审查问题，不扩样本或重复旧报告；评分冻结、NET暂停、模式门禁与其他线并发成果继续保护。
