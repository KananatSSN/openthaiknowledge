"""MC19 figure: six resistors join four nodes A, Q, S, B pairwise (A-Q, Q-S, S-B, Q-B, A-S, A-B). With all equal to R the network between A and B is R/2 (answer 2). Adapted: any six values; ohms."""

from fractions import Fraction


def _parallel(*rs):
    return 1 / sum(Fraction(1) / r for r in rs)


def solve(aq=10, qs=10, sb=10, qb=10, as_=10, ab=10):
    # Star-mesh: nodal equations for Q and S with A at 1 V and B at 0.
    g = {k: Fraction(1, v) for k, v in dict(aq=aq, qs=qs, sb=sb, qb=qb, as_=as_, ab=ab).items()}
    # Q: (1 - q) g_aq + (s - q) g_qs + (0 - q) g_qb = 0
    # S: (1 - s) g_as + (q - s) g_qs + (0 - s) g_sb = 0
    a11, a12, b1 = g["aq"] + g["qs"] + g["qb"], -g["qs"], g["aq"]
    a21, a22, b2 = -g["qs"], g["as_"] + g["qs"] + g["sb"], g["as_"]
    det = a11 * a22 - a12 * a21
    q = (b1 * a22 - a12 * b2) / det
    s = (a11 * b2 - b1 * a21) / det
    current = (1 - q) * g["aq"] + (1 - s) * g["as_"] + g["ab"]
    return 1 / current


def check(aq=10, qs=10, sb=10, qb=10, as_=10, ab=10):
    # Relax the node potentials iteratively (Gauss-Seidel) instead.
    q = s = 0.5
    for _ in range(5000):
        q = (1 / aq + s / qs) / (1 / aq + 1 / qs + 1 / qb)
        s = (1 / as_ + q / qs) / (1 / as_ + 1 / qs + 1 / sb)
    current = (1 - q) / aq + (1 - s) / as_ + 1 / ab
    return 1 / current


PARAMS = {"aq": 10, "qs": 10, "sb": 10, "qb": 10, "as_": 10, "ab": 10}
VARIANTS = [{"aq": 2, "qs": 3, "sb": 4, "qb": 6, "as_": 12, "ab": 5}, {"ab": 1}, {"qs": 1, "sb": 7}]
ANSWER = Fraction(5, 1)
