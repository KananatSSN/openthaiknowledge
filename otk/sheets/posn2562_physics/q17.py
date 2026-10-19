"""Short17 circuit: sourceEMFE inseries internalr andloadx; beta=i^2 x. Given quadratic x^2+(2r-E^2/beta)x+r^2=0. Positive real load permits maximum beta=E^2/(4r), achievedx=r (discriminantzero and maxpowertransfer)."""

from fractions import Fraction


def solve(emf=12, internal=3):
    return Fraction(emf * emf, 4 * internal)


def check(emf=12, internal=3):
    # Numerically maximize actual load power, rather than using discriminant.
    def power(load):
        current = emf / (internal + load)
        return current * current * load

    lo, hi = 0.0, 10.0 * internal
    for _ in range(120):
        a, b = (2 * lo + hi) / 3, (lo + 2 * hi) / 3
        if power(a) < power(b):
            lo = a
        else:
            hi = b
    return power((lo + hi) / 2)


PARAMS = {"emf": 12, "internal": 3}
VARIANTS = [{"emf": 24}, {"internal": 6}, {"emf": 10, "internal": 2}]
ANSWER = Fraction(12, 1)
