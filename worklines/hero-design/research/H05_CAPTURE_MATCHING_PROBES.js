/** Research projections only; no production equality key or A/B policy. */
const fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
const assert=require('node:assert/strict');
const source=fs.readFileSync(path.join(__dirname,'H05_TWO_DIFFERENT_CAPTURES_FIXTURE_20261113.js'),'utf8');
const marker='  const old=move(B,"b",[3,8],[1,7]), revised=move(B,"b",[3,8],[5,7]);';
assert.equal(source.split(marker).length,2);
const context={console:{log(){}}};
vm.runInNewContext(source.replace(marker,'  globalThis.geometry={B0,move,checked};\n'+marker),context);
const {B0,move,checked}=context.geometry;
let board=new Map(B0);
const prefix=[[[3,4],[3,5]],[[3,5],[3,6]],[[3,6],[3,7]],[[3,7],[3,8]],[[7,4],[7,5]]];
for(const [from,to] of prefix){board=move(board,'r',from,to).board;assert.ok(!checked(board,'r')&&!checked(board,'b'));}
// Four black prayers between first four red moves are source-modeled, not run.
const pools={old:['b-R-1','b-A-4','b-A-6','b-R-9'],
 unrelated:['b-R-1','b-A-4','b-A-6','b-H-8'],
 claw:['b-R-1','b-A-4','b-A-6','b-H-2']};
const findings=[],test=(id,f)=>{f();findings.push(id);};
test('all-three-pools-are-four-friendly-nonkings',()=>{
 for(const ids of Object.values(pools)){
  assert.equal(new Set(ids).size,4);
  for(const id of ids)assert.ok([...board.values()].some(p=>p.id===id&&p.s==='b'&&p.kind!=='K'));
 }
});
const variants=Object.fromEntries(Object.entries(pools).map(([name,buffs])=>{
 const action=move(board,'b',[2,10],[3,8]);
 return [name,{buffs,board:[...action.board].map(([pos,p])=>[pos,p.id]).sort(),
  projection:{opportunity:'black5',actor:'b-H-2',victim:action.victim,phase:'main',
    action:'ordinary-I-attack',from:[2,10],to:[3,8],
    declaredSources:buffs.includes('b-H-2')?['ordinary-endpoint','dragon-claw']:['ordinary-endpoint']},
  safe:!checked(action.board,'r')&&!checked(action.board,'b')}];
}));
test('three-variants-share-geometric-capture-and-safe-30-piece-board',()=>{
 for(const v of Object.values(variants)){
  assert.equal(v.projection.victim,'r-P-3');assert.equal(v.board.length,30);assert.equal(v.safe,true);
  assert.deepEqual(v.board,variants.old.board);
 }
});
test('unrelated-buff-change-breaks-global-state-equality',()=>{
 assert.notDeepEqual(variants.old.buffs,variants.unrelated.buffs);
 assert.deepEqual(variants.old.projection,variants.unrelated.projection);
});
test('actor-claw-change-breaks-capture-source-projection',()=>{
 assert.notDeepEqual(variants.old.projection,variants.claw.projection);
});
// This classifier only labels observed projections. It NEVER returns SAME_CAUSE,
// never increments a reset counter, and never decides the unapproved A/B policy.
function compare(a,b){
 const fields=['opportunity','actor','victim','phase','action','from','to','declaredSources'];
 if(fields.some(k=>a[k]==null||b[k]==null))return 'INSUFFICIENT_EVIDENCE';
 return fields.every(k=>JSON.stringify(a[k])===JSON.stringify(b[k]))?
  'MATCHING_PROJECTION_POLICY_PENDING':'DIFFERENT_OBSERVATIONS_POLICY_PENDING';
}
test('matching-projection-is-not-causal-equivalence-approval',()=>{
 assert.equal(compare(variants.old.projection,variants.unrelated.projection),'MATCHING_PROJECTION_POLICY_PENDING');
});
test('changed-source-does-not-automatically-approve-extra-reset',()=>{
 assert.equal(compare(variants.old.projection,variants.claw.projection),'DIFFERENT_OBSERVATIONS_POLICY_PENDING');
});
test('missing-source-is-unknown-not-same',()=>{
 assert.equal(compare(variants.old.projection,{...variants.old.projection,declaredSources:null}),'INSUFFICIENT_EVIDENCE');
});
test('new-execution-label-alone-does-not-prove-new-cause',()=>{
 assert.equal(compare({...variants.old.projection,execution:'old'},{...variants.old.projection,execution:'replay'}),'MATCHING_PROJECTION_POLICY_PENDING');
});
console.log(JSON.stringify({status:'PASS_LOCAL_RESEARCH_ONLY',checks:findings.length,cases:findings,
 runtime:process.version,variants,sourceEngineRuns:0,independentQA:false,
 limits:['prayer/descent source-modeled','no full causal equivalence key','no actual RNG',
 'no mode admission','no reset multiplicity policy','no legal Q-RS2 early sample'],
 A_B:'UNCONFIRMED'},null,2));
