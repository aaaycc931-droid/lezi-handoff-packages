# 半混乱r60：F1修复接收与真实房主适配审查

2026-11-13，Asia/Shanghai。源交接 `4bd603113914ff8c4fd59cb8fc9c497f347fdb62`，任务 `MAIN-HC-F1-FIX-AND-HOST-ADAPTER-REVIEW-20261113`。协作核验L3，工作稿2026-10-23.v0.18／正式基线1.8.0；本轮适用来源、权限、局限与并发保护范围见READ_RECEIPTS.f1_fix_host_review_20261113。

两段任务均已完成。F1原缺字段问题在固定PR24修复上得到本线定向验证；新PR26已完成有界源码审查，没有新确认缺陷。两者不是同一验证层级。

## 实际执行与来源

| 项目 | 结果 | 边界 |
|---|---|---|
| PR24修复 `6ba35636ecf5c69203225149a7b746893299b39b` | 4项新控制通过、0失败：完整scope正例、缺authorityId、缺matchEpoch、缺query.scope | 原两反例各核构造拒绝及查询invalid，查询不改authority；不覆盖原观察结果 |
| PR26 `e88a5a6bce6732a29e887b10636c827cd3f2eab5` | host/ledger/新测试/说明全文核对，7个manifest项身份匹配 | 本线未运行PR26测试，34通过仅主线公开执行报告 |
| 主线r59接收 | 主线已全文读并独立复现两变体后修复 | 本线r60是否已被主线读取仍UNKNOWN |

本线研究成果：[提交 02cbe7e](https://github.com/aaaycc931-droid/jieqi-engine/commit/02cbe7e0fc77af997799ebe98cb00ef31c1ba7c7)，三文件均已发布读回一致：

- `scripts/research/hc-result-f1-fix-review.ts`
- `review/hc-result-evidence/F1_FIX_RESULTS_20261113.json`
- `review/hc-result-evidence/HOST_ADAPTER_REVIEW_20261113.md`（完整源码审查表和局限记录）

两份外部依赖均固定为干净只读检出，无复制/合并到本线研究分支；原`2204ef6`及r59反例仍在历史和当前文件中。PR24/26读取时均open draft、未合并。任务中的短报告名已定位为engine `docs/research/MAIN_RESULT_SCOPE_FIX_20261113.md`；不是handoff主线目录中的同名文件。

## 采用结论

实际BluetoothHostRoom用同一owner持有room和ledger，tracked/legacy共用dispatch；先构造新账本再同步发布room＋结果，后执行输出。默认未启用，调用协议和Web/native入口尚未接入。保留真实两次时钟，advance完整操作已有重入保护；仅hero/resign处置有明确accepted/rejected映射，其余与未知异常保持边界。

断连、重连和成功再战让当前owner停止新的tracked调用；旧scope旧记录仍只能是原本机owner内的历史查询。不能据此证明重连身份。actor与attempt ID、完整规范化JSON载荷分别绑定，FIFO淘汰/预算容不下仍unknown，ID淘汰后不得复用是调用者前提，不是持久去重方案。PR26允许scope附带JSON额外键，PR24修复要求恰好三个键；两者均要求三个身份字段存在，本轮不将差异误报为F1复发。

没有找到需要另加实验的具体新缺陷假设，因此按任务停止扩样；此结论不是“没有其他缺陷”的证明。未重跑旧13/29/32/34/935、110/56矩阵；未改生产/主线研究实现/协议/其他工作线。评分冻结、NET暂停、featuresReady=false；原56完整、64正式、实际半混乱客户端送达不增加。

## 下一步

本包无剩余独立段。下一等待主线具体host/wire/调用合同/生命周期差分或可复现新问题，再核受影响边界；不循环自审或自动轮询。发布前看到混乱C5新回传，仅核变更路径并保留并发，没有冒充完整读取或接入采用。r60发布不代填主线接收。
