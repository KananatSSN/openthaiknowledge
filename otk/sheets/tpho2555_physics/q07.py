"""Theory 2 (c): over one cycle dust dm sticks at the mean square speed <v^2> = u0^2/2, so the energy drops by dm u0^2/4 = dm E0/(2m). Adapted: m (g), E0 (mJ) and dm (mg) vary; returns the loss in microjoules."""


def solve(mass=200.0, energy=40.0, dust=2.0):
    return dust * 1e-6 * energy * 1e-3 / (2 * mass * 1e-3) * 1e6


def check(mass=200.0, energy=40.0, dust=2.0):
    # Spread the dust evenly in time over one cycle and add up (1/2) dm v^2
    # with v = u0 cos(w t).
    from math import cos, pi, sqrt

    u0 = sqrt(2 * energy * 1e-3 / (mass * 1e-3))
    n = 4000
    total = 0.0
    for i in range(n):
        v = u0 * cos(2 * pi * (i + 0.5) / n)
        total += 0.5 * (dust * 1e-6 / n) * v * v
    return total * 1e6


PARAMS = {"mass": 200.0, "energy": 40.0, "dust": 2.0}
VARIANTS = [{"mass": 50.0}, {"energy": 100.0}, {"dust": 10.0, "mass": 500.0}]
ANSWER = 0.19999999999999996
TOL = 1e-9
