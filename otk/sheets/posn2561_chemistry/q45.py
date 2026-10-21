"""Source p10, MC45: sodium-ion concentration after mixing two salts."""

from decimal import Decimal
from fractions import Fraction


def solve(sulfate_m="0.10", sulfate_ml=20, phosphate_m="0.30", phosphate_ml=50):
    assert sulfate_ml > 0 and phosphate_ml > 0
    sodium_mmol = (2 * Fraction(sulfate_m) * sulfate_ml
                   + 3 * Fraction(phosphate_m) * phosphate_ml)
    concentration = sodium_mmol / (sulfate_ml + phosphate_ml)
    return Decimal(concentration.numerator) / Decimal(concentration.denominator)


def check(sulfate_m="0.10", sulfate_ml=20, phosphate_m="0.30", phosphate_ml=50):
    # Charge balance: sodium positive equivalents equal sulfate plus phosphate.
    sulfate_charge = 2 * Fraction(sulfate_m) * sulfate_ml
    phosphate_charge = 3 * Fraction(phosphate_m) * phosphate_ml
    result = (sulfate_charge + phosphate_charge) / (sulfate_ml + phosphate_ml)
    return Decimal(result.numerator) / Decimal(result.denominator)


PARAMS = {"sulfate_m": "0.10", "sulfate_ml": 20,
          "phosphate_m": "0.30", "phosphate_ml": 50}
VARIANTS = [
    {"sulfate_m": "0.10", "sulfate_ml": 50, "phosphate_m": "0.20", "phosphate_ml": 50},
    {"sulfate_m": "0.20", "sulfate_ml": 25, "phosphate_m": "0.30", "phosphate_ml": 75},
    {"sulfate_m": "0.15", "sulfate_ml": 40, "phosphate_m": "0.20", "phosphate_ml": 60},
]
ANSWER = Decimal("0.7")
