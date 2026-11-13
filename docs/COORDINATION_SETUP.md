# 固定项目入口与换对话接续

当前规程见[WORKFLOW](WORKFLOW.md#项目内新对话接续与收束)。本页只维护配置方法和职责路由，不复制实时任务表；各线下一步以自己的固定入口和最新来源为准。旧派发、接收和配置历史可从[本次整理前版本](https://github.com/aaaycc931-droid/lezi-handoff-packages/blob/4c93812a5e357e5c14e4b2831a46b146d6f4a9ba/docs/COORDINATION_SETUP.md)及既有主线记录追溯。

## 一次配置，之后用短指令

用户已报告各支线项目说明里填过入口链接。2026-11-13用户以“已更新，收束”确认主线项目说明已更新，当前对话也实际收到对应指令；全新对话效果、其他项目安装与具体分组仍未验证。下面是完整可复制配置，文件存在不代表其他项目均已安装。已经一线一个项目的，替换相应说明即可，无须重建项目、搬历史对话或新建仓库。

| 固定工作线 | 可复制项目说明 | 来源分支 |
|---|---|---|
| 主线 | [main.txt](project-instructions/main.txt) | main |
| 普通象棋 | [standard.txt](project-instructions/standard.txt) | main |
| 混乱象棋 | [chaos.txt](project-instructions/chaos.txt) | main |
| 半混乱象棋 | [half_chaos.txt](project-instructions/half_chaos.txt) | main |
| 英雄设计 | [hero-design.txt](project-instructions/hero-design.txt) | main |
| 单英雄自主试点 | [hero-pilot.txt](project-instructions/hero-pilot.txt) | main |
| UI图片 | [ui-image.txt](project-instructions/ui-image.txt) | ui/restart-asof-20261104-1119 |
| 世界观／英雄视觉文字 | [world-hero-text.txt](project-instructions/world-hero-text.txt) | ui/restart-asof-20261104-1119 |

每个前端项目只采用对应的一份，不能把多份不同身份说明同时粘进去。只配置实际使用的入口，不要求一次建立八个新项目。说明里固定身份/分支/入口，动态任务仍读GitHub；以后阶段变化无需反复改项目说明。

如果仍让三模式或多英雄共用一个项目，可保留兼容说明：[三模式](project-instructions/modes.txt)、[英雄研究](project-instructions/heroes.txt)、[视觉](project-instructions/visual.txt)。已有对话可以说“继续”；没有身份的新对话只需说“继续普通线”这类短句。若希望新对话也只说“继续”，需给该项目唯一默认线，或将实际长期使用的线分别放入独立项目。不能用最近活跃聊天、文件更新时间或硬编码默认普通线猜身份。

主线版包含一条**仅经用户实际采用才生效的条件接任任命**：旧主线已收束后，在该主线项目中新开对话并说“继续”，任命该对话接任。它仅在用户把该文字实际设为项目说明、且新对话确实获得该指令时生效；仓库文件存在不授予主线角色。本轮主线已按用户要求收束，用户已确认采用对应文字；接手者仍须核自己收到的有效指令和触发条件，不允许同时抢占仍在施工的主线。

## 日常用法

1. 在已配置对应说明的项目内打开新对话，说“继续”。执行者核GitHub最新HEAD和当前路由，简短报告断点，然后按已有授权推进；缺权限或有决定性冲突只报告实际缺口。
2. 需要换对话时说“收束，我会换对话继续”。执行者保存有意义正文、确认、代码版本、未验事项、未发布工作和下一动作，发布并读回；不要求用户携带长启动词。
3. 回传已经入库后，主线在自己的实际运行中主动查收，用户无需转贴整段报告。发布、接收、采用分别记；不会在后台自动唤醒其他ChatGPT对话。

## 必须保持的区分

- UI图片与世界观/英雄文字共用设计分支和部分文件，但接续track不同。main同路径是另一历史资产状态；模板将共享规程指向main、设计来源指向独立分支。不能把文字收束当作图片收束，也不能整树覆盖main。
- 当前正文/任务/收束以各线自己的入口定位，不强制迁移全部旧schema。主线保留普通工程责任；新复核输入与已撤回的工程派发分别判断。无新输入不重复工程、测试或APK。
- 仓库配置已发布，主线说明更新已有用户确认且在当前对话指令中可见；未独立打开设置界面。全新对话是否实际恢复、其他项目安装和自然使用收益仍待验证；不能用静态文件检查替代这些结果。
- 评分原账本冻结、NET暂停、图稿/候选审批、私密来源和其他线未回传成果继续保护。

本轮依据、路由核对及限度见[主线接续流程核对](../worklines/main/PROJECT_CONTINUATION_REVIEW_20261113.md)。
