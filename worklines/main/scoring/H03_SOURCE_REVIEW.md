# H03首个校准试点：源码绑定与配对输入已准备

2026-10-25，`SCORE-H03-PREP-01`。本阶段完成源码核对、可复现输入和具体执行规格；**引擎导入/运行0，合法前缀尚未通过权威入口复验**。这是评分候选准备，正式方法与账本继续冻结。

读基底为交接仓库 `a0c617910821583f4dc52df4f357b715c5aca48e`；保留评分提交6991之后三线收尾。引擎固定在草稿PR13 `3f98bc9fb89a2a209209c424c4bf1bbd2cf6aca7`，不采用旧main覆盖开发链。19个直接相关文件与该提交blob一致，准确身份及阅读作用域见 `H03_SOURCE_BINDING.json`。身份一致不等于全文语义审查。

## 原规则与实际接口

规则采用 `worklines/standard/rules/shared/02_CURRENT_HEROES.md` 完整H03节：最多3枚不同己方明置非将帅；首次成功移/攻离己方九宫取得防御，同棋一次、名额不返还；直接普通进攻消耗防御，目标存活留原位、进攻者返回并正常落位；覆盖3个敌方正式回合。将帅铁甲是另一分支。

| 语义 | 固定源码入口 | 本次核对结果 |
|---|---|---|
| 初始开局及身份来源 | setup.ts:createInitialGame/createIdentityPool/shuffleIdentities；slots.ts:COVERED_SLOTS | 真实30身份全局Fisher–Yates；32枚公开开局，不事后替换暗子身份 |
| 独立反事实初始化 | game.ts:initializeFeatureGameState；hero-forms.ts:createHeroSelections/initializeHeroForms | 新局revision0分别配置红方warrior/无英雄；前者包含完整原H03，铁甲在本前缀无事件触发；禁止中途删技能或改锁 |
| 取得防御 | game.ts:awardWarriorBarrier | 明置、非将帅、当前控制、宫内至宫外；barrierPieceIds保存已占名额，最多3；设置3层 |
| 普通弹回 | game.ts:applyAuthoritativeMove防护终点分支 | 先清防御、记录bouncedAgainstPieceId与landed=false；源棋保留原位置、建立warrior_return落位，闭合后走正常回合结束 |
| 正式回合和到期 | game.ts:finishAfterPlayerAction；settlement.ts:finishFormalTurn/advanceToFormalTurn；turns.ts | 敌方正式回合结束递减，额外应将不另计；获得方本回合不递减；动作原子闭合与回合结束分别存在 |
| 落位与死亡 | settlement.ts:settleLandings/closeDirectDeaths；settlement-context.ts | 普通落位及直接死亡闭合；本试点无陷阱/幽魂/飞行/畸变，不能据此验收空间冲突或复杂死亡 |
| 观察有效性 | mechanism-observer.ts；scripts/scoring/mechanism-evidence.ts | sticky失效必须传到样本分类；失效结果不能当0效应或有效终局 |

主线ADJUDICATION的H03键只检出 `shared_hero_design_updates/half_chaos_local/H03` 所述“同原子落位死亡前占名额”。这是半混乱局部确认；本次不推广其作用域，也不覆盖它。现有EX-WARRIOR-01包含强行轮转、恢复棋子和清状态，是合成组件回归参考，不能拿它证明本试点自然前缀或校准通过。

## 两项会改变执行选择的发现

**准入边界。** `modes.ts` 中xiangqi/half_chaos仍featuresReady=false；research-source-context.ts普通研究只允许hunter/rogue/shuffler，半混乱只允许shuffler；H03不在现有能力表。PolicySession与FixtureRunner还绑定各自特定英雄/畸变来源，不能只改JSON英雄就复用。禁止通过去掉gameMode、伪装英雄、扩大白名单或关闭英雄后补字段启动H03普通模式。

