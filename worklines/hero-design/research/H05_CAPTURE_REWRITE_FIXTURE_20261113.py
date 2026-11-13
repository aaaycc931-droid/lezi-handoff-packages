"""Two-way H05 capture/non-capture replay geometry probes.

Independent ordinary 32-piece Xiangqi geometry only. Not the Lezi engine.
Run from this directory: python H05_CAPTURE_REWRITE_FIXTURE_20261113.py
"""
from H05_SIX_CHECK_FIXTURE_20261112 import P, do, in_check

PRE = (
    ("r", "R1", (5,4), (5,5)),
    ("b", "B1", (5,7), (5,6)),
    ("r", "R2", (5,5), (5,6)),
    ("b", "B2", (2,10), (3,8)),
    ("r", "R3", (5,6), (5,7)),
)

def run():
    board = P.copy()
    for side, name, fr, to in PRE:
        board, _ = do(board, side, name, fr, to)
    assert len(board)==31
    assert board[(3,8)] == ("b","H")
    assert board[(5,7)] == ("r","P")
    assert not in_check(board, "r") and not in_check(board, "b")

    capture, killed = do(board, "b", "B3_CAPTURE", (3,8),(5,7))
    simple, not_killed = do(board, "b", "B3_MOVE", (3,8),(2,10))
    assert killed == ("r","P") and not_killed is None
    assert len(capture)==30 and len(simple)==31
    assert capture[(5,7)] == ("b","H")
    assert simple[(5,7)] == ("r","P")
    assert not in_check(capture, "r") and not in_check(capture, "b")
    assert not in_check(simple, "r") and not in_check(simple, "b")

    print("PASS: five-step ordinary 32-piece reachable prefix")
    print("PASS: original B3 captures red P, H05 rewritten B3 is non-capture")
    print("PASS: original B3 non-capture, H05 rewritten B3 captures red P")
    print("PASS: both variants ordinary-geometrically legal, kings safe")
    print("PASS: old capture state 30 bodies; alternate restores P and 31 bodies")
    print("UNTESTED: project H05 engine, official phase/counters/repetition/replay ledger")

if __name__ == "__main__":
    run()
