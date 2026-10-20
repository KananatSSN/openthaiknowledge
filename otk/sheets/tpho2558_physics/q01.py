"""Theory 1.1 (a) figure a: released from the vertical, the charge swings until the field's work qE l sin(theta) equals the rise in potential energy mgl(1 - cos theta), so tan(theta_m/2) = qE/mg and theta_m = 2 arctan(qE/mg). Adapted: the ratio qE/mg varies (charge in microcoulombs, E in kN/C, m in grams); returns theta_m in degrees."""

from math import atan, degrees


def solve(charge=2.0, field=10.0, mass=4.0, g=9.8):
    return degrees(2 * atan(charge * 1e-6 * field * 1e3 / (mass * 1e-3 * g)))


def check(charge=2.0, field=10.0, mass=4.0, g=9.8, length=1.0):
    # RK4 swing from rest at the vertical until the angular speed turns back.
    from math import cos, sin

    k = charge * 1e-6 * field * 1e3 / (mass * 1e-3)

    def acc(t):
        return (k * cos(t) - g * sin(t)) / length

    t, w, dt = 0.0, 0.0, 1e-5
    while True:
        k1t, k1w = w, acc(t)
        k2t, k2w = w + dt / 2 * k1w, acc(t + dt / 2 * k1t)
        k3t, k3w = w + dt / 2 * k2w, acc(t + dt / 2 * k2t)
        k4t, k4w = w + dt * k3w, acc(t + dt * k3t)
        nt = t + dt / 6 * (k1t + 2 * k2t + 2 * k3t + k4t)
        nw = w + dt / 6 * (k1w + 2 * k2w + 2 * k3w + k4w)
        if nw < 0 < w:
            # interpolate the turning point
            return degrees(t + (nt - t) * w / (w - nw))
        t, w = nt, nw


PARAMS = {"charge": 2.0, "field": 10.0, "mass": 4.0, "g": 9.8}
VARIANTS = [{"field": 5.0}, {"mass": 1.0}, {"charge": 5.0, "field": 20.0, "mass": 20.0}]
ANSWER = 54.06172051968596
TOL = 1e-5
