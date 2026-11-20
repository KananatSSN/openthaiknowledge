"""Theory 3.1 figure 1: without viscosity or surface tension Bernoulli gives v = sqrt(v0^2 + 2gh) and continuity pi R0^2 v0 = pi R^2 v gives R = R0 (1 + 2gh/v0^2)^(-1/4); R1 = 1.33 mm at h = 10 cm for R0 = 0.50 cm, v0 = 0.10 m/s. Adapted: R0 (cm), v0 and h vary; returns R in mm."""


def solve(radius0=0.5, speed0=0.10, height=0.10, g=9.8):
    return radius0 * 10 * (1 + 2 * g * height / speed0**2) ** -0.25


def check(radius0=0.5, speed0=0.10, height=0.10, g=9.8):
    # March a fluid parcel down in small time steps (exact for constant g),
    # then keep the volume flow pi R^2 v fixed.
    from math import sqrt

    t_hit = (-speed0 + sqrt(speed0**2 + 2 * g * height)) / g
    n = 1000
    v = speed0
    for _ in range(n):
        v += g * t_hit / n
    return radius0 * 10 * sqrt(speed0 / v)


PARAMS = {"radius0": 0.5, "speed0": 0.10, "height": 0.10, "g": 9.8}
VARIANTS = [{"height": 0.05}, {"radius0": 0.3, "speed0": 0.2}, {"height": 0.2}]
ANSWER = 1.3346071518232403
TOL = 1e-9
