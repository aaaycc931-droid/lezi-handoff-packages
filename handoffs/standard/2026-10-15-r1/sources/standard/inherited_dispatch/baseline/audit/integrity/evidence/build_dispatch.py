from pathlib import Path
import json, shutil, hashlib, zipfile

ROOT = Path('/workspace/scratch/a57cd429fd9e')
SRC = ROOT / 'closeout'
OUT = ROOT / 'deliverables'
WORK = ROOT / 'dispatch_build'
OUT.mkdir(exist_ok=True)
COMMIT = '14b306fe1cf9f459ef54e22d9ffa4ce2e83db510'

def dump(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2)+'\n')

def copy_file(base, source, target=None):
    dest = base / (target or source)
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(SRC/source, dest)

common = '''# 乐子象棋｜2026-10-13分发

主要读取者：接续AI。任务授权来自本次主线对话：用户确认在现有验收未全部完成时，优先继续剩余英雄与畸变适配设计，保留已有验收进度。此前主线还建议独立UI从B2字体断点接续；UI包用于用户转交后启动。

本包已准备，尚未由主线发送或在外部对话启动。转交对应包并要求执行START.txt后，接续AI只恢复该工作线。主线裁判仍由主对话负责；NET未恢复。没有规则新增、候选自动批准、仓库修改、合并、部署或评分解冻。

读取顺序：START.txt → DISPATCH_STATE.json → SOURCE_PRIORITY.md → inherited/CURRENT_STATE.json → reference/X_Collaboration_System.md按AI_READ_ORDER → 本线原设计交接/最新回传 → 任务所需具体规则。
当前协作系统v1.8.0。报告自己实际读取范围，不复用旧AI阅读收据；个人系统的历史次数不是本项目实测次数。

设计确认、代码实现、局部运行通过、完整模式验收、正式评分是不同状态，须分别记录。新增适配必须列明基础差异、原规则来源、真实规则差分、候选、边界与确认状态。未讨论的条目先核对来源，不能默认全部沿用或全部未适配。

评分继续冻结：q/H/I/B/J=null、经验n=0、featuresReady=false。旧573项全量测试和web build属于f1c01585；14b没有全量重跑。不得用9/9、8/8限定结果宣称全英雄或完整对局通过。

私有运行归档只给用户和可信审计AI，不给对弈策略进程；P3协作文档与私有归档不得自动公开。文件转交不等于GitHub发布。代码工作开始前只读核对远端差分；离线包76个依赖源文件不是完整Git检出。

阶段完成、用户要求收束或出现需主线协调的共享冲突时回传；不要求每条回复造包。需要确认时一次呈现一个关键候选，未答复不算同意；可先推进不依赖该项的工作。不得擅自修改共享规则、另一模式或实现未确认候选。
'''

priority = '''# 来源与新旧状态

1. 当前用户明确指令最高；本次只调整任务优先级，没有批准H03、H11×H15或GC-01～GC-04。
2. START.txt与DISPATCH_STATE.json定义本轮分发范围；inherited/CURRENT_STATE.json保留收到的项目快照，不能以任务恢复推断实现资格变化。
3. rules/lezi-adjudication-reference-decision-2026-10-12.json记录裁判确认与候选。三模式60无吃子、200总长、5次重复、连续6己方正式回合施压及第7禁着等已确认，但独立裁判尚未实现；有效捉GC四项尚未批准。
4. design/原适配交接保存逐项设计批准、候选与跨模式差分；其中2026-10-09实现/测试未完成描述是历史，已由2026-10-12实际支线回传在限定范围更新，不能恢复旧阻断。
5. reference/product_20261009/是通用英雄/畸变基线快照；其中模式文件的旧待办不覆盖其后逐项确认。H10流共享修正已确认；其他模式专属结论不可互相覆盖。
6. scoring/原件与runtime/记录实际限定验收。普通9/9、半混乱8/8继承，不默认重复；未测字段不回填。
7. UI以ui/审批登记和原回传的实际图片为准；设计批准不等于运行验收。

若来源存在冲突，报告具体段落、时间、来源与影响，不用代码当前行为倒推设计批准。确需解决的新规则提交用户确认；跨模式共享语义由主线协调。
'''

