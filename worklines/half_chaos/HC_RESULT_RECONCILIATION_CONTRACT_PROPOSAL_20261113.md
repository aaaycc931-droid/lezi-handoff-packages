# 旧请求结果核对：候选合同、兼容方案与失败复核

- 日期：2026-11-13；执行者：半混乱支线。
- 任务：MAIN-DELEGATE-HC-RESULT-CONTRACT-20261113；后续复核：HC-RESULT-CONTRACT-FAILURE-REVIEW，两步均完成文档交付。
- 交接源：`6979552f76ec0a8866510306891eee9137b3ab7c`；引擎：PR22 `71145df45ad17215a3731e53150b6728e079e375`，本轮实际核为 open draft，未合并。
- **状态：候选，未批准、未实现、未运行。** 本文供主线比较及确定实施范围；不改变协议、游戏规则、生产代码、门禁或评分/NET边界。
- 复用 HC56 P0/P1，不重做110/56联表。主线已在 MODE_STARTUP_RECEPTION_20261113.md 限定接收HC56；这不代表主线已接收本文。

## 1. 本轮采用的输入与源码范围

交接库读取：本线 TASK_FROM_MAIN 的 followup/parallel_execution、主线 MODE_DISPATCH/SHARED_COORDINATION 的 parallel_execution、MODE_STARTUP_RECEPTION、H02_H05_INTEGRATION_REVIEW、MAIN_NATIVE_SEND_REPORT；混乱 RETURN_TO_MAIN.latest_receiver_phase.unknown_result_action_source_20261113；HC56 requirements、HC55三个代表请求。H02/H05新正式设计未据此升级为已准入共享规则，原110来源不改。

下列行号固定于PR22；Git blob身份见本线READ_RECEIPTS本轮对象。文件取回与实际语义审查分开。

| 来源 | 实际语义读取范围 | 可用结论 |
|---|---|---|
| src/bluetooth-protocol.ts | 全文 | v2、六种类型白名单、48 KiB、未知类型/版本拒绝；payload未作分型校验；编码也回经parser |
| src/bluetooth-host-room.ts | 全文 | host/guest固定playerId；half_chaos/xiangqi门禁；handle先推进时钟，丢弃底层duplicate并返回views；views再次推进时钟 |
| src/remote-room.ts | 247—250、373—390、807—850、874—936、982—1017、1145—1287、1530—1587 | 返回room/duplicate不足以表示完整旧请求结果；phase先于去重；无ID准备动作、超时返回、再战沿用roomId |
| src/room.ts | 全文 | player到side映射，已处理ID绕过turn检查；不是actor+payload绑定的结果账本 |
| src/game.ts | 490—548 | 普通路径processedActions按ID存在判duplicate；flowDance先分流，本轮未审其全部语义 |
| src/hero-actions.ts | 50—128 | 技能ID去重先于技能窗口/版本；不是保存完整请求/错误的回执 |
| web/app.ts | 353—377、1248—1407、3640—3760及动作ID定义锚点 | 传输id与command.actionId分离；旧hello无处理分支；pong与checked仅各自限定意义；连接状态重置等待 |
| Android BluetoothGameSession.java | 185—250、309—334及单I/O/回调锚点 | 写入、逐行读取都验v/type；未知类型在接收侧进入fail；JSON重新序列化；本轮不证明跨线程自然可达时序 |
| Android GameWebBridge.java | 33—55、97—125、184—202 | status无协议能力字段；sendChecked是本机写结果；JS回调无连接代次标签 |
| PR21旧端对照 `96fa7394f0371ab966b8b3572bf3f21b9bfe0da3` | protocol相应白名单、Java validateEnvelope、bridge send/status锚点、web接收1308—1339 | 同样拒绝新v/type；hello被解析但无业务处理；旧桥无sendChecked。本兼容结论不外推所有历史APK |

未重跑Node/JVM/Android/网络；未重新审查所有英雄/动作；未读取owner-only权威原包。混乱正在承担生命周期深审，本线不重复其全量调查，也不以未回传为阻断全部设计。

## 2. 当前实现与候选必须分开

### 已由固定源码支持

