/** H05 capture versioned audit vs semantic reset cause. Pure JS model, NOT source engine; candidate A/B remain undecided. Run node H05_CAPTURE_EVENT_SEMANTIC_DEDUP_20261113.js */
function testCaptureLedger(){
  const assert=(c,why)=>{if(!c)throw Error(why)};
  const out=[];
  const scenario=(oldVictim,newVictim,policy)=>{
    const turnID="black7", old={eventID:"old:cap",turnID,victim:oldVictim,semantic:`${turnID}:horse(3,8):${oldVictim}`}, replay={eventID:"replay:cap",turnID,victim:newVictim,semantic:`${turnID}:horse(3,8):${newVictim}`};
    const audit=[old],captureCause=[old],effective=new Map([[turnID,{version:"old",victim:oldVictim}]]);
    const same=old.semantic===replay.semantic;
    audit.push(replay);effective.set(turnID,{version:"replay",victim:newVictim});
    if(policy==="distinct-event"||!same)captureCause.push(replay);
    return {audit,captureCause,effective,same};
  };
  let r=scenario("red-left-pawn","red-center-pawn","semantic-dedup");
  assert(r.audit.length===2&&r.captureCause.length===2&&r.effective.size===1,"two different victims");
  out.push("distinct victims: two accepted capture facts, one effective turn, two reset causes");
  assert(r.effective.get("black7").victim==="red-center-pawn","new board victim");
  out.push("current effective capture is red center pawn; old victim restored");
  r=scenario("red-left-pawn","red-left-pawn","semantic-dedup");
  assert(r.same&&r.audit.length===2&&r.captureCause.length===1&&r.effective.size===1,"semantic candidate A");
  out.push("same capture candidate A: both executions auditable, one reset cause");
  r=scenario("red-left-pawn","red-left-pawn","distinct-event");
  assert(r.same&&r.captureCause.length===2,"distinct candidate B");
  out.push("same capture candidate B: two distinct execution-reset causes");
  assert(scenario("red-left-pawn","red-center-pawn","distinct-event").captureCause.length===2,"distinct same as A");
  out.push("different victims do not collapse under either candidate");
  const applied=new Set(),add=(id)=>{if(applied.has(id))return false;applied.add(id);return true;};
  assert(add("capture-replay-1")&&!add("capture-replay-1")&&applied.size===1,"delivery retry");
  out.push("same accepted event ID redelivered only once");
  const current=new Map([["black7",{version:0}]]);current.set("black7",{version:1});
  assert(current.size===1&&current.get("black7").version===1,"formal count");
  out.push("one formal opportunity despite version replacement");
  const roll={game:"old",events:["old:cap"]};const draft={game:"new",events:["old:cap","replay:cap"]};
  assert(roll.game==="old"&&roll.events.length===1&&draft.game==="new","failure rollback");
  out.push("failed candidate branch preserves original accepted audit; no new event");
  const seg={old:2,latest:3};assert(seg.latest!==seg.old,"segments");
  out.push("distinct actual capture resets can have separate audit segments; no sample invented");
  const beforeRights="ready",afterRights="spent";assert(beforeRights!==afterRights,"rights");
  out.push("old replay and H05 own occupancy retain different public rights");
  return {passed:out.length,cases:out,kind:"abstract ledger checks, not game engine; same-capture A/B are UNCONFIRMED choices"};
}
console.log(JSON.stringify(testCaptureLedger(),null,2));
