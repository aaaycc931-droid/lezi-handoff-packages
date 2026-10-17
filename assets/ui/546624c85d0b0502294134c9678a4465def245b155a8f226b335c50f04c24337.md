# B8-v1｜蓝牙权限未允许（可再次授权）

本张为待用户审批的静态候选。继承B7批准母版的原852×1846画幅、纸纹、山水、标题、返回箭头、蓝色墨框和页尾，使用未修改Long Cang真实字形。只替换状态/解释/主按钮文字并移除连接会话的返回入口；不整图生成、不缩放、不锐化、不提亮，不做新背景估计。

状态限定：Android蓝牙可用且已开启，权限未允许，未被永久拒绝，无连接会话。隐藏创建/加入、设备列表及会话面板。允许蓝牙权限调用requestPermission；授权成功后按真实可用状态显示创建/加入，不自动连接。顶部箭头返回主菜单。永久拒绝及系统设置入口属于后续独立图稿，不混入本张。source-behavior-excerpts.json保存实际app.ts/index.html来源与原始按钮名称。这里是静态映射，没有实现或验收真实系统弹窗。

相对批准B7改变35352像素，实际文字alpha与限定区域交集之外改变0；色彩配置一致。B4/B5源层重合成差异0。105项基线和29项既有工作文件身份匹配。源底层继承历史B2旧字遮挡区估计；不宣称这些区域恢复为最初未遮挡纸纹。

批准状态由固定APPROVAL_REGISTER.json控制；本目录生成时快照为pending_user_review。B7/B6及其他已有批准继续有效，首页/V4字体例外和撤回记录保留。评分冻结、NET暂停；真实蓝牙交互、双机、屏幕适配、产品接入、APK与部署未验收。

在worklines/ui运行restore_task.py --task B8 --target <工作目录>，可从已有资产与新增源文件恢复。只在工作副本内合成：

```bash
python3 work/B8-v1/export-glyphs.py --baseline baseline
node work/B8-v1/compose.cjs baseline work/B7-v1
python3 baseline/sources/B4-v1/verify_pixel_diff.py work/B7-v1/lezi-bluetooth-B7-v1.png work/B8-v1/lezi-bluetooth-B8-v1.png --regions work/B8-v1/evidence/regions.json --mask work/B8-v1/evidence/allowed-mask.png --expected-source-sha256 1ab53dbaec7936e720835425ec117e431a2bbf5385410ced7d898d222a03f74a
```

依赖Node/sharp（CODEX_PRIMARY_RUNTIME_NODE_MODULES）和Python fontTools/Pillow。SVG的状态、两行解释和按钮文字为四个独立命名组，参数可编辑。下一动作：展示本张实际候选，由用户具体审批或提出修改。
