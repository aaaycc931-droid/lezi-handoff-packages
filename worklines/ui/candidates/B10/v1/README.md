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

GitHub 已保留 parameters.json、build.py、evidence.json；原始 B10 PNG 是本轮对话附件，尚未作为二进制上传 GitHub。不要把 GitHub 的文字源冒充 PNG 原图已发布。

构建命令（从已有固定资产本地调用）：

    python build.py --base /path/to/b4-fixed-local-base.png --font /path/to/LongCang-Regular.ttf --approved-b9 /path/to/lezi-bluetooth-B9-v1.png --out /path/to/lezi-bluetooth-B10-v1.png

源程序核验来源摘要、批准 B9 精确重合成、画布尺寸、像素保护区和候选 PNG 的 SHA。源程序回传已复读；GitHub 上的程序尚未在独立机器重新执行，不能声称跨机器重现已验收。

## 范围边界

仅供用户具体审批一张静态图。蓝牙双机、真实切屏、交互、屏幕适配、APK、游戏代码与主线合并均未验证。评分冻结，NET 暂停。既有批准及首页/V4 例外不变。