1. `BluetoothHostRoom.handle(playerId, action)`不接收外层envelope.id；Web发送action时另生成传输ID。局内command可能另有actionId，准备操作没有这个字段。它们不能互相替代。
2. 普通移动/技能remote入口先检查playing及断连，再进入内部ID去重。旧行动使phase变为finished后，重新提交可能在去重前被拒。**新一次INVALID_PHASE不能倒推旧行动没成功。**
3. `processedActions[id]`存在只支持所审路径的ID去重；未绑定原actor、完整载荷与旧裁定。不能单凭它签发“这份载荷由此玩家成功执行”的凭据。
4. `expiredFormalAction`可返回推进后的room且duplicate=false；hero选择/RPS到期也能正常返回推进后的房间。故“return且duplicate=false”不等于行动accepted。准备已完成时返回相同room，也不自动等于同一请求duplicate。
5. handle在执行前推进时间、末尾调用会推进时间的views；规则成功、后续投影/同步失败必须分开。不得将handle整段catch中所有异常统一登记为“原行动rejected”。这是源码所需边界，未声称特定故障本轮实际可达。
6. 再战beginRematch沿用roomId和席位，重置棋局/准备；roomId不能唯一标识局次。
7. 原生/JS旧端严格拒绝未知type或v；hello为合法旧类型且旧Web无处理分支。sendChecked有无仅说明本机写结果API，不能证明对端协议能力。
8. 当前CONNECTED/DISCONNECTED清等待；事件对象未给可信连接代次。历史请求凭据不能存于这几个瞬时UI字段而假定重连后仍在。

### 本轮候选，不是现行行为

引入只读结果账本及查询通道；账本与主权威提交的边界需由主线确定并实现。没有完整账本记录的旧请求默认unknown，绝不靠再次执行“试出来”。查询不会调用submit、handle、views、advance，也不取样RNG，不改变棋盘、时钟、历史或phase。现有常规计时/同步可继续独立运行，不能把它的变化归因于查询或拿它代替结果。

## 3. 最小身份与内容合同（两方案共用）

以下为**候选字段**，不表示现有wire已经存在；具体名称可由主线收敛，但对应身份不能缺失。

| 字段/内部事实 | 最小用途与约束 |
|---|---|
| authoritySessionId | 房主权威实例身份；进程/权威重建必须换代。不是蓝牙MAC，也不是roomId |
| roomId + matchEpoch | 房间与局次；再战必须换matchEpoch，旧局保留记录按旧epoch查询。现行无此epoch，需实现 |
| actorKey | 由已绑定的传输端/本机调用导出席位身份；不得信任请求自报playerId或仅用红/黑。红黑可由RPS改变 |
| originalTransportId | 原发送尝试的外层id，在发前保留；当前parser允许action不带id，候选账本只覆盖身份完整的新请求，不追溯补造 |
| commandActionId（可空） | 有ID动作的内部逻辑身份，用于辅助关联；无ID准备动作仍以原传输请求身份记账。不能凭相同ID合并不同actor或不同载荷 |
| actionKind + canonicalPayload | 房主实际收到、解释的完整请求绑定；包括expectedRevision、skip/ability、准备选项等。未知字段/缺省值处理必须有schema版本 |
| payloadBindingVersion + digest | 同一规范化算法下的内容摘要；内部保留足够的规范化内容核对。Java重序列化JSON，不能直接把客户端原字符串hash与房主重排字符串hash作等价 |
| queryId + querySessionNonce | 每次查询的新挑战与当前已协商会话绑定；与originalTransportId分离，防旧回复串入新查询 |
| originConnectionEpoch/currentConnectionEpoch | 区分原发送所在连接与当前查询连接。旧桥无可信代次；具体关联须接混乱生命周期来源，不得由当前CONNECTED布尔值冒充 |
| recordVersion/coverage | 声明账本覆盖开始点、动作种类、仍可查询的局次与记录可用性。无记录不代表未执行 |

原请求的完整载荷和摘要只在有权限的发起方/房主之间使用，不广播、不放公开GitHub；摘要也可能暴露低熵私密选择，不把hash视为自动安全。公开报告只用已公开声明ID与字段名。能力nonce用于相关性，不是新认证协议或对蓝牙安全性的证明。

无动作ID准备操作：必须在**首次发送前**生成并保留原传输ID和内容，房主在首次实际执行边界记录结果。已经发生而没有账本的旧选择，不能从HERO_ALREADY_LOCKED、PREPARATION_LOCKED或当前配置推断旧请求结果。查询协议不得把缺失ID补成一次新行动。

