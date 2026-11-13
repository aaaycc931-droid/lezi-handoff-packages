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

**当前真实状态：入口、授权和专属分支已准备；新Work对话尚未被本主线验证已启动，英雄设计/代码/运行尚未完成。** 后续以最新CURRENT_STATE和执行者真实回执为准。
