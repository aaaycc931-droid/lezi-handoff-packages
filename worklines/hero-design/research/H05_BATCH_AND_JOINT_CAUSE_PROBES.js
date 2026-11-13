/**
 * Local source-conditioned research only. No jieqi-engine import or acceptance.
 * Run: node worklines/hero-design/research/H05_BATCH_AND_JOINT_CAUSE_PROBES.js
 * Geometry is reused unchanged. Hero phases, fatal settlement and ledgers below
 * are explicit small models, not implementations of the full game.
 */
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const crypto = require('node:crypto');
const assert = require('node:assert/strict');
const sourceCommit = 'f2f0f8914682b29466370f0aeedeb87c19add27f';
const helper = 'H05_TWO_DIFFERENT_CAPTURES_FIXTURE_20261113.js';
const source = fs.readFileSync(path.join(__dirname, helper), 'utf8');
const marker = '  const old=move(B,"b",[3,8],[1,7]), revised=move(B,"b",[3,8],[5,7]);';
assert.equal(source.split(marker).length, 2, 'unique instrumentation site');
const context = {console: {log() {}}};
vm.runInNewContext(source.replace(marker,
  '  globalThis.geometry={B0,move,checked};\n' + marker), context);
const {B0, move, checked} = context.geometry;
const results = [];
function check(id, category, run) { run(); results.push({id, category}); }
const boardSignature = B => JSON.stringify([...B].map(([p,v]) => [p,v.id]).sort());
const byID = (B,id) => [...B].find(([,v]) => v.id === id);

// F1: Red H05 / Black H21-Invincible. Four prayer turns are source-modeled.
// Revealed ordinary 32-piece geometry; no mode admission or RNG probability claim.
let B = new Map(B0);
const prefix = [], redMoves = [
  [[3,4],[3,5]], [[3,5],[3,6]], [[3,6],[3,7]],
  [[3,7],[3,8]], [[7,4],[7,5]]
];
for (let i=0;i<redMoves.length;i++) {
  const [from,to] = redMoves[i], action = move(B,'r',from,to);
  B = action.board;
  assert.equal(checked(B,'r'),false);
  assert.equal(checked(B,'b'),false,'prayer must not be in check');
  prefix.push({opportunity:`red${i+1}`,kind:'ordinary-I',from,to,victim:action.victim});
  if(i<4) prefix.push({opportunity:`black${i+1}`,kind:'source-modeled-prayer'});
}
const oldBuffs = ['b-R-1','b-A-4','b-A-6','b-R-9'];
const newBuffs = ['b-R-1','b-A-4','b-A-6','b-H-2'];
check('F1-prefix-four-prayers-response-and-31-pieces','conditional-geometry',()=>{
  assert.equal(prefix.length,9);
  assert.equal(prefix.filter(x=>x.kind==='source-modeled-prayer').length,4);
  assert.equal(prefix.at(-1).opportunity,'red5');
  assert.equal(B.size,31);
});
check('F1-two-distinct-four-piece-friendly-nonking-pools','conditional-geometry',()=>{
  for(const ids of [oldBuffs,newBuffs]) {
    assert.equal(new Set(ids).size,4);
    for(const id of ids) {
      const entry = byID(B,id);
      assert.ok(entry && entry[1].s==='b' && entry[1].kind!=='K');
    }
  }
});
check('F1-horse-claw-status-changes-with-random-pool','conditional-geometry',()=>{
  assert.equal(oldBuffs.includes('b-H-2'),false);
  assert.equal(newBuffs.includes('b-H-2'),true);
});
const oldMove = move(B,'b',[2,10],[3,8]);
const replayMove = move(B,'b',[2,10],[3,8]);
check('F1-identical-horse-route-victim-and-board','conditional-geometry',()=>{
  assert.equal(oldMove.victim,'r-P-3');
  assert.equal(replayMove.victim,'r-P-3');
  assert.equal(oldMove.board.get('3,8').id,'b-H-2');
  assert.equal(boardSignature(oldMove.board),boardSignature(replayMove.board));
});
check('F1-one-actual-victim-per-version-not-two-for-claw','conditional-geometry',()=>{
  assert.equal(oldMove.board.size,30);
  assert.equal(replayMove.board.size,30);
  assert.equal(byID(replayMove.board,'r-P-3'),undefined);
});
check('F1-both-kings-safe-in-both-local-final-boards','conditional-geometry',()=>{
  for(const board of [oldMove.board,replayMove.board]) {
    assert.equal(checked(board,'r'),false);
    assert.equal(checked(board,'b'),false);
  }
});
const oldDeclaredSources = ['ordinary-endpoint'];
const newDeclaredSources = ['ordinary-endpoint','H21-dragon-claw-crush'];
check('F1-same-action-key-collides-despite-declared-source-difference','source-projection',()=>{
  const key = v => JSON.stringify(['black5','b-H-2',[2,10],[3,8],v]);
  assert.equal(key(oldMove.victim),key(replayMove.victim));
  assert.notDeepEqual(oldDeclaredSources,newDeclaredSources);
  // Actual source grouping and H05 cross-version reset equivalence remain open.
});