同ID异载荷：结果查询先核原actor、epoch和内容绑定；不匹配是**查询身份冲突**，不能返回原accepted/duplicate，也不代表原行动rejected。本候选不顺带改变现行游戏去重规则；若主线拟让新行动通道拒绝冲突，需显式另定差分。只读查询绝不把冲突载荷送入引擎。

## 4. 结果语义与写入位置

### 查询结果与原行动结果分层

- 查询本身：valid / invalid_or_unauthorized。后者拒绝提供结果，不暴露他人记录；不得写作原行动rejected。
- 原行动：accepted / rejected / duplicate / unknown。duplicate须带可证明的原始结果关联，不能作为脱离内容的布尔成功。
- 本机发送：not_sent / written / unknown，沿用PR22限定意义，独立于房主结果。
- 界面等待：pending/已解除，仍不是上述任何正式结果。

| 原行动状态 | 可签发的必要证据 | 禁止推断 |
|---|---|---|
| accepted | 完整请求身份/内容绑定，原执行分支明确完成了该命令语义，权威提交和结果记录属于同一可证明边界 | 函数正常返回、棋盘看起来相同、snapshot/pong/written、当前phase均不充分 |
| rejected | 该原尝试已识别；记录来自明确的原规则拒绝边界，证明其命令没有提交；保留当时允许发给actor的原因 | 不能用后续重试拒绝、投影/发送异常、未知JS异常推断；拒绝也不保证时钟/到期处理前后的room完全不变 |
| duplicate | 原尝试被实际识别为同actor/同局/同内容的重复，且可连到可信原结果记录；只报告已发生事实 | 反复查询不是duplicate执行；旧processedActions的ID存在不足；不同请求payload不可借ID套结果 |
| unknown | 未覆盖动作、无记录/淘汰/重启、仅有旧ID表、记录不完整、执行中、提交与记录边界不明、连接绑定不能证明 | unknown不是rejected，不授权自动重发 |

候选账本流程：合法接收且身份完整 → 内部received/executing（对外只能unknown）→ 原规则执行 → 在权威正式赋值/拒绝确定点保存对应结果 → 之后再做views/序列化/发送。若原调用在超时分支只推进room，须有明确“原命令未执行”的分支证据；当前接口未表达时继续unknown，不能制造新的游戏错误码。准备类幂等无变化返回也须依实际语义分类，不能通用地记accepted或duplicate。

实现不能只在Web的handle返回后追加一条记录：那会混淆预先推进、动作提交和末尾views异常。最小实施需在主线指定的共享权威边界提供可识别结果，保留现有游戏裁判/时间规则。对于暂不能识别的kind，能力advertisement不声明覆盖；返回unknown。未审flowDance等特殊路径不能被普通移动结论全覆盖。

内存账本可作为较小候选实施，但只保障同一存活权威实例内、未淘汰记录的查询；进程重启/权威丢失一律unknown。若需要跨重启保证，另需持久化与原子性方案，不在本任务中默认承诺。容量、TTL和保留到再战后多久待主线决定；淘汰可以发生，但不得把淘汰变成未执行证明。查询不可刷新游戏机会、原拒绝窗口或行动时钟。

## 5. 两个有实际差分的兼容候选

### A：v2外壳，hello内协商的result-query-v1

保留现有六类type、v=2及48 KiB限制。在hello.payload增加明确命名空间与schema：
- offer/accept：双方能力、随机挑战、authoritySessionId/matchEpoch、覆盖动作及保留条件；无响应或不完整响应即无能力。
- query/result：携带第3节身份。result只能回应已匹配的当前query；role、session、nonce、payload schema都严格校验。
- 原action外壳不改类型；候选新端可在经协商的元数据中绑定match/session及内容版本，房主内部捕获原envelope.id。具体元数据位置必须在实施差分中确定并被双端校验，不能在旧链路上静默认为存在。

旧PR21/22原生接受hello且保留JSON payload；旧Web不处理hello，因此可以进行有限的无游戏副作用能力探测。旧端无响应时只禁用结果查询，既有对局路径保持原行为。能力探测timeout不证明命令未执行；禁止随后发送旧端不能识别的新type。

