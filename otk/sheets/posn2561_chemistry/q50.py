"""Source p11, MC50: transfer molality from freezing depression to boiling rise."""

from decimal import Decimal
from fractions import Fraction


def solve(a_freeze_pure="4.5", a_freeze_solution="2.0", a_kf="5.0",
          b_boiling_pure="63.0", b_kb="4.0"):
    depression = Fraction(a_freeze_pure) - Fraction(a_freeze_solution)
    assert depression > 0 and Fraction(a_kf) > 0 and Fraction(b_kb) > 0
    molality = depression / Fraction(a_kf)
    temperature = Fraction(b_boiling_pure) + Fraction(b_kb) * molality
    return Decimal(temperature.numerator) / Decimal(temperature.denominator)


def check(a_freeze_pure="4.5", a_freeze_solution="2.0", a_kf="5.0",
          b_boiling_pure="63.0", b_kb="4.0"):
    # Predict A's freezing temperature for candidate B boiling temperatures.
    target_a = Fraction(a_freeze_solution)
    pure_b = Fraction(b_boiling_pure)
    for tenths in range(-200, 2001):
        boiling_b = Fraction(tenths, 10)
        molality = (boiling_b - pure_b) / Fraction(b_kb)
        if Fraction(a_freeze_pure) - Fraction(a_kf) * molality == target_a:
            return Decimal(tenths) / 10
    raise AssertionError("no tenth-degree solution matches the variant")


PARAMS = {"a_freeze_pure": "4.5", "a_freeze_solution": "2.0", "a_kf": "5.0",
          "b_boiling_pure": "63.0", "b_kb": "4.0"}
VARIANTS = [
    {"a_freeze_pure": "4.5", "a_freeze_solution": "1.5", "a_kf": "5.0",
     "b_boiling_pure": "60.0", "b_kb": "4.0"},
    {"a_freeze_pure": "3.0", "a_freeze_solution": "1.0", "a_kf": "4.0",
     "b_boiling_pure": "70.0", "b_kb": "3.0"},
    {"a_freeze_pure": "5.0", "a_freeze_solution": "2.0", "a_kf": "6.0",
     "b_boiling_pure": "80.0", "b_kb": "2.0"},
]
ANSWER = Decimal("65")