// F2: Red H05 / Black H12 after one ordinary red move. H12 is explicit same-batch
// source, but its occupancy turn is NOT an eligible H05 target.
const beforeFlame = move(new Map(B0),'r',[7,4],[7,5]).board;
const center = [2,10], levels = {P:1,A:2,E:2,H:3,C:3,R:4};
const centerPiece = beforeFlame.get(center.join(','));
const locked = [...beforeFlame].filter(([p,v])=>{
  const [x,y] = p.split(',').map(Number);
  return Math.abs(x-center[0])<=1 && Math.abs(y-center[1])<=1 &&
    (v.kind==='K' ? levels[centerPiece.kind]>=3 : levels[v.kind]<=levels[centerPiece.kind]+1);
}).map(([p,v])=>({p,id:v.id}));
check('F2-horse-center-locks-rook-horse-elephant','conditional-geometry',()=>{
  assert.equal(centerPiece.id,'b-H-2');
  assert.deepEqual(locked.map(x=>x.id).sort(),['b-E-3','b-H-2','b-R-1']);
});
function explicitBatch(board, targets, afterClose=()=>{}) {
  const copy = new Map(board), trace = [], deaths = [];
  for(const target of targets) {
    assert.equal(copy.get(target.p)?.id,target.id);
    copy.delete(target.p); deaths.push(target.id);
    trace.push({type:'death',id:target.id});
  }
  trace.push({type:'batch-close'});
  afterClose(copy,trace);
  return {board:copy,trace,deaths};
}
const flame = explicitBatch(beforeFlame,locked);
check('F2-three-deaths-one-explicit-batch-no-intermediate-sample','batch-contract',()=>{
  assert.equal(flame.deaths.length,3);
  assert.equal(flame.trace.filter(x=>x.type==='batch-close').length,1);
  assert.equal(flame.trace.filter(x=>x.type==='sample').length,0);
  assert.equal(flame.board.size,29);
});
check('F2-both-kings-safe-after-flame','conditional-geometry',()=>{
  assert.equal(checked(flame.board,'r'),false);
  assert.equal(checked(flame.board,'b'),false);
});
check('F2-all-locked-deaths-finish-before-after-close-observer','batch-contract',()=>{
  explicitBatch(beforeFlame,locked,(board,trace)=>{
    assert.ok(locked.every(t=>!byID(board,t.id)));
    assert.equal(trace.at(-1).type,'batch-close');
  });
});
check('F2-synthetic-post-close-arrival-is-not-rescanned','synthetic-contract',()=>{
  const result = explicitBatch(beforeFlame,locked,(board,trace)=>{
    board.set('2,10',{id:'synthetic-later-body',s:'b',kind:'H'});
    trace.push({type:'synthetic-after-close-arrival'});
  });
  assert.ok(byID(result.board,'synthetic-later-body'));
  assert.equal(result.deaths.length,3);
  // Observer injection is NOT a claimed resurrection source in this matchup.
});
check('F2-premature-trigger-mutant-is-detected','negative-control',()=>{
  const validate = trace => {
    const close = trace.indexOf('batch-close');
    assert.ok(close>=0 && trace.indexOf('new-trigger')>close);
  };
  validate(['death','death','batch-close','new-trigger']);
  assert.throws(()=>validate(['death','new-trigger','death','batch-close']));
});
const eligibleHistory = actions => actions.length===1 && actions[0]==='ordinary-I';
check('F2-H12-occupancy-not-eligible-H05-history','source-eligibility',()=>{
  assert.equal(eligibleHistory(['occupancy-III']),false);
  assert.equal(eligibleHistory(['ordinary-I']),true);
  assert.equal(eligibleHistory(['ordinary-I','extra-II']),false);
});
check('F1-H21-same-atom-alone-does-not-certify-same-batch','source-eligibility',()=>{
  const classification = (sameAtom,explicitBatch) => explicitBatch?'EXPLICIT_BATCH':sameAtom?'BATCH_UNRESOLVED':'UNKNOWN';
  assert.equal(classification(true,false),'BATCH_UNRESOLVED');
  assert.equal(classification(true,true),'EXPLICIT_BATCH');
});

