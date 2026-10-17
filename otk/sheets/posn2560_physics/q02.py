"""Part1,2: source decreasing slope only fixes tangential acceleration, not total acceleration. Adaptation asks speed and tangential acceleration at a specified drop and slope, explicitly neglects friction. Return(v,a_t)."""

from math import sqrt


def solve(drop=5, sine=0.6, g=9.8):
    return (sqrt(2 * g * drop), g * sine)


def check(drop=5, sine=0.6, g=9.8):
    # A sequence of small height drops: sum gravitational work independently.
    energy = sum(g * drop / 1000 for _ in range(1000))
    lo, hi = 0.0, 1 + 2 * energy
    for _ in range(100):
        v = (lo + hi) / 2
        if v * v / 2 < energy:
            lo = v
        else:
            hi = v
    # Unit downhill tangent dot vertical gravity (normal part removed).
    tangent = (sqrt(1 - sine * sine), -sine)
    return ((lo + hi) / 2, -g * tangent[1])


PARAMS = {"drop": 5, "sine": 0.6, "g": 9.8}
VARIANTS = [{"drop": 10}, {"sine": 0.8}, {"g": 10}]
ANSWER = (9.899494936611665, 5.88)
