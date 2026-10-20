"""Theory 2.4: from O to B the work -kqQ/(2R) slows the particle: v_O = sqrt(v_B^2 + kqQ/(mR)). Adapted: K = kqQ/m (m^3/s^2), R and v_B given; m/s."""

from math import sqrt


def solve(speed=3.0, strength=8.0, radius=1.0):
    return sqrt(speed**2 + strength / radius)


def check(speed=3.0, strength=8.0, radius=1.0):
    # Run the motion backwards from B to O inside the ball (RK4).
    x, v, dt = radius, speed, 1e-5
    while x > 0:
        def accel(x):
            return -strength * x / radius**3

        k1x, k1v = -v, -accel(x)
        k2x, k2v = -(v + dt / 2 * k1v), -accel(x + dt / 2 * k1x)
        k3x, k3v = -(v + dt / 2 * k2v), -accel(x + dt / 2 * k2x)
        k4x, k4v = -(v + dt * k3v), -accel(x + dt * k3x)
        nx = x + dt / 6 * (k1x + 2 * k2x + 2 * k3x + k4x)
        nv = v + dt / 6 * (k1v + 2 * k2v + 2 * k3v + k4v)
        if nx <= 0:
            return v + (nv - v) * x / (x - nx)
        x, v = nx, nv
    return v


PARAMS = {"speed": 3.0, "strength": 8.0, "radius": 1.0}
VARIANTS = [{"speed": 1.0}, {"strength": 2.0, "radius": 0.5}, {"radius": 2.0}]
ANSWER = 4.123105625617661
TOL = 1e-5
