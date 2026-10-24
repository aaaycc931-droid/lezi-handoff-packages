"""Reproduce the candidate arithmetic/properties; never invokes a chess engine."""
import json, hashlib, sys, unittest
from pathlib import Path
from candidate_model import paired_value, publication_gate
from validation_cases import cases, sensitivity, historical_wind_schedule

root=Path(__file__).resolve().parent
suite=unittest.defaultTestLoader.discover(str(root),pattern='test_candidate_model.py')
with (root/'VALIDATION_LOG.txt').open('w') as stream:
    result=unittest.TextTestRunner(stream=stream,verbosity=2).run(suite)
rows=[]
for case in cases():
    row={**case, 'computed':paired_value(case['without'],case['with']),
         'publication_gate':publication_gate({'kind':case['evidence_kind'],'utility':'outcome'})}
    rows.append(row)
files={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in root.glob('*.py')}
payload={'schema':'lezi.scoring_candidate_validation.v1','candidate':'CF-OUTCOME-v0.1',
  'python':sys.version.split()[0],'unit_tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),
  'conditional_cases':len(rows),'cross_types':['mobility','protection','information','direct_destruction','terminal'],
  'cases':rows,'sensitivity_25_30_35':sensitivity(),'wind_opening_schedule':[historical_wind_schedule(n) for n in (0,1,2)],'source_sha256':files,
  'full_game_replays':0,'game_engine_runs':0,'hero_scores_published':0,
  'verification_independence':'same author, deterministic arithmetic/property execution; not independent QA or empirical calibration',
  'empirical_probability_inputs':0,'source_probability_status':'local assumed laws or explicit rule rates only',
  'scoring_frozen':True,'NET':'paused'}
(root/'VALIDATION_RESULTS.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:payload[k] for k in ('unit_tests','failures','errors','conditional_cases','game_engine_runs','hero_scores_published')}))
raise SystemExit(0 if result.wasSuccessful() else 1)