查询可重发，重发的仍是只读query（有限次数/退避由主线定），绝不改发action。新的hello控制分支必须在任何hostRoom.handle/views之前分流，也不能误落到ping/pong解锁逻辑。双方角色不对称：客端只能查自身原请求，房主在本机按同样语义查自身账本；不把对方payload里的actor当授权。

优势：可复用已核旧原生v2白名单，协议变动较集中。代价：hello承担新的命名空间、分型和协商状态机；这是**协议语义变更**，不是“v2没变所以免审批”。旧原生无连接代次，跨重连启用仍取决于生命周期源证明；仅协商nonce不能宣称所有陈旧回调已被隔离。

### B：v2 hello能力探测，协商后的v3专用查询/结果

先用旧端可解析的v2 hello探测，确认双方应用支持v3、双方原生收发支持v2+v3，并完成当前会话绑定后，才允许v3专用result_query/result消息。原有v2游戏action可保留；不能一方单方面升级所有消息。

当前Java PROTOCOL_VERSION固定2，Web parser也固定2；所以本方案必须修改双方原生和Web验证、编码与版本能力接口。sendChecked函数存在或status.CONNECTED都不能作为v3能力；现行status没有该字段。新桥需提供明确的协议能力，缺字段默认仅旧v2。接收v3未知/超限/无协商消息需有明确拒绝且不能作用于旧请求的策略。

优势：控制类型和业务动作清晰分开，版本语义显式。代价：两端APK/桥支持与混合版本测试成本较大；旧桥组合不能使用v3，本轮不授权打包/部署。协商中断、单方升级或能力不实应禁用查询/保留unknown，不猜测回落为A（A若要作为另一个启用路径，须另经明确协商和采用）。

### 组合与降级矩阵

“新应用”指将来实现候选的一端；“旧应用”以已审PR21/22为界。“旧桥”支持现有v2六type；是否有sendChecked另算。

| 房主应用 / 客端应用 | 两端桥组合 | A结果查询 | B结果查询 | 旧行动/降级界限 |
|---|---|---|---|---|
| 旧 / 旧 | 任意未改语义旧桥 | 不支持 | 不支持 | 保持旧行为；不能事后生成结果凭据 |
| 新 / 旧 | 旧或新桥 | 旧客端不查询 | 不启用v3 | 不向旧客端发送未知type/版本；旧snapshot/error原语义保持 |
| 旧 / 新 | 旧或新桥 | hello无有效能力回执则禁用 | 禁用 | 新客端标结果不可核对；不能凭旧pong降级成accepted |
| 新 / 新 | 两端均旧桥，含无sendChecked桥 | v2 payload通路源级可行；真实链路/生命周期待验 | 禁用v3 | 无sendChecked时本机送达知识弱，但匹配的真实房主账本结果仍可与发送状态分别判；未收到结果保留unknown |
| 新 / 新 | 一新桥一旧桥 | 同上 | 禁用v3 | 不因单侧支持而发送v3 |
| 新 / 新 | 两端均新增v3能力桥 | 协商A时可用 | 仅双方明确协商B后可用 | 两方案不暗中互切；重连/重启重新核能力与会话 |
| 任意新端组合 | 原权威已重建/账本丢失 | 可回unknown，不能恢复旧结果 | 同左 | 旧roomId/相同席位不足以跨实例续接 |
| 新 / 新 | 同一权威重连，保留账本 | 条件化可核旧记录 | 条件化可核旧记录 | 需新的query挑战、原请求身份、当前通道归属均证明；本轮未证明真实回调时序 |

本线比较意见（非选定）：若目标仅为现有v2上的最小可用只读查询，A的改动面较小；若主线明确要求独立协议版本和可控双端升级，B更清晰。两者都必须先补真实结果账本，**换编码方案不能解决缺原结果**。主线/用户按原边界决定，不在本文自动采用。

## 6. 三个原110代表请求如何接证据

以下只有已有公开声明ID/结果索引，**没有真实传输ID、真实查询回复或新运行**。红黑actor还须映射到当时真实playerId，不能直接拿颜色当跨局身份。

