# B6-v1｜连接中，设备名与取消

本稿是待审批静态候选。用户2026-10-16T12:30:15+08:00要求从B6继续，不代表批准本图。B5-v1及B1/B2/S1/B3/B4批准继续有效；首页/V4原版字体例外、H1/V4撤回继续有效。评分冻结，NET暂停。

画面显示“正在连接”“对方设备：朋友的手机”，主按钮为“取消连接”。设备名为示例。延续已批准B3等待页的状态/设备名/取消按钮布局，使用未修改Long Cang真实字形。进入连接中状态后移除B4设备选择、地址、重新检测、系统设置和返回链接；取消回到蓝牙初始页。顶部既有返回箭头取消连接后回主菜单。此处只有静态设计，未实现或验收真实操作。

从B4固定底层与新独立字层合成，原852×1846尺寸与比例保留。标题、返回箭头、纸纹、山水、主按钮墨框和页尾像素受保护。B4/B5源层重合成均差异0；相对B4有37576像素变化，真实文字/控件alpha蒙版与五个范围外差异0。实际检查了整张图及文字/按钮细节。历史B2旧字下补底仍为估计，本轮未做新补底、重绘、缩放、锐化或提亮。

SOURCE_DEPENDENCIES.json引用原TASKS.B6的105项来源，并列出本候选直接使用的11个既有对象；字体、许可、母版和原源层复用assets/ui已有Git对象，不重复上传。layers/中的SVG包含三个独立命名文字组，PNG为其透明合成层；parameters.json可编辑文本与布局。source-behavior-excerpts.json只读核对了历史UI分支的连接/取消/返回函数，不证明当前生产运行。

在worklines/ui运行restore_task.py --task B6 --target <工作目录>，将冻结来源放baseline/、本候选放work/B6-v1/。已有不同字节的本地文件会保留并报冲突。然后在work/B6-v1/运行：

```bash
python3 export-glyphs.py --baseline ../../baseline
node compose.cjs ../../baseline
python3 ../../baseline/sources/B4-v1/verify_pixel_diff.py ../../baseline/images/lezi-bluetooth-B4-v1.png lezi-bluetooth-B6-v1.png --regions evidence/regions.json --mask evidence/allowed-mask.png --expected-source-sha256 7c11e53aaa7c76b04e77ca60b59780ca4b61dfc251e541fea9df21a3ce38f72c --out evidence/pixel-check.json
```

合成使用Node sharp（CODEX_PRIMARY_RUNTIME_NODE_MODULES）及Python fontTools/Pillow。源脚本只在候选副本运行，禁止覆盖baseline或历史源。批准状态由固定审批登记控制，候选内记录是生成时快照。

唯一下一动作：展示本张B6-v1并等待用户针对该候选明确审批或指出修改。长名、多设备、动效、设备适配、取消竞态、真实蓝牙双机、产品接入均未验收；本轮没有产品源码修改、APK或部署。
