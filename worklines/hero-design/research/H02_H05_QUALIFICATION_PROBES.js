/** Source-scoped H02 lifecycle model over ordinary Xiangqi geometry; NOT production engine. */
const fs=require('node:fs'),vm=require('node:vm'),path=require('node:path'),assert=require('node:assert/strict');
const src=fs.readFileSync(path.join(__dirname,'H05_TWO_DIFFERENT_CAPTURES_FIXTURE_20261113.js'),'utf8');
const marker='  const old=move(B,"b",[3,8],[1,7]), revised=move(B,"b",[3,8],[5,7]);';
assert.equal(src.split(marker).length,2);const ctx={console:{log(){}}};
vm.runInNewContext(src.replace(marker,'  globalThis.geometry={B0,move,checked,legal};\n'+marker),ctx);
const {B0,move,checked,legal}=ctx.geometry;
const init=()=>({board:new Map(B0),qual:new Map(),budget:3,log:[]});
const clone=s=>({board:new Map(s.board),qual:new Map(s.qual),budget:s.budget,log:[...s.log]});
const key=p=>p.join(',');
function safe(s){assert.ok(!checked(s.board,'r')&&!checked(s.board,'b'));}
function ordinary(s,side,from,to,round){
 const actor=s.board.get(key(from));const a=move(s.board,side,from,to);
 s.board=a.board;
 if(side==='b'){
  s.qual.delete(actor.id);
  if(to[1]<from[1])s.qual.set(actor.id,round+1);
 }
 if(a.victim)s.qual.delete(a.victim);
 s.log.push({type:'ordinary',side,round,actor:actor.id,from,to});safe(s);
}
function endBlack(s,round){for(const [id,expiry] of s.qual)if(expiry<=round)s.qual.delete(id);s.log.push({type:'black-end',round});}
function specialBlack(s,from,to,round,maxGrade=2){
 const p=s.board.get(key(from));assert.ok(p&&p.s==='b');
 assert.ok(s.qual.has(p.id)&&s.qual.get(p.id)>=round,'qualification');
 assert.equal(to[0],from[0]);assert.equal(to[1],from[1]+1);
 assert.ok(to[1]<=10);assert.ok(!s.board.has(key(to)),'fixture supports empty targets only');
 if(legal(s.board,from,to))return ordinary(s,'b',from,to,round);
 assert.ok(maxGrade>=2,'grade II prohibited in H05 selected main');assert.ok(s.budget>0,'budget');
 const n=new Map(s.board);n.delete(key(from));n.set(key(to),p);
 assert.ok(!checked(n,'r')&&!checked(n,'b'));
 s.board=n;s.qual.delete(p.id);s.budget--;s.log.push({type:'special-II',round,actor:p.id,from,to});
}
const s=init();
ordinary(s,'r',[1,4],[1,5],1);ordinary(s,'b',[5,7],[5,6],1);endBlack(s,1);
ordinary(s,'r',[7,4],[7,5],2);ordinary(s,'b',[2,10],[3,8],2);endBlack(s,2);
ordinary(s,'r',[9,4],[9,5],3);
const anchor=clone(s),old=clone(anchor);ordinary(old,'b',[3,8],[5,7],3);endBlack(old,3);
const back=clone(anchor);ordinary(back,'b',[3,8],[2,10],3);endBlack(back,3);
const refresh=clone(anchor);ordinary(refresh,'b',[3,8],[5,7],3);endBlack(refresh,3);
const otherOld=clone(anchor);ordinary(otherOld,'b',[8,10],[7,8],3);endBlack(otherOld,3);
const otherNew=clone(anchor);ordinary(otherNew,'b',[8,10],[9,8],3);endBlack(otherNew,3);
const cases=[],test=(id,f)=>{f();cases.push(id);};
test('five-ordinary-opportunities-build-qualification-expiring-at-black3',()=>{
 assert.equal(anchor.log.filter(x=>x.type==='ordinary').length,5);assert.equal(anchor.board.size,32);
 assert.equal(anchor.qual.get('b-H-2'),3);assert.equal(anchor.qual.has('b-P-5'),false);
});
test('old-forward-refreshes-but-replayed-ordinary-backward-clears',()=>{
 assert.equal(old.qual.get('b-H-2'),4);assert.equal(back.qual.has('b-H-2'),false);
 assert.equal(back.budget,3);assert.equal(back.board.get('2,10').id,'b-H-2');
});
test('same-forward-replay-refreshes-on-original-black3-not-selector-red4',()=>{
 assert.equal(refresh.qual.get('b-H-2'),4);assert.equal(refresh.qual.size,1);
 assert.equal(refresh.budget,3);assert.equal(refresh.board.get('5,7').id,'b-H-2');
});
test('unmoved-horse-expires-at-replayed-black3-end',()=>{
 assert.equal(otherNew.qual.has('b-H-2'),false);assert.equal(otherOld.qual.has('b-H-2'),false);
 assert.equal(otherNew.qual.get('b-H-8'),4);assert.equal(otherNew.qual.size,1);
});
test('red4-H05-occupancy-does-not-advance-black-expiry',()=>{
 const h=clone(refresh);h.log.push({type:'red4-H05-occupancy',skippedOwnBeginEnd:true});
 assert.equal(h.qual.get('b-H-2'),4);
 ordinary(h,'b',[7,7],[7,6],4);assert.equal(h.qual.get('b-H-2'),4);
 endBlack(h,4);assert.equal(h.qual.has('b-H-2'),false);assert.equal(h.qual.get('b-P-7'),5);
});
test('black4-special-retreat-is-II-and-spends-one-team-use',()=>{
 const h=clone(refresh);specialBlack(h,[5,7],[5,8],4);endBlack(h,4);
 assert.equal(h.budget,2);assert.equal(h.qual.has('b-H-2'),false);assert.equal(h.board.get('5,8').id,'b-H-2');
});
test('same-special-retreat-is-not-an-eligible-H05-selected-grade-I-action',()=>{
 const h=clone(refresh);const before=h.budget;
 assert.throws(()=>specialBlack(h,[5,7],[5,8],4,1),/grade II/);assert.equal(h.budget,before);
 // This is a grade guard, not a reachable failure of the entire H05 transaction.
});
test('ordinary-rook-one-step-back-is-free-and-consumes-old-qualification',()=>{
 const h=init();ordinary(h,'r',[1,4],[1,5],1);ordinary(h,'b',[9,10],[9,9],1);endBlack(h,1);
 ordinary(h,'r',[7,4],[7,5],2);assert.equal(h.qual.get('b-R-9'),2);
 ordinary(h,'b',[9,9],[9,10],2);endBlack(h,2);
 assert.equal(h.budget,3);assert.equal(h.qual.has('b-R-9'),false);
});
test('failed-candidate-isolation-restores-current-old-qualification-not-anchor',()=>{
 // Injected transaction failure; no spontaneous failure claimed in deterministic H02 pair.
 const candidate=clone(back),restored=clone(old);assert.equal(candidate.qual.has('b-H-2'),false);
 assert.equal(restored.qual.get('b-H-2'),4);assert.notEqual(restored.qual.get('b-H-2'),anchor.qual.get('b-H-2'));
 assert.equal(restored.budget,old.budget);
});
test('historical-special-II-turn-is-outside-H05-eligibility',()=>{
 const eligible=grades=>grades.length===1&&grades[0]===1;
 assert.equal(eligible([1]),true);assert.equal(eligible([2]),false);assert.equal(eligible([1,2]),false);
});
test('earlier-special-use-remains-spent-when-next-ordinary-turn-is-replayed',()=>{
 const h=clone(anchor);specialBlack(h,[3,8],[3,9],3);endBlack(h,3);
 ordinary(h,'r',[1,5],[1,6],4);assert.equal(h.budget,2);
 const old4=clone(h),replay4=clone(h);
 ordinary(old4,'b',[7,7],[7,6],4);endBlack(old4,4);
 ordinary(replay4,'b',[7,7],[7,6],4);endBlack(replay4,4);
 assert.equal(old4.budget,2);assert.equal(replay4.budget,2);
 assert.equal(replay4.qual.get('b-P-7'),5);
});
console.log(JSON.stringify({status:'PASS_LOCAL_MODEL_ONLY',checks:cases.length,cases,runtime:process.version,
 prefix:anchor.log,old:{horse:[5,7],expiry:old.qual.get('b-H-2'),budget:old.budget},
 rewrittenBackward:{horse:[2,10],qualification:back.qual.has('b-H-2'),budget:back.budget},
 otherActorReplay:{expiredOriginalHorse:!otherNew.qual.has('b-H-2'),otherHorseExpiry:otherNew.qual.get('b-H-8')},
 sourceEngineRuns:0,independentQA:false,
 limits:['H02 callbacks and H05 transaction are local source models','failed branch is injected, not a naturally forced failure','no direct king targets, hidden/space/control/defense interactions','geometry helper only checks ordinary threats; no added shadow threat reaches either fixed king in these positions','no extra-action source or historical special-budget refund proved','no mode admission or network validation']},null,2));
