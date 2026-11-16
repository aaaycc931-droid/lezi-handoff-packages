# 自主英雄试点｜EXP-HERO-001｜司衡

## 最新接续｜2026-11-16｜两次额度中断已核查，原件保全，整批美术上传尚未完成

先读 [CURRENT_STATE](CURRENT_STATE.json)、[本轮中断与保存记录](ART_UPLOAD_INTERRUPTION_20261116.md)、[SESSION_CLOSEOUT](SESSION_CLOSEOUT.json) 和 [RETURN_TO_MAIN](RETURN_TO_MAIN.json)。用户本轮提供两段因Work额度中断的旧对话，要求核查并先保全。用户已经明确批准全部上传更新，且明确指定将包内司衡原图、导出资产及配套工程提交到公开 jieqi-engine 的 PR23 专属分支。**旧记录的“等待图片公开授权”已被后续确认更新，不重复索要同范围批准。** 平台工具审核仍须遵守。

### 已找回和保全

- 原私有恢复包 `siheng-art-recovery-20261113.zip`，35,899,664字节，687个文件成员；本轮ZIP CRC通过，31项发布清单的大小、SHA-256及Git blob全部匹配。包内另有两张用户上传PNG原件，仍完整私有保存，与生成母版不冒称字节相同。
- 7个原实现文件、两张生成母版、4个WebP、检查板、提示词和原/复核日志都在。未重画、未重编码、未重建；本轮没有重跑游戏测试。
- 初核PR23仍为 `5ab688c96f4960aad70467e7e4c15c21dc55a2e1`。但远端有3个未形成整批美术提交的原对象；本轮直接复用并保全到隔离暂存目录。它们是 PROMPTS、素材README、64px WebP，不能说此前完全未上传，也不能认定31项已上传。
- PR23保全提交 **`3df63e0c8d100fe040a32de4e0f8246c3b046b06`** 已发布且核验记录已读回，`review/hero-pilot/ART_UPLOAD_CHECKPOINT_20261116.json` 记录全部边界。保全子树 `082468bbcda7fb6496d60f4ca79ec1411414be3c` 与本地原件计算一致。只改review下暂存与检查点，不改现行游戏逻辑和运行界面。
- 最新私有接续包 `siheng-upload-resume-20261116.zip` 与可公开续传包 `siheng-art-remaining-upload-20261116.zip` 已保存Library。前者保留来源定位、原清单、完整源快照清单、核查记录及续传包；前者不是公开上传包。原35.9MB恢复ZIP也不要整包公开。

### 唯一上传下一步

可公开续传包解压后为 **29个平铺文件：28项待转移或再核对象＋1份索引**。另3项已固定保存，后续直接复用，不重复传输。现已明确查到头像母版与ART_ASSET_MANIFEST两个对象未存在；其余26项没有逐一证明远端有或无，不能说28项全都缺失。

目标仅为 `aaaycc931-droid/jieqi-engine` 的 `codex/autonomous-hero-01-20261113`，复用 [PR23](https://github.com/aaaycc931-droid/jieqi-engine/pull/23)。收到实际文件传输后，先核最新HEAD和索引，校验31项身份；完整归位到原清单路径后再删除已核实的临时路径，保留日志历史身份，更新本线与PR并读回。不覆盖较新并发成果；latest-parent、expected_sha、force=false。当前容器GitHub DNS失败，不能把连接器文本/Git对象写入成功说成已完成本地大图传输；这不是重新等待授权。

## 原任务、职责与未验项

原委托仍为 [TASK_FROM_MAIN](TASK_FROM_MAIN.json)，设计目标见 [DESIGNER_BRIEF](DESIGNER_BRIEF.md)，项目说明见 [PROJECT_INSTRUCTIONS](PROJECT_INSTRUCTIONS.txt)，共同恢复规程见 `docs/WORKFLOW.md` 与 `collaboration/CURRENT.json`。本次只处理同一司衡任务的保全及上传接续，不任命业务主线，不重做设计，不写岑缨/PR31或独立UI。

专属工程基线仍为PR22 `71145df45ad17215a3731e53150b6728e079e375`，已完成换轨修复的运行版本仍为5ab688c；新保全提交不冒充完整美术集成发布。通过 `/web/?heroPilot=1` 的原门禁不变。独立UI分支本轮只核HEAD `e2c8d4f2799998f37fbfda25e3c9a5b0ca03525d`，未修改。

历史恢复与验证正文：[ART_RESTORE_STATUS_20261113](ART_RESTORE_STATUS_20261113.md)；更早原图恢复：[ART_RECOVERY_CLOSEOUT_20261113](ART_RECOVERY_CLOSEOUT_20261113.md)；换轨修复：[VISUAL_REPAIR](VISUAL_REPAIR.md)。旧授权等待文字只代表当时，不覆盖本轮较新确认。此前完整入口和状态保留于本仓库 `a835d6eff9d362933e3c5915487cc9f6c5490240`。

56项Web、14项DOM、构建和4项HTTP等为原恢复包中的历史验证，不是本轮新运行。真实浏览器/触摸、真人对抗强度、全面独立QA、动画等仍未完成。已有V1有限接收保留；新美术接收UNKNOWN，接收方只写自己的回执。PR保持draft，不合并、部署、发布APK或开放模式；评分原账本与NET边界不变，不暂停其他线。
