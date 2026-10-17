"""Part1,5: equal masses/drop heights/contact times imply larger AVERAGE normal force for larger rebound height. Instantaneous forces unspecified. Generalized solver returns mean normal force, includes weight during contact."""

from math import sqrt


def solve(mass=1, drop=5, rebound=1, contact=0.1, g=9.8):
    return mass * (sqrt(2 * g * drop) + sqrt(2 * g * rebound)) / contact + mass * g


def check(mass=1, drop=5, rebound=1, contact=0.1, g=9.8):
    before = -sqrt(2 * g * drop)
    # Given a trial mean normal force, integrate mean net acceleration.
    lo, hi = mass * g, mass * g + 1
    while (
        before + (hi / mass - g) * contact < 0
        or (before + (hi / mass - g) * contact) ** 2 / (2 * g) < rebound
    ):
        hi = 2 * hi
    for _ in range(100):
        normal = (lo + hi) / 2
        after = before + (normal / mass - g) * contact
        if after < 0 or after * after / (2 * g) < rebound:
            lo = normal
        else:
            hi = normal
    return (lo + hi) / 2


PARAMS = {"mass": 1, "drop": 5, "rebound": 1, "contact": 0.1, "g": 9.8}
VARIANTS = [{"rebound": 2}, {"contact": 0.2}, {"mass": 2}]
ANSWER = 153.06683660847398
