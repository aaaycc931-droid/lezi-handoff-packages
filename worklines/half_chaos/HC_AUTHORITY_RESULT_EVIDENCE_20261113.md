# 半混乱 r58：权威结果边界离线实证

任务 `MAIN-HC-AUTHORITY-RESULT-EVIDENCE-20261113` 的 H1/H2/H3 已完成本包交付。交接读源 `d5d05f92df1be0b3fef43b22245c0a0c5cc25fbf`；限定继承主线本包明确委派的离线研究权限，不接任主线。协作检查 L3，工作稿 v0.18／正式基线1.8.0。

引擎固定 PR22 `71145df45ad17215a3731e53150b6728e079e375`，启动时仍 open draft。实际研究提交：[9f0b14c](https://github.com/aaaycc931-droid/jieqi-engine/commit/9f0b14ccb02308fd3579e3cf58cde063aca11cf6)，分支 `codex/hc-result-evidence-20261113`；5个新文件发布后逐内容读回一致。生产 src/web/android/package 零差分，受保护 Git 对象及11个读取源 SHA-256 见范围清单。

- [测试驱动](https://github.com/aaaycc931-droid/jieqi-engine/blob/9f0b14ccb02308fd3579e3cf58cde063aca11cf6/scripts/research/hc-result-evidence.ts)
- [实际结果](https://github.com/aaaycc931-droid/jieqi-engine/blob/9f0b14ccb02308fd3579e3cf58cde063aca11cf6/review/hc-result-evidence/RESULTS_20261113.json)
- [运行纠错记录](https://github.com/aaaycc931-droid/jieqi-engine/blob/9f0b14ccb02308fd3579e3cf58cde063aca11cf6/review/hc-result-evidence/RUN_LOG_20261113.md)
- [范围及哈希](https://github.com/aaaycc931-droid/jieqi-engine/blob/9f0b14ccb02308fd3579e3cf58cde063aca11cf6/review/hc-result-evidence/SCOPE_20261113.json)
- [引擎说明](https://github.com/aaaycc931-droid/jieqi-engine/blob/9f0b14ccb02308fd3579e3cf58cde063aca11cf6/docs/research/HC_RESULT_EVIDENCE.md)

## 1. 实际执行与覆盖

环境 Node v24.22.1、Python 3.12.14；JDK21已核可用但本包未执行Java。命令：引擎根目录 `node scripts/research/hc-result-evidence.ts`。最终 **13例通过、0失败**：H1七例、H2五例及H3再战对照一例。执行真实TypeScript房间函数；Web部分复用既有receipt-channel提取的生产函数，DOM与原生发送端是记录替身。不是纯概念模型，也不是真机／独立QA。

来源：BTHOST-03/04/06/07、remote-room MODE-05与退出重复控制、hero-forms R4-FORM-18认输调用。均从真实create/join、选英雄、猜拳、入场、准备、认输／退出等合法前缀建立状态；未注入秘密棋局、绕开准入或修改生产代码。新探针不冒充原110请求刺激。

| 编号／层次 | 实际观测 | 结论边界 |
|---|---|---|
| H1 direct hero，期限前1ms／到期／后1ms | 前者提交hunter、RNG0；后二者正常返回，随机两次得到warrior并进RPS，原hunter命令没有执行 | 底层正常返回不代表接受；当前API没给原请求处置字段 |
| H1 host hero，同样三时点 | 到／过期时先提交随机选择，再对原命令抛INVALID_PHASE；固定零随机恰好也抽到hunter | 与直接函数不同。最终选择即使等于请求，也不能倒推原选择接受；拒绝也不保证房间完全不变 |
| H1 host preparation首次／已完成 | 首次锁定2层；第二次返回三份完全相同投影，revision仍0、消息及公开事件不变、无额外RNG | 无ID准备操作具有已完成无变化分支；不能自行把它归为可关联旧请求的duplicate |
| H2认输后同ID | 合法playing→认输提交finished/revision1/原ID系统消息；同载荷同ID重发INVALID_PHASE，原提交保持 | 新拒绝不否定旧接受。仅认输路线，未验证吃子终局 |
| H2退出反向对照 | finished同ID可返回duplicate=true；raw函数换actor同ID仍duplicate=true、原败方不变；host丢弃duplicate字段 | 终局重试行为因动作而异；ID命中不等于actor绑定，也不是本次新玩法批准 |
| H2 Web无注入正控 | 真实receive→host.handle→snapshot，已提交认输保持 | 对照同一实际调用链 |
| H2 Web投影故障注入 | 认输赋值后第一次views人为抛错；Web发同传输ID error“房主拒绝了此操作。”，随后发finished快照；权威仍revision1 | 证实该catch边界会混淆提交后异常；只证明注入条件，不宣称生产投影自然抛错或真机故障 |
| H2 Web序列化故障注入 | 第二次views返回的guest投影被测试加抛错toJSON；真实编码失败、提示同步失败、原生记录端收到0帧；权威仍finished | 投影对象注入不改权威；序列化失败与原命令处置分开 |
| H3再战对照 | roomId相同、进入新hero_selection、旧forfeitOutcome消失 | roomId不能独自代表局次；未实现matchEpoch |

运行中保留两类驱动错误：首轮manifest误列不存在的check.ts，在任何用例前失败；随后11通过/2失败来自测试误以为随机选项必与提交项不同。查明固定零RNG也抽中hunter后修断言，保留“相同快照也可能来自已拒命令”的更强反例。另将不存在的formalEvents输出计数改为真实公开automaticEvents/landingEvents/destructionBatches；无棋局为null。仅修测试和报告，未修改生产源让测试通过。

## 2. H3：具体合同增量及最小产生点

以下是依据实测的候选要求，**A/B均未选定、账本／查询未实现**。原候选§1—9保留历史，新增§10链接本增量。

| 需修订处 | 已证产生点／不足 | 主线最小实施需求 |
|---|---|---|
| 原选择处置 | submitRemoteHeroSelection期限分支返回替代随机房间；host预推进又可先改变phase | 分离预推进和原命令处置；记录动作专属分支，不能用return、room changed或最终选项分类；未覆盖分支保留unknown |
| 无ID准备 | completeRemoteHeroPreparation ready分支返回原room；host只返回views | 发前保存传输ID/内容；首次结果记录须在原处理时形成，不能从事后ready重建原尝试 |
| 终局与去重 | surrender的playing门禁早于内部去重；forfeit有finished同ID早返且未绑定actor | 按kind分别定义证据；查询绕开执行门禁；不得用原ID表为不同actor/载荷签发结果；本线不顺带改变既有游戏去重政策 |
| 提交与同步 | host.handle已给this.room赋值，再进入views；当前Web catch可把后续异常发为error | accepted/明确rejected的记录要与权威提交一致并早于views；同步错误单列，不能覆盖已提交事实。若原子性不能证明则unknown |
| 局次 | beginRematch保留roomId但重建准备／结果 | 权威实例、局次和actor绑定独立于roomId／红黑；旧局记录不串新局 |

只在外层Web catch或handle返回后追加账本均不够。当前实验证明产生点的必要区分，尚未证明所有动作的原子实现，也不从系统消息或ID表推导完整安全凭据。需要主线选择有限覆盖动作、结果语义和提交/记账一致性；缓存、容量、跨重启仍未决。

## 3. 与混乱来源的交叉核对

本轮全文读取 CH_CONNECTION_LIFECYCLE_SOURCE_REVIEW_20261113.md（固定交接d5d05f9）。采用来源约束，不把其中W1—W3规格当已运行，不等待其C1—C3才完成本包。下列是**该报告的来源结论**，本包不新跑原生队列：

| 项目 | A/B共同边界 | 方案特有／仍unknown |
|---|---|---|
| 完整JSON无换行＋EOF | 旧尾段过滤器不等于生产readLine；不能从缺换行推出未执行 | 两方案相同；本包不宣称C1生产接收通过 |
| 连接代际 | 单io不保证全线程串行；旧事件无可信代次，不能任意重排造自然竞态 | A复用旧桥不能自动取得代际；B增加版本支持也不自动取得代际。自然队列未证仍unknown |
| actor／无动作ID | 固定guest字符串、颜色、无ID准备快照都不构成原请求身份 | 两者必须保留原传输尝试并绑定真实actor及内容；缺记录unknown |
| 再战／权威重建 | 当前roomId重用已获本包运行对照；进程重启恢复未测 | 两者都需局次／实例，不能借本包声称跨重启可靠 |
| 旧端兼容 | A/B原源码兼容结论仍以r57范围为准 | A需hello分流且不触发handle/views；B需双端原生v3能力，sendChecked不算能力证明；本包未实现或互通验证 |


### 3.1 发布前到达的新实证已接收（H3补充）

在本线引擎9f0b14c发布后，交接main更新至 `d47d1697f3f9dcb3d480ae2fbc7e61587c2c6a8b`。已实际全文读取混乱 [C1/C2/C3回传](../chaos/CH_OFFLINE_LIFECYCLE_VALIDATION_20261113.md) 与旧来源报告§9；固定引擎 `09af8bf1dae274e180d123370b86d444aafad4c9` 的方法全文、WEB_RESULTS全部8例、JVM_RESULTS用例输入/事件/关键轨迹及SOURCE_AUDIT也已读取。未重跑它的15例或重新审计全部驱动，不称本线独立验证。

实际校验8/8 Web行与JVM输入哈希、消息数、权威选择和清等待状态对应；JVM结果文件哈希及3份生产Java/Web源哈希匹配。混乱报告7 JVM/8 Web通过，本线按其明示替身范围有限接收：完整无换行EOF已由生产接收方法送入真实房间；同字节IOException和partial没有该选择。不同权威结果都被断连回调清成pending=false、unknown=false、requestId=null。因此A/B都必须把未决请求保存在这些瞬时UI字段之外，不能在清等待时删除身份，也不能依赖换行失败将旧请求判作未执行。

C2证明的只是“close释放输入但不释放阻塞输出”流模型下旧send可晚于新attach且新流保留，不升级为RFCOMM/JNI自然竞态。C3为两种保持端内顺序的跨端记录回放，仍不证明真实陈旧回调越过新CONNECTED。这里把EOF判断从旧静态可能性推进到限定运行来源接收；连接代际／自然调度／全部动作与真实设备继续未知。此增量已纳入候选§10和本线回执，不要求混乱或主线先确认本线读取。

## 4. HC56与三个原请求的对应

HC56-P0本轮增加“不能从哪些表面推断结果”的可复现证据，仍缺正式结果凭据和真实跨断连关联。HC56-P1的同ID处理需按动作区分；本包forfeit/认输/准备对照不核销PD-S35／DS-S12自然刺激，不重跑原110/56。

| 原公开ID | 本轮增量要求 | 保持未验 |
|---|---|---|
| MA-PD01:R1:main | 原accepted必须在对应主行动提交点保留；后来finished拒绝或投影错误不改变原结果 | 本包未跑该移动；不拿认输代替原主行动或两个checkpoint |
| MA-DS01-02:B2:pre-1 | 原成功技能须独立绑定actor/内容/技能提交点；不能套一般return或主行动结束凭据 | 未跑原技能／真实wire |
| MA-DS04:B3:pre-1 | 原IN_CHECK必须来自该原尝试的规则拒绝边界；事后Web error不一律是原拒绝 | 未验证原错误到客户端；不改原4拒绝来源 |

以上三个ID复用r57已核公开索引，不生成新传输ID或伪造查询记录。P2半混乱客户端送达仍未验；P3独立QA仍未做；56完整及64正式验收仍0。

## 5. 交接、风险与停止条件

已确认主线READ_RECEIPTS.result_reconciliation_intake_20261113实际读过r57并将其作为设计输入；A/B没有正式采用。本r58主线实际读取／采用仍UNKNOWN，接收者自行填写。

风险：把合成离线证据误写为生产端到端保证（medium）。已知是固定源真实函数和指定故障边界；AI推断是最小产生点需求；未知包括所有动作、自然投影异常、设备/回调调度、账本原子性及重启。竞争解释通过uninjected正控、direct/host分层、forfeit反控排除局部混淆，不证明覆盖完整。可证伪条件为源变更、自然调用产生不同分支、身份不匹配或注入污染权威；必须回受影响源复验。验证为限定条件运行证据＋来源审查，同一执行者设计测试，非独立QA。检查完成只指本包。

本包有意义阶段已完成，停止扩样本。下一具体新输入：主线A/B和结果记录的实施范围／实际补丁，或混乱新的生产接收／自然队列证据。届时只对受影响合同定向复核；不循环18例、不定时轮询、不承诺后台运行。本轮没有新增规则确认、生产实现、原半混乱自然回放、合并／部署／APK。评分冻结、NET暂停、featuresReady=false保持。
