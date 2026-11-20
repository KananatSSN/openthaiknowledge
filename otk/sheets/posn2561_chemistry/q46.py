"""Source p11, MC46: mass of HCl solution consumed while making chlorine."""

from decimal import Decimal
from fractions import Fraction


def solve(chlorine_g="3.55", acid_percent="36.5"):
    assert Fraction(chlorine_g) > 0 and 0 < Fraction(acid_percent) < 100
    # MnO2 + 4HCl -> MnCl2 + Cl2 + 2H2O.
    chlorine_mol = Fraction(chlorine_g) / 71
    pure_hcl_g = 4 * chlorine_mol * Fraction("36.5")
    solution_g = pure_hcl_g / (Fraction(acid_percent) / 100)
    return Decimal(solution_g.numerator) / Decimal(solution_g.denominator)


def check(chlorine_g="3.55", acid_percent="36.5"):
    # Forward-search hundredths of a gram of acid solution against Cl2 output.
    target = Fraction(chlorine_g)
    fraction = Fraction(acid_percent) / 100
    for hundredths in range(1, 10001):
        solution_g = Fraction(hundredths, 100)
        predicted_cl2_g = solution_g * fraction / Fraction("36.5") / 4 * 71
        if predicted_cl2_g == target:
            return Decimal(hundredths) / 100
    raise AssertionError("no hundredth-gram solution matches the variant")


PARAMS = {"chlorine_g": "3.55", "acid_percent": "36.5"}
VARIANTS = [
    {"chlorine_g": "7.10", "acid_percent": "36.5"},
    {"chlorine_g": "2.13", "acid_percent": "30.0"},
    {"chlorine_g": "3.55", "acid_percent": "25.0"},
]
ANSWER = Decimal("20")
