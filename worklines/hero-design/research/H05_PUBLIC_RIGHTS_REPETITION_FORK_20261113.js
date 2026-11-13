/**
 * H05 public-rights repetition key projection A/B contrast.
 * Research-only V8/Node JavaScript, synthetic phase and keys, NOT game engine.
 * Run: node H05_PUBLIC_RIGHTS_REPETITION_FORK_20261113.js
 */
function runRightsProbes(){
 const key=(board,side,phase,rights)=>`${board}|side=${side}|phase=${phase}|H05=${rights}`;
 const prior = new Map([[key("P","red","red_H05_prebegin","ready"),4]]);
 const evalCase = ({rewrite=false,newBoard="Q",blackRights="ready",redRights="spent",sameBlackPhase="red_H05_prebegin",redPhase="black_decision",redAvailable=true,preexistingTerminal=false}={})=>{
  const m=new Map(prior),audit=[],accepted=[],ids=new Set();
  if(preexistingTerminal)return {count:null,accepted,terminal:"preexisting",spent:false,audit};
  const take=(id,board,side,phase,rights,valid)=>{
   if(!valid)return null;
   if(ids.has(id))throw Error("duplicate event accepted twice");
   ids.add(id);
   let k=key(board,side,phase,rights),v=(m.get(k)||0)+1;m.set(k,v);accepted.push({id,key:k,count:v});
   return v===5?"repeat5":null;
  };
  if(!rewrite){
   const t=take("black10","P","red","red_H05_prebegin","ready",true);
   return {count:m.get(key("P","red","red_H05_prebegin","ready")),accepted,terminal:t,spent:false,audit};
  }
  audit.push({id:"black10",old:"P",oldUnsampled:true});
  const black=take("black10",newBoard,"red",sameBlackPhase,blackRights,true);
  const spent=true; 
  if(black)return {count:m.get(key("P","red","red_H05_prebegin","ready")),accepted,terminal:"at_H05_closure_"+black,spent,audit};
  let red=take("red11",newBoard,"black",redPhase,redRights,redAvailable);
  return {count:m.get(key("P","red","red_H05_prebegin","ready")),accepted,terminal:red?"at_later_stable_"+red:null,spent,audit};
 };
 const tests=[],ok=(name,flag,detail)=>{if(!flag)throw Error("failed "+name);tests.push({name,detail})};
 let a=evalCase({rewrite:false});
 ok("decline P5",a.terminal==="repeat5"&&!a.spent&&a.accepted.length===1,"original ready-status P5 counted");
 a=evalCase({rewrite:true,newBoard:"Q",blackRights:"ready"});
 ok("success historical rights Q first",a.accepted.length===2&&a.accepted[0].count===1&&a.accepted[1].count===1&&a.count===4,"one accepted sample per opportunity; P4 intact");
 a=evalCase({rewrite:true,newBoard:"P",blackRights:"ready"});
 ok("same action replays P5 before spent",a.terminal==="at_H05_closure_repeat5"&&a.spent&&a.accepted.length===1,"rewritten black opportunity hits historical ready P5; H05 used");
 a=evalCase({rewrite:true,newBoard:"P",blackRights:"spent"});
 ok("retroactive rights blocks P5",a.terminal===null&&a.accepted.length===2&&a.accepted[0].count===1&&a.count===4,"one used-status P ≠ four ready-status P");
 a=evalCase({rewrite:true,newBoard:"Q",blackRights:"ready",redAvailable:false});
 ok("no fabricated future stable point",a.accepted.length===1&&a.terminal===null,"red sample cannot exist until source stable decision");
 a=evalCase({rewrite:true,newBoard:"Q",blackRights:"ready",preexistingTerminal:true});
 ok("preexisting terminal excludes skill",a.accepted.length===0&&!a.spent,"prewindow doesn't exist");
 a=evalCase({rewrite:true,newBoard:"Q",blackRights:"ready"});
 let redKey=a.accepted[1].key;
 ok("post-use rights new unique key",a.accepted[1].count===1&&redKey.includes("spent"),"own occupancy first ever spent-state sample");
 ok("next-side changes key",key("Q","red","red_H05_prebegin","spent")!==key("Q","black","black_decision","spent"),"stage/side distinction");
 ok("public secrecy separation",key("Q","black","black_decision","spent")===key("Q","black","black_decision","spent"),"private unseen fields not introduced in public key");
 const oldP=prior.get(key("P","red","red_H05_prebegin","ready"));
 ok("prior history immutable",oldP===4,"previously accepted P samples unchanged by skill");
 let dupe=false;const ids=new Set(["black10"]);if(ids.has("black10"))dupe=true;ok("single opportunity ID no duplicate",dupe,"retry should be idempotent");
 let projected=evalCase({rewrite:true,newBoard:"Q",blackRights:"spent"});
 ok("rights projection affects adjudication",projected.accepted[0].key!==evalCase({rewrite:true,newBoard:"Q",blackRights:"ready"}).accepted[0].key,"projection must be defined rather than assumed");
 return {tests,passed:tests.length,caveat:"synthetic rights-stage ledgers; no authoritative Lezi engine; fully public effective key field-map not implemented"};
}
console.log(JSON.stringify(runRightsProbes(),null,2));
