"""Theory 1.3 i): from the half cylinder at the bottom (w0) to the top, energy gives w^2 = ([m' + (3/4 - k)m]R^2 w0^2 - 2(m + m')g k'R)/([m' + (3/4 + k)m]R^2) with k = 4/(3 pi) and (m + m')k' = mk. Adapted: both masses (kg), R (cm) and w0 (rad/s) vary; returns rad/s with g = 9.81."""

from math import sqrt


def solve(tube=1.0, half=0.5, radius=10.0, spin=20.0):
    from otk.sheets.tpho2564_physics._shared import HALF_DISC as k

    r = radius * 1e-2
    top = (tube + (0.75 - k) * half) * r * r * spin**2 - 2 * half * 9.81 * k * r
    return sqrt(top / ((tube + (0.75 + k) * half) * r * r))


def check(tube=1.0, half=0.5, radius=10.0, spin=20.0):
    from math import pi

    from otk.sheets.tpho2564_physics._shared import HALF_DISC, rolling_inertia

    r = radius * 1e-2
    total = 0.5 * rolling_inertia(0.0, tube, half, r) * spin**2 + half * 9.81 * (-HALF_DISC * r)
    rise = half * 9.81 * HALF_DISC * r
    return sqrt(2 * (total - rise) / rolling_inertia(pi, tube, half, r))


PARAMS = {"tube": 1.0, "half": 0.5, "radius": 10.0, "spin": 20.0}
VARIANTS = [{"half": 2.0}, {"radius": 5.0}, {"spin": 12.0}]
ANSWER = 16.334316613996172
TOL = 1e-9
