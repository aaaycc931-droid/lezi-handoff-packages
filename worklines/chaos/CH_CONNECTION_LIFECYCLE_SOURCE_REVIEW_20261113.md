# 混乱线：蓝牙连接生命周期来源审查与最小验证规格

日期：2026-11-13（Asia/Shanghai）。任务：MAIN-DELEGATE-CH-LIFECYCLE-20261113；续任务：CH-LIFECYCLE-MINIMAL-WITNESS-SPEC。两步文档交付均完成，三个验证规格均NOT_RUN。交接源：6979552f76ec0a8866510306891eee9137b3ab7c。PR22实际核对仍为open draft，HEAD 71145df45ad17215a3731e53150b6728e079e375。

本报告是主线委派的只读源码/既有证据审查，不是独立QA或生产故障复现。没有运行引擎/JVM/Android/网络，没有修改协议或生产代码。复用83b6d6f逐动作地图，不重做H15/H11/吃子全部入口。旧主线已接收前两次混乱回传；本报告的主线接收另待其实际登记。

## 1. 可直接用于主线方案审查的结论

1. 同一BluetoothGameSession的建立连接任务与整个readLoop占用同一单线程执行器。旧readLoop的finally结束前，同执行器的新连接任务不能执行attach。不能用“两个readLoop任意并行”制造本来源的旧finally关闭新连接证明。
2. send不经该执行器排队；它由调用线程同步执行并持writeLock。attach/关闭路径用session监视器，未统一使用writeLock。因此单I/O执行器不等于读、写、主线程、Web全部串行；旧writer替换控制仍只证明防护分支，不能升级为真实Android竞态已复现。
3. PR22的unknown可以对应已经接受，也可以对应没有可解析行动。其既有newline用例只证明离线转接器没有转发不带换行的尾段，不证明生产readLoop在EOF时一定丢弃完整JSON。这是本轮新增的具体覆盖缺口。
4. 原生状态变化、主线程回调、evaluateJavascript提交及Web事件执行是不同节点。现有记录替身没有验证真实自动重连或端到端队列顺序。旧回调越过新CONNECTED不能仅凭“异步”推定。
5. 原请求身份和未决结果应与UI pending状态分开保留，连接/房间代际及结果查询机制只能作为待主线选择的技术候选。本报告不规定线上消息格式，也不批准自动重放。

## 2. 固定来源与实际范围

下列行号均指上述固定HEAD；blob身份另见本线READ_RECEIPTS.json的connection_lifecycle_20261113.sources。

