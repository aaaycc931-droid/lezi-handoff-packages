# 当前来源优先级与历史保护

1. 用户本轮收束要求及明确范围；根目录CURRENT_STATE、MODE_SYNC、PENDING_ITEMS描述本轮状态。
2. rules/shared/02_CURRENT_HEROES、共享H10 F1/H15增量、各模式CURRENT_RULES和CONFIRMED_DECISIONS描述当前设计。普通专属修改不能扩展到另两个模式。
3. rules/lezi-adjudication-reference-decision-2026-10-12.json v1.22是确认账本，GC01—04已经确认普通明子；暗子公开信息提案仍待批准。v1.22只更新本次收束状态，规则对象与v1.21保持一致。
4. 完整性审查及恢复来源随audit/integrity可访问；H15原09专稿恢复，并保留后续覆盖与未决项。摘要缺失不等于废止，来源缺失不等于未批准；不把所有旧规则整份复活。
5. inputs中的收到ZIP、audit/integrity中的旧快照、history中的原状态均只读追溯。旧GC“未批准”、旧H03 B候选、H10自由指定S1、H10后续任意回合首发、H15自动开局/死亡重训、HC A1均不得覆盖当前确认。内层START要求继续也不能覆盖本轮“总体收束、停止推进”。
6. scoring、evidence、runtime记录限定实际运行；14b的9/9、8/8与111相关回归不等于完整模式或全量验收。573全量和web build来自旧f1c提交，没有14b全量重跑。本轮新运行次数0，未运行规格不记PASS。
7. UI批准以ui/APPROVAL_REGISTER及inputs原图字节为准；公开交接已发布属于既有事件，本轮未更新公开规则或发布本总包。NET保持暂停。当前分发、接收、采用、代码实现、运行验收分别登记。

读取者按本次任务选取最小充分材料；维护/审计需要的原文必须实际读取，不以索引标题存在冒充语义完整。恢复另一个项目、人物或成长系统不得使用本棋项目状态替代其事实源。
