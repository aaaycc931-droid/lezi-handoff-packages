---
schema: repository_cleanup_inventory.v1
repository: aaaycc931-droid/lezi-handoff-packages
observed_source_commit: cc4c45ad9dcb46d2f04809d38dcddebf1a254054
observed_at_local: 2026-10-15T19:57:26+08:00
phase: inventory_and_targeted_dependency_review_only
current_tree_inventory_complete: true
full_history_storage_measured: false
full_semantic_deletability_review_complete: false
ready_to_delete_candidates: 0
files_deleted: 0
history_rewritten: false
---

# 保守清理盘点与下一步

用户于2026-10-15同意先盘点占用／依赖、保留可恢复依据、再处理确证无用的内容。本次只完成当前树盘点和有范围的依赖检查，不把相同内容、旧日期或未出现在某任务清单等同于无用。没有执行删除、Git历史重写或后台自动清理。

## 核对范围和计量

| 指标 | 本次结果 |
|---|---|
| 当前文件数 | 461 |
| 各路径文件字节之和 | 50,319,622 bytes（50.320 MB，十进制） |
| 当前唯一Git文件对象数 | 418 |
| 当前唯一对象未压缩字节之和 | 49,629,757 bytes（49.630 MB，十进制） |
| 相同对象的多路径组数 | 33 |
| 多路径重复的逻辑字节 | 689,865 bytes（0.690 MB，十进制） |

以上是固定源提交当前文件树的统计，不是GitHub服务器实际占用、完整历史体积、网络传输量或预计可回收空间。相同Git对象在多个路径出现，不代表再次存储一份对象；删除其中路径不能直接把逻辑重复字节当作物理节省。没有克隆全部历史或测量重写后的大小。

来源范围：完整递归Git树未截断；本地缓存只在Git blob身份与该远端对象精确一致时用于程序化文本引用扫描。已扫描78份可匹配文本，还有318份文本未纳入该扫描。此扫描只发现可识别引用，不是全文语义审查，也不能证明未发现引用的文件没有用途。日常工作不必读取本盘点全文。

## 处置清单

| 对象 | 观察与作用 | 当前处置 |
|---|---|---|
| assets/ui素材库 | 136个资产，45,218,112 bytes（45.218 MB，十进制）；目录身份均与索引Git对象及字节匹配 | 保留；没有为盘点重新下载／编码图片 |
| B6任务依赖 | 105个旧路径别名复用75个资产，共21,425,633 bytes（21.426 MB，十进制） | 保留；本次不新增图稿或重跑像素／设备验收 |
| 普通线当前稿／returns／sources副本 | 当前字节相同，但分别承担工作稿和原始返回／来源身份；PUBLISHED_FILES覆盖相应路径 | 暂留；合并路径属于有依赖的结构调整，不当作直接删垃圾 |
| 共享规则的相同来源副本 | 有审计／历史／原始来源职责，不能从相同对象推断这些角色无用 | 暂留；未完成逐项语义依赖核查 |
| 不在当前任务清单的2个小脚本 | 共3,159 bytes：scripts/recompose-approved.cjs与scripts/verify-manifest.py；已读脚本，分别用于批准源重合成和原包校验，素材索引仍有别名及历史来源 | 暂留；未运行，不把不在任务清单视为无用途；收益很小 |
| archive/INDEX.json指向的旧提交 | 仍依赖52002b3762bd948a134c67cfbc99427035790eba恢复旧目录；素材fallback也引用该提交 | 历史清理前必须处理依赖，当前不具备清除该恢复链的依据 |

相同对象的主要多路径组：

