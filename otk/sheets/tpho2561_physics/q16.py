"""Theory 3.5: the kinetic energy density (1/2) rho v^2 averages to rho0 v_m^2/4 over a period. Adapted: rho0 and v_m (mm/s) vary; returns it in mJ/m^3."""


def solve(density=1.2, velocity=50.0):
    return density * (velocity * 1e-3) ** 2 / 4 * 1e3


def check(density=1.2, velocity=50.0):
    from math import pi, sin

    n = 4000
    vm = velocity * 1e-3
    return sum(0.5 * density * (vm * sin(2 * pi * (i + 0.5) / n)) ** 2 for i in range(n)) / n * 1e3


PARAMS = {"density": 1.2, "velocity": 50.0}
VARIANTS = [{"velocity": 200.0}, {"density": 1000.0}, {"velocity": 10.0}]
ANSWER = 0.7500000000000001
TOL = 1e-9
