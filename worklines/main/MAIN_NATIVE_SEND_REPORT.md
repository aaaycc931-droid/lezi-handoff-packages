# 原生发送结果核算｜2026-10-30

[草稿PR22](https://github.com/aaaycc931-droid/jieqi-engine/pull/22)，代码`71145df45ad17215a3731e53150b6728e079e375`，基于PR21，未合并。可选本机sendChecked区分not_sent、written、unknown，保留旧void send和v2线上格式。written只表本地write/newLine/flush返回；unknown可能已部分/完整进入权威。未知行动不退回旧send、不自动重试/发ping，额外同编号pong也不解除其未知等待。已知写前失败才直接清该等待；ping失败保留等待。

完整生产Java两类的当前版本和PR21父版均编译执行。明确writer故障在旧版产生首写失败后再ping、半行后拼ping；本版隔离失败当前writer/socket，旧writer反射替换控制不会误关闭新writer。共16当前JVM检查及3父版故障控制通过。Android/org.json/writer/UI是最小替身，不是Android SDK/JNI/真实解析器/Handler/radio验证；替换writer控制不冒充自然可达竞态。

8组行动和3组ping边界将精确JVM输入、返回和完整writer行接生产Web函数及真实jieqi房间，实际桥回调脚本解码送实际原生事件监听器。flush故障完整行动可已被房主接受，而本机仍unknown；零字节/半行则无完整行动，二者均不自动重放。原断连生命周期会清UI等待、继续锁断连操作，重连不补交，**不代表旧行动已接受/拒绝**。旧桥缺少sendChecked时原兼容路线仍无写入结果，不能追溯宣称旧APK已修。

21项新增Node检查、60相关文件最终935串行、另50现有Web静态、16JVM/3父版控制通过；37模块生产转换通过。首轮全量934/935，未改评分隔离子进程invalid_policy_execution；21项孤立与完整935再跑通过，根因未证，16评分源/执行预算不改。4旧二进制检查、全资产/全类型/Android SDK/JNI/radio/设备/完整DOM/独立QA未验。19引擎路径逐内容/blob远端复读，622其他旧blob保持。

下一`MAIN-BLUETOOTH-UNKNOWN-RESULT-RECONCILIATION-20261030`：先核真实可达的跨断连顺序与各动作幂等/冲突来源，再给新旧端兼容的正式结果核对。written/pong/重连/新snapshot都不是旧请求接受ACK，未知行动不自动补交。半混乱/普通门禁、原56/64正式验收及普通NG11/暗子来源/三态消费者等缺口保持。

公开证据只有明确固定fixture命令/本机状态/比较元数据，无私密权威包或新ZIP，旧owner身份不变。本轮未新读三线采用回传，TASK只加输入，真实采用由其线写。三线/英雄/UI/H03保护，评分冻结、NET暂停，无合并/部署/APK，本阶段不自动关闭对话。

[引擎说明](https://github.com/aaaycc931-droid/jieqi-engine/blob/71145df45ad17215a3731e53150b6728e079e375/docs/BLUETOOTH_SEND_ACCOUNTING_20261030.md) · [JVM运行](https://github.com/aaaycc931-droid/jieqi-engine/blob/71145df45ad17215a3731e53150b6728e079e375/review/native-send-accounting/JVM_RESULTS_20261030.json) · [Web边界](https://github.com/aaaycc931-droid/jieqi-engine/blob/71145df45ad17215a3731e53150b6728e079e375/review/native-send-accounting/RESULTS_20261030.json) · [发布复读](NATIVE_SEND_PUBLICATION_VERIFICATION.json)
