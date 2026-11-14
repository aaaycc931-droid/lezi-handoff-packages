# 第二自主英雄｜EXP-HERO-002｜岑缨
本线只制作第二名自主英雄，与司衡同属 WORLD-EXP-01／世界 E「悬衡界」。第一名司衡仍归 `worklines/hero-pilot/` 及 PR23；旧启动词中的分支、任务和断点不在本线接续。

## 当前恢复断点｜2026-11-14
先读 [恢复发布实况](RECOVERY_PUBLICATION.json) 和 [CURRENT_STATE](CURRENT_STATE.json)。原工程、美术和日志已实际取回，54项原件及16项源码／4项证据哈希核对通过；原素材未重画，原业务测试未重跑。

`cen-ying-publication-ready-20261114.zip` 已沿原成果保存渠道保全并重新取回逐字节核对，SHA-256 为 `842a2a45ce9ab9a3873b3fd7063b19ce33f70cee8598cb7d7edcb15cbea51a1f`。包内38个工程文件：36项原增量加2份恢复／作者记录；原增量33项完全同字节，仅3份JSON做执行路径移除和资产哈希引用同步。源码、图片及原日志未改。该包不是已发布的GitHub资产。

**工程分支仍为 `71145df`，尚无本英雄draft PR。** 当前执行环境缺少本地文件到GitHub的有效大文件传输通道；这是能力缺口，不是等待重复授权。下一执行者应核当前权限、归属和最新HEAD，在具备字节上传能力的环境用已准备包发布、读回并创建／复用draft PR。包内脚本含并发保护和中断续传检查，6项测试仅为离线模拟，不冒称远端发布成功。环境未变时不重试同一失败路线，不重做设计、美术和未变的原测试。

原主创模型仍待原始证据；恢复者只记实际贡献，模型标签注明证据等级，不倒填原作者或宣称前端已安装。真实浏览器／触摸、真人或更强策略平衡、独立QA和完整类型检查仍未完成。主线接收保持UNKNOWN。

## 开始／继续
1. 核本库 main 与 `jieqi-engine/codex/autonomous-hero-02-20261114` 最新 HEAD；读取 [TASK_FROM_USER](TASK_FROM_USER.json)、[DESIGNER_BRIEF](DESIGNER_BRIEF.md)、[CURRENT_STATE](CURRENT_STATE.json)、[SESSION_CLOSEOUT](SESSION_CLOSEOUT.json)、[RETURN_TO_MAIN](RETURN_TO_MAIN.json)、[READ_RECEIPTS](READ_RECEIPTS.json)。
2. 这是2026-11-14用户直接委托的新任务；没有伪造主线派发或主线已接收。后续若主线发来任务，实际读取后再登记。
3. 按 `collaboration/CURRENT.json`、`docs/WORKFLOW.md` 和 [PROJECT_INSTRUCTIONS](PROJECT_INSTRUCTIONS.txt) 恢复来源、有效授权、并发保护与中断断点。先核关联分支的实际成果，不因旧文件未更新重做。
4. 世界观读取独立分支 `ui/restart-asof-20261104-1119` 当前原文，并结合司衡的 `worklines/hero-pilot/DESIGN.md`。同世界不等于同职业、同画风、同技能。
5. 沿 [DESIGN](DESIGN.md) 与较新恢复记录继续尚未完成的验收；复用已经完成并找回的真实引擎、页面、美术和原实验。自主作本英雄授权内的创意和工程决定，不逐项向用户问参数。
## 所有权与交付
交接仅写 `worklines/hero-pilot-02/`；工程仅写第二英雄专属分支。共同开发底座采用 PR22 `71145df45ad17215a3731e53150b6728e079e375`，与司衡为同底座兄弟增量，不依赖PR23未合并资产，也不把较旧engine/main当现行工程。
只在显式 `?heroPilot2=1` 的本机混乱象棋入口加入岑缨；默认英雄池、其他模式门禁和NET保持。产物为可审工程候选，保留draft；合并、部署、APK仍不在本任务范围。
阶段成果按最新父树、expected_sha、force=false保存并读回。具体状态以CURRENT_STATE与实际分支为准；独立QA、真人强度、真实设备验证分别记录，不用自测替代。
