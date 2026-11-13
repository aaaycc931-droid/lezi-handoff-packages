/** 13-ply ordinary Xiangqi dual-capture H05 test, geometry + abstract IDs only, NOT game engine. Run: node H05_TWO_DIFFERENT_CAPTURES_FIXTURE_20261113.js */
function runDualCapture(){
  const pos=(x,y)=>`${x},${y}`, B0=new Map();
  for(const [s,r,cr,pr] of [["r",1,3,4],["b",10,8,7]]){
    [..."RHEAKAEHR"].forEach((kind,i)=>B0.set(pos(i+1,r),{s,kind,id:`${s}-${kind}-${i+1}`}));
    for(const x of [2,8])B0.set(pos(x,cr),{s,kind:"C",id:`${s}-C-${x}`});
    for(const x of [1,3,5,7,9])B0.set(pos(x,pr),{s,kind:"P",id:`${s}-P-${x}`});
  }
  const legal=(B,F,T)=>{
    const v=B.get(pos(...F));if(!v||T[0]<1||T[0]>9||T[1]<1||T[1]>10||String(F)===String(T)||B.get(pos(...T))?.s===v.s)return false;
    const [dx,dy]=[T[0]-F[0],T[1]-F[1]],[ax,ay]=[Math.abs(dx),Math.abs(dy)],target=B.get(pos(...T));
    const empty=(x,y)=>!B.has(pos(x,y));
    const countBetween=()=>{let n=0;for(let x=F[0]+Math.sign(dx),y=F[1]+Math.sign(dy);x!==T[0]||y!==T[1];x+=Math.sign(dx),y+=Math.sign(dy))n+=!empty(x,y)?1:0;return n};
    if(v.kind==="H")return ax===1&&ay===2&&empty(F[0],F[1]+Math.sign(dy))||ax===2&&ay===1&&empty(F[0]+Math.sign(dx),F[1]);
    if(v.kind==="P")return !dx&&dy===(v.s==="r"?1:-1)||ax===1&&!dy&&(v.s==="r"?F[1]>=6:F[1]<=5);
    if(v.kind==="E")return ax===2&&ay===2&&empty(F[0]+dx/2,F[1]+dy/2)&&(v.s==="r"?T[1]<=5:T[1]>=6);
    if(v.kind==="A")return ax===1&&ay===1&&T[0]>=4&&T[0]<=6&&(v.s==="r"?T[1]<=3:T[1]>=8);
    if(v.kind==="R")return (!dx||!dy)&&countBetween()===0;
    if(v.kind==="C")return (!dx||!dy)&&countBetween()===(target?1:0);
    if(v.kind==="K")return ax+ay===1&&T[0]>=4&&T[0]<=6&&(v.s==="r"?T[1]<=3:T[1]>=8)||!dx&&target?.kind==="K"&&countBetween()===0;
    return false;
  };
  const checked=(B,s)=>{let k=[...B].find(([,v])=>v.kind==="K"&&v.s===s);if(!k)throw Error("king missing");const point=k[0].split(",").map(Number);return [...B].some(([p,v])=>v.s!==s&&legal(B,p.split(",").map(Number),point))};
  const move=(B,s,F,T)=>{const v=B.get(pos(...F));if(v?.s!==s||!legal(B,F,T))throw Error("illegal "+s+F+"->"+T);const N=new Map(B),hit=N.get(pos(...T));N.set(pos(...T),v);N.delete(pos(...F));if(checked(N,s))throw Error("king unsafe "+s);return {board:N,victim:hit?.id||null,checkEnemy:checked(N,s==="r"?"b":"r")}};
  const steps=[
    ["r",[1,4],[1,5]],["b",[1,7],[1,6]],["r",[5,4],[5,5]],["b",[5,7],[5,6]],
    ["r",[1,5],[1,6]],["b",[2,10],[3,8]],["r",[5,5],[5,6]],["b",[9,10],[9,9]],
    ["r",[1,6],[1,7]],["b",[9,9],[9,10]],["r",[5,6],[5,7]],["b",[2,8],[2,7]],
    ["r",[7,4],[7,5]]
  ];
  let B=B0, history=[];
  for(const [s,F,T] of steps){const a=move(B,s,F,T);B=a.board;history.push({side:s,from:F,to:T,capture:a.victim,check:a.checkEnemy})}
  const old=move(B,"b",[3,8],[1,7]), revised=move(B,"b",[3,8],[5,7]);
  const A="r-P-1", C="r-P-5";
  const assert=(test,msg)=>{if(!test)throw Error(msg)};
  assert(history.length===13,"prefix");
  assert(history.filter(a=>!!a.capture).length===2,"two prior captures");
  assert(history.every(a=>!a.check),"no checks");
  assert(B.size===30,"30 before black7");
  assert(old.victim===A&&revised.victim===C,"captured distinct pawn identities");
  assert(old.board.size===29&&revised.board.size===29,"each variant 29 survivors");
  assert(old.board.get("5,7")?.id===C&&revised.board.get("1,7")?.id===A,"opposite survivor identities");
  assert(!checked(old.board,"r")&&!checked(old.board,"b")&&!checked(revised.board,"r")&&!checked(revised.board,"b"),"kings safe");
  const audit=[],opportunityID="black7",effectiveHistory=new Map();
  const acceptedEvent=(eventID,version,victim)=>{if(audit.some(x=>x.eventID===eventID))return false;audit.push({eventID,opportunityID,version,victim,type:"accepted_capture"});return true};
  assert(acceptedEvent("black7:old:cap",0,old.victim),"accepted old");
  effectiveHistory.set(opportunityID,{version:0,victim:old.victim});
  assert(acceptedEvent("black7:rewrite:cap",1,revised.victim),"accepted replay");
  effectiveHistory.set(opportunityID,{version:1,victim:revised.victim});
  assert(!acceptedEvent("black7:rewrite:cap",1,revised.victim),"retry not new");
  assert(audit.length===2&&effectiveHistory.size===1,"two capture event IDs but one effective formal opp");
  assert(effectiveHistory.get(opportunityID).victim===C,"effective replay captured center pawn");
  return {pass:true,level:"ordinary Xiangqi geometry + illustrative abstract versioned event IDs only",prefixPlies:history.length,oldVictim:old.victim,newVictim:revised.victim,originalBoardPieces:B.size,oldBoardPieces:old.board.size,newBoardPieces:revised.board.size,distinctAcceptedCaptureEventIDs:audit.length,effectiveFormalOpportunityIDs:effectiveHistory.size,retryAdded:false,trace:history};
}
console.log(JSON.stringify(runDualCapture(),null,2));
