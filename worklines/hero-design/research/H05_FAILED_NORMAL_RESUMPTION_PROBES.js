/** Research only: ordinary geometry plus a source-contract phase adapter, not a game engine. */
const fs=require('node:fs'),path=require('node:path');
const assert=require('node:assert/strict'),Module=require('node:module');
const dependency=path.join(__dirname,'H05_FAILED_REPLAY_LEDGER_PROBES.js');
const src=fs.readFileSync(dependency,'utf8'),marker='console.log(JSON.stringify({status:';
assert.equal(src.split(marker).length,2);
const adapter=new Module(dependency,module);adapter.filename=dependency;adapter.paths=module.paths;
adapter._compile(src.replace('console.log(JSON.stringify(',
 'module.exports={fixture:{oldEnd,move,checked,failTransaction,initial,signature},summary:')
 .replace(/,null,2\)\);\s*$/, '};'),dependency);
const {fixture:f,summary:inherited}=adapter.exports,cases=[],test=(id,fn)=>{fn();cases.push(id);};
const copy=x=>JSON.parse(JSON.stringify(x));
function resume({terminalAtOriginalSample=false}={}){
 const failed=copy(f.failTransaction().state);
 const s={...failed,board:new Map(f.oldEnd),h21:{prayers:4,premonition:false,descended:true},
 trace:['failure-restores-current-old-line','original-handoff-sample'],
 redBegin:0,redEnd:0,redMain:0,acceptedBlack7Begin:1,nextBlackBegin:0,
 h05Occupancies:0,wallClockPolicy:'UNRESOLVED_SOURCE_BINDING',terminal:terminalAtOriginalSample};
 if(s.terminal)return s;
 s.redBegin++;s.trace.push('red8-normal-begin');
 s.board=f.move(s.board,'r',[7,5],[7,6]).board;s.redMain++;s.trace.push('red8-main-closed');
 s.redEnd++;s.trace.push('red8-normal-end');s.formal.push('red8-ordinary');
 assert.ok(!f.checked(s.board,'r')&&!f.checked(s.board,'b'));
 s.nextBlackBegin++;s.trace.push('black8-normal-begin');
 if(s.h21.premonition)throw Error('unexpected repeated H21 descent');
 s.board=f.move(s.board,'b',[3,8],[2,10]).board;s.trace.push('black8-main-closed');
 assert.ok(!f.checked(s.board,'r')&&!f.checked(s.board,'b'));return s;
}
const normal=resume(),terminal=resume({terminalAtOriginalSample:true});
test('failed-candidate-restores-current-board-not-historical-anchor',()=>{
 assert.equal(f.failTransaction().state.board,f.signature(f.oldEnd));
 assert.equal(normal.board.get('5,7').id,'r-P-5');
 assert.equal([...normal.board.values()].some(p=>p.id==='r-H-2'),false);assert.equal(normal.board.size,27);
});
test('normal-red8-and-following-black8-have-legal-concrete-moves',()=>{
 assert.equal(normal.board.get('7,6').id,'r-P-7');assert.equal(normal.board.get('2,10').id,'b-H-2');
 assert.equal(normal.redMain,1);assert.equal(normal.nextBlackBegin,1);
});
test('normal-begin-and-end-occur-once-after-original-sample',()=>{
 assert.deepEqual(normal.trace.slice(0,5),['failure-restores-current-old-line','original-handoff-sample','red8-normal-begin','red8-main-closed','red8-normal-end']);
 assert.equal(normal.redBegin,1);assert.equal(normal.redEnd,1);
});
test('failure-spends-attempt-but-not-use-or-occupancy',()=>{
 assert.equal(normal.attempted,true);assert.equal(normal.used,false);
 assert.deepEqual(normal.rngLock,copy(f.failTransaction().state.rngLock));
 assert.equal(normal.h05Occupancies,0);assert.deepEqual(normal.formal,['black7','red8-ordinary']);
});
test('accepted-h21-descent-is-not-rearmed-at-next-begin',()=>{
 assert.deepEqual(normal.h21,{prayers:4,premonition:false,descended:true});assert.equal(normal.acceptedBlack7Begin,1);
 assert.deepEqual(normal.audit,copy(f.initial.audit));
});
test('formal-draw-at-original-sample-prevents-all-later-game-phases',()=>{
 // Verdict is an input oracle, not a reachable fifth-repetition fixture.
 assert.deepEqual(terminal.trace,['failure-restores-current-old-line','original-handoff-sample']);
 assert.equal(terminal.redBegin+terminal.redMain+terminal.redEnd+terminal.nextBlackBegin,0);
 assert.equal(terminal.used,false);assert.equal(terminal.attempted,true);assert.deepEqual(terminal.formal,['black7']);
});
test('duplicate-begin-and-premature-begin-mutants-are-detectable',()=>{
 assert.throws(()=>assert.equal({...normal,redBegin:2}.redBegin,1));
 assert.throws(()=>assert.equal({...terminal,redBegin:1}.redBegin,0));
});
test('hypothetical-timer-counters-are-not-installed-as-extra-hero-effects',()=>{
 assert.equal(normal.wallClockPolicy,'UNRESOLVED_SOURCE_BINDING');
 assert.equal(Object.hasOwn(normal,'cooldown'),false);assert.equal(Object.hasOwn(normal,'training'),false);
});
console.log(JSON.stringify({status:'PASS_LOCAL_MODEL_ONLY',checks:cases.length,cases,runtime:process.version,
 inheritedFixtureChecksRerun:inherited.checks,normalTrace:normal.trace,terminalTrace:terminal.trace,
 ordinaryMoves:[{side:'red8',from:[7,5],to:[7,6]},{side:'black8',from:[3,8],to:[2,10]}],
 finalPieces:normal.board.size,sourceEngineRuns:0,independentQA:false,
 scope:'H21 source-conditioned old failure fixture plus local phase adapter; terminal verdict supplied externally',
 notVerified:['actual source-specific timer/cooldown callbacks','H05 wall-clock window and failure deadline binding','reachable fifth-repeat terminal fixture','production H05 transaction and mode admission','network retries or independent QA']},null,2));
