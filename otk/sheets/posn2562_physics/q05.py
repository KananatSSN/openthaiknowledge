"""MC5: equal electric/magnetic energy densities of an EM plane wave give E/B=1/sqrt(epsilon mu), source answer1. Relative epsilon_r,mu_r return E/B in units c0=1/sqrt(epsilon0 mu0). Homogeneous lossless nondispersive medium."""

from math import sqrt


def solve(epsilon_r=1, mu_r=1):
    return 1 / sqrt(epsilon_r * mu_r)


def check(epsilon_r=1, mu_r=1):
    # Normalize vacuum constants to1, set B=2 and equalize actual energies.
    magnetic = 2**2 / (2 * mu_r)
    lo, hi = 0.0, 10.0
    for _ in range(100):
        electric_field = (lo + hi) / 2
        if epsilon_r * electric_field**2 / 2 < magnetic:
            lo = electric_field
        else:
            hi = electric_field
    return (lo + hi) / 4


PARAMS = {"epsilon_r": 1, "mu_r": 1}
VARIANTS = [{"epsilon_r": 4}, {"mu_r": 4}, {"epsilon_r": 9, "mu_r": 4}]
ANSWER = 1.0
