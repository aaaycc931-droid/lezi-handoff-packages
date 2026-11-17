# 当前交付与阶段收束｜2026-11-17

司衡现有、已找回的设计、工程、静态美术及配套证据已完成上传与保留核查，本阶段按用户要求暂告一段落。PR23当前工程提交为 `7f428c869b01f4f1310493d24f80e269d3ed7255`；正式美术归位提交为 `2ba4e01c9d8e6ea896327b2c412c44a03bdc7d45`。2张生成母版、4个WebP、检查板、7份原接入实现/脚本与原日志均按31项清单正式归位；原换轨修复与门禁保留。

完整恢复包重新取回并核验：687项与先前清单一致，其中683个工程文件与当前PR23对象身份和大小逐项匹配，另2份用户PNG原件及2份包说明/清单仍私有保留。只表示已知现有成果保存齐全；浏览器/触摸、真人强度、全面独立QA和动画仍未完成。PR仍草稿、未合并，无部署/APK/模式开放。

本次没有运行游戏、DOM、构建或浏览器测试；以下命令与测试数字为原阶段的运行说明/历史证据，不写成2026-11-17新测。最新状态、完成核查和后续恢复见 [CURRENT_STATE](CURRENT_STATE.json) 与 [SESSION_CLOSEOUT](SESSION_CLOSEOUT.json)。

# 历史追加｜2026-11-13：换轨反馈修复

当时的换轨修复代码推进至 `5ab688c96f4960aad70467e7e4c15c21dc55a2e1`，见[VISUAL_REPAIR.md](VISUAL_REPAIR.md)。双端标记与公开动作元数据修复不改变技能规则；本轮155项定向回归、10项DOM检查、3项王安全探针及构建通过。下文1025项/34项与18局为v1历史验证，未在本轮全部重跑。试玩入口和运行方式保持。

# 司衡 v1｜工程与试玩

专属分支：`aaaycc931-droid/jieqi-engine` → `codex/autonomous-hero-01-20261113`。固定开发基线为 PR22 的 `71145df45ad17215a3731e53150b6728e079e375`，入口初始化为 `7f47b740b01b9a1e6ef126fc9e2628682b603e6d`。交付 SHA 和 draft PR 以 CURRENT_STATE.json / RETURN_TO_MAIN.json 的实际发布记录为准。

## 本机运行

```sh
git clone --branch codex/autonomous-hero-01-20261113 --single-branch https://github.com/aaaycc931-droid/jieqi-engine.git
cd jieqi-engine
node --version  # >=24，本次24.22.1
npm run dev
```

在运行该进程的电脑浏览器打开 `http://127.0.0.1:4173/web/?heroPilot=1`，选择本机双人 → 司衡 → 确定，将设备交给另一方选英雄 → 猜拳 → 完整混乱象棋开局。技能按钮显示剩余次数。初始30枚暗子不能换轨；正常走棋揭示己方两枚明棋并使其距离不超过4后，点“换轨”，从合法搭档列表选择，再点“换轨并结束本手”。交给对手正常回应。未加参数时司衡不出现在产品池。

本次实际运行了构建、完整页面模块的 DOM 交互和真实引擎对局。**没有声称 Chromium/手机视觉试玩通过**：容器 Chromium 启动受到 EPERM/进程套接字限制；云浏览器拒绝本地 file URL。没有绕过。DOM 测试不是视觉、触摸或真机证据。

## 精确接入

| 文件 | 必要增量 |
| --- | --- |
| `src/hero-pilot.ts` | 独立候选枚举、距离/次数/层/窗口/落位检查、原子双棋移置与公开次数 |
| `src/types.ts` | `siheng`、试点开关、`relayUses`、`relay_swap`、`partnerId` 类型 |
| `src/heroes.ts` | 独立实验注册与中文技能说明；`HERO_IDS` 默认池不变 |
| `src/hero-forms.ts` | 实验包可识别；权威校验必须显式开关且jieqi；无里包 |
| `src/game.ts` | 初始化第6参数显式开启试点，默认false |
| `src/hero-actions.ts` | 将换轨接入既有II级占步、候选事务、历史/生命周期/落位结算 |
| `src/rules.ts` | 尚有合法换轨时计为有合法行动，避免错误困毙 |
| `src/index.ts` | 导出试点模块给引擎调用者与测试 |
| `web/app.ts` | 本机参数选将、资源说明、合法搭档选择、真实权威命令与接手流程 |
| `tests/hero-pilot.test.ts` | 34项试点边界/重复/秘密/生命周期/循环/H05/H06测试 |
| `scripts/hero-pilot/*` | 完整对局、局部反制、实际页面DOM交互的可重跑脚本 |
| `review/hero-pilot/*` | 实际运行证据、完整示例对局及内容哈希绑定 |

没有修改服务端房间协议、Bluetooth来源、正式评分实现、既有英雄规则或产品featuresReady。NET和模式门禁不变。所有生产增量在专属分支，集成前只审本英雄的必要差分。

## 验证命令

```sh
node --test --test-concurrency=1 tests/*.test.ts
node --test tests/hero-pilot.test.ts
node scripts/hero-pilot/scenarios.ts
node scripts/hero-pilot/playout.ts
npm run build:web
# 可选DOM验证，测试依赖放仓库外，不增加产品依赖
npm install --prefix /tmp/hero-pilot-dom jsdom@31.0.1
HERO_PILOT_JSDOM=/tmp/hero-pilot-dom/node_modules/jsdom/lib/api.js node scripts/hero-pilot/dom-smoke.ts
```

全套回归1025/1025通过后补了3个纯测试（生产代码未再改动）；最终试点专项34/34通过。不是宣称最后一次完整命令跑了1028项。构建成功。没有运行正式评分CLI、更新评分账本或批准新评分方法。

DOM脚本加载真实 `web/index.html` 和完整 `web/app.ts`，追加只供测试的观测与局面注入导出，临时模块在finally删除。正常选将、猜拳、32子初始化由真实按钮完成；技能部分明确从合成中局注入，随后真实技能按钮→候选选择→权威处理→次数显示→接手→认输结果面板。它不验证布局，也不冒充自然从开局走到该中局。

## 保留限制

- 静态立绘、头像和原接入已于2026-11-17完整发布；动画尚未制作，真实浏览器视觉/触摸验收仍未完成。
- 终局计数、长将/压力和重复的全局规则缺口不由本技能改写；没有声称现有引擎已覆盖全部正式裁判条款。
- 八种普通畸变跑了关键移置边界；仅铁壁进行18局完整演练；全部英雄交叉组合、末日宿命、镜像等未穷尽。
- H06快照回溯、H05历史资格拒绝为已测；不把旧引擎H05同后来设计线新版H05混称。
- 本轮自测，不是独立QA；没有合并、部署、APK、真人对战或线上开放。
