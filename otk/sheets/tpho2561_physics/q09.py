"""Theory 2.4: in balance m g = I N 2 pi r B_r; with B_r from 2.3 and I = 1.928 A, g = 9.8122567 m/s^2, the mass is 1.0 kg. Adapted: I (A) and B_r (T) vary with r = 10 cm, N = 100; returns m in kg."""

from math import pi


def solve(current=1.928, field=0.08105694691387022, radius=10.0, turns=100, g=9.8122567):
    return current * turns * 2 * pi * radius * 1e-2 * field / g


def check(current=1.928, field=0.08105694691387022, radius=10.0, turns=100, g=9.8122567):
    # Sum I dl x B around the coil in small segments (radial field gives an
    # axial force), then balance against the weight.
    n = 4000
    from math import cos, sin

    fz = 0.0
    for i in range(n):
        a0, a1 = 2 * pi * i / n, 2 * pi * (i + 1) / n
        r = radius * 1e-2
        dx, dy = r * (cos(a1) - cos(a0)), r * (sin(a1) - sin(a0))
        mid = (a0 + a1) / 2
        bx, by = field * cos(mid), field * sin(mid)
        fz += turns * current * (dx * by - dy * bx)
    return abs(fz) / g


PARAMS = {"current": 1.928, "field": 0.08105694691387022, "radius": 10.0, "turns": 100, "g": 9.8122567}
VARIANTS = [{"current": 3.0}, {"field": 0.12}, {"turns": 200, "current": 1.0}]
ANSWER = 1.00070999661042
TOL = 1e-6
