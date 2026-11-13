/** Confirmed A time-budget contract model only. No server clock, transport or game engine. */
const assert=require('node:assert/strict');
class Budget {
 constructor(duration,now=0){this.duration=duration;this.start=now;this.paused=0;this.pauseStart=null;this.last=now;this.phase='prewindow';this.attempted=false;this.used=false;this.events=new Set();}
 remaining(now){assert.ok(now>=this.last,'monotonic time');return Math.max(0,this.duration-(now-this.start-this.paused-(this.pauseStart===null?0:now-this.pauseStart)));}
 event(id,type,now){
  assert.ok(now>=this.last,'monotonic event time');
  if(this.events.has(id))return false;
  if(type==='attempt'){assert.equal(this.phase,'prewindow');assert.equal(this.attempted,false);this.attempted=true;this.phase='replay';}
  else if(type==='opponent-pause'){assert.equal(this.phase,'replay');assert.equal(this.pauseStart,null);this.pauseStart=now;}
  else if(type==='opponent-resume'){assert.notEqual(this.pauseStart,null);this.paused+=now-this.pauseStart;this.pauseStart=null;}
  else if(type==='fail'){assert.equal(this.phase,'replay');assert.equal(this.pauseStart,null);this.phase='original-sample';}
  else if(type==='decline'){assert.equal(this.phase,'prewindow');this.phase='original-sample';}
  else if(type==='sample-continue'){assert.equal(this.phase,'original-sample');this.phase=this.remaining(now)>0?'normal':'expired-await-existing-timeout-rule';}
  else if(type==='sample-terminal'){assert.equal(this.phase,'original-sample');this.phase='terminal';}
  else if(type==='success'){assert.equal(this.phase,'replay');assert.equal(this.pauseStart,null);this.used=true;this.phase='completed-H05';}
  else throw Error('unknown event');
  this.last=now;this.events.add(id);return true;
 }
}
const cases=[],test=(id,fn)=>{fn();cases.push(id);};
test('sixty-second-budget-failure-after35-leaves25',()=>{
 const c=new Budget(60000);c.event('a','attempt',10000);c.event('f','fail',35000);c.event('s','sample-continue',35000);
 assert.equal(c.remaining(35000),25000);assert.equal(c.phase,'normal');assert.equal(c.used,false);assert.equal(c.attempted,true);
 assert.throws(()=>c.event('a2','attempt',35000));
});
test('decline-keeps-only-original-remainder',()=>{
 const c=new Budget(60000);c.event('d','decline',15000);c.event('s','sample-continue',15000);
 assert.equal(c.remaining(15000),45000);assert.equal(c.start,0);assert.equal(c.attempted,false);
});
test('opponent-twenty-second-window-does-not-charge-H05',()=>{
 const c=new Budget(60000);c.event('a','attempt',10000);c.event('p','opponent-pause',15000);
 assert.equal(c.remaining(35000),45000);c.event('r','opponent-resume',35000);
 c.event('f','fail',55000);c.event('s','sample-continue',55000);assert.equal(c.remaining(55000),25000);
});
test('multiple-source-windows-sum-only-real-pauses',()=>{
 const c=new Budget(60000);c.event('a','attempt',5000);c.event('p1','opponent-pause',10000);c.event('r1','opponent-resume',20000);
 c.event('p2','opponent-pause',25000);c.event('r2','opponent-resume',32000);c.event('f','fail',45000);
 assert.equal(c.paused,17000);assert.equal(c.remaining(45000),32000);
 assert.throws(()=>c.event('bad','opponent-resume',45000));
});
test('duplicate-delivery-does-not-repeat-pause-or-refresh-budget',()=>{
 const c=new Budget(60000);c.event('a','attempt',5000);c.event('p','opponent-pause',10000);c.event('r','opponent-resume',30000);
 assert.equal(c.event('r','opponent-resume',31000),false);c.event('f','fail',40000);assert.equal(c.event('f','fail',41000),false);
 c.event('s','sample-continue',42000);assert.equal(c.paused,20000);assert.equal(c.remaining(42000),38000);assert.equal(c.start,0);
});
test('source-duration-is-an-input-not-forced-to60',()=>{
 // 45/75 are illustrative inputs, not newly authorized source durations.
 for(const d of [45000,60000,75000]){const c=new Budget(d,1000);c.event('a','attempt',6000);c.event('f','fail',21000);c.event('s','sample-continue',21000);assert.equal(c.remaining(21000),d-20000);}
});
test('exhausted-budget-does-not-give-new-normal-window',()=>{
 const c=new Budget(60000);c.event('a','attempt',10000);c.event('f','fail',60000);c.event('s','sample-continue',60000);
 assert.equal(c.remaining(60000),0);assert.equal(c.phase,'expired-await-existing-timeout-rule');assert.equal(c.used,false);
 // Input ordering is stipulated; no network/deadline race winner is asserted.
});
test('original-sample-terminal-stops-normal-flow',()=>{
 const c=new Budget(60000);c.event('a','attempt',10000);c.event('f','fail',20000);c.event('s','sample-terminal',20000);
 assert.equal(c.phase,'terminal');assert.throws(()=>c.event('later','sample-continue',20000));
});
test('successful-occupancy-does-not-open-normal-action-budget',()=>{
 const c=new Budget(60000);c.event('a','attempt',5000);c.event('ok','success',35000);
 assert.equal(c.used,true);assert.equal(c.phase,'completed-H05');assert.throws(()=>c.event('extra','sample-continue',35000));
});
console.log(JSON.stringify({status:'PASS_LOCAL_CONTRACT_MODEL_ONLY',checks:cases.length,cases,runtime:process.version,
 confirmedPolicy:'Q-H05-CLOCK-01=A',sourceEngineRuns:0,independentQA:false,
 examples:{failure35of60RemainingSeconds:25,opponentPauseSeconds:20,elapsed55WithPause20RemainingSeconds:25},
 notVerified:['production monotonic clock and pause ownership','game begin/end and resource callbacks','network identity/conflicting payloads/reconnect','simultaneous terminal-deadline-request priority','commit-gate placement and committed atom completion','complete time-source interactions','mode admission or independent QA']},null,2));
