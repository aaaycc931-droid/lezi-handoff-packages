# B7-v1｜首次连接失败／重试（待用户审批）

继承已批准B6-v1的固定底层、原852×1846画幅、纸纹、山水、标题、返回箭头、墨框和页尾。只改变状态文字、重试按钮文字及返回大厅入口。使用未修改Long Cang字形路径与独立透明图层，不整图生成、不缩放、不锐化、不提亮。

本稿为加入方第一次连接失败。朋友的手机是示例设备名。重新连接保留原目标；返回执行cancelBluetoothSetup回初始蓝牙大厅；顶部箭头回主菜单。source-behavior-excerpts.json保存实际源码摘录；不等同于对局中断线重连或权限拒绝状态。

相对批准B6有17145像素变化，限定矩形与实际文字alpha交集之外变化0；颜色配置一致。B4/B5源层重合成差异0。历史B2文字底层估计沿用，没有新增背景估计。

批准状态以固定APPROVAL_REGISTER.json为准。本候选待用户明确审批；静态检查、GitHub写入和源码保存均不等于批准。评分冻结、NET暂停，未修改产品代码，未运行真实双机，未构建APK或部署。

在worklines/ui目录运行restore_task.py --task B7 --target <工作目录>，恢复105项历史基线和B6/B7独立源文件。历史基线状态快照不覆盖固定审批登记。以下命令只在恢复的工作目录运行：

```bash
node work/B6-v1/compose.cjs baseline
python3 work/B7-v1/export-glyphs.py --baseline baseline
node work/B7-v1/compose.cjs baseline work/B6-v1
python3 baseline/sources/B4-v1/verify_pixel_diff.py work/B6-v1/lezi-bluetooth-B6-v1.png work/B7-v1/lezi-bluetooth-B7-v1.png --regions work/B7-v1/evidence/regions.json --mask work/B7-v1/evidence/allowed-mask.png --expected-source-sha256 7659f9b0e3d33184d9d4a2cdcac7aa8c3ebedce9c5058fd28191135bc1e0d945
```

需要Node/sharp（CODEX_PRIMARY_RUNTIME_NODE_MODULES）与Python fontTools/Pillow。SVG每组文字可独立编辑。下一动作：展示本图由用户审批或提出修改。