因此，原合同所提“全明地面”不是立即可运行的普通模式方案。本阶段具体输入改为**已开放jieqi的真实开局来源＋普通移/攻权威组件接口**：少数相关棋子在正常移动中揭示，其他棋子仍暗置；无对手英雄、无畸变。它研究一个固定条件分支，不代表普通模式准入、房间完整开局或总体英雄强度。纯组件初始化允许Partial英雄选择，并不证明房间英雄选取流程允许同样组合。若后续要求房间/全明模式，仍需独立来源和现有门禁范围核对。

**王安全试算差异。** `rules.ts:simulatePublicMove`仅对龙鳞直接返回原状态；对H03防御仍删除目标、将源棋移到终点。实际 `game.ts` 则弹回并让目标存活。`validatePublicMove/getLegalMoves/isCheckmate`依赖此前者，`closeDirectDeaths`在双方将帅存活时返回false；不能从这些接口的普通成功推断“弹回后己王已安全”。这与原主线闭合安全任务相邻，尚未运行复现、未修改源码，不登记为已复现缺陷。`H03_GUARD_PROBES.json`给出具体组件反例和准入负例；在权威复验前，不能使用候选合法行动集作为完整最优对手策略，更不能进入强度校准。发现只阻断依赖它的证据，不抹掉其他输入准备。

## 已准备的公平对照

`H03_OPENING_WITNESS.json`提供完整32枚开局、30个权威身份和29次合法抽样输入。其身份库存与原池相同，仅各方将一枚车身份与炮位身份交换，能由原Fisher–Yates实现；这是一份刻意条件化输入，不是实际随机样本或开局频率。

共同前缀为：红中兵(4,6)→(4,5)；黑左炮位暗子(1,2)→(3,2)揭为黑车；红左炮位暗子(1,7)→(4,7)揭为红车；黑车(3,2)→(3,6)；红车(4,7)→(4,6)首次离宫。坐标遵循引擎x=0…8、y=0…9。此处只是按来源整理的候选请求，未通过引擎证明全部合法。

两臂从两次独立新局初始化进入，使用同一开局输入和同一公开策略。除了红方H03选择，棋盘、身份、行动机会和前缀相同；不清生产状态字段。动作ID在两臂独立且可关联，expectedRevision逐条固定。P04因公开结果不同改用不同合法行动，使用同一条“己车仍在则车吃进攻者，否则马吃进攻者”的公开决策规则；不强迫无车反事实执行不存在的车行动。

| 输入 | 覆盖 | 条件预测，非实测 |
|---|---|---|
| P01立即进攻 | 取得、消耗、弹回、普通主行动仍占步 | 短期兵分差+9；不等于胜率或英雄分 |
| P02等待到期 | 黑方第3/4/5手后层数2/1/0，之后进攻 | 两臂均失车，短期差0；不等于整局价值0 |
| P03转攻其他棋并回宫再离宫 | 共同比较损失、同棋不重获/不刷新 | 共同行动损失相消；原防御只余1层 |
| P04按公开状态换子 | 回应者变化、相同行动预算、避免重复计分 | 两臂都吃掉黑车，区别只是红车是否保留；差+9，不能把共同吃车再加9 |

四类输入**同属一个开局族**；不能当4个独立样本或留出集。72条是两臂合计的计划请求数，不是72次引擎执行。未结束统一记录删失，不伪记和棋；所有观察、效应和新英雄分字段保持null。饱和3个名额、死亡复活、铁甲、返回冲突和终局推断仍不覆盖。

## 实际验证与下一断点

`python validate_h03_pilot.py --engine-root /path/to/jieqi-engine` 已执行：19个源码blob身份一致；32枚开局/29次洗牌输入库存与实现顺序可重建；四类配对、72条预定请求的ID/版本/轮序/坐标字段及公平性结构检查通过；9项恶意损坏输入被拒绝。准确结果和代码/输入SHA-256在 `H03_STATIC_VALIDATION.json`。

该脚本不实现棋规、不导入引擎、不证明逐手合法性。下一步是按 `H03_EXECUTION_PLAN.md` 实现并运行独立、限定的组件回放器和安全负例。先把可执行证据门槛补齐，再讨论真实终局校准；不是批准英雄新机制或正式评分采用。
