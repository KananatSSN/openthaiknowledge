"""Theory 1.1.1 figure 1.1: bars of metals 1 and 2 (lengths L1, L2) side by side with a bar of metal 3 of length L1 + L2; sound v = sqrt(Y/rho) takes the same time through both paths. With Y1 = Y3/3, Y2 = 2Y3, rho1 = 3rho3, rho2 = rho3/2 the slownesses relative to metal 3 are 3 and 1/2, so L1/L2 = 1/4. Adapted: relative slownesses s1 > 1 > s2, L1/L2 = (1 - s2)/(s1 - 1)."""


def solve(slow1=3.0, slow2=0.5):
    return (1 - slow2) / (slow1 - 1)


def check(slow1=3.0, slow2=0.5):
    # Bisect on L1 (with L2 = 1) until the two travel times agree.
    def gap(l1):
        return (l1 * slow1 + 1 * slow2) - (l1 + 1) * 1.0

    lo, hi = 0.0, 1e6
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if gap(mid) < 0 else (lo, mid)
    return lo


PARAMS = {"slow1": 3.0, "slow2": 0.5}
VARIANTS = [{"slow1": 2.0}, {"slow2": 0.25}, {"slow1": 1.5, "slow2": 0.75}]
ANSWER = 0.25
TOL = 1e-9
