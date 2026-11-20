"""Source p9, MC39: final Fe3+ after acidic permanganate oxidation."""

from decimal import Decimal
from fractions import Fraction


def solve(iron_ii_m="0.150", iron_iii_sulfate_m="0.00150",
          mixture_ml=30, permanganate_m="0.0200", permanganate_ml=30):
    iron_ii = Fraction(iron_ii_m) * mixture_ml
    oxidized = 5 * Fraction(permanganate_m) * permanganate_ml
    assert iron_ii > oxidized > 0
    final_iron_iii = 2 * Fraction(iron_iii_sulfate_m) * mixture_ml + oxidized
    concentration = final_iron_iii / (mixture_ml + permanganate_ml)
    return Decimal(concentration.numerator) / Decimal(concentration.denominator)


def check(iron_ii_m="0.150", iron_iii_sulfate_m="0.00150",
          mixture_ml=30, permanganate_m="0.0200", permanganate_ml=30):
    # Track dissolved iron by conservation, then subtract unoxidized Fe2+.
    fe2 = Fraction(iron_ii_m) * mixture_ml
    fe3 = 2 * Fraction(iron_iii_sulfate_m) * mixture_ml
    unused_fe2 = fe2 - 5 * Fraction(permanganate_m) * permanganate_ml
    assert unused_fe2 > 0
    result = (fe2 + fe3 - unused_fe2) / (mixture_ml + permanganate_ml)
    return Decimal(result.numerator) / Decimal(result.denominator)


PARAMS = {"iron_ii_m": "0.150", "iron_iii_sulfate_m": "0.00150",
          "mixture_ml": 30, "permanganate_m": "0.0200", "permanganate_ml": 30}
VARIANTS = [
    {**PARAMS, "iron_iii_sulfate_m": "0.00200", "permanganate_m": "0.0100"},
    {**PARAMS, "iron_iii_sulfate_m": "0.00300", "permanganate_m": "0.0250"},
    {**PARAMS, "iron_iii_sulfate_m": "0.00100", "permanganate_m": "0.0150"},
]
ANSWER = Decimal("0.0515")
