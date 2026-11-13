/** Source-conditioned geometry + illustrative transaction model, NOT engine. */
const fs=require('node:fs'),vm=require('node:vm'),path=require('node:path'),assert=require('node:assert/strict');
const src=fs.readFileSync(path.join(__dirname,'H05_TWO_DIFFERENT_CAPTURES_FIXTURE_20261113.js'),'utf8');
const marker='  const old=move(B,"b",[3,8],[1,7]), revised=move(B,"b",[3,8],[5,7]);';
assert.equal(src.split(marker).length,2);
const ctx={console:{log(){}}};vm.runInNewContext(src.replace(marker,'  globalThis.geo={B0,move,checked};\n'+marker),ctx);
const {B0,move,checked}=ctx.geo;
const steps=[['r',[5,4],[5,5]],['b',[8,10],[7,8]],['r',[5,5],[5,6]],['b',[7,8],[8,10]],
 ['r',[5,6],[5,7]],['prayer'],['r',[1,1],[1,2]],['prayer'],['r',[1,2],[5,2]],['prayer'],
 ['r',[5,2],[5,4]],['prayer'],['r',[7,4],[7,5]]];
let B=new Map(B0),prayers=0;const trace=[];
for(const [side,from,to] of steps){
 if(side==='prayer'){assert.equal(checked(B,'b'),false);prayers++;trace.push({type:'source-modeled-prayer',number:prayers});}
 else {const a=move(B,side,from,to);B=a.board;trace.push({side,from,to,victim:a.victim});}
 assert.equal(checked(B,'r'),false);assert.equal(checked(B,'b'),false);
}
const cases=[],test=(id,f)=>{f();cases.push(id)},signature=b=>JSON.stringify([...b].map(([p,v])=>[p,v.id]).sort());
const oldIDs=['r-A-4','r-A-6','r-H-2','r-H-8'];
const failIDs=['r-A-4','r-A-6','r-P-5','r-H-8'];
const adverseIDs=['r-A-4','r-A-6','r-R-1','r-H-8'];
function descent(ids){const b=new Map(B);assert.equal(new Set(ids).size,4);for(const id of ids){const entry=[...b].find(([,p])=>p.id===id);assert.ok(entry&&entry[1].s==='r'&&entry[1].kind!=='K');b.delete(entry[0]);}return b;}
const oldBegin=descent(oldIDs),badBegin=descent(failIDs),adverseBegin=descent(adverseIDs);
const oldEnd=move(oldBegin,'b',[2,10],[3,8]).board;
const adverseEnd=move(adverseBegin,'b',[2,10],[3,8]).board;
const legalDestinations=[];
for(let x=1;x<=9;x++)for(let y=1;y<=10;y++){try{move(badBegin,'b',[2,10],[x,y]);legalDestinations.push([x,y]);}catch(e){if(!/illegal|king unsafe/.test(e.message))throw e;}}
test('13-opportunity-prefix-four-prayers-and-response',()=>{assert.equal(trace.length,13);assert.equal(prayers,4);assert.equal(B.size,31);assert.equal(B.get('5,4').id,'r-R-1');assert.equal(B.get('5,7').id,'r-P-5');});
test('old-black7-ordinary-horse-move-closes-safely',()=>{assert.equal(oldEnd.size,27);assert.ok(!checked(oldEnd,'r')&&!checked(oldEnd,'b'));});
test('new-begin-removes-screen-and-exposes-black-king',()=>{assert.equal(checked(badBegin,'b'),true);assert.equal(checked(badBegin,'r'),false);assert.equal(badBegin.get('5,4').id,'r-R-1');assert.equal(badBegin.has('5,7'),false);});
test('all-90-horse-destinations-fail-so-required-original-actor-cannot-act',()=>{assert.deepEqual(legalDestinations,[]);});
test('adverse-rook-loss-still-allows-safe-original-horse-action',()=>{assert.ok(!checked(adverseEnd,'r')&&!checked(adverseEnd,'b'));assert.equal(adverseEnd.size,27);assert.equal([...adverseEnd.values()].some(p=>p.id==='r-R-1'),false);assert.equal(adverseEnd.get('5,7').id,'r-P-5');});
// Ledger is deliberately synthetic: illustrates isolation, not reset multiplicity.
const initial={board:signature(oldEnd),audit:oldIDs.map(victim=>({version:'old',victim})),segmentToken:'accepted-old-segment',used:false,attempted:false,formal:['black7'],rngLock:null};
function failTransaction(){const s=structuredClone(initial);s.attempted=true;s.rngLock=[...failIDs];const staged=failIDs.map(victim=>({version:'failed-candidate',victim}));return {state:s,discarded:staged};}
test('failure-discards-all-staged-deaths-preserves-accepted-old-audit-and-board',()=>{const {state:s,discarded}=failTransaction();assert.equal(discarded.length,4);assert.deepEqual(s.audit,initial.audit);assert.equal(s.board,initial.board);assert.equal(s.segmentToken,initial.segmentToken);});
test('failure-keeps-attempt-and-random-lock-but-not-use-or-successful-occupancy',()=>{const {state:s}=failTransaction();assert.equal(s.attempted,true);assert.deepEqual(s.rngLock,failIDs);assert.equal(s.used,false);assert.deepEqual(s.formal,['black7']);/* normal red8 will proceed; not simulated */});
test('eager-candidate-audit-mutation-is-detected',()=>{const s=failTransaction().state;s.audit.push({version:'failed-candidate',victim:'r-P-5'});assert.throws(()=>assert.deepEqual(s.audit,initial.audit));});
test('success-retains-old-audit-accepts-new-version-and-spends-once',()=>{const s=structuredClone(initial);s.board=signature(adverseEnd);s.audit.push(...adverseIDs.map(victim=>({version:'replay',victim})));s.used=true;s.attempted=true;s.formal.push('red8-H05-occupancy');assert.deepEqual(s.audit.slice(0,4),initial.audit);assert.ok(s.audit.some(x=>x.version==='replay'&&x.victim==='r-R-1'));assert.equal(s.used,true);assert.equal(new Set(s.formal).size,2);/* eight execution audit rows do NOT imply eight resets */});
test('adverse-result-alone-is-not-legality-failure',()=>{assert.equal(legalDestinations.length,0);assert.notEqual(signature(adverseEnd),signature(oldEnd));assert.equal(checked(adverseEnd,'b'),false);assert.equal(checked(adverseEnd,'r'),false);});
console.log(JSON.stringify({status:'PASS_LOCAL_MODEL_ONLY',checks:cases.length,cases,runtime:process.version,
 prefix:trace,prayers,oldDeaths:oldIDs,failedCandidateDeaths:failIDs,adverseSuccessDeaths:adverseIDs,
 failedOriginalHorseLegalDestinations:legalDestinations,oldFinalPieces:oldEnd.size,successFinalPieces:adverseEnd.size,
 sourceEngineRuns:0,independentQA:false,notVerified:['production prayer/descent/H05 transaction','mode admission','actual RNG distribution or secret projections','no-capture/pressure/repetition merge multiplicity','formal commit implementation','normal turn after failure','network or independent QA']},null,2));
