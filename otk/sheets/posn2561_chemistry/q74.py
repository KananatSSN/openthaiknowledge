"""Source p16, written 14: rigid oxygen cylinder and relief-valve threshold."""

from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction


def _rounded(value):
    return (Decimal(value.numerator) / Decimal(value.denominator)).quantize(
        Decimal("0.1"), rounding=ROUND_HALF_UP,
    )


def solve(initial_atm="50.0", initial_c=27, final_c=48,
          valve_mmhg=57000):
    pressure = (Fraction(initial_atm) * Fraction(final_c + 273, initial_c + 273))
    return _rounded(pressure), pressure > Fraction(valve_mmhg, 760)


def check(initial_atm="50.0", initial_c=27, final_c=48,
          valve_mmhg=57000):
    # Compare moles inferred at the two states through PV=nRT. The fixed
    # 10 L volume and R cancel; compare the resulting mmHg with the valve.
    p1 = Fraction(initial_atm) * 760
    predicted_mmhg = p1 * Fraction(final_c + 273, initial_c + 273)
    return _rounded(predicted_mmhg / 760), predicted_mmhg > valve_mmhg


PARAMS = {"initial_atm": "50.0", "initial_c": 27, "final_c": 48,
          "valve_mmhg": 57000}
VARIANTS = [
    {**PARAMS, "initial_atm": "65.0"},
    {**PARAMS, "initial_atm": "72.0"},
    {**PARAMS, "valve_mmhg": 40000},
]
ANSWER = (Decimal("53.5"), False)
