"""Short6 figure: +q at (0, +a) and (0, -a). The field at the origin cancels; on the X axis E = 2kq x/(x^2 + a^2)^(3/2), largest 4kq/(3 sqrt3 a^2) = q/(3 sqrt3 pi eps0 a^2). Returns E_max in V/m for q in nC and a in m, k = 9e9."""

from math import sqrt

K = 9e9


def solve(charge=3, half=0.3):
    return 4 * K * charge * 1e-9 / (3 * sqrt(3) * half * half)


def check(charge=3, half=0.3):
    # Golden-section search of the vector sum along the X axis.
    q = charge * 1e-9

    def field(x):
        total = 0.0
        for y in (half, -half):
            r3 = (x * x + y * y) ** 1.5
            total += K * q * x / r3
        return total

    lo, hi = 0.0, 10 * half
    ratio = (sqrt(5) - 1) / 2
    for _ in range(300):
        a = hi - ratio * (hi - lo)
        c = lo + ratio * (hi - lo)
        if field(a) < field(c):
            lo = a
        else:
            hi = c
    return field((lo + hi) / 2)


PARAMS = {"charge": 3, "half": 0.3}
VARIANTS = [{"charge": 1, "half": 1}, {"half": 0.1}, {"charge": 27, "half": 0.5}]
ANSWER = 230.94010767585033