| 路径数 | 每份逻辑字节 | 部分路径 | 判断 |
|---|---|---|---|
| 3 | 108,616 | worklines/standard/returns/standard/LEZI_STD_DESIGN_03_WORKING_20261014.md；worklines/standard/sources/standard/LEZI_STD_DESIGN_03_WORKING_20261014.md；worklines/standard/work/LEZI_STD_DESIGN_03_WORKING_20261014.md | 暂留；相同对象仍可能承担不同来源／工作职责 |
| 7 | 17,178 | worklines/standard/rules/shared/03_CURRENT_MUTATIONS.md；worklines/standard/sources/standard/inherited_dispatch/baseline/audit/integrity/current/03_CURRENT_MUTATIONS.md；worklines/standard/sources/standard/inherited_dispatch/baseline/audit/integrity/evidence/dispatched_reference/03_CURRENT_MUTATIONS.md；另4个来源路径 | 暂留；相同对象仍可能承担不同来源／工作职责 |
| 2 | 101,789 | assets/ui/6b56cfad53eddaaa820d0d8346c02449ed3cdfe868e07938517b55e2fe448469.json；worklines/ui/APPROVAL_REGISTER.json | 暂留；相同对象仍可能承担不同来源／工作职责 |
| 3 | 30,719 | worklines/standard/sources/standard/inherited_dispatch/baseline/audit/integrity/current/01_CURRENT_RULES.md；worklines/standard/sources/standard/inherited_dispatch/baseline/audit/integrity/evidence/dispatched_reference/01_CURRENT_RULES.md；worklines/standard/sources/standard/inherited_dispatch/baseline/audit/integrity/evidence/pinned_repo/handoff/current/01_CURRENT_RULES.md | 暂留；相同对象仍可能承担不同来源／工作职责 |
| 2 | 36,313 | worklines/standard/sources/standard/inherited_dispatch/baseline/audit/integrity/evidence/dispatched_reference/02_CURRENT_HEROES.md；worklines/standard/sources/standard/inherited_dispatch/baseline/audit/integrity/evidence/pinned_repo/handoff/current/02_CURRENT_HEROES.md | 暂留；相同对象仍可能承担不同来源／工作职责 |
| 2 | 35,456 | worklines/standard/sources/standard/inherited_dispatch/baseline/audit/integrity/evidence/pinned_repo/handoff/current/08_SCORE_LEDGER.md；worklines/standard/sources/standard/inherited_dispatch/baseline/audit/integrity/evidence/pinned_repo/rules/transferred/2026-10-07-r7-clean/08_SCORE_LEDGER.md | 暂留；相同对象仍可能承担不同来源／工作职责 |

普通线文件清单当前包含288项。本次核对其路径覆盖与候选角色，没有执行全部旧来源的语义去重审查。CURRENT_ALL任务引用134个资产；其余两个辅助脚本的明确用途已单独说明，不登记为可删。

## 历史清理条件与当前缺口

尚未测量完整历史对象体积与预计回收收益；仍有明确固定提交引用；本次没有验证仓库外备份恢复，也没有其他账号真实读取／采用／写回回执。因此当前历史清理不进入执行。未来只围绕有收益的目标路径做依赖迁移、独立副本演练与恢复核验；协调正在进行的写回，保护其他对话未回传成果。

主线／半混乱完整资料尚未在此展开，以CURRENT_HANDOFF真实状态为准。它影响对应工作线接续的完整性，不意味着其他已展开工作线不能继续，也不阻断无关低风险临时文件整理。

## 下一项可执行动作

从已展开的普通线固定入口完成一次真实接续：接收对话实际读当前协作索引与任务所需完整源，正确识别M04待决、冻结／暂停和下一动作，然后只记录自己真实读取／采用的范围。具备写权限时在自己的READ_RECEIPTS.json写回源提交、实际文件／章节及剩余项，由主线复读；无写权限就明确报告具体阻断，不预填成功。

此为正常接续的有限验证，不启动正式G-2，不批准M04、不解冻评分或恢复NET。先用真实结果判断维护成本和准确性，再推进具体清理候选，不为验证清理而修改业务事实。

## 盘点与删除决定的边界

目前“确证可立即删除”的候选为0，表示本次证据尚不足以执行删除，不表示已经证明全库没有冗余。本记录本身不是删除指令。新候选需有具体路径、内容身份、替代来源、依赖检查、预期收益及恢复方法；拿不准的暂留。普通可逆目录整理与历史重写按各自实际影响判断，不把后者自动包含在日常整理中。

方法参考：[Git对象与未变文件复用](https://git-scm.com/book/en/v2/Getting-Started-What-is-Git%3F)、[GitHub历史重写的影响](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)、[仓库备份与恢复](https://docs.github.com/en/repositories/archiving-a-github-repository/backing-up-a-repository)。技术参考不证明本仓库已完成实际恢复演练。
