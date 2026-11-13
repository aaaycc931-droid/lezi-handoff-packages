"""HISTORICAL geometry-only H05 repetition-5 probe; NOT official Lezi engine.\n\nCORRECTION 2026-11-13: This 16-ply fixture only compares board+side, not\nsource-eligible decision phase or public hero rights. Its P5 is NOT proven\nvalid official repetition and MUST NOT be used as a repetition draw case.\nUse H05_FIFTH_REPETITION_PHASE_AWARE_20261113.py for the newer conditional\n20-ply source-phase model. Even that does NOT verify full Lezi public keys.

Run beside H05_SIX_CHECK_FIXTURE_20261112.py:
    python H05_FIFTH_REPETITION_PREWINDOW_FIXTURE_20261113.py

Only exact ordinary 32-piece Xiangqi geometry + side to act is compared.
Real public-effective equality includes mode, eligible phase and source-relevant
public rights/effects, which this script DOES NOT verify.
"""
from collections import Counter
from H05_SIX_CHECK_FIXTURE_20261112 import P, do, in_check

CYCLE = (
    ("r", (2,1), (3,3)),
    ("b", (2,10), (3,8)),
    ("r", (3,3), (2,1)),
    ("b", (3,8), (2,10)),
)

def key(board, next_side):
    return next_side, tuple(sorted(board.items()))

def run():
    board=P.copy()
    base=key(board,"r")
    accepted=Counter({base: 1})   # initial stable sample, if source permits
    pending=None
    prefix=[]
    for cycle in range(1,5):
        for i,(side,fr,to) in enumerate(CYCLE):
            before=board.copy()
            label=f"C{cycle}_T{i+1}"
            board,killed=do(board,side,label,fr,to)
            assert killed is None
            assert not in_check(board,"r") and not in_check(board,"b")
            assert len(board)==32
            outcome=key(board,"b" if side=="r" else "r")
            prefix.append((cycle,side,fr,to))
            if cycle==4 and i==3:
                pending=(before,board.copy(),outcome)
            else:
                accepted[outcome]+=1
                assert accepted[outcome]<=4,("early fifth occurrence",label)
    assert len(prefix)==16 and pending is not None
    before,old_board,old_key=pending
    assert old_key==base and accepted[base]==4
    assert not in_check(old_board,"r") and not in_check(old_board,"b")

    revised,killed=do(before,"b","BLACK8_REWRITE",(3,8),(5,9))
    revised_key=key(revised,"r")
    assert killed is None and len(revised)==32
    assert revised_key!=old_key and accepted[revised_key]==0
    assert not in_check(revised,"r") and not in_check(revised,"b")

    # Hypothetical same-phase eligible sample at source-allowed point.
    decline=accepted.copy();decline[old_key]+=1
    success=accepted.copy();success[revised_key]+=1
    assert decline[base]==5
    assert success[base]==4 and success[revised_key]==1

    print("PASS 16 ordinary legal moves, no captures or checks, 32 bodies")
    print("PASS initial board+red-to-act sample P is 4 before pending BLACK8")
    print("PASS BLACK8 original would become P5 if formally sampled")
    print("PASS BLACK8 rewritten horse (3,8)->(5,9) creates a different Q")
    print("PASS pending P5 omitted on successful rewrite, Q1 if source-eligible")
    print("NOT TESTED full Lezi repetition public key, phase legality, hero skill")
    print("NOT DECIDED black original opportunity versus red H05 occupancy sampling")

if __name__=="__main__":
    run()