return_contract = {
    'schema':'lezi.dispatch_return_contract.v1',
    'when':['阶段完成','共享规则或接口阻断','用户要求收束'],
    'required':['本线ID与模式ID','实际阅读来源和范围','已继承且未重做的成果','本轮新增设计与用户确认原话','候选/未确认/阻断的区别','设计确认/代码实现/运行验证分别记录','跨模式影响与主线协调问题','实际修改文件清单与提交（如有）','新测试命令/范围/结果及证据（如有）','下一步精确断点'],
    'scoring':'冻结；不得产生正式强度分数或经验样本资格',
    'private':'权威/玩家私有归档仅可信主线审计；策略不得读取',
    'manifest':'回传包包括sha256与字节清单；修改现有文档时保留来源及候选历史'
}

std = '''继续《乐子象棋》普通象棋工作线，执行NEXT-STD-DESIGN-02。本轮优先剩余英雄/畸变适配设计；已确认机制可同步补充验证，不以旧验收未全通过作为整体设计阻断。

先按00_READ_FIRST.md读取，激活X_Collaboration_System v1.8.0，显示协作门禁。核对MANIFEST.json。只负责standard_xiangqi，引擎ID=xiangqi。

从design/STANDARD_MAIN_DIALOGUE_HANDOFF.md的H03断点继续：普通防御方案B“首次越河获得防御”是未批准候选；先继承候选与反例，再提交具体适配审查。将帅铁甲需单独审查，不能自动扩展成免疫普通将军/将死。用户确认前不写成正式规则。

H01/H02/H11已经阶段性设计确认，不重新从头设计；继承scoring/standard/RETURN.json及CASE_MATRIX.json的14b、v0.3、9/9实际结果和12项人工案例，不重复相同重跑。普通H11标准开局复原、S1结束飞行/河道等专属确认不得套到半混乱。

建立剩余适配清单：H01–H21含里形态及H21互斥形态，M01–M08及D01宿命。按已确认/候选/待审/规则依赖/代码依赖/待运行逐项区分，先恢复已有结论而非重做全套矩阵。H03后优先无共享阻断的下一来源；每项检查触发、目标、效果、次数、冷却、占步、士象区域、隐藏信息、死亡与复原、终局及必要交叉。数值强度评分继续冻结，可做定性方向与反例分析。

补验收为第二优先：STD-FX-04/07/08/11/12/13/14等未测条目先核对规格和前置依赖；只测试已确认且依赖齐备的新增路径。若需实际运行，先解压runtime中的原包并读README；这是76依赖文件的限定源码，并非完整仓库。新的用例可在本线独立文件构造；不能擅自实现未确认能力或改共享引擎。无新增测试能力时完成可运行用例规格和明确主线依赖，不重复造旧通过证据。

主线尚在有效捉GC-01～GC-04审查；新裁判未实现。依赖裁判的设计边界明确待定，其他部分继续；H11×H15等不得自行批准。完整对局与正式评分仍冻结。源码修改需独立范围授权；本次先设计与已确认机制补验收，不自动扩大到产品实现、合并或部署。

阶段结果按RETURN_CONTRACT.json回传主线；不自动发送跨对话消息。
'''
hc = '''继续《乐子象棋》半混乱揭棋工作线，执行NEXT-HC-DESIGN-02。本轮优先剩余英雄/畸变适配设计；已确认机制可同步补充验证，不以旧验收未全通过作为整体设计阻断。

先按00_READ_FIRST.md读取，激活X_Collaboration_System v1.8.0，显示协作门禁。核对MANIFEST.json。只负责half_chaos_jieqi，引擎ID=half_chaos。

从design/HALF_CHAOS_HANDOFF.md第4节H11×H15继续：方案A“洗牌保留飞行”与方案B均未批准。审查空层/地面层分配、公开身份与暗置复原、未毕业训练、死亡恢复、重训、飞行寿命及A/B窗口时序，先给具体候选和反例，等用户逐项确认。普通象棋H11已确认的S1地面复原不能移植为半混乱结论。

继承半混乱H11分阵营洗牌、M07独立50/50及H11解锁M07、H11保持风影绑定等设计确认，不重问；它们的完整运行联动未因设计确认自动通过。继承H11-B计数/时钟确认及14b v0.3实际8/8结果、26项人工案例；不沿用缺确认/Node22旧阻断，不重复同一8/8回传。旧41字段的null不可用其他场景结果回填。

建立剩余适配清单：H01–H21含里形态及H21互斥形态，M01–M08及D01宿命。先恢复已确认/候选/待审/规则依赖/代码依赖/待运行状态；不能把所有未运行项目都说成规则未确认。H11×H15后优先其他可独立设计来源；检查暗子位置控制与真实身份阵营、分阵营暗池、揭示、目标、次数、冷却、占步、秘密字段、死亡/复原及必要交叉。普通象棋与原揭棋专属规则不得覆盖本线。正式强度评分继续冻结，可做定性方向和反例分析。

补验收为第二优先：先筛选HC-F04未覆盖字段及HC-F05地面路径，确认来源与合法前缀后才补测；M07/刷新前秘密读取、H11×H15等未就绪项按具体依赖保持阻断。实际运行先解压runtime原包并读README，其76限定依赖文件不是完整Git仓库。可在本线独立文件构造已确认机制用例；不能擅自实现未确认能力或修改共享引擎。无新增测试能力时完成用例规格与主线依赖，不重造已通过证据。

主线新裁判尚未实现，GC-01～GC-04未批准；受其影响的边界单列待定，继续其他独立设计。正式评分、完整对局资格和featuresReady继续冻结。产品实现、合并、部署不自动恢复。

阶段结果按RETURN_CONTRACT.json回传主线；不自动发送跨对话消息。
'''
ui = '''继续《乐子象棋》独立UI设计工作线，执行NEXT-UI-B2-20261013。本包供用户转交后恢复UI，不代表已在外部对话自动启动。

先按00_READ_FIRST.md读取，激活X_Collaboration_System v1.8.0并显示门禁，核对MANIFEST.json。解压trusted_returns/UI/lezi-ui-stage-return-2026-10-12.zip，读原回传根目录状态/审批/待办，实际查看批准与被否定的图片，再从B2字体接续。若执行完整协作文档交接，实际阅读全文；不得把前AI收据当自己的阅读。

UI-001已完成，不重复。首页/V4、S1-v2.1、B1-v1沿用；B2-v1布局/内容/状态已批准，字体未定稿；B2-v2未批准、B2-v3被否定。真实字形方法获认可不等于AR PL UKai CN字体获批准。AI审美诊断仍是待验证判断，不冒充用户已确认偏好。

第一任务：同一张B2图内进行字体审美定位和局部修订，每次展示一张实际待审图，简述相对基线的变化并等待用户审批。保留未指定背景、边框、返回和布局；字体候选不自动推广到其他批准页面。工具无法保证局部保真时先说明能力边界，不能以局部修改名义重绘全页。对现有原图的编辑优先保真方式，禁止重复生成已经批准的整页来替代资产保留。

图稿批准、动效实播、运行交互、字体/触控适配和双机蓝牙验收分开记录。不得引用主线P0结果作为UI验收。新规则相关提示/文案与交互先登记依赖，待主线确认后再落实，不把60/200/5裁判显示成已接入。

生产代码尚未接入这些静态批准。设计确认后的实现需用户在UI线明确指定范围，并使用独立UI分支；不自动恢复APK、联网、微信上线、部署或main合并。正式评分仍冻结。

阶段完成、规则/接口跨线冲突或用户收束时按RETURN_CONTRACT.json回传主线，不自动跨对话发送。
'''

