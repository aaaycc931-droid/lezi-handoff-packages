# 普通象棋接收主线PR15—PR17限定证据｜2026-10-29

- 接收者：standard；任务：`STD-RECEIVE-NP32-PUBLIC-QUERY-QUALIFICATION-20261029`；任务来源：`worklines/standard/TASK_FROM_MAIN.json`（`STD-RECEIVE-NP32-RUNTIME-20261028` + PR16/17增量）；开始核查的交接HEAD：`96e78d142fe15fac87289a704f6aba89861da18d`；阶段写入前远端HEAD：`96e78d142fe15fac87289a704f6aba89861da18d`。
- 结论：**实际阅读并接收三项限定研究证据；仅在普通模式的技术证据/缺口台账内采用，不表示独立重跑、产品/规则采用、正式资格或合并。** 原普通31确认和本线直接共享13确认、玩法Δ0、评分冻结、NET暂停。保留2026-10-27旧收束为历史，不能再用“等待主线”概括全部工程阻断。
- 原PR14旧任务：已核对PR14草稿元数据、H21 invoke源代码和后续PR15继承的AS来源保留代码；并阅读主线PR14阶段报告。此处**不**宣称对PR14全部代码/owner-only私密原始记录逐项独立完成验收。PR15给出的后继可执行证据优先核实。

## PR15真实普通NP32（commit `680966fff6484b418c25c9afb8b6759b7a44b594`）
- 实读主线`MAIN_NP32_REPORT.md`、`NP32_PROGRESS.json`、引擎`docs/STANDARD_NP32_RESEARCH_20261028.md`、`review/standard-np32/RESULTS_20261028.json`、`tests/standard-np32-research.test.ts`、`scripts/research/standard-np32.ts`、`src/research-source-context.ts`及原标准合同。
- 三份原始输入中NP合同、H21 RNG合同、AS/AP/ES观察guard的Git blob分别为`4fb70b4d29a9b077ce799e4c00375982d1f7a066`、`4be095dd7d9799062b23f4fb3421f5231c2133`、`294c988f9c1cfa78eb76129b93371f819d2ffb1b`；引擎引用相同blob。测试代码显式检查源固定、32明棋、受限真实房间/选择/RPS/形态、每行动检查点、时钟、祈求与随机次序。
- 发布结果按AS=11/AP=13/ES=13，共37**实际权威房间请求**，37原子闭合与37正式结束检查点、12次H21授鳞receipt；原定条件式受控索引流，不是生产随机抽样。AS：路径兵死亡/终点马耗鳞生存/红车返位/发动英雄来源未消耗；AP：路径兵耗鳞存活/终点马死亡/车落位/R7使用后续机会；ES：路径兵死亡/终点马耗鳞生存/车返位/R7后续机会已用不退款。B1–B4 invoke均计主行动，B4预兆、R5后B5实际降临。
- 51相关文件749项通过是**主线发布并附测试代码/结果的执行证据**，本次标准线未独立运行。原观察矩阵15项NG-01…NG-15与结果标识逐项一致；NG11明确未运行、NG12仅首后续窗口实际执行，NG03/05/07/08/10/13/15等为受限/部分核证，不可全部写PASS。6旧危险王安全符号样例转拒绝及6合法对照为组件，不宣称自然局面可达。
- H21实际抽样池/顺序可复核，不是概率证明，`min(4,N)`不因测试而升级为新玩法批准；无原始私密轨迹独立取得或完整正式验收。

## PR16限定公开闭合查询（commit `765a6bc6799ac823c9ba6e1ed6b10fd0c0705608`）
- 阅读`MAIN_PUBLIC_PATH_QUERY_REPORT.md`、`PUBLIC_PATH_QUERY_PROGRESS.json`、引擎`review/public-path-query/RESULTS_20261028.json`、`DIFFERENTIAL_20261028.json`和`src/game.ts`的`coveredPathMove`、`supportsClosedPublicPathQuery`、`projectClosedPublicPathAction`。
- 限定明置公开接触的旧12处查询/权威差异在18个符号组件中降为0；6个危险候选取消、6个合法解将恢复；37原NP请求旧/新及插入查询的权威/事件/视图/RNG一致。主线发布52文件782项通过，本线未重跑。其公开查询范围不包含秘密接触、其他英雄/空间、晚期来源或完整产品搜索。

## PR17三态公开动作资格（commit `1bda5bc9f7840d0d601a85fb0faeda842753a199`）
- 阅读`MAIN_PUBLIC_PATH_QUALIFICATION_REPORT.md`、`PUBLIC_PATH_QUALIFICATION_PROGRESS.json`、引擎`docs/PUBLIC_PATH_QUALIFICATION_RESEARCH_20261028.md`、`review/public-path-qualification/RESULTS_20261028.json`、`SOURCE_AUDIT_20261028.json`、`src/public-path-qualification.ts`及`tests/public-path-qualification.test.ts`。
- 实际源码接口为`qualifyPublicPathAction`：`legal`、`illegal`、`uncovered`，前二者附来源，后者明确缺项；无私密真身兜底，不把旧boolean true当完整资格。18符号来源×90目标=1620同源权威比对（**非独立样本**）；原37请求前后与插入资格查询结果一致；报告53文件821项通过，独立QA仍否。
- 明置M04路径龙鳞仅沿原批准范围，暗置接触/倒戈/真正死亡身份仍未覆盖。room、UI、终局等消费者**未迁移三态**；本次不改变实际提交/公开政策，不解锁普通模式。

## 缺口及回主线
1. `MAIN-STD-R8-NATURAL-WINDOW-20261028`由**主线**负责：H02 R7保留/R8使用/到期三支完整自然窗口，NG12尚缺。
2. NG11：H10、多防护、返位位置冲突、特殊控制、空中/河道、历史变化等组合待独立资格化。其余NG的部分结论各保留原标签。
3. 生产随机分布/真实概率、完整32棋正式验收、全源搜索、公共消费者三态迁移、独立QA、完整类型检查、UI/真机均**未完成**；`xiangqi.featuresReady=false`，PR14—17仍草稿未合并。
4. 独立可做：`NEXT-STD-INDEPENDENT-PRIVATE-PUBLIC-OBSERVABILITY-MAP`（原H10/H15/D01/H21/H14/M07三视图静态合法展示）；本次只登记为下一项，**尚未实施**。

## 回执权属
- 普通线实际阅读：是（以上精确范围）；普通线证据采用：是，仅限已经核实的有界结果及未验边界；普通线自行引擎运行/独立QA：否；游戏实现/上线/规则批准：否。
- 主线是否实际阅读/采纳**本次回执**：未知，保持`null`；其他工作线回执不代填。
- 不修改原任务的主线发行快照；新的接收事实登记在普通线`READ_RECEIPTS.json`、`RETURN_TO_MAIN.json`、`CURRENT_STATE.json`。
