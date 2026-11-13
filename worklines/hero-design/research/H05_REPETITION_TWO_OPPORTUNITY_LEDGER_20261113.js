/**
 * Research-only deterministic ledger model for H05 two-opportunity repetition sampling.
 * Synthetic keys and phases, NOT actual Lezi engine or adjudication implementation.
 * Run: node H05_REPETITION_TWO_OPPORTUNITY_LEDGER_20261113.js
 */
function runProbes(){
  const passed=[];
  const assert=(x,msg)=>{if(!x)throw Error(msg)};
  function fresh(){
    return {audit:[], samples:new Map(), active:new Map([["S1:P",4]]), segment:"S1", used:false, closed:false, terminal:null, stagedTerminal:null, formal:new Set(), phase:"h05_window"};
  }
  function acceptSample(s,{id,key,phase,side,stable,terminalSuppression=false}){
    if(!stable||s.terminal||terminalSuppression)return false;
    const composite=`${s.segment}:${phase}:${side}:${key}`;
    const prior=s.samples.get(id);
    if(prior){if(prior!==composite)throw Error(`conflicting committed sample ${id}`);return false}
    s.samples.set(id,composite);
    let count=(s.active.get(composite)||0)+1;
    s.active.set(composite,count);
    if(count>=5)s.stagedTerminal={kind:"repetition5",id,key,phase,side};
    return true;
  }
  function setupP4(s){s.active.set("S1:red_h05_prebegin:red:P_ready",4);}
  function play({rewrite=false,oldKey="P_ready",newKey="Q_ready",redStable=true,redKey="Q_used",blackNewTerminal=false,alreadyTerminal=false,redPhase="black_post_begin"}={}){
    let s=fresh();s.active.clear();setupP4(s);
    if(alreadyTerminal){s.terminal={kind:"established"};return s}
    // Input old black opportunity is waiting; neither skill UI click nor rewind samples.
    if(!rewrite){
      acceptSample(s,{id:"black10",key:oldKey,phase:"red_h05_prebegin",side:"red",stable:true});
      if(s.stagedTerminal)s.terminal=s.stagedTerminal;
      return s;
    }
    s.audit.push({id:"black10",oldKey,priorResult:"accepted_old_path_for_audit"});
    s.formal.add("black10");
    // H05 action and rewritten opponent form one source transaction, no intermediate public commit.
    acceptSample(s,{id:"black10",key:blackNewTerminal?"P_ready":newKey,phase:"red_h05_prebegin",side:"red",stable:true});
    s.formal.add("red11");s.used=true;s.closed=true;
    // Official terminal at H05 atomic closure, not in the trial branch.
    if(s.stagedTerminal){s.terminal=s.stagedTerminal;return s}
    acceptSample(s,{id:"red11",key:redKey,phase:redPhase,side:"black",stable:redStable});
    if(s.stagedTerminal)s.terminal=s.stagedTerminal;
    return s;
  }
  let a=play();assert(a.active.get("S1:red_h05_prebegin:red:P_ready")===5&&a.terminal&&a.samples.size===1,"decline path P5");passed.push("decline path samples old P5 before any H05 own opportunity");
  a=play({rewrite:true});assert(a.samples.size===2&&a.formal.size===2&&a.used&&a.closed&&!a.terminal,"successful two sample opportunities");passed.push("rewrite uses two distinct accepted formal opportunities and samples");
  assert(a.active.get("S1:red_h05_prebegin:red:P_ready")===4,"old pending P must not be accepted");passed.push("pending old P is excluded, old previous P4 retained");
  let before=a.samples.size;let again=acceptSample(a,{id:"red11",key:"Q_used",phase:"black_post_begin",side:"black",stable:true});assert(!again&&a.samples.size===before,"duplicate");passed.push("identical delivery cannot duplicate red sample");
  let conflict=false;try{acceptSample(a,{id:"red11",key:"P_used",phase:"black_post_begin",side:"black",stable:true})}catch{conflict=true}assert(conflict,"conflict not rejected");passed.push("different key for accepted formal ID rejected");
  let t=fresh();t.active.clear();acceptSample(t,{id:"e1",key:"P",phase:"red_h05_prebegin",side:"red",stable:true});acceptSample(t,{id:"e2",key:"P",phase:"black_post_begin",side:"black",stable:true});assert(t.active.size===2,"phase side equivalence");passed.push("identical ordinary board but different side/phase not equal");
  a=play({rewrite:true,blackNewTerminal:true});assert(a.samples.size===1&&a.formal.size===2&&a.used&&a.closed&&a.terminal?.kind==="repetition5","terminal before second sample");passed.push("hypothetical rewritten black P5 draw seals at H05 occupation closure, suppress red sample");
  a=play({rewrite:true,alreadyTerminal:true});assert(a.samples.size===0&&!a.used&&!a.closed,"already terminal");passed.push("already official terminal prevents H05 activation");
  a=play({rewrite:true,redStable:false});assert(a.samples.size===1&&!a.terminal,"no stable after black begin");passed.push("no red11 sample while required next-phase effects remain unclosed");
  let u=fresh();u.active.clear();u.segment="S2";u.audit.push({oldSegment:"S1",capture:true});acceptSample(u,{id:"red11",key:"P",phase:"black_post_begin",side:"black",stable:true});assert(u.active.get("S2:black_post_begin:black:P")===1&&u.audit.length===1,"segment");passed.push("actual accepted prior destruction retains new segment; restoration does not reverse it");
  t=fresh();t.active.clear();acceptSample(t,{id:"k1",key:"P_unused",phase:"red_h05_prebegin",side:"red",stable:true});acceptSample(t,{id:"k2",key:"P_used",phase:"red_h05_prebegin",side:"red",stable:true});assert(t.active.size===2,"right keyed");passed.push("if public source-effective H05 right differs, equal board must not force same repetition key");
  a=play({rewrite:true,redStable:true,redKey:"post_required_black_begin_effect"});assert(a.samples.get("red11").endsWith("post_required_black_begin_effect"),"black begin");passed.push("own occupation sample must reflect source-allowed post-required-effects state");
  return {passed:passed.length,cases:passed,level:"synthetic phase/ledger specification checks only; NOT official Lezi engine nor fully specified public key"};
}
console.log(JSON.stringify(runProbes(),null,2));
