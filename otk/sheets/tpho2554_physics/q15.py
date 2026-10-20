"""Theory 3.6: Plateau and Rayleigh put the break-up after t = 2.91 sqrt(rho R0^3/gamma) = 0.12 s; falling from v0 with acceleration g the water covers h = v0 t + g t^2/2 = 0.084 m (the bound solution prints 0.84 m, a factor of ten too large). Adapted: R0 (cm), v0 and gamma vary; returns h in cm."""

from math import sqrt


def solve(radius0=0.5, speed0=0.10, tension=0.072, density=1000.0, g=9.8):
    t = 2.91 * sqrt(density * (radius0 * 1e-2) ** 3 / tension)
    return (speed0 * t + g * t * t / 2) * 100


def check(radius0=0.5, speed0=0.10, tension=0.072, density=1000.0, g=9.8):
    # Step the fall in time (trapezoid rule on the linear speed is exact).
    t_end = 2.91 * sqrt(density * (radius0 * 1e-2) ** 3 / tension)
    n = 1000
    dt = t_end / n
    x, v = 0.0, speed0
    for _ in range(n):
        x += (v + (v + g * dt)) / 2 * dt
        v += g * dt
    return x * 100


PARAMS = {"radius0": 0.5, "speed0": 0.10, "tension": 0.072, "density": 1000.0, "g": 9.8}
VARIANTS = [{"radius0": 0.3}, {"speed0": 0.3, "tension": 0.05}, {"radius0": 1.0}]
ANSWER = 8.416265625000003
TOL = 1e-9