shared_files = ['CURRENT_STATE.json','NEXT_ACTIONS.json','SOURCE_PRIORITY.md','ADJUDICATION_NORMALIZED_STATE.json','NET_PAUSED_STATE.json','UI_NORMALIZED_STATE.json']
rule_files = ['rules/lezi-adjudication-reference-decision-2026-10-12.json','rules/CONFIRMATION_HC_H11_B_COUNT_CLOCK.json','rules/HALF_CHAOS_H11_B_COUNT_CLOCK_2026-10-12.md']
configs = [('standard','lezi-standard-design-dispatch-2026-10-13',std,'NEXT-STD-DESIGN-02'),('half_chaos','lezi-half-chaos-design-dispatch-2026-10-13',hc,'NEXT-HC-DESIGN-02'),('UI','lezi-ui-dispatch-2026-10-13',ui,'NEXT-UI-B2-20261013')]
outputs = []
for line, name, prompt, task in configs:
    base = WORK/name
    if base.exists(): shutil.rmtree(base)
    base.mkdir(parents=True)
    (base/'00_READ_FIRST.md').write_text(common)
    (base/'SOURCE_PRIORITY.md').write_text(priority)
    (base/'START.txt').write_text(prompt)
    dump(base/'DISPATCH_STATE.json', {
        'schema':'lezi.design_dispatch.v1','date_local':'2026-10-13','timezone':'Asia/Shanghai',
        'primary_reader':'AI','workline':line,'task_id':task,'status':'prepared_for_user_forwarding_not_sent',
        'priority':'UI_B2_typography' if line=='UI' else 'remaining_mode_adaptation_design_first',
        'secondary':'confirmed_mechanism_additional_scoped_validation' if line!='UI' else 'separate_static_and_runtime_acceptance',
        'engine_baseline':COMMIT,'source_snapshot_cutoff':'2026-10-13T00:17:59+08:00',
        'latest_remote_not_rechecked':True,'new_rule_delta':0,'new_code_delta':0,
        'current_candidate_not_approved': 'H03-B' if line=='standard' else ('H11xH15-A/B' if line=='half_chaos' else 'B2_font'),
        'inherited_scoped_runtime': '9/9' if line=='standard' else ('8/8' if line=='half_chaos' else 'not_run'),
        'scoring_frozen':True,'q':None,'H':None,'I':None,'B':None,'J':None,'empirical_n':0,
        'GC01_GC04':'pending','new_adjudication':'not_implemented',
        'product_implementation_authorized':False,'merge_deploy_authorized':False,
        'external_chats_started':False,'main_adjudication':'retained_paused_until_user_resumes','NET':'paused'})
    dump(base/'RETURN_CONTRACT.json',return_contract)
    for f in shared_files: copy_file(base,f,'inherited/'+f)
    copy_file(base,'reference/X_Collaboration_System.md')
    for f in (SRC/'reference/product_20261009').glob('*'): copy_file(base,str(f.relative_to(SRC)))
    for f in rule_files: copy_file(base,f)
    for f in (ROOT/'dispatch_sources').glob('*.md'):
        d=base/'design'/f.name;d.parent.mkdir(exist_ok=True);shutil.copy2(f,d)
    if line=='UI':
        for f in (SRC/'ui').glob('*'): copy_file(base,str(f.relative_to(SRC)))
        copy_file(base,'trusted_returns/UI/lezi-ui-stage-return-2026-10-12.zip')
    else:
        folder='standard' if line=='standard' else 'half_chaos'
        for f in (SRC/'scoring'/folder).glob('*'): copy_file(base,str(f.relative_to(SRC)))
        for f in (SRC/'trusted_returns'/folder).glob('*'): copy_file(base,str(f.relative_to(SRC)))
        copy_file(base,'runtime/lezi-two-branches-offline-runtime-and-review-2026-10-12.zip')
        copy_file(base,'evidence/MAIN_REVIEW_V03_INHERITED.json')
        copy_file(base,'evidence/MAIN_SCOPED_TEST_V03_INHERITED.log')
    entries=[]
    for f in sorted(base.rglob('*')):
        if f.is_file():
            b=f.read_bytes();entries.append({'path':str(f.relative_to(base)),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
    dump(base/'MANIFEST.json',{'schema':'lezi.dispatch_manifest.v1','task_id':task,'files':entries})
    archive=OUT/(name+'.zip')
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for f in sorted(base.rglob('*')):
            if f.is_file(): z.write(f,str(f.relative_to(base)))
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        manifest=json.loads(z.read('MANIFEST.json'))
        for e in manifest['files']:
            b=z.read(e['path']);assert len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256']
        assert set(z.namelist())=={e['path'] for e in entries}|{'MANIFEST.json'}
    outputs.append({'workline':line,'path':str(archive),'bytes':archive.stat().st_size,'manifest_entries':len(entries),'validation':'passed'})
print(json.dumps(outputs,ensure_ascii=False,indent=2))
