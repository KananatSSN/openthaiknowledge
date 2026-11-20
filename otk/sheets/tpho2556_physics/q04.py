"""Theory 1.2 (a): air brought to rest in front of the meteor gains pressure (1/2) rho v^2 (Bernoulli), pushing on the cross-section pi r^2 with F = (1/2) rho v^2 pi r^2. Adapted: rho, v (km/s) and r vary; returns F in newtons."""

from math import pi


def solve(density=0.1, speed=15.0, radius=0.5):
    return 0.5 * density * (speed * 1e3) ** 2 * pi * radius**2


def check(density=0.1, speed=15.0, radius=0.5):
    # Bernoulli along the stagnation streamline: integrate dp = -rho v dv
    # from the free-stream speed down to rest, then push on the disc.
    v = speed * 1e3
    n = 10000
    rise = 0.0
    for i in range(n):
        w = v * (i + 0.5) / n
        rise += density * w * v / n
    return rise * pi * radius**2


PARAMS = {"density": 0.1, "speed": 15.0, "radius": 0.5}
VARIANTS = [{"density": 1.2}, {"speed": 30.0}, {"radius": 2.0}]
ANSWER = 8835729.338221293
TOL = 1e-9
