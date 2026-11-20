"""Theory 1.4: with M >> m, M stops when all its energy is in m, v = V0 sqrt(M/m); l_n (v_n + V_n) = l0 V0 then gives the closest approach l_min ~ l0 sqrt(m/M). Adapted: l0 and M/m (large) vary; metres."""

from math import sqrt


def solve(ratio=10000, gap=2.0):
    return gap / sqrt(ratio)


def check(ratio=10000, gap=2.0):
    # Exact collision-by-collision run until M turns back; the last meeting
    # before that is M's closest approach.
    from otk.sheets.tpho2553_physics._wall import collisions

    closest = gap
    for distance, V, _ in collisions(float(ratio), 1.0, 1.0, gap):
        closest = min(closest, distance)
        if V <= 0:
            return closest
    return closest


PARAMS = {"ratio": 10000, "gap": 2.0}
VARIANTS = [{"ratio": 40000}, {"gap": 0.5}, {"ratio": 250000, "gap": 3.0}]
ANSWER = 0.02
TOL = 1e-3
