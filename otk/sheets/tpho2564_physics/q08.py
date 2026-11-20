"""Theory 1.3 j): with the half cylinder at the top the angular acceleration vanishes and the system's cm (k'R above the axis) accelerates down at k'R w^2, so the floor pushes N = (m + m')(g - k'R w^2). Adapted: both masses (kg), R (cm) and w0 (rad/s) vary, w from 1.3 i); returns newtons with g = 9.81."""


def solve(tube=1.0, half=0.5, radius=10.0, spin=20.0):
    from otk.sheets.tpho2564_physics import q07
    from otk.sheets.tpho2564_physics._shared import HALF_DISC

    w = q07.solve(tube=tube, half=half, radius=radius, spin=spin)
    return (tube + half) * 9.81 - half * HALF_DISC * radius * 1e-2 * w * w


def check(tube=1.0, half=0.5, radius=10.0, spin=20.0):
    from math import cos, pi

    from otk.sheets.tpho2564_physics._shared import HALF_DISC, rolling_inertia

    # w(phi) from energy, then the cm height's second time derivative at the top
    r, k = radius * 1e-2, HALF_DISC
    total = 0.5 * rolling_inertia(0.0, tube, half, r) * spin**2 - half * 9.81 * k * r

    def rate2(phi):
        return 2 * (total + half * 9.81 * k * r * cos(phi)) / rolling_inertia(phi, tube, half, r)

    def height(phi):  # the half cylinder's cm height above the axis
        return -k * r * cos(phi)

    h = 1e-4
    # y'' = h'(phi) phi'' + h''(phi) w^2, with phi'' = (1/2) d(w^2)/dphi
    accel = (rate2(pi + h) - rate2(pi - h)) / (4 * h)
    slope = (height(pi + h) - height(pi - h)) / (2 * h)
    curve = (height(pi + h) - 2 * height(pi) + height(pi - h)) / h**2
    ay = half * (slope * accel + curve * rate2(pi)) / (tube + half)
    return (tube + half) * (9.81 + ay)


PARAMS = {"tube": 1.0, "half": 0.5, "radius": 10.0, "spin": 20.0}
VARIANTS = [{"half": 2.0}, {"radius": 5.0}, {"spin": 12.0}]
ANSWER = 9.053118089214045
TOL = 1e-5