| 简称 | 原文件 | 实际阅读 |
|---|---|---|
| S | [BluetoothGameSession.java](https://github.com/aaaycc931-droid/jieqi-engine/blob/71145df45ad17215a3731e53150b6728e079e375/android/app/src/main/java/com/jieqi/bluetooth/BluetoothGameSession.java) | 全文；48—61线程/字段，73—176启动/退出，190—230写入与attach，232—307读取/重连，324—359关闭/发事件 |
| B | [GameWebBridge.java](https://github.com/aaaycc931-droid/jieqi-engine/blob/71145df45ad17215a3731e53150b6728e079e375/android/app/src/main/java/com/jieqi/bluetooth/GameWebBridge.java) | 全文；98—125两种发送，162—203状态/消息到JS |
| W | [web/app.ts](https://github.com/aaaycc931-droid/jieqi-engine/blob/71145df45ad17215a3731e53150b6728e079e375/web/app.ts) | 731—734断连锁；1248—1369发送/消费；3619—3797原生事件；上一轮动作ID地图复用 |
| A | [MainActivity.java](https://github.com/aaaycc931-droid/jieqi-engine/blob/71145df45ad17215a3731e53150b6728e079e375/android/app/src/main/java/com/jieqi/bluetooth/MainActivity.java) | 19—50继承/桥注入，104—108销毁；不是全文UI审计 |
| J | [JVM_RESULTS](https://github.com/aaaycc931-droid/jieqi-engine/blob/71145df45ad17215a3731e53150b6728e079e375/review/native-send-accounting/JVM_RESULTS_20261030.json) | cases/ping_cases、16/0统计、环境、父版3控制；既有实验，不新执行 |
| R | [Web边界结果](https://github.com/aaaycc931-droid/jieqi-engine/blob/71145df45ad17215a3731e53150b6728e079e375/review/native-send-accounting/RESULTS_20261030.json) | 全文8行动/3ping与限制 |
| P | [native_send_jvm.py](https://github.com/aaaycc931-droid/jieqi-engine/blob/71145df45ad17215a3731e53150b6728e079e375/scripts/research/native_send_jvm.py) | 11—82替身与注入/排队/排空代码；其余仅案例/断言锚点 |
| N | [native-send-channel.ts](https://github.com/aaaycc931-droid/jieqi-engine/blob/71145df45ad17215a3731e53150b6728e079e375/scripts/research/native-send-channel.ts) | 全文，重点21—29尾段过滤、34—47投递与回调次序 |
| D | [原生核算说明](https://github.com/aaaycc931-droid/jieqi-engine/blob/71145df45ad17215a3731e53150b6728e079e375/docs/BLUETOOTH_SEND_ACCOUNTING_20261030.md) | 全文；主线MAIN_NATIVE_SEND_REPORT.md也已复读 |

协调输入：当前TASK.parallel_execution；MODE_DISPATCH/SHARED_COORDINATION同名对象；MODE_STARTUP_RECEPTION与H02_H05_INTEGRATION_REVIEW全文；HC56_REQUIREMENT_CLOSURE_PRIORITY_MAPPING的requirements。半混乱新的结果契约候选正文本轮未读取、不声称已返回或采用；只对齐HC56-P0/P1现有要求。新H02/H05设计未被引入现有fixture。

补充API来源（2026-11-13实际读取，用于解释代码所调用API，不是设备验证）：
- [Android BufferedReader.readLine](https://developer.android.com/reference/java/io/BufferedReader#readLine())：EOF可结束最后一行。
- [Android Executors.newSingleThreadExecutor](https://developer.android.com/reference/java/util/concurrent/Executors#newSingleThreadExecutor())：同一执行器任务逐个执行。
- [Android WebView.addJavascriptInterface/evaluateJavascript](https://developer.android.com/reference/android/webkit/WebView)：JS接口运行于WebView私有后台线程；evaluateJavascript为UI线程上的异步求值。
- [Activity.runOnUiThread](https://developer.android.com/reference/android/app/Activity#runOnUiThread(java.lang.Runnable))：当前已在UI线程则直接执行，否则入UI队列。

## 3. 线程、队列与状态边界

| 边 | 固定来源 | 可以确认 | 不能据此确认 |
|---|---|---|---|
| host/join → startHost/startGuest → io.execute | S87—176、48 | 建立连接在同一io队列；accept/connect后直接调用attach/readLoop | 两端无线连接同时完成或固定耗时 |
| attach → writer安装 → CONNECTED → readLoop | S217—229 | writer/socket在session锁内设置；CONNECTED事件被post后继续阻塞读 | Web已处理CONNECTED后才收到第一条消息 |
| 收到行 → JSON/协议校验 → onMessage入主线程 | S232—254 | 解析成功才post；同一readLoop按读取顺序提交消息回调；没有连接代际字段 | 所有跨线程post的全序、真实Web端到端排序 |
| sendChecked → session.send → write/newLine/flush | B109—120、S190—214 | 不经io.execute；同一writeLock内写入；written仅本地方法返回 | 远端已解析、权威接受或客户端已显示 |
| 写异常 → 当前writer身份检查 → close → DISCONNECTED → 重连调度 → throw | S202—213 | 仅writer仍等于output才关闭当前流；同步返回unknown与异步状态回调分离 | unknown返回与Web回调的真实JNI时序已测 |
| 读EOF/IOException → unexpected disconnect → finally | S249—260 | 发断连、关socket、排重连；finally在旧io任务返回前执行 | finally可自然越过同执行器下一次attach |
| scheduleReconnect → 1秒延迟回调 → start | S282—307 | 条件检查autoReconnect/role/state；延迟到期只使任务有资格执行；新io任务仍等旧任务退出 | 1秒内必恢复、被关闭的读立即退出、无滞留计时器 |
| mainHandler → Bridge.emit → evaluateJavascript | S242、331—334；B162—203 | 状态/消息监听器通常已在主线程，runOnUiThread不必再多排一轮；JS求值仍异步 | JVM替身的两个数组排空就是Android真实队列 |
| Web CONNECTED / established DISCONNECTED或ERROR | W3657—3715 | 清pendingAction/ID/unknown；断连锁由everConnected与nativeState决定 | 清UI等待等于旧请求接受/拒绝 |
| Web恢复房主 | W3675—3688 | 已有hostRoom用??=保留；按disconnects恢复、发最新授权视图 | 页面/Activity重建后旧房间与结果仍持久存在 |
| 主动disconnect/close | S73—84、347—359；A104—108 | 禁自动重连、关资源；close停止executor；无回调代际过滤/已post回调撤销代码 | 已在主线程或Web队列中的事件一定消失 |

send的代码注释“May be called from UI”不是固定调用线程证明。实际桥经A48注入，Android API将JS接口调用放在WebView后台线程。S的writeLock与session监视器不是同一把锁；writer/socket字段也不是volatile。仅由本轮局部锁序不能声称已完成跨线程可见性证明或自然旧writer替换证明，须保留真实调用调度验证。

S331的lambda捕获next/detail，但role在回调执行时读取当前字段；B的adapterEnabled也在回调处理时查询。故事件所携角色/适配器信息不是完整的“发出时连接快照”。这说明候选连接代际需要明确捕获点；不证明已经发生角色串线。

同一readLoop先post消息后处理EOF/断连，可建立该生产路径的提交先后；send失败从另一线程post状态，可能与读端消息交错。新attach仍受单io限制。不能任意倒置同一队列来冒充自然重现；旧事件进入Web后何时相对新连接事件执行，现有证据不足。

## 4. 三种未知结果的来源解释

### 4.1 完整帧已经进入权威，但本机unknown

J的flush记录保留完整JSON及换行，sendChecked返回unknown；R.channelCases[flush]将同一字节交真实房间，authorityChoice为shuffler，同时Web仍unknown；交付原生断连回调后pending变false。此为既有完整生产Java方法＋记录转接实验，足以否定“unknown=拒绝”和“解锁=接受”。

生产可能路径：写入已把足够字节交给对端，后续flush报错；对端解析和权威处理与本地失败/回调无跨端全序。本轮没有测出实际RFCOMM在哪一刻交付、是先接受还是先本地报错。保留同一原请求并核权威结果是技术需求，不是自动再发的理由。

### 4.2 零字节、截断JSON、完整JSON但无换行必须分开

- J.write_zero记录空输出，partial记录固定截断的JSON前缀；R未把它们送成合法行动。该控制下没有合法行动，不代表所有未知异常均零送达。
- J.newline实际记录是完整JSON但没有换行，不能与partial归为同一种内容。
- N使用wire.split换行后去掉最后一段，故newline尾段不进入host.receive，R.newline的authorityChoice=null是这个离线转接器的真实结果。
- 生产S232—246采用BufferedReader.readLine。API允许EOF返回已读的末行，因此若接收端在EOF前已取得完整JSON、closed条件允许且解析成功，可post该行动；若底层抛IOException、字节仍在发送缓冲、JSON不完整或本地closed提前阻断，则结果可能不同。
- 因而不能把R.newline扩大成“真实蓝牙没写换行一定未提交”。这是覆盖不等价，不撤销原16JVM/8行动结果，不声称新生产bug已复现。W1专门补这个缺口。

### 4.3 旧读任务、旧发送异常、旧回调与新连接

**可排除的常规构造：**同一session正常自动重连中，新attach由旧io任务结束后下一任务执行，因此不能让旧readLoop finally排在新attach之后，除非绕开真实执行器/直接反射调用。PR22的old_writer正是反射替换writer/socket，不是上述自然时序证明。

**仍需验证的交错：**send独立于io执行。若旧发送尚未结束而读端断开、排队重连，则旧send结束相对新attach的关系不能只靠io单线程决定；真实BufferedWriter/OutputStreamWriter内部同步、socket关闭是否唤醒阻塞写、WebView同步桥是否阻塞UI及其重连定时回调，会进一步限制它。不能凭示意图宣布此竞态自然可达。W2用生产入口和真实锁边界求证。

**旧回调：**已post的消息/状态没有session或connection generation，Web消息分支只判断当前bluetooth存在，不检查事件所属连接。状态清等待也不按原请求身份。这里能确认“缺身份过滤”，不能确认“某个旧回调必然在新CONNECTED之后”。W3记录提交/执行节点，禁止随意重排以制造结论。

## 5. 复用的证据及明确未覆盖

| 既有证据 | 本轮采用 | 不外推 |
|---|---|---|
| 16 JVM检查、3父版writer控制 | 本机写入三态、失败当前流隔离、反射旧writer防护 | 真实socket/readLoop/自动重连/Android队列 |
| R的8行动、3ping | 精确输入/返回/完整行转接到生产Web和真实jieqi房间 | 全部H15/H11动作、实际JNI或完整DOM |
| P18 Handler替身 | post收集；postDelayed直接返回而不执行 | 实际延迟重连已跑 |
| P的MainActivity替身 | runOnUiThread总入自己的数组；先排空Handler再排空Activity | UI线程直执行分支及跨队列自然交错 |
| P.old_writer | write期间反射换writer/socket后抛错 | 通过host/join/readLoop自然形成替换 |
| N投递次序 | 先交完整行/房主返回，再交记录的native callbacks | 断连回调与远端结果的全部真实先后 |
| 主线原935相关检查 | 保留主线原范围，本轮未重跑 | 本轮新增测试通过或全CH07验收 |

## 6. 主线需要决策的最小保留信息（候选，未实施）

1. 未决请求：房间/对局身份、发起玩家、传输请求ID、原动作类型、原载荷或可核验指纹、可选游戏actionId与expectedRevision。开局H15无游戏actionId仍须能关联原请求；不从新快照重建历史请求。
2. 连接代际：区分原生session、一次attach、Web房间生命周期；记录事件发出时的所属代际而非回调执行时才读取当前role。是否加本机事件字段、是否改线上协议由主线与半混乱契约候选整合后决定。
3. 结果保留：本机not_sent/written/unknown与权威接受/拒绝/去重/无记录分别存义；UI pending清除不得顺带抹掉未决事实。主线须决定权威查询与记录保留范围、终局/重连/重建/无记录时的兼容行为。
4. 降级：旧桥无sendChecked、旧端无正式结果接口时明确保持unknown。禁止把pong、CONNECTED或新snapshot当旧请求ACK；不能通过自动补交消除未知。
5. 保密：结果关联不得额外披露H15训练对象/进度/实时失败或私密随机源；保持原合法公开吃子。仅技术方案候选，不批准任何新的公开字段或新玩法。

这些是供主线决策的必要问题；不是要求支线直接发明协议，也不替半混乱采用未返回的方案。

## 7. Follow-on：最多三个最小缺失时序规格

以下均NOT_RUN；只有另获相应执行授权的责任方才能运行。复用PR22公开hero-selection原命令与原房间，不注入游戏secret，不重跑原16/3/8/3全套。需要时再用既有CH06/H15/H11来源做后续动作适配，不把hero例算全动作验收。

### W1 — 完整JSON无换行，在接收EOF/异常时的解析与权威结果

初始：复用J.newline的确切原输入和输出记录；接收session通过真实attach/readLoop路径进入CONNECTED，使用生产BufferedReader和JSON校验。
事件：输入端依次提供①完整JSON无换行后正常EOF；②同字节后IOException；③原partial截断JSON后EOF负控。只控制输入流边界，不直接调用listener伪造接收；不使用N的尾段过滤器代替readLoop。
观测：readLine返回/异常、协议解析、onMessage提交与执行、权威动作次数、disconnect/ERROR、是否有回复；发送端保留unknown，不重发。
反证：①若收到合法完整末行且进入权威，直接反驳“newline失败必未接受”；若没有，必须说明是closed/未实际交付/解析/异常哪一门，而不能仅引用旧R.null。②③不得被强行等同①。记录式流验证仍不是实际radio送达证明。
新增价值：补真实接收器EOF边界，非重跑PR22既有记录转接。

### W2 — 单io、阻塞写、断连及重连的真实锁顺序

初始：以生产host/join建立同一session；复用PR22命令，令发送在真实writer底层输出边界受控阻塞，同时readLoop可等待输入。
事件：通过输入EOF/IOException触发真实handleUnexpectedDisconnect；让主线程的真实调度/等价可证明调度推进scheduleReconnect；另一路释放旧写并使其成功或抛IOException。不得反射安装新writer或直接调用attach绕过io。
观测：线程身份、io任务开始/退出、锁获取、旧readLoop finally、每次attach和writer身份、send返回、回调入队/执行、新流是否被关闭。阻塞到主线程无法推进本身也是有效结果，不强造新连接。
反证：新attach若先于旧readLoop finally，须查是否替换了执行器或绕开生产入口；只有通过真实路径完成的旧send晚于新attach才可支持自然旧writer竞态。若内部锁/桥阻塞排除了该次序，缩小可达集并保留反射防护仅为防御性控制。
新增价值：验证原old_writer控制的自然可达性与单io约束，不重复其反射分支断言。

### W3 — 未决请求跨原生回调/Web队列与重连的身份保留

初始：既有Web guest/session与原hero命令，记录请求r；复用flush已知可接受/unknown证据作为输入条件，但自然回调路径从生产readLoop/emit/Bridge发出。
事件：在真实队列边界记录（不任意倒序）收到结果消息、断连状态、重连计时/attach、CONNECTED及evaluateJavascript提交与执行。若需可控调度，只允许保持单队列因果顺序的门闩；保留unknown、不自动发送原行动。额外新操作仅在实际UI与门禁允许后产生独立编号。
观测：事件发出与执行时的room/session/连接标识、role、pendingActionId/unknown、权威是否已执行、快照刷新、旧事件是否影响新状态。
反证：pending清除或CONNECTED不能算r已接受；如声称旧事件越过新CONNECTED，必须给真实提交/执行因果记录，不能仅重放数组顺序。若旧事件总在新连接前处理，记录该范围结论，不据此声称跨Activity重建永久安全。
新增价值：补真实回调与身份关联；与半混乱HC56-P0的正式结果要求对接，不重复N中“先帧后回调”的固定顺序。

## 8. 交付和下一步

本任务源码审查与follow_on三规格均已完成；引擎/JVM/设备运行0，CH07新增正式验收0。源报告足以让主线避免把单io误作全局串行、把newline控制当生产未送达、把反射竞态当自然故障；实际readLoop/Handler/WebView时序仍需以上限定验证。

主线可按到达增量采用本报告并结合半混乱候选形成最小兼容方案；本线不替主线实施、定协议或运行验证。后续只接具体新证据/冲突或新增授权任务。评分冻结、NET暂停、模式门禁、原资产与其他支线成果保持。
