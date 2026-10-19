"""MC2 figure: four branches in parallel between two rails, each R in series with an emf, all facing the same way: E, E (branch through A), E, 2E. The rail voltage is the mean emf 5E/4, so the current through A is |E - 5E/4|/R = E/(4R) (answer 4). Adapted: equal R, any emfs; returns the current in branch `branch` (amps)."""


def solve(emfs=(4, 4, 4, 8), resistance=1, branch=1):
    rail = sum(emfs) / len(emfs)
    return abs(emfs[branch] - rail) / resistance


def check(emfs=(4, 4, 4, 8), resistance=1, branch=1):
    # Bisect on the rail voltage until the branch currents sum to zero (KCL).
    lo, hi = min(emfs) - 1.0, max(emfs) + 1.0
    for _ in range(200):
        v = (lo + hi) / 2
        net = sum((e - v) / resistance for e in emfs)
        if net > 0:
            lo = v
        else:
            hi = v
    v = (lo + hi) / 2
    return abs((emfs[branch] - v) / resistance)


PARAMS = {"emfs": (4, 4, 4, 8), "resistance": 1, "branch": 1}
VARIANTS = [{"emfs": (6, 12, 3), "resistance": 3, "branch": 0}, {"emfs": (2, 5, 9, 4, 10), "branch": 3}, {"resistance": 2}]
ANSWER = 1.0
