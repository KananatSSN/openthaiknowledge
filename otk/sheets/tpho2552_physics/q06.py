"""Theory 2.2: with m = M/6 and h = 5.00 m (v0 = 10 m/s) the light ball leaves the first collision at (17/7) v0 = 24.29 m/s upward (M at 4.29 m/s), 1.0 s after release. Adapted: m/M and h vary; m/s with g = 10."""


def solve(ratio=1 / 6, drop=5.0, g=10.0):
    v0 = (2 * g * drop) ** 0.5
    return (3 - ratio) / (1 + ratio) * v0


def check(ratio=1 / 6, drop=5.0, g=10.0):
    # Momentum and energy, solved as the quadratic in v (the other root is the
    # incoming -v0).
    from math import sqrt

    v0 = (2 * g * drop) ** 0.5
    m, big = ratio, 1.0
    p = big * v0 - m * v0
    e = big * v0**2 + m * v0**2
    # big V = p - m v ; big V^2 + m v^2 = e
    a = m * m / big + m
    b = -2 * p * m / big
    c = p * p / big - e
    roots = [(-b + s * sqrt(b * b - 4 * a * c)) / (2 * a) for s in (1, -1)]
    return max(roots)


PARAMS = {"ratio": 1 / 6, "drop": 5.0, "g": 10.0}
VARIANTS = [{"ratio": 0.5}, {"drop": 1.8}, {"ratio": 0.25, "drop": 3.2}]
ANSWER = 24.285714285714285
TOL = 1e-12
