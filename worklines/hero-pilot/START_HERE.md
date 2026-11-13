【2026-11-13 主线已接收司衡候选｜直接修换轨反馈】
先读TASK_FROM_MAIN.json#main_visual_repair_20261113及../main/reviews/hero-pilot/INTAKE_REPORT.md。主线子代理另行复跑34专项、3有界王安全探针、原4 DOM检查，并复现换轨真实端点(0,6)/(2,6)却把(0,0)标为上一手起终点。此为合成fixture上真实页面模块反馈错误，不是设计被否决。按既有单英雄自主设计/工程授权在自己的PR23分支做最小修复及实际DOM断言，不等用户逐项批准、主线结果协议或浏览器环境。保留尚未回传成果；若已修先查较新commit再核验，避免重做。修后仍可自主推进本英雄最终美术等独立事项，真实浏览器/真人强度/独立QA分别保留；不合并部署。实际新任务已读/执行由本线回执，不由主线预填。

# 自主英雄试点｜EXP-HERO-001 固定入口

用户先试**一个**新英雄；本线在这一英雄范围代替用户担任设计决策者并完成工程。用户不逐项审批，游戏规范与合理强度要求和既有英雄一致。准确委托见[TASK_FROM_MAIN](TASK_FROM_MAIN.json)；如何理解用户目标与偏好见[DESIGNER_BRIEF](DESIGNER_BRIEF.md)。

## 开始／继续

1. 核本库main、专属引擎分支、独立UI分支的最新HEAD；保护本线未回传成果，读[CURRENT_STATE](CURRENT_STATE.json)、[SESSION_CLOSEOUT](SESSION_CLOSEOUT.json)、[RETURN_TO_MAIN](RETURN_TO_MAIN.json)、[READ_RECEIPTS](READ_RECEIPTS.json)及最新任务。
2. 读[项目说明](PROJECT_INSTRUCTIONS.txt)、设计准则和任务required_sources。已读未变源可按scope复用，涉及的关键原规则必须真正读取。最新正文/原确认优先于旧摘要。
3. 代码仓库`aaaycc931-droid/jieqi-engine`，分支`codex/autonomous-hero-01-20261113`，基线PR22 `71145df45ad17215a3731e53150b6728e079e375`；入口初始化提交`7f47b740b01b9a1e6ef126fc9e2628682b603e6d`仅文档。查最新分支再接续，不重置到初始提交。
4. 世界观只读`ui/restart-asof-20261104-1119`的当前来源，不读main旧UI副本替代。既有D属于H15，本新增世界暂称E，不占现有H编号。
5. 先理解3个对标英雄和棋规→自主设计→尽早真实引擎实现/可玩→测试/对手反制/平衡迭代→完整候选回传。无需让用户继续选择人物、技能或数值。

## 范围与交付

首版在现有混乱象棋jieqi基线上做离线完整可玩集成；既有模式门禁、NET、评分原账本保持。允许本分支为新英雄做所需最小接入，不允许只有旁路小游戏。目标是可集成上线的完整候选，不是现在部署或把少量自测冒称全局平衡。

具体设计由本线自主定稿并记录为受托决定，不伪称用户逐条确认。与旧线遇到依赖时优先采用已有实现、在本分支解决可隔离问题或调整自己的机制；需要更改共同规则时带最小具体问题回主线，其余工作继续。

固定产物：DESIGN.md、IMPLEMENTATION.md、BALANCE.md、VALIDATION.json及上述状态/回执。尚未生成的产物不要用空文件冒充完成。阶段保存源版本、真实运行命令/结果和剩余限制；发布后读回，主线自行接收。工程draft PR保持仅本英雄增量，无合并部署/APK授权。

**当前真实状态（2026-11-13执行者回传）：司衡／世界E悬衡界已自主定稿，真实引擎代码及局部证据已发布至专属分支，draft PR #23；全回归1025项、最终专项34项、18局演练及4项DOM交互通过。真实浏览器/触摸、最终立绘、真人强度与独立QA尚未完成；未合并部署。** 详见[DESIGN](DESIGN.md)、[IMPLEMENTATION](IMPLEMENTATION.md)、[BALANCE](BALANCE.md)、[VALIDATION](VALIDATION.json)及[RETURN_TO_MAIN](RETURN_TO_MAIN.json)。主线接收/采用仍UNKNOWN。
