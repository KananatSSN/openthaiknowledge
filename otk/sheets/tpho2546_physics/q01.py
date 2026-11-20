"""Theory 1.1 figure: a smooth quarter cylinder PCQ (mass M, radius R) rests on a smooth floor; a small mass m slides from rest near the top P. v is m's speed relative to the cylinder when the line Cm makes angle theta with the vertical: v^2 = 2gR(M + m)(1 - cos theta)/(M + m sin^2 theta). Adapted: numbers for M, m, R, theta; m/s."""

from math import cos, radians, sin, sqrt


def solve(big=4, small=1, radius=0.5, angle=60, g=10):
    c, s = cos(radians(angle)), sin(radians(angle))
    return sqrt(2 * g * radius * (big + small) * (1 - c) / (big + small * s * s))


def check(big=4, small=1, radius=0.5, angle=60, g=10):
    # Integrate the Lagrangian equation of motion in theta (the cylinder's
    # coordinate eliminated by zero total momentum) from a tiny start angle.
    def f(t):
        return radius**2 * (small - small**2 * cos(t) ** 2 / (big + small))

    def df(t):
        return radius**2 * 2 * small**2 * cos(t) * sin(t) / (big + small)

    def accel(t, w):
        return (small * g * radius * sin(t) - 0.5 * df(t) * w * w) / f(t)

    start = 1e-3
    t, w = start, 0.0
    target, dt = radians(angle), 2e-4
    while True:
        k1t, k1w = w, accel(t, w)
        k2t, k2w = w + dt / 2 * k1w, accel(t + dt / 2 * k1t, w + dt / 2 * k1w)
        k3t, k3w = w + dt / 2 * k2w, accel(t + dt / 2 * k2t, w + dt / 2 * k2w)
        k4t, k4w = w + dt * k3w, accel(t + dt * k3t, w + dt * k3w)
        nt = t + dt / 6 * (k1t + 2 * k2t + 2 * k3t + k4t)
        nw = w + dt / 6 * (k1w + 2 * k2w + 2 * k3w + k4w)
        if nt >= target:
            w = w + (nw - w) * (target - t) / (nt - t)
            return radius * w
        t, w = nt, nw


PARAMS = {"big": 4, "small": 1, "radius": 0.5, "angle": 60, "g": 10}
VARIANTS = [{"big": 1, "small": 1}, {"angle": 30, "radius": 1.2}, {"big": 10, "small": 3, "angle": 45}]
ANSWER = 2.2941573387056176
TOL = 1e-4
