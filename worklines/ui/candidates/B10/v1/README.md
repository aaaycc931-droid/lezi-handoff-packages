# B10-v1｜蓝牙首次连接成功（静态候选，待用户审批）

本项从 B9-v1 已批准原图之后的独立状态继续；不覆盖 B9 或其他批准画面。

## 对应的产品状态

依据 aaaycc931-droid/jieqi-engine 的历史 UI 设计分支 codex/ui-design-20261011（commit 1f6c1635ad756eefc871f2075883bf26b82176ea）的 web/app.ts：首次 transport CONNECTED，且此前未建立连接时，画面显示「连接成功」，正文为「正在同步房间，即将进入英雄选择。」；此时取消和返回会话按钮隐藏。真正进入英雄选择依赖接收房间状态，不假定固定延迟。

本张采用房主视图：不显示对端设备名。蓝色墨框内「正在同步房间」是非交互反馈，不能按按钮接入点击。再战属于 finished/rematch 分支，另行设计；不可混入此张。

当前 jieqi-engine/main 是另一套实现，历史 UI 分支不代表生产代码已经接入和验收。

## 画面保真

- 原画布 852×1846，纸纹、山水、顶部箭头、标题、墨框和页尾均继承固定 B4 源底层。
- 原始 Long Cang 字库身份：e5bf2c3f24ef2327c6f136d8f73e2f9dfdf44896fdbeb35a9515f44777bb91bc；字库未修改，也不随本候选打包。
- B9 批准图 SHA-256：d81a19895bef348709180a6a5ecf9ed82b06ad4822fef3f7709c9ea7874f0bf0。
- B10 候选 PNG SHA-256：a7b314afe8d3dedf68f114b0442ee802a5853cedff2ae90893554e2ed8a99d95。
- 本地先精确重合成 B9，差异 0；B10 对 B9 的实际变化 35,272 像素，在原新文字 alpha 并集与指定区域之外变化 0。

## 源资产和重建

原始制作时只回传了 parameters.json、build.py、evidence.json，PNG 当时留在对话。2026-11-13 已实际核得后续私库保存的原 PNG；上述历史“未上传”状态已被本次核验覆盖，原 parameters/evidence 作为制作快照保持不改。

- 私库：`aaaycc931-droid/lezi-ui-asset-staging`，固定提交 `e2c51985eabc9fb17106ad166f9d4d405fb55a95`。
- B10 原件：`UI-IMG-042_a7b314afe8d3.png`；Git blob `ccddf4d9011b26c917a5df011001c6456642c598`，2610870 字节。
- B9 批准原件：`UI-IMG-043_d81a19895bef.png`；Git blob `60bb39f5595c02b3f42ff15aea73027bf6aba6d1`，2622399 字节。
- 两张图均已实际取回，完整 SHA-256 与上列既有身份一致。原件留在私库，本公库只保存来源和恢复记录，不重复上传图片。

构建命令（从已有固定资产本地调用）：

    python build.py --base /path/to/b4-fixed-local-base.png --font /path/to/LongCang-Regular.ttf --approved-b9 /path/to/lezi-bluetooth-B9-v1.png --out /path/to/lezi-bluetooth-B10-v1.png

源程序核验来源摘要、批准 B9 精确重合成、画布尺寸、像素保护区和候选 PNG 的 SHA。2026-11-13 接收环境发现并修正一处参数读取笔误：`--approved-b9` 对应值原误写为 `a.approved_b8`，现为 `a.approved_b9`。没有改变字库、底层、布局参数或预期 SHA。

修正后实际运行返回 0：B9 重合成差异 0；B10 与取回的私库原件逐字节一致、RGBA 差异 0；B10 对 B9 的变化仍为 35,272 像素，文字 alpha 并集和指定区域之外变化 0。B10 原图已实际看图，继续待用户具体审批。完整环境与范围见 `restoration-verification.json`；此结果只证明本张静态候选在本次接收环境可恢复。

## 范围边界

仅供用户具体审批一张静态图。蓝牙双机、真实切屏、交互、屏幕适配、APK、游戏代码与主线合并均未验证。评分冻结，NET 暂停。既有批准及首页/V4 例外不变。
