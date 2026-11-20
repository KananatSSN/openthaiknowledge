"""MC7 figure: +Q and -Q, each of mass m, circle their common centre at fixed separation D with speed v. m v^2/(D/2) = kQ^2/D^2, so m v^2 D / Q^2 = 1/(8 pi eps0) (answer 2). Adapted: Q in uC, m in g, D in m; returns v in m/s."""

from math import sqrt

K = 9e9


def solve(charge=2, mass=4, distance=0.9):
    q, m = charge * 1e-6, mass / 1000
    return sqrt(K * q * q / (2 * m * distance))


def check(charge=2, mass=4, distance=0.9):
    # Bisect on the speed: integrate the relative motion for a short time with
    # a velocity-Verlet step and see whether the separation grows (too fast)
    # or shrinks (too slow). Relative acceleration -2 K q^2 / (m r^2).
    q, m = charge * 1e-6, mass / 1000
    pull = 2 * K * q * q / m

    def drift(speed):
        x, y, vx, vy = distance, 0.0, 0.0, 2 * speed
        period = 2 * 3.141592653589793 * distance / (2 * speed)
        dt = period / 20000
        for _ in range(2000):
            r3 = (x * x + y * y) ** 1.5
            ax, ay = -pull * x / r3, -pull * y / r3
            vx += ax * dt / 2
            vy += ay * dt / 2
            x += vx * dt
            y += vy * dt
            r3 = (x * x + y * y) ** 1.5
            vx += -pull * x / r3 * dt / 2
            vy += -pull * y / r3 * dt / 2
        return (x * x + y * y) ** 0.5 - distance

    lo, hi = 1e-6, 1e4
    for _ in range(100):
        mid = (lo + hi) / 2
        if drift(mid) < 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2

PARAMS = {"charge": 2, "mass": 4, "distance": 0.9}
VARIANTS = [{"charge": 3, "mass": 9, "distance": 0.5}, {"distance": 0.1}, {"charge": 1, "mass": 1}]
TOL = 1e-6
ANSWER = 2.2360679774997894
