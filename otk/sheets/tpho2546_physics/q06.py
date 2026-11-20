"""Theory 2.2: D = 7.3 g/cm^3, c = 0.23 J/g C, rho = 11.5e-6 ohm cm, l = 5.0 cm, r = 0.10 cm, i = 10 A: dT/dt = i^2 rho/(pi^2 r^4 c D) = 0.694 C/s (0.70 in the marking scheme). CGS-length units as in the paper."""

from math import pi


def solve(current=10, resistivity=11.5e-6, radius=0.1, heat=0.23, density=7.3, length=5.0):
    return current**2 * resistivity / (pi**2 * radius**4 * heat * density)


def check(current=10, resistivity=11.5e-6, radius=0.1, heat=0.23, density=7.3, length=5.0):
    # Heat one second of Joule power into the wire's mass, step by step.
    area = pi * radius**2
    power = current**2 * resistivity * length / area
    mass = density * area * length
    temperature, steps = 0.0, 1000
    for _ in range(steps):
        temperature += power / steps / (mass * heat)
    return temperature


PARAMS = {"current": 10, "resistivity": 11.5e-6, "radius": 0.1, "heat": 0.23, "density": 7.3, "length": 5.0}
VARIANTS = [{"current": 5}, {"radius": 0.05, "length": 2.0}, {"heat": 0.39, "density": 8.9, "resistivity": 1.7e-6}]
ANSWER = 0.6939807098790258
TOL = 1e-9
