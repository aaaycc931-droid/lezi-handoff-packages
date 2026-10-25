# H03限定组件执行方案：具体输入就绪，运行UNRUN

2026-10-25。交接基底a0c6179，实际引擎基底PR13 `3f98bc9fb89a2a209209c424c4bf1bbd2cf6aca7`。本阶段用户“开始吧”接续的是源码绑定和公平配对准备；已完成这些准备，不记作引擎实施/运行授权。此前各项投弹/铁马/沙漏授权不能自动扩大成H03评分运行或新模式准入。已有同范围明确授权若在后续来源找到，按真实来源继承，无须重复索取。

## 最小技术范围

拟新增引擎研究脚本 `scripts/scoring/h03-component-pilot.ts` 与针对性 `tests/h03-component-pilot.test.ts`；此刻两个文件均未创建。输入引用交接仓库本阶段的H03_OPENING_WITNESS、H03_PAIRED_CASES、H03_GUARD_PROBES及固定提交身份；不复制/修改旧评分方法，不把数据放进产品注册表。依赖只读：setup、game、hero-forms、rules、settlement、mechanism-observer及MechanismEvidence。若必须修改业务源码或准入才能通过，先保存失败证据、将缺口回交共享安全任务，另形成具体补丁范围；不在回放器中掩盖错误。

预定入口为直接权威组件API，**不复用现有受限PolicySession/FixtureRunner constructor、不创建伪房间、不改MODE_RESEARCH_SOURCES/featuresReady**。两臂各用新的 `createInitialGame(tape, "jieqi")`，校验完整开局和30身份精确一致；分别 `initializeFeatureGameState(state, {red:"warrior"})` / `initializeFeatureGameState(state, undefined)`，无mutation。然后调用正常 `applyAuthoritativeMove(state, secret, command, false, fixedNow)`。fixedNow随动作递增且两臂配对相同；不得设置deferTurnEnd或allowIntermediateCheck、改turn/状态/资源、直接调用finishFormalTurn来跳手。组件无房间计时，turnDeadlineAt等记not_applicable，不据此验收超时/wire。

最小拟执行命令（**计划命令，脚本尚未实现，本阶段未执行**）：

```bash
node --experimental-strip-types --test tests/h03-component-pilot.test.ts
node --experimental-strip-types scripts/scoring/h03-component-pilot.ts --input-dir /path/to/pinned/handoff/worklines/main/scoring --output-dir /path/to/new/h03-evidence
```

后续执行前核实际Node版本、package命令、全部输入/脚本身份和最新HEAD。新输出目录不得覆盖既有证据。不运行既有acceptance批次以冒充本试点，也不启动原半混乱12/64。

## 执行次序与通过条件

1. **来源及初始化。** 哈希必须等于输入绑定；29次抽样逐一核bound/value，缺/多/不匹配即失败。每臂独立对象；开始和结束的原输入不变；初始公开棋盘及权威身份两臂一致；英雄锁按各自新局固定。配对间没有状态或观察器复用。
2. **先做负例与安全差异复验。** S01合成组件只诊断“先获防御的棋后来将军；对手试图吃它但被弹回”后的己王安全。其手工防御字段明确是单独合成恢复夹具，不能进入来源合法的配对样本。若实际允许弹回后继续非法受将，则标source_safety_gap；保存原始输入/结果/合法查询/最终棋盘，停止依赖完整合法行动集与全局结果的校准，不通过回放器补改规则。S02/S03须证明未授权模式/能力继续拒绝；新增回放器不能扩大门禁。
3. **四类候选前缀。** 每次请求前核side、revision、公开from/pieceId与预定策略分支，再捕获正常权威提交。拒绝、重复或提前终局均原样记录，不当作成功前缀，不再盲送后续请求；配对一臂失效则整对不能计算有效配对效应。任何未计划随机调用中止该样本并保存原因，不借Math.random静默补抽。
4. **实际机制检查。** P01取得时3层、名额含covered-23、弹回时目标存活/源留起点/防御耗尽、Ⅰ级普通进攻及主行动/正式回合各一次；P02敌方回合末2/1/0并于下一攻击时已无防御；P03未增加名额或刷新层数；P04先核公开分支实际可用，再核两臂都吃黑车、只有H03臂保留红车。实际兵分重算使用原参考值，结果与手写预测冲突时报告冲突，禁止改期望凑分。
5. **被动观察与重放。** 每臂一个独立MechanismEvidence，输入不变，观察开/关执行结果及RNG调用严格相同；从开局重放相同请求/抽样，忽略的字段只限明确的研究run-ID等，状态/秘密/资源/时序不得忽略。事件有效性sticky传播；未捕获到某事件不推断它不存在。
6. **归档。** 保存源提交与blob、输入hash、初始化抽样原样、请求原样、接受/拒绝/重复、前后权威快照、公开策略输入、实际回执、分类、原子/回合证据、资源/名额/防御计数、捕获有效性、合法性覆盖和删失。私有权威资料仅供harness审计，决策只读公开输入；先核发布数据范围，不把秘密投给玩家或策略。所有归档验收通过才叫组件前缀PASS。

## 观察接口的已知限制

现有formal_main_action在行动前发出；formal_turn_end在持续效果扣减之前发出；下一formal_turn_begin已进入下一回合。**三者不能冒充“全部主行动/返回/死亡闭合后、下个begin前”的新观察点。**

本组件阶段使用函数返回的完整权威状态和明确标记的现有源事件，只验证可直接读到的上述局部结果；不新增hook、不伪造after-main检查点。要推广到会在下一begin改变状态、死亡/空间交叉、通用最优对手或自然全局效果时，先落实主线R38所需精确安全/观察边界。本试点也不替半混乱原始checkpoint写通过。

## 输出分级与停止

组件合法前缀通过，只支持“在这一个条件开局和这条公开策略下机制如此、短期代理量如此”。本计划在每臂6/12/9/9次请求后截止；未终局写censored，真实终局需权威来源和完整闭合证据，不能用固定步数代和棋。不能把四个同源分支当独立样本计算置信区间。

下一层真实校准还缺：不同源局面族及预先声明分布、独立留出、策略水平/预算、双先后手、全部终局或适用且已校准的预测器、可靠不确定性。当前population/outcome_delta/global_score全部不发布。新风等待设计路线完整规则回传，三模式回传与山2B、共享工程断点、旧账本和NET状态继续保持。
