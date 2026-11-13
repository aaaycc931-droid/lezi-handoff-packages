/**
 * Source-conditioned local probes, NOT Lezi engine or formal H05 acceptance.
 * Reuses the existing 13-ply geometry fixture by exposing its local helpers.
 * Adds a source-conditioned 32-piece prefix with four prayer opportunities.
 * Prayer/descent/H05 phases are local source models, not production execution.
 * node worklines/hero-design/research/H05_CAPTURE_CAUSAL_BOUNDARY_PROBES.js
 */
const fs = require("node:fs");
const vm = require("node:vm");
const assert = require("node:assert/strict");
const path = require("node:path");
const fixturePath = path.join(__dirname, "H05_TWO_DIFFERENT_CAPTURES_FIXTURE_20261113.js");
const fixtureText = fs.readFileSync(fixturePath, "utf8");
const marker = '  const old=move(B,"b",[3,8],[1,7]), revised=move(B,"b",[3,8],[5,7]);';
assert.equal(fixtureText.split(marker).length, 2, "pin unique instrumentation site");
const context = {console:{log(){}}};
vm.runInNewContext(fixtureText.replace(marker, '  globalThis.localGeometry={B0,move,checked};\n'+marker), context);
const {B0, move, checked} = context.localGeometry;
const results=[];
function check(name, f){f();results.push(name)}
let B=new Map(B0), prayers=0;
const prefix=[];
const redMoves=[[[3,4],[3,5]],[[3,5],[3,6]],[[3,6],[3,7]],[[3,7],[3,8]],[[7,4],[7,5]]];
for(let i=0;i<redMoves.length;i++){
  const [from,to]=redMoves[i],result=move(B,"r",from,to); B=result.board;
  assert.equal(checked(B,"b"),false,"H21 prayer cannot occur in check");
  assert.equal(checked(B,"r"),false,"H05 king safe");
  prefix.push({opportunity:"red"+(i+1),type:"ordinary-I",from,to,victim:result.victim});
  if(i<4){prayers++;prefix.push({opportunity:"black"+(i+1),type:"prayer-occupancy"});}
}
check("source-modeled four prayers followed by one complete red response",()=>{
  assert.equal(prayers,4);assert.equal(prefix.length,9);assert.equal(prefix.at(-1).opportunity,"red5");
  assert.equal(B.size,31);assert.equal(B.get("3,8").id,"r-P-3");
  assert.equal(B.get("2,10").id,"b-H-2");assert.equal(B.has("2,9"),false);
});
const oldIDs=["r-R-1","r-H-2","r-A-4","r-A-6"];
const newIDs=["r-R-1","r-H-2","r-A-4","r-H-8"];
function descent(ids){
  const board=new Map(B);
  for(const id of ids){
    const p=[...board].find(([,v])=>v.id===id);
    assert.ok(p && p[1].s==="r" && p[1].kind!=="K", "revealed enemy nonking pool");
    board.delete(p[0]);
  }
  return board;
}
const oldBegin=descent(oldIDs), newBegin=descent(newIDs);
const oldMove=move(oldBegin,"b",[2,10],[3,8]), newMove=move(newBegin,"b",[2,10],[3,8]);
check("H21 conditional begin: four distinct legal nonking targets per branch",()=>{
  assert.equal(new Set(oldIDs).size,4);assert.equal(new Set(newIDs).size,4);
});
check("same black horse and route still capture r-P-3 in both branches",()=>{
  assert.equal(oldMove.victim,"r-P-3");assert.equal(newMove.victim,"r-P-3");
  assert.equal(oldMove.board.get("3,8").id,newMove.board.get("3,8").id);
});
check("both local final boards have 26 pieces and safe kings",()=>{
  for(const r of [oldMove,newMove]){
    assert.equal(r.board.size,26);
    assert.equal(checked(r.board,"r"),false);assert.equal(checked(r.board,"b"),false);
  }
});
const deathsOld=new Set([...oldIDs,oldMove.victim]),deathsNew=new Set([...newIDs,newMove.victim]);
check("same command does not imply same complete destruction set",()=>{
  assert.equal(deathsOld.size,5);assert.equal(deathsNew.size,5);
  assert.ok(deathsOld.has("r-A-6")&&!deathsNew.has("r-A-6"));
  assert.ok(deathsNew.has("r-H-8")&&!deathsOld.has("r-H-8"));
});
check("turn+actor+main-victim collision cannot suppress changed begin deaths",()=>{
  const naive=()=>JSON.stringify(["black5","b-H-2","r-P-3"]);
  assert.equal(naive(),naive());
  assert.notDeepEqual([...deathsOld].sort(),[...deathsNew].sort());
});
check("same-main-capture question remains distinct from changed begin batch",()=>{
  assert.equal(oldMove.victim,newMove.victim);
  assert.notDeepEqual(oldIDs,newIDs);
  // Deliberately no assertion assigning A or B to this capture.
});
check("exact casualty-set comparison ignores random enumeration order only",()=>{
  assert.deepEqual([...oldIDs].sort(),[...oldIDs].reverse().sort());
  // Batch order canonicalization is NOT permission to reorder sequential effects.
});
function compareCause(a,b){
  const fields=["opportunity","actor","victim","source","phase","causalSlot","deathKind"];
  if(fields.some(k=>a[k]==null||b[k]==null))return "UNRESOLVED";
  return fields.every(k=>a[k]===b[k])?"SAME_CANDIDATE_ONLY":"DISTINCT_PROJECTION";
}
const base={opportunity:"black5",actor:"b-H-2",victim:"r-P-3",source:"ordinary-attack",phase:"main",causalSlot:"main/endpoint",deathKind:"capture"};
check("same scoped cause is only an A/B candidate, never automatic approval",()=>{
  assert.equal(compareCause(base,{...base}),"SAME_CANDIDATE_ONLY");
});
check("same victim via begin skill vs main capture must not collide",()=>{
  assert.equal(compareCause(base,{...base,source:"H21-whisper",phase:"begin",deathKind:"skill",causalSlot:"descent/batch"}),"DISTINCT_PROJECTION");
});
check("same victim in a different formal opportunity must not collide",()=>{
  assert.equal(compareCause(base,{...base,opportunity:"black6"}),"DISTINCT_PROJECTION");
});
check("missing causal source cannot be guessed equivalent",()=>{
  assert.equal(compareCause(base,{...base,source:null}),"UNRESOLVED");
});
check("same capture with H04 rain may have different terminal consequence, conditional only",()=>{
  const terminal=(rain,unlocked,legalCheck)=>unlocked&&rain&&legalCheck;
  assert.equal(terminal(false,true,true),false);assert.equal(terminal(true,true,true),true);
  assert.equal(terminal(true,true,false),false);assert.equal(terminal(true,false,true),false);
  // No reachable 15-round prefix, special H05 legality, or engine terminal asserted.
});
const ledger=new Map();
function accept(event){
  if(!event.committed)return "NO_EFFECT";
  const body=JSON.stringify(event);
  if(ledger.has(event.id)){
    if(ledger.get(event.id)!==body)throw Error("EVENT_ID_PAYLOAD_CONFLICT");
    return "RETRY";
  }
  ledger.set(event.id,body);return "ACCEPTED";
}
const event={id:"rewrite/black5/main",committed:true,victim:"r-P-3"};
check("identical committed event redelivery adds nothing",()=>{
  assert.equal(accept(event),"ACCEPTED");assert.equal(accept({...event}),"RETRY");assert.equal(ledger.size,1);
});
check("same delivery ID with changed payload is conflict, not benign retry",()=>{
  assert.throws(()=>accept({...event,victim:"r-P-5"}),/PAYLOAD_CONFLICT/);assert.equal(ledger.size,1);
});
check("failed candidate contributes no accepted new event",()=>{
  assert.equal(accept({id:"failed",committed:false}),"NO_EFFECT");assert.equal(ledger.size,1);
});
const locks=new Map();let draws=0;
function drawOnce(anchor,slot,draw){
  const key=JSON.stringify([anchor,slot]);
  if(!locks.has(key)){draws++;locks.set(key,draw())}
  return locks.get(key);
}
check("illustrative random slot lock reuses same result across retry",()=>{
  assert.equal(drawOnce("black5","descent",()=>0.1),0.1);
  assert.equal(drawOnce("black5","descent",()=>0.9),0.1);assert.equal(draws,1);
});
check("random slots are not global per-turn deduplication",()=>{
  assert.equal(drawOnce("black5","later-source",()=>0.9),0.9);assert.equal(draws,2);
});
check("formal opportunities remain one rewritten opponent plus one H05 occupancy",()=>{
  const effective=new Map([["black5","old"]]);effective.set("black5","rewrite");effective.set("red6","H05-occupancy");
  assert.equal(effective.size,2);
});
console.log(JSON.stringify({
  status:"PASS_LOCAL_MODEL_ONLY",checks:results.length,cases:results,
  conditionalFixture:{prefix,prefixFormalOpportunities:prefix.length,ordinaryMoves:redMoves.length,prayers,preBeginPieces:B.size,oldBeginDeaths:oldIDs,newBeginDeaths:newIDs,
    sameMainVictim:oldMove.victim,finalPieces:oldMove.board.size},
  notVerified:["production H21 prayer/descent and full H05 transaction","actual mode admission",
    "H04 15 bilateral rounds and H05 terminal legality","production RNG or network",
    "formal reset multiplicity or segment IDs","source engine or independent QA"],
  captureDedupPolicy:"A/B_UNCONFIRMED"
},null,2));
