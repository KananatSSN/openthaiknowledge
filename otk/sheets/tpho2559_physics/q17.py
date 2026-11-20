"""Theory 3.4: to rewind the same n turns and stop with no braking, the spin-up energy F1 b - 2 n pi k(Mg + F1) must equal the free spin-down loss 2 n pi k Mg, so F1 = 4 n pi k M g/(b - 2 n pi k). Adapted: n, M (kg), k (mm) and b (cm) vary; returns F1 in newtons with g = 9.8."""

from math import pi


def solve(turns=5, mass=1.0, k=0.3, reach=3.0, g=9.8):
    kk = k * 1e-3
    return 4 * turns * pi * kk * mass * g / (reach * 1e-2 - 2 * turns * pi * kk)


def check(turns=5, mass=1.0, k=0.3, reach=3.0, g=9.8):
    # Bisect the push whose spin-up energy is used up exactly by n turns of
    # free spin-down against k M g.
    from otk.sheets.tpho2559_physics._shared import bisect

    kk, b = k * 1e-3, reach * 1e-2

    def leftover(F):
        energy = F * b - 2 * turns * pi * kk * (mass * g + F)
        return energy - 2 * turns * pi * kk * mass * g

    return bisect(leftover, 0.0, 1e5)


PARAMS = {"turns": 5, "mass": 1.0, "k": 0.3, "reach": 3.0, "g": 9.8}
VARIANTS = [{"turns": 3}, {"mass": 2.0, "k": 0.2}, {"reach": 4.0}]
ANSWER = 8.978063404558396
TOL = 1e-9