| 原请求 | 已有有界事实 | 将来需绑定的凭据 | 不允许外推 |
|---|---|---|---|
| MA-PD01:R1:main | HC55红方正常移动accepted，主原子与normal-end两个checkpoint | 原room/match/actor、真实传输ID与commandActionId/完整载荷；原正式提交记录accepted，查询只返回该事实 | 不假定此R1造成终局，不用提交后快照替代两个精确阶段 |
| MA-DS01-02:B2:pre-1 | HC55黑方dragon_bomb成功，单技能观察点 | 单独原技能身份、ability/to等真实内容绑定、成功提交记录；不得套正常主行动结束记录 | 技能成功不等于普通主行动结束，不补造玩家wire ACK |
| MA-DS04:B3:pre-1 | HC55黑方dragon_bomb原IN_CHECK拒绝 | 原尝试拒绝记录及允许actor看到的原因，与后续新窗口/新请求分开 | 不拿后续成功或新拒绝反证原结果；原4服务端错误不变成客户端已送达 |

三个ID来自HC55原索引；本轮仅核其存在、actor/类型/原公开处置和checkpoint。106新增服务端同载荷探针及4重复拒绝仍是额外研究对照；原PD-S35/DS-S12自然刺激仍缺。56完整/64正式验收均不增加。

## 7. follow_on：失败案例复核（已完成静态设计审查）

下表同时检验A/B；“应拒绝”指拒绝查询或回复匹配，不是宣布原行动失败。不是运行通过。

| 失败案例 | 必须拒绝 / unknown / 可核对的条件 | A与B差异及所需来源 |
|---|---|---|
| F01 旧回复串新连接 | 旧queryId/session/当前挑战不匹配则丢弃，不清新行动等待；若只是缺可信代次则原结果保持unknown。新查询明确指旧原请求且账本完整才可核对 | 两者都需生命周期绑定；A不能以旧桥兼容代替隔离证明；等混乱原生/JS调度审查 |
| F02 actor混淆 | 查询自报actor与已绑定席位不符应拒绝，不能泄露记录是否存在；固定bluetooth:guest跨实例不充分 | 两者相同；host-room常量、room玩家映射已读，重连接入身份连续性待核 |
| F03 同ID异载荷 | digest/规范化内容或kind不同则拒绝查询匹配；原行动结果保留，不能称本载荷duplicate | 两者相同；已审ID-only去重不足，账本未实现 |
| F04 缓存淘汰/升级前旧记录 | unknown/not_retained或not_covered；不从absence推出not_sent/rejected，不重执行 | 两者都须声明覆盖和保留期；容量/TTL待主线选 |
| F05 accepted后finished | 不走playing门禁/submit；同局完整账本可直接返回原accepted。若只有当前finished则unknown | 两者相同；remote-room phase门禁已读。原提交与记账原子性待实施 |
| F06 旧端无能力/无回应 | 继续旧路径、禁用查询，旧请求结果unknown；不给旧端发新type/v | A旧hello被忽略；B必须双桥能力。源码结论不是设备互通实测 |
| F07 无ID准备动作已进入下一phase | 只有当原传输请求完整记账才能核对；HERO_ALREADY_LOCKED/INVALID_PHASE不能代替旧结果 | 两者相同；hero/RPS超时及准备已完成返回均需明确分类 |
| F08 执行提交后views/发送失败 | 有原子accepted记录则返回accepted并单独同步失败；无可靠记录则unknown，不统一rejected | 两者相同；handle末尾views会推进时间已读，故障是否自然可达未运行 |
| F09 超时仅推进房间且正常返回 | 缺明确原命令处置继续unknown；不可用duplicate=false当accepted；若未来有证明未执行的原裁定可记录rejected及适当原因 | 两者相同；expiredFormalAction、hero/RPS deadline分支已读，不发明现行错误码 |
| F10 再战roomId不变 | 必须区分matchEpoch；旧局结果只能明确指定旧局查询，不得用于新局等待 | 两者相同；beginRematch已读，epoch为候选新字段 |
| F11 账本执行中/重启中断 | executing对外unknown；恢复后仅完整提交记录可核对；不依据received写入认定accepted | 两者相同；内存丢失不承诺跨重启，持久事务另案 |
| F12 canonical JSON不一致 | 键序/Java重序列化不应误判冲突；须同schema规范化，数组顺序、缺省与额外字段策略显式；无法一致则unknown或查询无效 | 两者相同；双方算法/测试待实现，不能用宽松归一化吞不同skip/revision |
| F13 规则拒绝但时钟已推进 | 原命令rejected与到期/断连时钟事实分别记录；不能宣称整room完全未动 | 两者相同；handle预推进与PR20拒绝后snapshot保留 |
| F14 query被发成action或触发views | 必须阻止分流错误；查询不得更新游戏、抽数、时钟或历史。未来需调用路径证据 | A的hello新分支需严格schema；B的新type需明确只读路由 |
| F15 反复查询被算重复执行 | 同一原记录每次查询可仍返回accepted/rejected；不得因查询次数改成duplicate或增记游戏动作 | 两者相同；duplicate只指已发生的原重复命令事实 |
| F16 私密准备/他人ID探测 | 只回应本actor允许的结果；内容摘要/原因不广播，拒绝查询不泄露他人存在性 | 两者相同；不公开原包，合法公开消息另走现有投影 |
| F17 旧ID-only表与账本内容冲突 | 只读账本不“修复”游戏去重；若无法证明原actor/载荷则unknown，交主线定去重差分 | 两者相同；不能把候选冲突策略伪装为已确认玩法 |
| F18 原生known not_sent vs host记录accepted | 若各自身份确为同一原尝试，说明来源/关联矛盾；停止自动归类并保留审计，不覆盖任一证据、不重放 | 两者同样需精确原尝试身份；PR22本机边界不是全局证明 |

