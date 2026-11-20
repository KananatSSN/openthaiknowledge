"""Theory 3 C.3: crossing a quadrupole of length d at speed v, a proton at x gets the impulse qvbx(d/v) toward the axis, so it reaches the axis after f_x = mv/(bqd) (focusing); along y the same push is outward, f_y = -mv/(aqd). Adapted: the gradient (T/m), d (cm) and the energy (MeV) vary; returns f_x in metres."""

from math import sqrt

Q, M = 1.6e-19, 1.67e-27


def solve(gradient=1.0, depth=10.0, energy=4.0):
    v = sqrt(2 * energy * 1e6 * Q / M)
    return M * v / (gradient * Q * depth * 1e-2)


def check(gradient=1.0, depth=10.0, energy=4.0):
    # Integrate the transverse motion through the lens in small steps, with
    # the lens shrunk a thousandfold and its gradient raised to match (the
    # thin-lens limit the answer assumes), then follow the ray to the axis.
    v = sqrt(2 * energy * 1e6 * Q / M)
    scale = 1e3
    g, d = gradient * scale, depth * 1e-2 / scale
    x, vx = 1e-4, 0.0
    steps = 20000
    dt = d / v / steps
    for _ in range(steps):
        vx += -Q * v * g * x / M * dt
        x += vx * dt
    return x / -vx * v


PARAMS = {"gradient": 1.0, "depth": 10.0, "energy": 4.0}
VARIANTS = [{"gradient": 3.0}, {"depth": 20.0}, {"energy": 9.0}]
ANSWER = 2.8896366553599786
TOL = 1e-4
