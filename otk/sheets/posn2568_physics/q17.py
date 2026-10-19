"""Short17 figure: capacitors C_i = i^2 C1 (i = 1..n, n large) in series with emf E. Every one holds the series charge E C_eq with 1/C_eq = (1/C1) sum 1/i^2 = pi^2/(6 C1): q = 6 C1 E/pi^2. Microcoulombs for C1 in microfarads."""

from math import pi


def solve(first=2, emf=10):
    return 6 * first * emf / pi**2


def check(first=2, emf=10, terms=200000):
    # Sum the series directly to many terms (tail ~ 1/n).
    inverse = sum(1 / (i * i * first) for i in range(1, terms + 1)) + 1 / (terms * first)
    return emf / inverse


PARAMS = {"first": 2, "emf": 10}
VARIANTS = [{"first": 5}, {"emf": 3}, {"first": 1, "emf": 100}]
TOL = 1e-6
ANSWER = 12.158542037080533
