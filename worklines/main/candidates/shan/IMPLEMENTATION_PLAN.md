# 山v1.2｜具体实现与验证方案
日期：2026-10-21（Asia/Shanghai）。用户指令：“开始下一步”。本轮完成源码核对及可审查的实施方案，未修改游戏源码、未导入或运行引擎、未执行测试。

## 目标与固定基准
实现[山v1.2定稿](FINAL_DESIGN.md)和[当前参数](CURRENT_PARAMETERS.json)：将帅固定、全局一次邻接己方士／仕掩护、致命等级及10／20／35／50／65／80%赌命、秘密死亡、后续6个己方回合／2次特殊应将／4次有效将军；同车原线持续威胁不重复计数。

源码仓库为aaaycc931-droid/jieqi-engine。实际读取engine main为c25749d4f21d394c3d94486cfba1d786864083b6；其树缺少后续英雄与共同结算文件，不能用它直接覆盖主线后续成果。本计划以[草稿PR10固定提交](https://github.com/aaaycc931-droid/jieqi-engine/tree/7ece1fdda7837d4f14433f3f74c6f6be8eef4cc9)为源码设计基准，保留其投弹、铁马和沙漏修复链。PR10实际仍open、未合并，head为7ece1fdda7837d4f14433f3f74c6f6be8eef4cc9、base为74edf370acf76a377b3f74e69f252d0b7de2169d。

实施时再次核对分支和依赖；若有后继提交，先重读差分，不以旧树接新父提交。拟从核对后的PR10后继在独立分支codex/shan-core-20261021工作，PR仍为草稿，合并另行处理。这里是拟实施安排，未创建分支或PR。

## 源码核对发现
|现有位置|实际行为|实现要求|
|---|---|---|
|rules.ts的validatePublicMove|行动末仍受将即SELF_CHECK；isGeneralInCheck只返回布尔值|山需专属、受约束的应将入口；布尔值不足以去重将军来源。|
|game.ts的applyAuthoritativeMove、finishAfterPlayerAction|版本/重复请求检查，复制权威，校验行动，闭合落位/死亡，结束回合并切换|复用一着正式行动生命周期，不用子行动或deferTurnEnd冒充普通行动。|
|settlement.ts的advanceToFormalTurn|开始下一方前按公开试算判将死／困毙|不能在山尚有合法特殊应将时提前安排裁决；须读取权威私有状态和实际可用行动。|
|settlement.ts的closeDirectDeaths|按真实将帅／风承载者是否还在棋盘判断消灭终局|山赌命死亡不能普通移除帅位或伪造captured事件；不复用风转移／归位机制。|
|finishFormalTurn、turns.ts|正式回合有幂等生命周期；子行动和额外应将另有分类|死后6回合只扣确认的己方正式机会，不随网络重试、预览或刷新多扣。|
|types.ts、heroes.ts、hero-forms.ts|HeroId和HERO_IDS均无山；getHeroPackage要求注册；风仍有完整既有实现|不能伪装成wind或替换其技能包；内部模块名称不等于分配正式英雄编号。|
|remote-room.ts的drawHero|直接从HERO_IDS抽取|新增注册可能同时导致随机入池，须与可选／随机池资格拆开审查，第一阶段不注册。|
|modes.ts、research-source-context.ts|普通／半混乱featuresReady=false，研究来源有精确白名单，未含山|不能加客户端allowShan标志或顺手开放模式；独立模块测试不依赖改门禁。|
|publicStateSnapshot、serializePublicRoom|分别深拷贝整个GameState|只在界面隐藏不够；生死、预算和死后进度不得进入公共GameState。|
|ownerHeroSecrets、playerRoomView|按已认证viewerSide分发本方秘密|后续在本方专属投影接入；公共序列化和敌方视图须配对验证。|

已核对的源码快照为15个文件；只对本任务相关函数／类型及两个既有测试文件开展定向语义审查，不宣称全仓库审计。文末保留文件身份。

## 第一阶段：独立规则模块，先验证计数
这是建议先实际实施的最小范围。拟新增两个文件：
- src/shan-core.ts：独立类型、纯状态转换、概率阈值与本方私有投影。
- tests/shan-core.test.ts：确定输入、确定抽样、状态分支和不泄露投影的组件检查。

第一阶段不修改HeroId／HERO_IDS／形态注册、GameState、公共协议、模式门禁或现有走棋入口；模块不从index.ts导出到产品入口。独立模块不等于可玩的英雄。测试提供明确来源标签与行动事实，它们不是可供客户端上报的权威字段；实际棋盘来源归属须在第二阶段由服务端适配器生成，不能把测试布尔值直接当成生产验证。

### 模块状态与接口
模块内维护：致命等级；亲卫是否已用；存活／秘密死亡；死亡触发行动ID与正式机会标记；剩余6回合／2次特殊应将；四次将军进度；最近已结算机会和持续威胁记录。全部是权威私有概念，不能挂在公共heroRuntime上。

拟提供三个内部步骤：previewShanAction（无副作用验证与分支预览）、commitShanAction（对已合法、闭合的一次行动结算）、ownerShanView（仅本方需要的信息）。名称为技术建议，不新增玩法关键词。一个普通行动连同亲卫支付是同一事务，不拆成“先永久扣亲卫、再尝试走棋”的两次请求。

存活赌命使用注入的均匀整数0—99，按r＜10／20／35／50／65／80判断死亡；每次合法赌命只抽一次。几何或资源不合法、重复请求、预览不抽随机，不消费资源。第一阶段模块不能调用Math.random，生产绑定的随机通道和已有其他英雄的随机调用隔离在第二阶段证明。

死亡触发行动以“行动开始时存活”的事实明确标记：本次不扣死后额度、不扣6回合、不把本次反将追溯入四次；不移除公开帅位。之后每个自己的正式回合在完整结算后检查普通将死／第四次将军获胜，再判倒计时到零。特殊应将消耗两次资源，普通解将不消耗；零额度且无普通应对才失败。

### 第一阶段12组拟验证（全部NOT_RUN）
|编号|输入／反例|预期结果|
|---|---|---|
|A01|等级0起第一次将军；1至5与6／7级|初始升至1；概率表正确，6及以上80%。|
|A02|原威胁保持、W09同车同线挪动、双将与新增另一来源|保持不重复；双将一次；新增有效威胁一着最多一次。|
|A03|等级3后一次无将军敌方行动；零级再恢复|3→2；0不会降成负数，献祭不降级。|
|A04|邻接士／仕、远处士、非士、已用亲卫|只接受已批准的邻接祭品与未用额度；拒绝不扣资源。|
|A05|各档阈值前一整数与恰好阈值；非法随机值|r＜阈值死亡，其余存活；范围外随机值不提交。|
|A06|第一次秘密死亡与再次收到死亡结算|仅第一次建立6／2／0，不刷新亲卫或重复重置。|
|A07|死亡触发行动同时反将|触发当次不扣死后时间／应将，也不增加死后将军进度。|
|A08|死后连续两次特殊应将后第三次；零额度普通解将|两次分别扣1；不能特殊应将时检查普通解将，不能直接按额度0判负。|
|A09|第六回合第四次将军／普通将死；第六回合仅第三次|先结已达成胜利；无胜则超时，失败后不再开放下一手。|
|A10|相同行动／机会重复结算；预览、无效请求|一次行动只推进一次，预览与拒绝无预算／等级／随机副作用。|
|A11|同一公共局面，固定同一行动但分别注入存活／秘密死亡结果|在尚无合法公开差异的相同可见前缀内，公共投影相同；本方可见生死预算，敌方无该字段。此组仅模块投影，不冒充实际wire验证。|
|A12|不支持的来源标签、未定义控制／复活／额外行动|明确标不覆盖且不提交，不默认当安全或给予新资源；这不是产品新拒绝政策。|

组件输入不应自称完整合法棋谱；A02需要实际普通车线采样的生产证明留给第二阶段。A11不要求不同隐藏状态永远产生相同未来行动／胜负；允许玩家选择和最终终局导致合法公开差异，只防未经规则允许的提前泄露。

第一阶段拟验证命令（实施后才运行）：
- node --test --test-reporter=spec tests/shan-core.test.ts
- 该独立模块不接入旧生产入口；完成后先核diff／导入图。只有确有共享依赖改动或失败触发，才扩大相关回归范围，避免重复跑无关测试。
仓库package.json要求Node≥24；执行时核实际运行环境，不把计划命令当已运行结果。通过后发布独立草稿与本线记录，附真实用例数量／结果，不沿用前轮560项作为山的验收。

## 第二阶段：普通走棋与权威结算接入
第一阶段达到相应组件证据后，单独形成具体接入补丁。潜在文件：types.ts、rules.ts、game.ts、settlement.ts、room.ts；另需将军来源采样与secret状态适配。注册／门禁、秘密协议有牵连时，先说明精确差分，不借接入包自动扩大模式或随机池。

### 具体接入次序
1. 在未变更公开角色选择的受控服务端适配范围内完成山状态初始化和一致性校验。未来正式注册需确定内部ID、完整技能包和可用模式；尚未分配的业务编号不在本计划中伪造。不能绕过validateHeroForms初始化“假wind”来测试。
2. 行动前核actor、revision、actionId、正式机会和确实受将；将帅本身不能走。没有选择特殊应将的普通行动继续执行原SELF_CHECK规则。特殊应将只能针对已确认的其他棋子普通行动放宽本次应将要求，不能跳过走法、目标、控制、阻挡与来源防御。
3. 亲卫先在隔离候选中真实移除，再按移除后的棋盘验证并完成本次行动，几何或后续失败整份候选丢弃；不让被献祭棋继续作挡子或炮架。
4. 采样完整行动前后威胁，且在双方每次相关稳定闭合后更新，不能只看敌方两次回合末：否则会漏掉中间已经正常解将、随后同车重新将军的W01。普通车按同一实体与同一未中断线路跟踪；不能只用“之前受将／之后受将”的两个布尔值，新增另一条威胁时也要能识别。炮架、复杂多阶段及特殊来源仍另适配，不擅自将同车条款泛化。
5. 真实闭合落位／死亡后形成最终结果；在advanceToFormalTurn提前checkmate处纳入山的合法特殊应对枚举。不能仅因“尚有额度”就宣称必有可行动棋子。不得调用普通裁决动画或吃帅来替代秘密赌命死亡。
6. 普通将死敌方／四次处决和倒计时的结算接入同一已闭合来源，避免finishFormalTurn先减至0并结束，导致末回合反杀丢失。新的内部outcome先保留来源，正式wire reason映射在该具体补丁中审查，不能把倒计时写成普通checkmate。
7. 模块私有秘密应进入SecretState后再接本方视图，GameState不含death／剩余次数／死后进度。真帅存活检测与公开伪装必须分开，不能让closeDirectDeaths把赌命秘密死亡当现有公开消灭，也不能授予对感染／背刺等专属消灭的未确认免疫。

第二阶段拟验证：实际入口SELF_CHECK例外只对山当前合法选择生效；普通将帅移动限制；W01—W10对应实际走棋；真正新增威胁与原车移位；第三次强制应将无解和零额度可正常解将；死亡当次反将排除；末回合反杀优先；错误／旧revision／重复actionId整局state＋secret＋RNG不变；正式回合、子行动和额外行动不混计。均NOT_RUN。

### 必须纠正坐标
[纸面推演](POSITION_WALKTHROUGH.md)以红底线为0，引擎现有测试以红底线y＝9、黑底线y＝0。转换为x＝字母索引、y＝9－纸面行号。例如纸面红帅e0→引擎(4,9)，黑将e9→(4,0)，黑车e3→(4,6)。将帅宫区、兵卒方向、马腿和士邻接必须按转换后的同一棋盘再验，不将原纸面数值直接复制进fixture。纸面入口没有从32子开局到残局的完整历史，此限制继续保留。

## 第三阶段：本方操作、实际序列化与联机保密
后续涉及hero-actions.ts的ownerHeroSecrets、remote-room.ts的playerRoomView／publicRemoteRoom、room.ts的serializePublicRoom，以及尚未在本轮审读的bluetooth-host-room.ts、bluetooth-protocol.ts和客户端实际操作代码。后几者须先读取再列精确补丁，本计划不宣称它们已适配。

实现正常解将／赌命行动／亲卫护主三个选择；显示本方致命等级、实际概率和死后6／2／4资源。公开帅位、公共消息、automaticEvents、captured、revision推进、时间戳与终局动画不得提前标明随机死亡；亲卫真实消失本身属于公开棋盘变化，不能为了保密隐藏这枚棋子的合法支付。

实际wire测试需配对生／死隐藏分支，固定同一公开行动前缀，比较publicRemoteRoom、敌方playerRoomView、serializePublicRoom和蓝牙编码后的载荷；本方视图可不同。还需测试串号／伪造viewerSide不能读秘密、重复请求不二次赌命、断线重连保持秘密资源且不刷新六回合、非法候选不会改变公共提示或其他英雄随机流。仅查找字段名不够，须比较完整允许公开内容和来源差异。

这些检查完成前，不称“联机可玩”或“保密通过”。不会仅凭独立模块单测将山加入随机名单，也不自动替换风、变更UI批准图稿或发布游戏。

## 仍未决的玩法与实现边界
暗子／临时控制／复活士仕资格、炮架与其他复杂将军来源、额外行动／多阶段、强制位移、特殊消灭与其他英雄畸变联动仍未确认或未适配。时间回溯／洗牌如何恢复山的秘密生命与资源，也需要独立来源规则，不能直接跟随现有secret.history深拷贝恢复，从而给出无限赌命或复活收益。第一阶段不实现这些联动，不用默认猜测堵上。

公开模式准入、正式英雄注册与随机池拆分属于第二／三阶段具体接入范围决策；第一阶段独立模块不依赖它们。若未来要实现在真实普通模式运行，须形成可信服务端精确准入，不修改现有全局featuresReady或接受用户JSON解锁。

## 本轮结果与接续
已完成：当前v1.2确认来源核对、main与PR10身份比较、15文件定向源码审读、三阶段文件／行为／验证计划、第一阶段两个文件与12组NOT_RUN检查定义。实际游戏源码写入0、游戏引擎运行0、自动测试0、分支／PR创建0、新评分0。

建议下一步先实施第一阶段两个文件及相应组件验证；实施指令指向本计划时按此限定推进，完成后提交真实结果，再处理普通权威接入。当前尚未开始实现。主线原路径消灭／终点防御工程断点、其他工作线成果、冻结评分及NET暂停均保留；不代填其他对话接收采用。

## 已读源码身份
固定源码提交：7ece1fdda7837d4f14433f3f74c6f6be8eef4cc9。上述函数和类型按实际相关范围审读，文件内容未被本轮修改。
|文件|Git blob|
|---|---|
|[src/types.ts](https://github.com/aaaycc931-droid/jieqi-engine/blob/7ece1fdda7837d4f14433f3f74c6f6be8eef4cc9/src/types.ts)|a837ca049d3d0a7fd8cc38c3b0a9552f7d24105e|
|[src/rules.ts](https://github.com/aaaycc931-droid/jieqi-engine/blob/7ece1fdda7837d4f14433f3f74c6f6be8eef4cc9/src/rules.ts)|2aa4deb68cec2f9330eadd8f41097d7b1c615721|
|[src/game.ts](https://github.com/aaaycc931-droid/jieqi-engine/blob/7ece1fdda7837d4f14433f3f74c6f6be8eef4cc9/src/game.ts)|989f2a77d03a7762cd8acbcffe3a349d8ee6520e|
|[src/turns.ts](https://github.com/aaaycc931-droid/jieqi-engine/blob/7ece1fdda7837d4f14433f3f74c6f6be8eef4cc9/src/turns.ts)|325eea5b12ad36ec7b1fc8bdd50c1a56833f0612|
|[src/settlement.ts](https://github.com/aaaycc931-droid/jieqi-engine/blob/7ece1fdda7837d4f14433f3f74c6f6be8eef4cc9/src/settlement.ts)|bf479ce7e5ecaef93fd4e9a51f1110a79e6a2373|
|[src/hero-actions.ts](https://github.com/aaaycc931-droid/jieqi-engine/blob/7ece1fdda7837d4f14433f3f74c6f6be8eef4cc9/src/hero-actions.ts)|0f862528ae09f3b6ea72cf693b17f159e0a13c52|
|[src/heroes.ts](https://github.com/aaaycc931-droid/jieqi-engine/blob/7ece1fdda7837d4f14433f3f74c6f6be8eef4cc9/src/heroes.ts)|0958d1e16103de4b808a96d4fb825bf446a45e59|
|[src/remote-room.ts](https://github.com/aaaycc931-droid/jieqi-engine/blob/7ece1fdda7837d4f14433f3f74c6f6be8eef4cc9/src/remote-room.ts)|97b60f7c1ab9a79bf85388a9fc824690f7115451|
|[src/modes.ts](https://github.com/aaaycc931-droid/jieqi-engine/blob/7ece1fdda7837d4f14433f3f74c6f6be8eef4cc9/src/modes.ts)|cb05c2fcfb0c617b6310e08ef8593e1d12ad95cc|
|[tests/hourglass-safety-boundaries.test.ts](https://github.com/aaaycc931-droid/jieqi-engine/blob/7ece1fdda7837d4f14433f3f74c6f6be8eef4cc9/tests/hourglass-safety-boundaries.test.ts)|86a56489b8679a7dd66e4b69b337881f0d71f0e1|
|[tests/bluetooth-private-contracts.test.ts](https://github.com/aaaycc931-droid/jieqi-engine/blob/7ece1fdda7837d4f14433f3f74c6f6be8eef4cc9/tests/bluetooth-private-contracts.test.ts)|22552654313c59a1833d39b97c6b884fb8981e2c|
|[package.json](https://github.com/aaaycc931-droid/jieqi-engine/blob/7ece1fdda7837d4f14433f3f74c6f6be8eef4cc9/package.json)|34b26233ab157051caeae779771ddc0fceb24465|
|[src/hero-forms.ts](https://github.com/aaaycc931-droid/jieqi-engine/blob/7ece1fdda7837d4f14433f3f74c6f6be8eef4cc9/src/hero-forms.ts)|e42cb0854bd71dfaf4004268ec79e11c115c692d|
|[src/room.ts](https://github.com/aaaycc931-droid/jieqi-engine/blob/7ece1fdda7837d4f14433f3f74c6f6be8eef4cc9/src/room.ts)|093a1732eed4ee48a6d3487ce938d3c1d17a58c2|
|[src/research-source-context.ts](https://github.com/aaaycc931-droid/jieqi-engine/blob/7ece1fdda7837d4f14433f3f74c6f6be8eef4cc9/src/research-source-context.ts)|01aa06251a9d76dca075a8899a3530ab0f47d0f2|
