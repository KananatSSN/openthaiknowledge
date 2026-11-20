"""Theory 2.1 figure: a particle (mass m, charge -q) fired at v_i toward a uniformly charged ball (radius R, charge +Q) from distance a, through a hole along a diameter; energy gives v_B^2 = v_i^2 + (2kqQ/m)(1/R - 1/a) at the far surface B (same potential as the near surface A). Adapted: K = kqQ/m given in m^3/s^2; m/s."""

from math import sqrt


def solve(speed=3.0, strength=8.0, radius=1.0, start=4.0):
    return sqrt(speed**2 + 2 * strength * (1 / radius - 1 / start))


def check(speed=3.0, strength=8.0, radius=1.0, start=4.0):
    # Integrate the motion from x = -a through the ball to x = +R (RK4).
    def accel(x):
        r = abs(x)
        magnitude = strength / r**2 if r >= radius else strength * r / radius**3
        return magnitude if x < 0 else -magnitude  # pulled toward the centre

    x, v, dt = -start, speed, 1e-5
    while x < radius:
        k1x, k1v = v, accel(x)
        k2x, k2v = v + dt / 2 * k1v, accel(x + dt / 2 * k1x)
        k3x, k3v = v + dt / 2 * k2v, accel(x + dt / 2 * k2x)
        k4x, k4v = v + dt * k3v, accel(x + dt * k3x)
        nx = x + dt / 6 * (k1x + 2 * k2x + 2 * k3x + k4x)
        nv = v + dt / 6 * (k1v + 2 * k2v + 2 * k3v + k4v)
        if nx >= radius:
            return v + (nv - v) * (radius - x) / (nx - x)
        x, v = nx, nv
    return v


PARAMS = {"speed": 3.0, "strength": 8.0, "radius": 1.0, "start": 4.0}
VARIANTS = [{"start": 2.0}, {"speed": 1.0, "strength": 2.0}, {"radius": 0.5, "start": 3.0}]
ANSWER = 4.58257569495584
TOL = 1e-5
