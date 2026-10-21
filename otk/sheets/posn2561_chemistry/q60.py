"""Source p13, MC60: expanding bubble with pressure and temperature changes."""

from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction


def solve(initial_cm3="2.10", bottom_atm="5.66", bottom_c=10,
          surface_atm="1.00", surface_c=27):
    assert Fraction(bottom_atm) > 0 and Fraction(surface_atm) > 0
    assert bottom_c > -273 and surface_c > -273
    raw = (Fraction(initial_cm3) * Fraction(bottom_atm) * (surface_c + 273)
           / (Fraction(surface_atm) * (bottom_c + 273)))
    return (Decimal(raw.numerator) / Decimal(raw.denominator)).quantize(
        Decimal("0.1"), rounding=ROUND_HALF_UP,
    )


def check(initial_cm3="2.10", bottom_atm="5.66", bottom_c=10,
          surface_atm="1.00", surface_c=27):
    before = Fraction(bottom_atm) * Fraction(initial_cm3) / (bottom_c + 273)
    candidates = (Fraction(tenths, 10) for tenths in range(1, 1001))
    best = min(candidates, key=lambda volume: abs(
        Fraction(surface_atm) * volume / (surface_c + 273) - before
    ))
    return Decimal(best.numerator) / Decimal(best.denominator)


PARAMS = {"initial_cm3": "2.10", "bottom_atm": "5.66", "bottom_c": 10,
          "surface_atm": "1.00", "surface_c": 27}
VARIANTS = [
    {"initial_cm3": "1.50", "bottom_atm": "4.00", "bottom_c": 20,
     "surface_atm": "1.00", "surface_c": 50},
    {"initial_cm3": "2.00", "bottom_atm": "3.00", "bottom_c": 27,
     "surface_atm": "1.00", "surface_c": 77},
    {"initial_cm3": "3.00", "bottom_atm": "2.50", "bottom_c": 27,
     "surface_atm": "1.50", "surface_c": 87},
]
ANSWER = Decimal("12.6")
