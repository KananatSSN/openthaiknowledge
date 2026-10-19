"""Short7: cut a wire R into R1 and R - R1 and join them in parallel; R1 (R - R1)/R is largest, R/4, at R1 = R/2. Ohms."""


def solve(resistance=12):
    return resistance / 4


def check(resistance=12):
    # Scan the cut position finely.
    best = 0.0
    for k in range(1, 100000):
        r1 = resistance * k / 100000
        best = max(best, r1 * (resistance - r1) / resistance)
    return best


PARAMS = {"resistance": 12}
VARIANTS = [{"resistance": 100}, {"resistance": 1}, {"resistance": 36}]
TOL = 1e-8
ANSWER = 3.0