// F3: isolated fatal-settlement contract. A pre-existing shield is synthetic:
// we do NOT insert a red H21 shield into the F1 H05-vs-H21 matchup.
function fatalSettlement({alive=true,scale=false,contributors,sameSettlement}) {
  if(!sameSettlement) return {status:'GROUPING_UNRESOLVED'};
  const sources = [...new Set(contributors)].sort();
  if(!alive || !sources.length) return {status:'CLOSED',deaths:0,scaleConsumed:0,sources};
  assert.ok(sources.every(x=>['ordinary-endpoint','H21-dragon-claw-crush'].includes(x)));
  return {status:'CLOSED',deaths:scale?0:1,scaleConsumed:scale?1:0,sources};
}
check('F3-two-contributors-one-live-to-dead-transition','synthetic-contract',()=>{
  const r=fatalSettlement({contributors:newDeclaredSources,sameSettlement:true});
  assert.equal(r.deaths,1); assert.equal(r.sources.length,2);
});
check('F3-one-scale-blocks-explicitly-joint-lethal-settlement','synthetic-contract',()=>{
  const r=fatalSettlement({scale:true,contributors:newDeclaredSources,sameSettlement:true});
  assert.equal(r.deaths,0); assert.equal(r.scaleConsumed,1);
});
check('F3-no-new-death-from-already-dead-body','synthetic-contract',()=>{
  assert.equal(fatalSettlement({alive:false,contributors:newDeclaredSources,sameSettlement:true}).deaths,0);
});
check('F3-unknown-settlement-grouping-remains-unknown','synthetic-contract',()=>{
  assert.equal(fatalSettlement({contributors:newDeclaredSources,sameSettlement:false}).status,'GROUPING_UNRESOLVED');
});
check('F3-contributor-enumeration-order-is-not-second-death','synthetic-contract',()=>{
  const a=fatalSettlement({contributors:newDeclaredSources,sameSettlement:true});
  const b=fatalSettlement({contributors:[...newDeclaredSources].reverse(),sameSettlement:true});
  assert.deepEqual(a,b);
});
check('F3-two-versions-can-share-body-with-distinct-execution-records','synthetic-contract',()=>{
  const audit=[{version:'old',victim:'r-P-3'},{version:'replay',victim:'r-P-3'}];
  assert.equal(audit.length,2);
  assert.equal(new Set(audit.map(x=>x.victim)).size,1);
  const uniqueOpportunity=new Map([['black5','old']]);
  uniqueOpportunity.set('black5','replay');
  assert.equal(uniqueOpportunity.size,1);
  // No assertion that two executions must mean two semantic resets.
});

// F4: deliberately hypothetical repetition counts. Only illustrates why reset
// count is not an observable distinction without eligible samples in between.
function repetitionExperiment(policy, interposedSample=false) {
  let counts=new Map([['P',3]]), segment=0;
  const restart=()=>{segment++;counts=new Map();};
  const sample=()=>counts.set('P',(counts.get('P')||0)+1);
  restart(); // already accepted old death; never undone
  if(interposedSample)sample();
  if(policy==='B')restart(); // A/B assumption, NOT adopted policy
  sample();
  return {count:counts.get('P'),segment};
}
check('F4-no-interposed-sample-A-B-same-first-count','synthetic-policy-comparison',()=>{
  assert.equal(repetitionExperiment('A').count,1);
  assert.equal(repetitionExperiment('B').count,1);
  assert.notEqual(repetitionExperiment('A').segment,repetitionExperiment('B').segment);
});
check('F4-hypothetical-interposed-sample-exposes-difference','synthetic-policy-comparison',()=>{
  assert.equal(repetitionExperiment('A',true).count,2);
  assert.equal(repetitionExperiment('B',true).count,1);
  // Legal early sampling reachability (Q-RS2) is NOT established by this model.
});
check('F4-distinct-new-victim-never-suppressed-by-shared-turn','synthetic-contract',()=>{
  const old=new Set(['r-R-1','r-H-2','r-A-4','r-A-6']);
  const replay=new Set(['r-R-1','r-H-2','r-A-4','r-H-8']);
  assert.deepEqual([...replay].filter(id=>!old.has(id)),['r-H-8']);
  assert.deepEqual([...old].filter(id=>!replay.has(id)),['r-A-6']);
});

console.log(JSON.stringify({
  status:'PASS_LOCAL_MODEL_ONLY',sourceCommit,runtime:process.version,
  checks:results.length,cases:results,
  geometryDependency:{file:helper,sha256:crypto.createHash('sha256').update(source).digest('hex')},
  invincibleFixture:{prefix,preBeginPieces:B.size,oldBuffs,newBuffs,
    oldDeclaredSources,newDeclaredSources,actor:'b-H-2',victim:'r-P-3',
    from:[2,10],to:[3,8],finalPieces:30,identicalBoardGeometry:true,
    fullPublicStateIdentical:false,actualContributorGrouping:'UNVERIFIED'},
  flameFixture:{redFirstMove:[[7,4],[7,5]],center,locked,finalPieces:29,
    eligibleH05History:false,resetMultiplicity:'UNRESOLVED'},
  pending:{sameCausePolicy:'A/B_UNCONFIRMED',Q_RS2:'NO_LEGAL_EARLY_SAMPLE_ESTABLISHED',
    H21WhisperBatch:'SAME_SOURCE_ATOM_CONFIRMED_BATCH_UNRESOLVED',
    changedContributorEquivalence:'UNRESOLVED'},
  sourceEngineRuns:0,independentQA:false,
  notVerified:['production hero phases or complete H05 transaction','mode admission',
    'actual RNG sampling/probabilities','complete causal identity and reset multiplicity',
    'synthetic shield/arrival reachability','source-stable early repetition sample',
    'full adjudication, network or independent QA']
},null,2));
