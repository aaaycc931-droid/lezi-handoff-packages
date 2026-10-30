# B9-v1｜蓝牙权限永久拒绝 → 系统设置

**状态：用户已批准的静态 UI 母版（2026-10-30T20:40+08:00，原话：「通过这一份」）。** 2026-10-30 本轮恢复 UI 设计线，最新读取主线 HEAD 为 `0d1f33d6464efccd3fded2588c330e536d690540`。B6/B7/B8 等既有批准保持不变；本次批准已写入固定 APPROVAL_REGISTER.json（见下方修正后的权威路径）。

## 本次候选

使用批准的 B8-v1 画面与固定 B4 源底层，852×1846，不重新生成山水、纸纹、墨框、标题、返回箭头或页尾。沿用同一份 Long Cang 原字库，四组新的文字轮廓独立成层：

- 状态：蓝牙权限已被永久拒绝
- 解释：请在系统设置中开启附近设备权限，／返回游戏后重新进入蓝牙对局。
- 主按钮：前往系统设置

本图仅用于 Android 系统已报告 `permission-denied` 且 `permanentlyDenied=true`、无当前连接会话的静态状态。上方返回入口保留；不出现请求同一权限的普通授权按钮、设备选择与连接操作。真实系统设置跳转依赖产品已有的 `bluetooth-app-settings-button`，其有效性仍未验收。历史 `source-behavior-excerpts.json` 来自 jieqi-engine 的 `1f6c163...`，不能当作 2026-10-30 生产运行证明。

## 资产与回放

- 已创建的实际候选 PNG 的本地 SHA-256：`d81a19895bef348709180a6a5ecf9ed82b06ad4822fef3f7709c9ea7874f0bf0`。
- 本次 GitHub 增量写入的是可恢复**文本源**（参数、生成程序与检查），PNG 原图目前只在本次对话产物中，**未上传此仓库**。在下一次接续时应按下方源身份重合成，再核对原候选内容身份；不能宣称 GitHub 已持有 PNG 或已有正式审美批准。
- 原有 GitHub 资产：`assets/ui/13a513a067abb972ab8e0c898faeba92eb17952a1ecc955248e418c73b429a8f.png`（冻底层）、`assets/ui/e5bf2c3f24ef2327c6f136d8f73e2f9dfdf44896fdbeb35a9515f44777bb91bc.ttf`（注意：依赖路径以资产索引为准；不要重传字库），批准 B8 原图 `candidates/B8/v1/lezi-bluetooth-B8-v1.png`。
- 从仓库资产恢复的 `base.png` 与 `LongCang-Regular.ttf`、B8 PNG 作只读输入，运行 `python build.py --base base.png --font LongCang-Regular.ttf --approved-b8 lezi-bluetooth-B8-v1.png --out B9.png`。不要将字库嵌入交付文件。

## 本地核对

原底层和字库 SHA-256 与批准依赖精确一致；产物尺寸 852×1846；经 Pillow + fontTools + CairoSVG 合成，B8 与 B9 的新旧文本字形 alpha 并集之外**0 个像素改变**。原 B8 通过同一图形路径重新光栅化时，抗锯齿/像素混合可能有极少量像素 1—4 通道值差异，这些落在允许文字区，不属于底层失真。视觉候选已在当前对话展示，**用户已明确批准 B9-v1 静态图稿**。双机、真实系统权限、设置返回、适配、APK、产品代码和主线合并均未运行。

本次是 UI 线独立静态候选，不修改游戏源码、英雄机制或其他三模式线成果；正式评分冻结，NET 暂停。

## 审批回执｜2026-10-30

用户原话：「通过这一份」。本次具体批准 B9-v1 已展示的原图，SHA-256 `d81a19895bef348709180a6a5ecf9ed82b06ad4822fef3f7709c9ea7874f0bf0`；审批权威记录在 `../../../APPROVAL_REGISTER.json`。批准内容仅为静态 UI；源层及图像身份保持不变。原 PNG 仍未上传 GitHub，应按源程序恢复并核对 SHA 后方可作为同一母版使用；审批不等于 Android 设置跳转、设备权限结果、双机、响应式、APK 或生产代码已验收。
