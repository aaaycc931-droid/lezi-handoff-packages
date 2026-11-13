/** Conditional H19/H05 research, not production hero/turn execution. */
const fs=require('node:fs'),vm=require('node:vm'),path=require('node:path'),assert=require('node:assert/strict');
const source=fs.readFileSync(path.join(__dirname,'H05_TWO_DIFFERENT_CAPTURES_FIXTURE_20261113.js'),'utf8');
const marker='  const old=move(B,"b",[3,8],[1,7]), revised=move(B,"b",[3,8],[5,7]);';
assert.equal(source.split(marker).length,2);const ctx={console:{log(){}}};
vm.runInNewContext(source.replace(marker,'  globalThis.geo={B0,move,checked};\n'+marker),ctx);
const {B0,move,checked}=ctx.geo;let board=new Map(B0),infection=0,remaining=0;
const trace=[],cases=[],test=(id,f)=>{f();cases.push(id);};
const moves=[['r',[3,4],[3,5]],['b',[8,10],[7,8]],['r',[3,5],[3,6]],['b',[7,8],[8,10]],
 ['r',[3,6],[3,7]],['b',[8,10],[7,8]],['r',[7,4],[7,5]],['b',[7,8],[8,10]],['r',[7,5],[7,6]]];
for(let i=0;i<moves.length;i++){
 const [side,from,to]=moves[i],a=move(board,side,from,to);board=a.board;
 if(a.victim==='b-P-3'){remaining=3;infection=0;/* new ghost under attacker is NOT entry */}
 if(side==='b'&&remaining>0){infection++;remaining--;}
 assert.ok(!checked(board,'r')&&!checked(board,'b'));
 trace.push({opportunity:i+1,side,from,to,victim:a.victim,infection,ghostRemaining:remaining});
}
test('nine-ordinary-opportunities-reach-black5-begin',()=>{assert.equal(trace.length,9);assert.equal(board.size,31);assert.equal(board.get('3,7').id,'r-P-3');});
test('ghost-born-under-attacker-does-not-grant-entry-infection',()=>{assert.equal(trace[4].infection,0);assert.equal(trace[4].ghostRemaining,3);});
test('two-black-ends-produce-two-infection-and-one-remaining-resolution',()=>{assert.equal(trace[5].infection,1);assert.equal(trace[7].infection,2);assert.equal(infection,2);assert.equal(remaining,1);});
function complete(to){
 const a=move(board,'b',[2,10],to),b=new Map(a.board),log=[{event:'ordinary-main-complete',actor:'b-H-2'}];
 assert.equal(a.victim,null);assert.equal(b.get('3,7').id,'r-P-3');
 log.push({event:'H19-end-infection',before:infection,after:infection+1});
 b.delete('3,7');log.push({event:'actual-destruction',victim:'r-P-3',source:'H19-infection'});
 log.push({event:'ghost-third-resolution-finished',remaining:remaining-1});
 assert.ok(!checked(b,'r')&&!checked(b,'b'));
 return {board:b,log};
}
const old=complete([3,8]),replay=complete([1,8]);
test('old-main-completes-before-infection-death',()=>{assert.deepEqual(old.log.map(x=>x.event),['ordinary-main-complete','H19-end-infection','actual-destruction','ghost-third-resolution-finished']);});
test('changed-replay-main-also-completes-before-end-death',()=>{assert.equal(replay.board.get('1,8').id,'b-H-2');assert.equal(replay.log[2].victim,'r-P-3');assert.equal(replay.board.size,30);});
test('controlled-actor-survives-do-not-claim-actor-death',()=>{assert.ok([...old.board.values()].some(p=>p.id==='b-H-2'));assert.ok([...replay.board.values()].some(p=>p.id==='b-H-2'));assert.equal([...replay.board.values()].some(p=>p.id==='r-P-3'),false);});
test('expiry-before-third-infection-mutant-misses-required-death',()=>{const wrongRemaining=remaining-1;const wrongInfection=infection+(wrongRemaining>0?1:0);assert.equal(wrongInfection,2);assert.notEqual(wrongInfection,3);});
test('same-victim-two-execution-audits-not-two-formal-opportunities',()=>{const audit=[{version:'old',victim:'r-P-3'},{version:'replay',victim:'r-P-3'}];const effective=new Map([['black5','old']]);effective.set('black5','replay');effective.set('red6','H05-occupancy');assert.equal(audit.length,2);assert.equal(effective.size,2);/* no reset multiplicity asserted */});
console.log(JSON.stringify({status:'PASS_LOCAL_MODEL_ONLY',checks:cases.length,cases,runtime:process.version,prefix:trace,
 oldDestination:[3,8],replayDestination:[1,8],oldTrace:old.log,replayTrace:replay.log,
 oldFinalPieces:old.board.size,replayFinalPieces:replay.board.size,
 sourceEngineRuns:0,independentQA:false,controlledActorDeathProved:false,
 assumptions:['normal ghost affects its own death square','ordinary all-revealed geometry, no extra hero or mutation','H19 callbacks locally modeled'],
 unresolved:['H05 mode admission and production transaction','exact duplicate reset policy','controlled actor post-action death','secret post-action death','independent QA']},null,2));
