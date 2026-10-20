"""Theory 1.3 figure: M_A hits a resting m, which hits a resting M_B; the energy fraction reaching M_B, [4 M_A m/(M_A + m)^2][4 m M_B/(m + M_B)^2], is largest at m = sqrt(M_A M_B). Adapted: numbers for M_A and M_B; kg."""

from math import sqrt


def solve(mass_a=2, mass_b=8):
    return sqrt(mass_a * mass_b)


def check(mass_a=2, mass_b=8):
    # Golden-section search for the best intermediate mass.
    def fraction(m):
        return 16 * mass_a * m * m * mass_b / ((mass_a + m) ** 2 * (m + mass_b) ** 2)

    lo, hi = 1e-6, 10 * max(mass_a, mass_b)
    phi = (sqrt(5) - 1) / 2
    for _ in range(300):
        x1, x2 = hi - phi * (hi - lo), lo + phi * (hi - lo)
        if fraction(x1) < fraction(x2):
            lo = x1
        else:
            hi = x2
    return (lo + hi) / 2


PARAMS = {"mass_a": 2, "mass_b": 8}
VARIANTS = [{"mass_a": 3, "mass_b": 3}, {"mass_a": 1, "mass_b": 50}, {"mass_a": 9, "mass_b": 4}]
ANSWER = 4.0
TOL = 1e-6
