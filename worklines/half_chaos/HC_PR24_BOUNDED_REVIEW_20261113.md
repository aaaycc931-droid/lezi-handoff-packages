# 半混乱 r59：PR24有界反例审查

任务 `MAIN-HC-PR24-ADVERSARIAL-REVIEW-20261113` 已完成。交接读源 `e7a581d1208479e5ab48d67dd96a77bc969cc0a5`；PR24固定 `f30f1f5541fd84ebbf6aa298a4bcc3e446adeb80`，实核仍open draft。主线r58接收已按自身回执核实：13例作为支线自测报告和设计约束采用，主线未重跑。A为主线后续技术草稿方向，B暂缓；不等于线上A已批准／实现。

本线全文读新原型、21项测试源码及原型方法说明，复用未变PR22的既有源阅读与r58证据。没有重跑原13／29／935或原110／56矩阵。仅针对一个新发现补4个最小对照，未改主线原型或生产文件。

## F1：必填scope字段缺失未被运行时校验拒绝

固定原型 `scripts/research/main-authority-result-prototype.ts` 第78—83行用 `Object.values(scope)` 检验非空字符串，却没有检查authorityId、roomId、matchEpoch是否齐全。省略authorityId或matchEpoch时，已存在字段仍能全部通过；随后query第101—102行以undefined对undefined相等，能够返回该记录的accepted。

| 最小控制 | 实际结果 |
|---|---|
| 三字段完整 | 合法选英雄并查询accepted |
| 缺authorityId | 构造通过，合法选英雄后查询accepted |
| 缺matchEpoch | 构造通过，合法选英雄后查询accepted |
| authorityId显式空字符串 | 构造抛Exact jieqi scope required |

**4项观察断言通过，复现1个校验问题的2个变体；不写成产品4项验收通过。** 前提是故意给可信离线调用方传入不符合TypeScript ResultScope形状的普通运行时对象。完整正确类型输入未因此证明有误绑定；PR24不接线，也不存在本轮已证的远程攻击／跨actor越权。风险为研究原型运行时防护缺口，进入更宽接入边界前应修复，不能夸大为已上线安全故障。

最小建议：主线显式检查三个必填自有字段均为非空字符串，再校验roomId；query也先校验scope结构，缺字段不能因双方undefined而授予结果。后续可按实际接入合同补遗漏／undefined／null／空串／错误类型否定控制。只建议主线修原型，不由本线改它的实现或确定生产错误码。

## 其他重点：源码结论与边界

| 检查项 | 实际结论 | 仍未证明 |
|---|---|---|
| 到期及同结果不同来源 | 预推进先于fresh与submit；英雄到期进入RPS，不能仅因随机选到同英雄记accepted | 全部动作及自然设备时钟 |
| 动作种类／duplicate | 只准hero/resign；认输底层ID命中保持unknown，forfeit、准备、移动等明确未覆盖 | 全动作duplicate凭据／生产重传策略；淘汰后仍依赖harness新ID前提 |
| actor与内容 | 记录按actor＋transportId分桶，查询检查已绑定caller，完整JSON规范化后脱离原对象执行 | actor是可信离线输入，未做跨重连认证；F1单列 |
| 提交与投影 | room＋record在同步#state赋值后再推进输出／投影，后续异常不能改写原结果 | 进程崩溃／持久事务；预推进时钟单独发布 |
| 查询 | query不调engine/clock/RNG/projection，返回答案副本 | 线上查询分流／协商／native代次 |
| 与host一致性 | 既有测试仅比较相同固定时钟下两条成功输出 | 原型两次advance共用一个now，真实host的views可能读到更晚时间，不宣称所有时序等价 |

以上未新增运行计数，不把静态审查升级为独立QA。F1以外未在本次范围发现新的相反证据，不代表原型完整无缺陷。

## 证据、保存和接续

实际研究提交：[2204ef6](https://github.com/aaaycc931-droid/jieqi-engine/commit/2204ef656c4d72684c0fce8f52789108796ed1f0)，仍在本线 `codex/hc-result-evidence-20261113`。新增3文件已逐内容读回一致：

- [最小驱动](https://github.com/aaaycc931-droid/jieqi-engine/blob/2204ef656c4d72684c0fce8f52789108796ed1f0/scripts/research/hc-result-pr24-scope-review.ts)
- [实际结果及依赖源哈希](https://github.com/aaaycc931-droid/jieqi-engine/blob/2204ef656c4d72684c0fce8f52789108796ed1f0/review/hc-result-evidence/PR24_SCOPE_RESULTS_20261113.json)
- [详细审查及复现命令](https://github.com/aaaycc931-droid/jieqi-engine/blob/2204ef656c4d72684c0fce8f52789108796ed1f0/review/hc-result-evidence/PR24_REVIEW_20261113.md)

Node v24.22.1；命令 `HC_PR24_ROOT=/absolute/path/to/pr24-checkout node scripts/research/hc-result-pr24-scope-review.ts`。依赖另行固定检出f30f1f5并验证HEAD、干净tracked文件及原型字节；未复制或合并主线实现。真实生产create/join/hero建立状态，没有私密包或游戏状态注入。4例一次运行完成，无失败修补或全量重跑。

检查L3，协作v0.18／基线1.8.0沿用。关键源码事实与malformed-input实验可追溯；修复建议为AI建议，非新玩法或正式协议。局限为受信调用前提、有限范围、同执行者设计；若主线明确只支持完整静态类型调用，也需显式保留该前提，不能把当前运行时guard当完整边界。源变更或真实调用合同改变时定向复验，不无限扩样本。

下一需要主线对F1的修复或明确适用边界及实际新差分；本任务审查到此结束。r59主线读取／采用UNKNOWN，由主线自己填写。线上A、跨重连、真机、原56／64正式验收仍未完成；评分冻结、NET暂停、featuresReady=false保持。未写任何他线文件，未改生产代码／协议，未合并／部署／APK。
