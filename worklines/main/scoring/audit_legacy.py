"""Historical consistency audit only. Never a numeric input to candidate_model."""
import json, re, hashlib, sys
from decimal import Decimal
from pathlib import Path

path=Path(sys.argv[1])
text=path.read_text()
b=path.read_bytes()
blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
if blob!='53f9a64721003a91702b0954b98f07559deb7cd4':raise ValueError('Unexpected frozen ledger bytes')
table=text.split('## 一、冻结结果总表',1)[1].split('### 虔信狂徒五形态分支',1)[0]
rows=[]
for line in table.splitlines():
    cells=[x.strip() for x in line.strip().strip('|').split('|')]
    if len(cells)!=6:continue
    try:r=Decimal(cells[1]);s=Decimal(cells[2].strip('*'))
    except Exception:continue
    rows.append({'hero':cells[0],'R_displayed':str(r),'S_displayed':str(s),'formula_using_displayed_R':str(r*Decimal('1.25')),'displayed_residual':str(s-r*Decimal('1.25'))})
values=[Decimal(r['S_displayed']) for r in rows]
summary=text.split('## 四、当前平衡结论',1)[1]
stale=[]
for name,old,current in [('江鹤','51.6','52.8'),('代号1','51.7','52.4'),('夜','52.1','52.9')]:
    if re.search(re.escape(name)+r'\s*'+re.escape(old),summary):stale.append({'hero':name,'summary':old,'main_table':current,'classification':'intra_snapshot_stale_summary_not_new_gameplay'})
payload={'schema':'lezi.scoring_legacy_audit.v1','source_path':str(path).split('scoring-sources/')[-1],
 'source_declared_blob':'53f9a64721003a91702b0954b98f07559deb7cd4',
 'primary_heroes':len(rows),'minimum_S':str(min(values)),'maximum_S':str(max(values)),
 'span':str(max(values)-min(values)),'mean_for_audit_only':str(sum(values)/len(values)),
 'rows':rows,'stale_summary':stale,
 'old_summary_span':'about2.5','main_table_span':str(max(values)-min(values)),
 'rounding_status':'42.2*1.25=52.75 vs displayed52.7: displayed precision/rounding is unspecified; hidden unroundedR could explain it, not established arithmetic fault',
 'causal_anchoring_proven':False,'all_historical_scores_proven_wrong':False,
 'candidate_calibration_uses_this_table':False,
 'reproducibility_gap':'A-L prose does not supply the per-dimension values/state frequencies/utility-to-R calibration required to reconstruct21 totals',
 'frozen_original_modified':False}
out=Path(__file__).parent/'LEGACY_AUDIT_RESULTS.json'
out.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:payload[k] for k in ('primary_heroes','minimum_S','maximum_S','span','stale_summary')},ensure_ascii=False))