## 8. 可交主线的最小实施分界与未决

第一阶段建议只覆盖明确可识别结果的动作与同一存活权威账本；无结果记录/特殊未审路径返回unknown。方案选择前不写生产代码；若主线决定实施，至少明确：
1. A或B，以及能力协商字段与双端降级行为。A同样是协议语义变化；B另涉及原生升级。
2. accepted/rejected/duplicate的动作专属产生点和权威提交/账本一致性，尤其超时无操作正常返回、准备幂等返回、提交后views失败。不能只包装现有RemoteActionResult。
3. actor/authority/match/连接代次与原请求保存；接收混乱生命周期报告后填真实可达顺序，未证部分继续unknown。
4. 暂存位置、容量/保留期、再战与重启的边界；默认不提供跨重启恢复保证。
5. 规范化内容/schema、冲突查询拒绝与隐私输出；是否进一步更改游戏去重须单列审批。
6. 未来验证先看查询零游戏副作用、旧端解析/忽略边界、F01—F18和三原请求绑定；具体运行由主线依法授权。不得把文档检查计入产品验收。

## 9. 检查与局限

协作检查：L3限定候选语义/来源审查，工作稿v0.18，正式基线1.8.0。关键主张分类：源码事实见§1—2；候选字段/方案/优先顺序为AI设计提议；跨线程自然时序与实际能力为待证，不混用。

风险：中等、可逆文档；若被误采为已实施协议会错误确认旧行动，因此完成层级显式保留。竞争方案是A/B；“仅展示当前快照不出正式结果”可保守降级，但不满足P0，不能冒充第三个等价完成方案。

本轮实际验证：固定PR22/PR21源码段读取和差分边界核对，HC55三个声明的索引核验，18项失败案例的同一执行者静态推演。没有运行实现、没有独立QA；源码符合不证明设计完整。未证明actor在断连重连后的认证连续性、原生回调全部可达顺序、所有动作的权威原子性、缓存策略成本与真机互通。

失败条件：把候选当批准；return当accepted；新拒绝倒推旧请求；同ID忽略载荷/actor；查询触发游戏；私密内容外泄；旧桥能力凭sendChecked推断；没有原记录却宣称可恢复。出现任何一项须收敛对应实现范围，保留unknown及原证据。

下一动作：主线比较选定协议/账本范围，并结合混乱生命周期回传核关键争议。本线在收到具体取舍、差分或新的源证据后针对性修订；两步已交付，不重复110/56联表或无新增依据的自审。评分冻结、NET暂停、featuresReady=false、原56/64完整验收不变。

发布基准：`b48e06001307fe38774c5395b67a242b12a279c1`。相对读源提交仅普通线7路径并发更新；本线5个既有写入目标及TASK正文逐内容比对未变，基于最新父树保留并发成果。
