# 乐子象棋普通模式｜2026-10-24 对话收束
ID：STD-SESSION-CLOSEOUT-20261024-H21-RNG-REPLAY-CONTRACT；用户原话：「先收束本轮对话，我可能会更换对话」。
仅关闭本普通模式对话，不停主线/其他两线、不视为项目完工、未批准或启动下一任务。
## 并发保护与已完成
在前次普通线提交 `2061024a14f42423c34ad56056dce4a9beb111ab` 后，收束前远端 HEAD `948085463bf19e88eddd7de76c7e27f4a48f01bb` 新增 5 次并发提交，比较确认未修改 `worklines/standard/`；本次普通线增量提交保护这些并发成果。
- `STD-RNG-01` 已交付 `reviews/H21_RNG_SOURCE_TRACE.md`：H21无敌抽样代码 `min(4,N)`、无放回是实现证据，不等于「最多4枚」规则获得新批准。
- `STD-H21-RNG-REPLAY-CONTRACT-20261024` 已交付 `specs/H21_RNG_REPLAY_CONTRACT_20261024.json` 和 `reviews/H21_RNG_REPLAY_CONTRACT_REVIEW_20261024.md`。含 N=0/1/3/4/15 和 NP 条件性AS/ES `[1,1,1,4]`、AP `[10,2,2,5]` 有效抽样索引。
- 随机注入缺少整数/区间验证可能错误抽取或停滞；以及自然对局权威随机来源/记录/复播证据接口，留共享主线审查，不写业务代码、不越模式门禁。主线实际接收/采用尚未核实。
## 未完成边界
普通模式 `xiangqi.featuresReady=false`；正式NP/AP/AS/ES/RE和其他所有规格均 **UNRUN**；本轮未跑引擎，未做独立QA或自然对局回放。普通确认31、直接共享13、Δ规则0，原合同与历史决定不改。普通线评分冻结、NET暂停，主线本轮并发工作不被本收束覆盖。
## 唯一下一断点（未开始）
`NEXT-STD-NP-H21-RNG-STATIC-INTEGRATION-PREFLIGHT`：只读核普通32棋 R1—B5 IDs、H21 beginFormalTurn、H02/M04 AS/AP/ES 原子、王安全/来源差异与正式测试前置接口。不得改规则、运行引擎、开启未准入模式或把文档当测试PASS；下次明确继续再推进。
## 更换对话启动
继续《乐子象棋》普通象棋工作线。先核对最新远端HEAD与并发成果；读取固定入口 https://github.com/aaaycc931-droid/lezi-handoff-packages/blob/main/START_STANDARD.txt ，以 worklines/standard/CURRENT_STATE.json#latest_session_closeout 和 NEXT_ACTIONS.json#first 为准。已完成H21授鳞随机来源追溯及N=0/1/3/4/15、AS/AP/ES条件性索引的复验合同。下一任务 NEXT-STD-NP-H21-RNG-STATIC-INTEGRATION-PREFLIGHT（只读静态接口预检）尚未启动。正式NP/AS/AP/ES/RE与真实引擎测试/自然回放仍UNRUN；普通模式门禁不绕过。确认普通31/直接共享13/规则Δ0，评分冻结、NET暂停；保护新旧成果、增量写回并复读，不代填主线接收采用回执。
固定入口 `START_STANDARD.txt` → `worklines/standard/START_HERE.txt` → `CURRENT_STATE.json#latest_session_closeout`、`NEXT_ACTIONS.json#first`。返回 `RETURN_TO_MAIN.json#session_closeout_20261024`；主线读回和采用必须真实记录，不代填。