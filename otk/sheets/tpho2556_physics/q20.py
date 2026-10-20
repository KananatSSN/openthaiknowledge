"""Lab part 5: inverting tau_max = (B_h/B_v)(1/f_t)(2 l_max/sqrt(R^2 + d^2/3)) gives B_v = B_h 2 l_max/(tau_max f_t sqrt(R^2 + d^2/3)); tau_max = 35 s, f_t = 1.47 Hz, l_max = 12.0 cm, B_h = 0.41 G give 0.133 G (the solution prints 0.13 T, a unit slip for 1.3e-5 T). Adapted: tau_max, f_t, l_max and B_h vary; returns B_v in gauss."""

from math import sqrt


def solve(tau=35.0, freq=1.47, length=12.0, field=0.41, radius=14.0, thickness=6.0):
    R, d = radius * 1e-3, thickness * 1e-3
    return field * 2 * length * 1e-2 / (tau * freq * sqrt(R * R + d * d / 3))


def check(tau=35.0, freq=1.47, length=12.0, field=0.41, radius=14.0, thickness=6.0):
    # Bisect B_v until equation (2) returns the measured tau_max.
    R, d = radius * 1e-3, thickness * 1e-3

    def tau_of(bv):
        return field / bv / freq * 2 * length * 1e-2 / sqrt(R * R + d * d / 3)

    lo, hi = 1e-6, 100.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if tau_of(mid) > tau:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


PARAMS = {"tau": 35.0, "freq": 1.47, "length": 12.0, "field": 0.41, "radius": 14.0, "thickness": 6.0}
VARIANTS = [{"tau": 20.0}, {"length": 14.0, "freq": 1.3}, {"field": 0.35}]
ANSWER = 0.13261054253780988
TOL = 1e-9
