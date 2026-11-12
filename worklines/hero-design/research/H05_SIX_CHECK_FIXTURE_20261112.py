"""Independent, limited Xiangqi geometry validator. Not the Lezi engine."""
from collections import Counter
from copy import deepcopy

START = "RHEAKAEHR"
P = {}
for side, home, cannon, pawn in (("r",1,3,4),("b",10,8,7)):
    for x,k in enumerate(START,1): P[x,home]=(side,k)
    for x in (2,8): P[x,cannon]=(side,"C")
    for x in (1,3,5,7,9): P[x,pawn]=(side,"P")

MOVES = [
("r","R1",(4,1),(5,2)),("b","B1",(9,10),(9,9)),
("r","R2",(5,2),(6,3)),("b","B2",(9,9),(4,9)),
("r","R3",(1,4),(1,5)),("b","B3",(4,9),(4,2)),
("r","R4",(7,4),(7,5)),("b","B4",(4,2),(5,2)),
("r","R5",(5,1),(4,1)),("b","B5",(5,2),(4,2)),
("r","R6",(4,1),(5,1)),("b","B6",(4,2),(5,2)),
("r","R7",(5,1),(4,1)),("b","B7",(5,2),(4,2)),
("r","R8",(4,1),(5,1)),("b","B8",(4,2),(5,2)),
("r","R9",(5,1),(4,1)),("b","B9",(5,2),(4,2)),
]

def legal_shape(b, fr, to):
    side,kind=b[fr]
    if not 1<=to[0]<=9 or not 1<=to[1]<=10 or fr==to:return False
    if to in b and b[to][0]==side:return False
    dx,dy=to[0]-fr[0],to[1]-fr[1]
    ax,ay=abs(dx),abs(dy)
    direction=1 if side=="r" else -1
    if kind in ("R","C") and (dx==0 or dy==0):
        steps=max(ax,ay)
        mid=[(fr[0]+(i*(1 if dx>0 else -1) if dx else 0),
              fr[1]+(i*(1 if dy>0 else -1) if dy else 0)) for i in range(1,steps)]
        occupied=sum(p in b for p in mid)
        return occupied==0 if kind=="R" else occupied==(1 if to in b else 0)
    if kind=="H":
        leg=(fr[0],fr[1]+(1 if dy>0 else -1)) if (ax,ay)==(1,2) else (
            (fr[0]+(1 if dx>0 else -1),fr[1]) if (ax,ay)==(2,1) else None)
        return leg is not None and leg not in b
    if kind=="P":
        return (dx==0 and dy==direction) or (ax==1 and dy==0 and
           (fr[1]>=6 if side=="r" else fr[1]<=5))
    if kind=="A":
        return ax==ay==1 and 4<=to[0]<=6 and (1<=to[1]<=3 if side=="r" else 8<=to[1]<=10)
    if kind=="E":
        return ax==ay==2 and ((to[1]<=5) if side=="r" else (to[1]>=6)) and (
          fr[0]+dx//2,fr[1]+dy//2) not in b
    if kind=="K":
        if ax+ay==1 and 4<=to[0]<=6 and (1<=to[1]<=3 if side=="r" else 8<=to[1]<=10): return True
        if dx==0 and b.get(to) is not None and b[to][1]=="K":
            return all((fr[0],y) not in b for y in range(min(fr[1],to[1])+1,max(fr[1],to[1])))
    return False

def in_check(b, side):
    k=next(pos for pos,piece in b.items() if piece==(side,"K"))
    enemy="r" if side=="b" else "b"
    return any(p[0]==enemy and legal_shape(b,pos,k) for pos,p in b.items())

def do(b, side, label, fr, to):
    assert b.get(fr,(None,None))[0]==side,(label,"wrong source")
    assert legal_shape(b,fr,to),(label,"illegal geometry",fr,to)
    new=b.copy()
    victim=new.pop(to,None)
    new[to]=new.pop(fr)
    assert not in_check(new,side),(label,"own king unsafe")
    return new,victim

def key(b,next_side):
    return tuple(sorted(b.items())),next_side

def probe():
    b=P.copy(); snapshots={}; checks=[]; repetition=Counter(); captures=0
    for side,label,fr,to in MOVES:
        snapshots[label+"_BEFORE"]=b.copy()
        b,victim=do(b,side,label,fr,to)
        captures+=victim is not None
        if side=="b" and in_check(b,"r"):checks.append(label)
        repetition[key(b,"r" if side=="b" else "b")]+=1
        assert not in_check(b,side)
    assert checks==["B4","B5","B6","B7","B8","B9"],checks
    assert captures==0 and len(b)==32
    assert max(repetition.values())==3
    old_b9=b
    revised_b9,_=do(snapshots["B9_BEFORE"],"b","B9_REWRITE",(5,2),(5,3))
    assert in_check(old_b9,"r") and not in_check(revised_b9,"r")
    b10_check,_=do(revised_b9,"b","B10_PROPOSED",(5,3),(4,3))
    assert in_check(b10_check,"r") and not in_check(b10_check,"b")
    b10_no_check,_=do(revised_b9,"b","B10_ALTERNATIVE",(5,3),(5,2))
    assert not in_check(b10_no_check,"r")
    print("PASS restricted geometry: 18 legal moves, B4..B9 six consecutive checks")
    print("PASS no capture, 32 pieces remain, max board+side-to-act repetitions 3")
    print("PASS B9 old checking move can be changed to noncheck (5,2)->(5,3)")
    print("PASS B10 candidate (5,3)->(4,3) checks by geometry")
    print("UNTESTED: H05 actual engine transaction / 7th forbidden adjudication")
if __name__=="__main__":probe()
