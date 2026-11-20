"""Theory 1.3 h): rolling on level ground with the half cylinder at the bottom and angular speed w0, the welded tube and half cylinder have kinetic energy [m' + (3/4 - k)m] R^2 w0^2, k = 4/(3 pi). Adapted: both masses (kg), R (cm) and w0 (rad/s) vary; returns joules."""


def solve(tube=1.0, half=0.5, radius=10.0, spin=20.0):
    from otk.sheets.tpho2564_physics._shared import HALF_DISC

    r = radius * 1e-2
    return (tube + (0.75 - HALF_DISC) * half) * r * r * spin * spin


def check(tube=1.0, half=0.5, radius=10.0, spin=20.0):
    from otk.sheets.tpho2564_physics._shared import rolling_inertia

    return 0.5 * rolling_inertia(0.0, tube, half, radius * 1e-2) * spin * spin


PARAMS = {"tube": 1.0, "half": 0.5, "radius": 10.0, "spin": 20.0}
VARIANTS = [{"half": 2.0}, {"radius": 5.0}, {"spin": 8.0}]
ANSWER = 4.651173636843225
TOL = 1e-9
