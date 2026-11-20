"""Theory 2.1: with no heat loss, dT/dt = i^2 rho/(pi^2 r^4 c D). Adapted: current multiplied by k and radius by s; returns the factor by which dT/dt changes, k^2/s^4."""


def solve(current_factor=2, radius_factor=0.5):
    return current_factor**2 / radius_factor**4


def check(current_factor=2, radius_factor=0.5):
    # Joule power over heat capacity, built from explicit wire properties.
    from math import pi

    def rate(i, r, rho=11.5e-6, length=5.0, c=0.23, density=7.3):
        power = i * i * rho * length / (pi * r * r)
        mass = density * pi * r * r * length
        return power / (c * mass)

    return rate(10 * current_factor, 0.1 * radius_factor) / rate(10, 0.1)


PARAMS = {"current_factor": 2, "radius_factor": 0.5}
VARIANTS = [{"current_factor": 3, "radius_factor": 2}, {"current_factor": 1, "radius_factor": 3}, {"radius_factor": 1}]
ANSWER = 64.0
