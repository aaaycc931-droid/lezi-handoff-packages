"""Phase-aware H05 fifth repetition fixture (independent geometry; NOT Lezi engine).

Requirements: sibling H05_SIX_CHECK_FIXTURE_20261112.py from this branch.
Run: python H05_FIFTH_REPETITION_PHASE_AWARE_20261113.py

Hypothetical uniform mode / stable phases / constant public hero rights are
a research assumption, not a validated full effective-state key or hero mode pool.
"""
from collections import Counter
from H05_SIX_CHECK_FIXTURE_20261112 import P, do, in_check

HORSE = {
  "r": {
    "L": ((2, 1), (3, 3)),
    "R": ((8, 1), (7, 3)),
  },
  "b": {
    "L": ((2, 10), (3, 8)),
    "R": ((8, 10), (7, 8)),
  },
}
PATTERNS = (("L", "L"), ("R", "L"), ("L", "R"), ("R", "R"), ("L", "L"))
MODE = "hypothetical_H05_enabled_standard_geometry"
H05_READY = "H05_public_right_available"  # unresolved source field map

def key(board, phase, rights=H05_READY):
    return (MODE, phase, rights, tuple(sorted(board.items())))

def run():
    board=P.copy()
    initial=key(board, "red_opening_before_begin")
    counts=Counter({initial:1})
    trace=[]
    final_pending=None
    for ci,(red_choice,black_choice) in enumerate(PATTERNS,1):
        r0,r1=HORSE["r"][red_choice]
        b0,b1=HORSE["b"][black_choice]
        seq=(("r",r0,r1),("b",b0,b1),("r",r1,r0),("b",b1,b0))
        for j,(side,fr,to) in enumerate(seq,1):
            before=board.copy()
            board,killed=do(board,side,f"C{ci}-T{j}",fr,to)
            assert killed is None and len(board)==32
            assert not in_check(board,"r") and not in_check(board,"b")
            phase="red_H05_pre_begin" if side=="b" else "black_normal_decision"
            current=key(board,phase)
            trace.append((ci,j,side,fr,to))
            if ci==5 and j==4: final_pending=(before,current)
            else:
                counts[current]+=1
                assert counts[current] < 5, ("premature 5th key", ci,j,counts[current])
    assert len(trace)==20
    assert final_pending is not None
    before,old=final_pending
    Pkey=key(P,"red_H05_pre_begin")
    assert old==Pkey and counts[Pkey]==4
    assert key(P,"red_opening_before_begin")!=Pkey
    assert before[(3,8)] == ("b","H")
    alt,killed=do(before,"b","B10_H05_REDIRECT",(3,8),(5,9))
    assert killed is None and len(alt)==32
    assert not in_check(alt,"r") and not in_check(alt,"b")
    Qkey=key(alt,"red_H05_pre_begin")
    assert Qkey!=Pkey and counts[Qkey]==0
    decline=counts.copy()
    decline[Pkey]+=1
    success=counts.copy()
    success[Qkey]+=1
    assert decline[Pkey]==5 and success[Pkey]==4 and success[Qkey]==1
    print("PASS 20 ordinary chess moves, no captures/checks, 32 bodies remain")
    print("PASS opening red normal phase distinct from later red H05 prebegin phase")
    print("PASS four prior matching red H05 prebegin P keys; fifth B10 P is pending")
    print("PASS no different earlier key reaches five within hypothetical phase model")
    print("PASS H05 redirects same B10 black horse (3,8)->(5,9), Q differs from P")
    print("CONDITIONAL full public rights/phase fieldmap and real stable sampling point")
    print("NOT PASS official Lezi H05, repetition adjudication or any game engine")

if __name__=="__main__": run()
