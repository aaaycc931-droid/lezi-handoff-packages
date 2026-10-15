# 乐子象棋｜独立UI设计线启动交接

这是现有项目的新工作线，不是新项目。本包用于启动UI设计，包含可直接使用的启动指令、批准首页原图、V4棋盘参考、现行交互约束、协作原件与边界。没有重新生成、抠取或修改图片。

## 最小读取顺序

1. NEW_UI_CHAT_PROMPT.txt 与 CURRENT_STATE.json：本次用户授权、当前分工及范围。
2. 实际读取 reference/X_Collaboration_System.md 全文（长文可分段）；优先按原文 AI_READ_ORDER 读取 YAML、MANDATORY_PRECHECK、PART-6_CURRENT_STATE 与任务相关模块，包括 FILE_OUTPUT_POLICY、AI_LIMITATION_CONTROL、PROACTIVE_DISCOVERY_AND_GUIDANCE。核对内部 system_version 为 1.8.0。项目约定另见 reference/06_PROJECT_COLLABORATION.md。个人协作系统的历史状态和 system_next_action 不替代本项目 CURRENT_STATE.json、UI_CURRENT_OVERRIDES.md 与 UI_NEXT_TASKS.json。
3. UI_BASELINE_LOCK.json 与 UI_CURRENT_OVERRIDES.md，再读取reference/04_CURRENT_UI_AND_FLOW.md。旧正文中的暂停状态、12英雄目录及Android语境按当前覆盖层解释。
4. 查看assets内两张批准原图；阅读UI_NEXT_TASKS.json、INTERFACE_AND_PRIVACY.md及PARALLEL_AND_RETURN.json。
5. 涉及具体技能时，再读reference/product_20261009中的对应规则与reference/mode_design_20261009对应模式差分，并核对Git源码中的最新产品玩家视图。

## 当前授权

用户于2026-10-11明确新开对话负责UI设计，并要求提供开启指令与交接包。此前“最终UI暂停/最后进行”对本次独立UI设计工作线不再构成阻止启动的理由。本次恢复的是UI设计：可以核对、提出方案、制作待审核原型并持续推进。批准资产不擅自改稿；暂缓几何和新美术可以提出方案，未获确认不得改标为正式定稿。APK、实机、联网部署、main合并未随之恢复。

主线与两条模式评分线继续各自工作。UI不另做评分模型、英雄平衡或规则适配。

## 本包能支持什么

可直接开始界面/状态盘点、非棋盘页面精修方案和交互原型。正式分层组件已在Git源码中，包内只保留批准视觉参考和交接文档，不复制整个仓库。素材可取得时使用既有层；不能只凭参考图重新抠整图代替分层源。

包内未生成新UI方案、APK或网页，也未执行UI浏览器/真机验收。已有554项测试是主线原揭棋策略代码回归证据，不是本UI工作线的设计批准或视觉验收。

## v2 协作文档补充

用户于2026-10-11重新提供协作文档并明确要求加入当前交接包，让新UI对话读取。全文保持原始字节与内部版本、P3标记不变；本次公开交接授权仅适用于该上传原件和本仓库，见 COLLABORATION_PUBLICATION_AUTHORIZATION.json，不构成未来资料的永久公开授权。v1保留不变。

接收者应报告实际读取的文件名、内部版本、读取范围、适用门禁、批准UI基线与首项任务。未取得或未读完的内容须如实列明；不可仅凭本入口声明已读全文。按当前用户授权推进独立UI设计，个人文档中的旧项目状态不能静默覆盖本包最新授权。
