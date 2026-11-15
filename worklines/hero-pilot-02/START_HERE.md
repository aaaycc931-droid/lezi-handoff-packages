# 第二自主英雄｜EXP-HERO-002｜岑缨
本线只制作第二名自主英雄，与司衡同属 WORLD-EXP-01／世界 E「悬衡界」。第一名司衡仍归 `worklines/hero-pilot/` 及 PR23；旧启动词中的分支、任务和断点不在本线接续。

## 当前上传断点｜2026-11-15｜分阶段第1批已收束
先读 [分阶段上传实况](STAGED_UPLOAD.json)、[CURRENT_STATE](CURRENT_STATE.json) 和 [SESSION_CLOSEOUT](SESSION_CLOSEOUT.json)。

用户本轮明确要求分阶段上传，不要求一个对话完成全部。本轮已实际发布 **36/38项工程候选**（源码、文档、历史验证材料、资产说明和3项WebP运行资源），另加一份分批记录，共37项改动。
- 专属工程提交：`101a970020fa7130c1367a04f67fdbb03dff5d3a`。
- 草稿 [PR31](https://github.com/aaaycc931-droid/jieqi-engine/pull/31)，基于 PR22 同底座；保留 draft，尚未合并。
- 36项已从固定提交逐项取回核对大小、SHA-256、Git blob SHA，全部一致，合计1,248,742字节。本轮未重跑未变的历史业务测试。
- **全部内容上传尚未完成**：38项候选还缺两张PNG母版；原件包补充材料还需另批核映射并上传，不能把36/38当作所有原件覆盖率。

### 下一批
从已保存的 `cen-ying-publication-ready-20261114.zip` 取出两张母版，保持原字节；包 SHA-256 仍为 `842a2a45ce9ab9a3873b3fd7063b19ce33f70cee8598cb7d7edcb15cbea51a1f`。两张母版精确路径、大小和双哈希在 STAGED_UPLOAD 的 pending_candidate_files。
先核最新专属分支和当前执行权，复用PR31；采用工具内字节传输，禁止图片Base64经模型文本回显后拼接上传。按最新父树、expected_sha、force=false保存并读回，收束有限批次。不得重传已成功且无差分的36项。

随后核原54项恢复包中的补充原件；R7曾识别8项补充，本轮未重新核其映射。缺源只阻断相关部分。来源身份和原恢复证据仍见 [RECOVERY_PUBLICATION](RECOVERY_PUBLICATION.json)。

原主创模型仍待原始证据。真实浏览器／触摸、真人或更强策略平衡、独立QA和完整类型检查仍未完成，主线接收为UNKNOWN。本轮执行已关闭，不停用长期入口或暂停其他线；旧后台状态仍UNKNOWN。

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
