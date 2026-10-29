# 主线已提交房间输出与同步修复｜2026-10-29

已接收混乱线具体探针并实际复现、修复H11 A到期拒绝后的状态不同步。[草稿PR20](https://github.com/aaaycc931-droid/jieqi-engine/pull/20)，代码`8161c348abeba3a99fa5a5b514252e69218f28fd`，基于PR19，未合并。

原CH06/PR14 seed476 H15红/H11黑，合法招募0/1，真实32棋房间：红1在5000行动后开始黑时钟，黑1在10000完成，A继承实际截止65000。旧A在截止或+1到达时，房主已自动放弃A/轮到红方，旧黑方请求抛WRONG_TURN；旧生产WebView只发error，来宾/房主渲染端仍持黑方/A。不是把独立H11的70000时钟套入本例。

本轮仅在`web/app.ts`修正消费者：行动接受或拒绝后发布既有的最新已提交房间；拒绝时原error message/请求编号保留，再发snapshot，房主本地拒绝也同步。同步发送/编码失败独立提示，不把已接受行动改报规则拒绝或再次提交。v2及原payload形状、公开权限保持，未发中间原子帧、未改引擎玩法/门禁或UI素材。

实际生产消息函数通过原样父版片段与当前源码执行，真实BluetoothHostRoom负责全部房间/规则；原生send和最终渲染端为记录替身。两合法私密世界×截止-1/截止/+1共6对旧新比较，完整权威/事件/RNG和重试后结果一致；仅迟到拒绝的error-only输出变为error→最新snapshot，接收端红方/无A。三个时点两私密世界的snapshot/error原字节及交给渲染端数据一致，合法公开红炮不遮蔽，私密训练目标/进度/失败不泄露。真实radio、完整DOM和全部原生失败路径**未测**；Java IOException发transport-error仅读源，不能拿同步替身测试冒充真机。

| 额外取证 | 结果 |
|---|---:|
| 原半混乱完整提交返回 | 110公共JSON＋220玩家JSON |
| 原正常主行动真实历史消息 | 100 |
| 原IN_CHECK服务端错误 | 4，客户端送达未证 |
| 新的精确原载荷服务端重传 | 106，duplicate/权威/历史/时钟核对通过 |
| 新的重复拒绝服务端控制 | 4，保持原权威 |

后110个探针明确是新增研究对照，不是原110或PD-S35/DS-S12全套自然客户端刺激。BluetoothHostRoom仍拒绝half_chaos/xiangqi；views返回不含duplicate ACK，错误线上仍只有message。完整56义务、原64正式验收、实际设备送达仍0。

新增20检查，58相关文件895项及另2文件50项Web静态通过、0失败。4个未改二进制素材检查明确未跑；37个src/web模块以生产脚本同样转换通过，没有全资产打包、APK、全TypeScript类型、真机或独立QA。17引擎路径逐内容/blob远端复读，595个其他旧blob（全部游戏业务源码和UI素材）保持。

来源读于`825dcb42aab686096e3a7111b9e4ac7c72f1d9b9`：HC54 findings/owner_requests/边界及r53/r54回传、混乱完整到期/隐私探针、普通完整PR18复核和选定回执；普通另一份信息图只读回传摘要，未声称全文采用。各线较新并发工作稿和回执保持，PR20实际采用待其线自行登记。

新的[所有者原始对照包](https://chatgpt.com/library?file_id=libfile_4a1e0b2482c881919d463fd63342a58b&account_id=personal)为`lezi-main-output-channel-evidence-20261029.zip`，73906字节，SHA256 `0749c43939d82774e08d913ddf4eb7b766843b06fa807679651b364726d35eb6`；源JSONL 3847646字节，SHA256 `df0d02bcba9282dd5e19fa435ecad280d68d9d5d9ccf05b062946ba7cd90d606`。ZIP已逐成员复读，私密权威、记录用wire回执、服务端返回分目录；不公开raw或覆盖旧HC56/NP32包。

下一`MAIN-BLUETOOTH-RECEIPT-CORRELATION-20261029`：核来宾pendingAction与错误请求号/重复延迟snapshot的实际关系，先以已有v2与真实来源做离线复现，不能靠任意快照推定某请求已确认。普通NG11、暗子完整来源、三态消费者和其他缺口保持。评分冻结、NET暂停，三线/山风/UI素材/H03保护，无合并/部署/重复APK。本阶段不自动关闭对话。

[引擎说明](https://github.com/aaaycc931-droid/jieqi-engine/blob/8161c348abeba3a99fa5a5b514252e69218f28fd/docs/COMMITTED_OUTPUT_CHANNEL_20261029.md)、[进度](COMMITTED_OUTPUT_PROGRESS.json)、[保护核对](COMMITTED_OUTPUT_VALIDATION.json)、[发布复读](COMMITTED_OUTPUT_PUBLICATION_VERIFICATION.json)保存完整边界与复现入口。
