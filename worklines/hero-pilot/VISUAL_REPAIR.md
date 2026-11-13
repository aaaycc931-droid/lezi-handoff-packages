# 司衡换轨反馈修复｜2026-11-13

任务 `MAIN-HERO-PILOT-SWAP-VISUAL-REPAIR-20261113` 已实际读取并完成。主线在 `04ae7489b0577f93fa074ae3854f8caf823253ee` 发布的接收报告、DOM记录和复现脚本是本轮来源；原设计与规则未被否决。本线先在引擎原HEAD `7a1dfbc92efa2a54bb85175cc251856bb2cdb4d3` 实际复现：真实两端为(0,6)/(2,6)，DOM却给(0,0)同时添加last-from/last-to。

修复提交：[5ab688c](https://github.com/aaaycc931-droid/jieqi-engine/commit/5ab688c96f4960aad70467e7e4c15c21dc55a2e1)，已更新原[draft PR23](https://github.com/aaaycc931-droid/jieqi-engine/pull/23)。14个增量文件均已读回，与本地Git blob精确一致；其中4个为生产文件。

## 实际修改

- `src/types.ts` / `src/hero-actions.ts`：`lastMove.relaySwap` 保存按棋子ID排序的两条公开移置记录，各含ID、真实起点和终点。通用兼容坐标也不再凭空使用(0,0)。记录绑定动作，不依赖暂存的automaticEvents；没有把换轨改成普通单棋移动，也没改变II级/整手、次数、落位、历史资格或王安全逻辑。
- `web/app.ts`：两个实际端点各显示“换轨 ↔”，无障碍标签和一次本地消息明确“两枚棋交换位置”。双棋行动不套用普通last-from/last-to样式；下一手普通行棋自然替换特殊反馈。换轨重复actionId不追加提示、交接或资源消耗。
- `web/style.css`：只新增本技能端点小标记样式；不重画全局UI或改旧英雄风格。

## 本轮真实验证

| 检查 | 结果与边界 |
| --- | --- |
| 试点、时间线、英雄形态相关回归 | 63通过，0失败；包括H05资格拒绝、H06恢复与默认池门禁 |
| 英雄接入及Web玩法/消息/布局回归 | 92通过，0失败 |
| 实际生产页面模块DOM | 10通过：正常选将开局、两端标记/文本、临时事件清空、重复命令、后续普通走子、敌子/同子/旧revision拒绝、无搭档说明与认输面板 |
| 主线王安全探针由本线复跑 | 3通过：秘密陷阱合法提交、消耗与处决；双端顺序；原输入及终局。属于本线复跑，不是新增独立QA |
| 构建与差分空白检查 | `npm run build:web`、`git diff --check`通过 |

证据与命令：[VISUAL_REPAIR.json](https://github.com/aaaycc931-droid/jieqi-engine/blob/5ab688c96f4960aad70467e7e4c15c21dc55a2e1/review/hero-pilot/VISUAL_REPAIR.json)、[DOM_SMOKE.json](https://github.com/aaaycc931-droid/jieqi-engine/blob/5ab688c96f4960aad70467e7e4c15c21dc55a2e1/review/hero-pilot/DOM_SMOKE.json)。修前记录、日志摘录、王安全复跑脚本/结果也在同一提交内。证据按源文件SHA256绑定。

本轮没有重新运行1025全套或18局弱策略实验，没有参数或规则变化；原结果仍绑定旧提交，不能把历史报告移称本轮新跑。DOM包含显式合成中局，非法/重复命令调用导出的真实生产处理器；不是自然到达局面或真实浏览器布局验证。

## 当前接续

本线完成了所派发的反馈修复，等待的是主线对新提交的定向接收，**不是等待用户再批准人物或技能**。主线已接收v1及有限技术复核的事实可以记录；本次修复是否已被主线读取仍UNKNOWN。

本线下一项可独立推进为司衡最终立绘与小尺寸资产；开展前须读取独立UI最新入口/英雄风格规则，不能把其他UI对话的新风格偏好未经范围核对套入本英雄。当前仅核独立UI最新HEAD `5a534377d705d28184b07078e3d3abf10978bf9e`，本轮未开始美术制作。真实浏览器画面/触摸、真人反制强度、最终美术和全面独立QA仍分别未完成。未合并、部署、发布APK、解冻评分或开放NET。
