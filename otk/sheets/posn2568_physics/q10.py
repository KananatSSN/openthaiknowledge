"""Short10 figure: same material; bar 1 (L, 2A) joined to bar 2 (2L, A); ends at T1 and T2. Thermal resistances L/(2A) and 2L/A are 1 : 4, so the junction is at (4 T1 + T2)/5. Adapted: lengths and areas in any ratio."""


def solve(hot=100, cold=0, l1=1, a1=2, l2=2, a2=1):
    r1, r2 = l1 / a1, l2 / a2
    return hot - (hot - cold) * r1 / (r1 + r2)


def check(hot=100, cold=0, l1=1, a1=2, l2=2, a2=1):
    # Relax a 1-D finite-volume temperature profile to steady state: each
    # interior node is the conductance-weighted mean of its neighbours.
    n1, n2 = 20 * l1, 20 * l2
    areas = [a1] * n1 + [a2] * n2  # segment i joins node i to node i + 1
    temps = [hot] + [(hot + cold) / 2] * (n1 + n2 - 1) + [cold]
    for _ in range(40000):
        for i in range(1, n1 + n2):
            ga, gb = areas[i - 1], areas[i]
            temps[i] = (ga * temps[i - 1] + gb * temps[i + 1]) / (ga + gb)
    return temps[n1]


PARAMS = {"hot": 100, "cold": 0, "l1": 1, "a1": 2, "l2": 2, "a2": 1}
VARIANTS = [{"hot": 80, "cold": 20}, {"l1": 2, "a1": 1, "l2": 1, "a2": 1}, {"l1": 1, "a1": 3, "l2": 3, "a2": 1}]
TOL = 1e-6
ANSWER = 80.0
