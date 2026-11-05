# 《乐子象棋》UI｜2026-11-05 Chat 执行修复的主线 / Work 延期回查索引

- **任务 ID**：UI-CHAT-REPAIR-INDEPENDENT-REVIEW-20261105
- **当前状态**：`queued_for_main` / `main_intake_deferred`，**未执行主线接收、未开展 Work 独立审计、不得结案**
- **当前责任边界**：获用户明确任命的主线将来实际接收，再由其协调具备权限的 Work 模式实施独立回查。**本索引及交接材料不能授权普通 Chat 或未获任命的对话自行担任主线。**
- **项目级通知**：[主线暂停接收、各支线独立推进及用户任命边界](../../PROJECT_NOTICE_MAINLINE_INTAKE_PAUSE_20261105.md)；[GitHub Issue #1](https://github.com/aaaycc931-droid/lezi-handoff-packages/issues/1)
- **问题主报告**：[UI_ASSET_PERSISTENCE_INCIDENT_20261105.md](UI_ASSET_PERSISTENCE_INCIDENT_20261105.md)（第 8—12 节为后续执行记录）；[UI 工作约定](UI_WORK_AGREEMENT.md)
- **事件归属**：此前任务实际由 **普通 Chat** 执行，不是 Work。用户于 2026-11-05 指出：当时未先向项目发出“主线暂停接收/用户任命”通知，是发生 Chat 代推进修复的背景，并要求未来主线回看这轮修复。**这是用户提供的过程归因；是否有具体越权及其影响，应由未来主线对当时授权与执行内容独立核查，不应仅据晚发公告倒推事实。**

## 一、可直接逐提交回看的原始 Git 历史（非摘要代替）

| 顺序 | 提交 | 实际改动及证据属性 |
|---|---|---|
| 修复前基准 | [`d762fc0b45d0`](https://github.com/aaaycc931-droid/lezi-handoff-packages/commit/d762fc0b45d053ddf097f9a0b17a85c3f9a687b4) | 初次 Chat 局部流程修补之前的父提交；用于比较 delta |
| 1. Chat 修复 | [`c0d808a293ce`](https://github.com/aaaycc931-droid/lezi-handoff-packages/commit/c0d808a293ce02a2aabaa3a79199d3d8d6e29436) | 原 PNG 从 Library 恢复与哈希核验，关键二进制交接闸门写入 `UI_WORK_AGREEMENT.md`，UI 状态/报告/入口/回传同步 |
| 2. 来源澄清 | [`308d5f8f65c0`](https://github.com/aaaycc931-droid/lezi-handoff-packages/commit/308d5f8f65c0449d0d7f2c2f46917497bcc3c1ed) | 明确上述恢复及修补由 Chat 而不是 Work 执行，不冒称独立验收 |
| 3. 复核责任声明 | [`7586dd99b672`](https://github.com/aaaycc931-droid/lezi-handoff-packages/commit/7586dd99b6729ed43a468671bb022ada65b1a19d) | 写明将来须由主线协调 Work 重审，不由 Chat 正式结案 |
| 4. 一次性 Chat 技术试验 | [`0c82b1210850`](https://github.com/aaaycc931-droid/lezi-handoff-packages/commit/0c82b121085074452d6f843dacdb650dbfb30291) | 合成大 PNG 的 Git Blob 写入与独立 SHA 身份比对；未获得实际原图的远端大文件完整读回 |
| 5. 用户手动原图入私库后更新 | [`8f9af748c534`](https://github.com/aaaycc931-droid/lezi-handoff-packages/commit/8f9af748c5344a8f46a206f3fe29a17f0a582554) | 三原 PNG 已由用户上传到**另一个私有仓库**、Chat 核对 Git Blob 身份后更新原项目第12节；SHA-256 远端完整读回和独立接收尚未验收 |

最关键的**正文修改对象**：`worklines/ui/UI_WORK_AGREEMENT.md` 的“关键二进制资产交接完成闸门”及“专项执行边界”，`CURRENT_STATE.json.ui_asset_persistence_20261105`，`RETURN_TO_MAIN.json.ui_asset_persistence_incident_20261105`，`START_HERE.txt`，问题报告第 8—12 节。可按每次提交的 Files changed 真正阅读差分，不能只看本表。

**资产现址**：私有仓库 [`aaaycc931-droid/lezi-ui-asset-staging`](https://github.com/aaaycc931-droid/lezi-ui-asset-staging)，目录 `originals/`，整理提交 `0bb1e07a53e2b80326812c9fb01cb39ea5072a9b`；三 PNG 大小/Git Blob SHA 对账已通过，**从远端独立下载原始大文件并重算 SHA-256、跨账号恢复仍未完成**。不要将原图复制到公开的交接仓库。

## 二、未来主线真正需要核对的事项

1. **权限与时序**：区分用户当轮授权 Chat 做的只读/原件恢复、阶段性流程修补、一次性技术试验，以及后续要求移交 Work 的正式修复责任；核查这些改动是否因缺少项目级通知而扩大了 Chat 的职责。后来公告不是对过去所有操作的自动撤销，也不追认无证据的主线授权。
2. **真实修复差分**：从修复前的 `d762fc0` 到每一阶段的真实 Git diff，审查它写进 `UI_WORK_AGREEMENT.md` 的五个状态闸门是否与当时有效的 `GITHUB_HANDOFF_WORKFLOW`、`UI_FIDELITY_POLICY.md` 兼容，是否只是文字生效、有没有做过完整交付实例验证。
3. **证据和状态传播**：比较各阶段 `CURRENT_STATE.json`、`RETURN_TO_MAIN.json`、`START_HERE.txt` 及报告的有效时点，区分旧时点“远端尚无原件”与现时点“私有仓库已有原件但恢复验收未完成”。不得把历史结论误作当前事实或把 Git Blob 身份当跨账号完整恢复。
4. **独立实验与修复**：Work 在用户后续明确解除主线接收暂停、由获任命主线实际协调后，独立下载 PNG、逐张算 SHA-256、验证接收环境和权限，再对实际 UI 二进制交接执行一次结案门禁；若发现 Chat 修补的具体逻辑缺口，基于有效源仅改授权差分，不简单覆盖已有有效资产/状态。
5. **收束与回执**：将“回看了哪些提交/文件、核验结果、修复/保留/阻断的项目”如实写回已有状态/审计资料，由真实接收者记录接收与采用。**仅看过此索引、收到 Issue、连接仓库或启动 Work，不代表已经完成审计。**

## 三、必须承认的证据缺口

- GitHub 存有上述**提交和持久化正文/状态**，可以准确回看“写了什么”；但 GitHub 不等于完整 Chat 对话的逐条原文、所有工具调用及所有本地实验输入输出均已归档。当前尚无被验证为完整可重读的 Chat 全对话原文包。
- 所以未来主线能够基于 Git diff 和报告做独立审查；若它需要逐字重建聊天授权/时序却缺原文，须标记来源不完整并向用户索取必要记录，**不能把 Git commit 或 AI 报告冒称完整聊天记录**。
- 本任务仍然由用户明确后续调度；现在只是**补全入口和待审索引**，不实施 Work 修复、不更改 UI 批准/游戏代码/评分冻结/NET 暂停、不自动恢复主线接收。
