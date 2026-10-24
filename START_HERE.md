> 2026-10-24评分路线更新：已实际完成[候选方法](worklines/main/scoring/CANDIDATE_METHOD.md)、[诊断/迁移与验证说明](worklines/main/scoring/REVIEW_REPORT.md)及30项检查/13个条件问题。正式方法尚未替换，原账本和英雄机制保持，全局新分数未发布；本轮明确执行覆盖此前评分路线停止。[当前评分状态](worklines/main/scoring/EXECUTION_STATE.json)。下方主线工程和三线任务信息属于前阶段记录，当前各线结果读自身固定状态；本评分阶段仅核对并发回传路径/身份，未做内容采用。

# 乐子象棋项目入口

2026-10-24主线：完成共用研究证据失效处理，草稿[PR13](https://github.com/aaaycc931-droid/jieqi-engine/pull/13)，继承PR8—12；6项新边界/99针对性/43文件612相关检查通过，未合并。游戏真实执行与证据资格分开：采集失效不能判验收通过。详见[主线报告](worklines/main/MAIN_FOUNDATION_REPORT.json)。

已分发三模式独立任务：[混乱模式（原揭棋/jieqi）](worklines/chaos/START_HERE.txt)、[普通象棋/xiangqi](worklines/standard/START_HERE.txt)、[半混乱/half_chaos](worklines/half_chaos/START_HERE.txt)。先读[统一任务](worklines/main/MODE_DISPATCH.json)及各线TASK_FROM_MAIN.json，再按各线当前状态接续。任务发布不等于接收对话已读/已执行；真实回执由接收者维护。

[主线入口](worklines/main/START_HERE.txt)负责共享源码与跨线整合；下一核M01/M04路径完整结果的差异与闭合检查点，具体方案已发布、路径代码尚未修改。[UI](worklines/ui/START_HERE.txt)保持独立，B8已批准、B9未制作，不属于三模式支线。

既有玩法原确认、山2B与风设计路线、批准图稿全部保留。评分冻结、评分优化本轮不恢复、NET暂停。半混乱原自然12执行0/64UNRUN；mode featuresReady与研究准入不变，未做完整对局或产品验收。

当前索引[CURRENT_HANDOFF.json](CURRENT_HANDOFF.json)，通用协作版本由[collaboration/CURRENT.json](collaboration/CURRENT.json)解析；写回按[docs/WORKFLOW.md](docs/WORKFLOW.md)。只在固定工作目录增量更新，复用资产/来源，普通非强制提交与发布后复读。旧轮次从[archive/INDEX.json](archive/INDEX.json)按固定提交恢复。
