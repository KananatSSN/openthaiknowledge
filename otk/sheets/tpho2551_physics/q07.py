"""Theory 2.5: inside the ball the motion is simple harmonic with omega = sqrt(kqQ/(mR^3)); from O (speed v_O) to B (speed v_B), v_B = v_O cos(omega t), so t = sqrt(mR^3/(kqQ)) arccos(v_B/sqrt(v_B^2 + kqQ/(mR))). Adapted: K = kqQ/m, R and v_B given; seconds."""

from math import acos, sqrt


def solve(speed=3.0, strength=8.0, radius=1.0):
    return sqrt(radius**3 / strength) * acos(speed / sqrt(speed**2 + strength / radius))


def check(speed=3.0, strength=8.0, radius=1.0):
    # Time the RK4 motion from O to B, starting at O with v_O from energy.
    v = sqrt(speed**2 + strength / radius)
    x, t, dt = 0.0, 0.0, 1e-6

    def accel(x):
        return -strength * x / radius**3

    while True:
        k1x, k1v = v, accel(x)
        k2x, k2v = v + dt / 2 * k1v, accel(x + dt / 2 * k1x)
        k3x, k3v = v + dt / 2 * k2v, accel(x + dt / 2 * k2x)
        k4x, k4v = v + dt * k3v, accel(x + dt * k3x)
        nx = x + dt / 6 * (k1x + 2 * k2x + 2 * k3x + k4x)
        nv = v + dt / 6 * (k1v + 2 * k2v + 2 * k3v + k4v)
        if nx >= radius:
            return t + dt * (radius - x) / (nx - x)
        x, v, t = nx, nv, t + dt


PARAMS = {"speed": 3.0, "strength": 8.0, "radius": 1.0}
VARIANTS = [{"speed": 1.0}, {"strength": 2.0, "radius": 0.5}, {"radius": 2.0, "strength": 27.0}]
ANSWER = 0.26727554824017075
TOL = 1e-5
