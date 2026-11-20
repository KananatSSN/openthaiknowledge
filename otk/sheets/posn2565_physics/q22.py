"""MC22: adiabatic ideal diatomic gas at modest temperature (no vibration): gamma = 7/5 (answer 3). Adapted: a mixture of n1 mol monatomic and n2 mol diatomic gas; gamma = Cp/Cv of the mixture."""

from fractions import Fraction


def solve(monatomic=0, diatomic=1):
    cv = Fraction(3 * monatomic + 5 * diatomic, 2)
    n = monatomic + diatomic
    return (cv + n) / cv


def check(monatomic=0, diatomic=1):
    # Count quadratic degrees of freedom per molecule (equipartition) and use
    # gamma = 1 + 2/f_mean with f weighted by moles.
    freedoms = [3] * monatomic + [5] * diatomic
    f_mean = Fraction(sum(freedoms), len(freedoms))
    return 1 + 2 / f_mean


PARAMS = {"monatomic": 0, "diatomic": 1}
VARIANTS = [{"monatomic": 1}, {"monatomic": 2, "diatomic": 3}, {"monatomic": 1, "diatomic": 0}]
ANSWER = Fraction(7, 5)
