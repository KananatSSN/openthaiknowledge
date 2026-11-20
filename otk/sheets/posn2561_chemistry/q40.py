"""Source p10, MC40: NaBH4 needed for diborane at partial yield."""

from decimal import Decimal
from fractions import Fraction


def solve(target_diborane_mol="0.210", yield_percent=70):
    assert Fraction(target_diborane_mol) > 0 and 0 < yield_percent <= 100
    # 3NaBH4 + 4BF3 -> 3NaBF4 + 2B2H6.
    required = Fraction(target_diborane_mol) * Fraction(3, 2) * 100 / yield_percent
    return Decimal(required.numerator) / Decimal(required.denominator)


def check(target_diborane_mol="0.210", yield_percent=70):
    # Search input in millimoles and predict actual diborane output.
    target = Fraction(target_diborane_mol)
    for millimoles in range(1, 2001):
        candidate = Fraction(millimoles, 1000)
        produced = candidate * Fraction(2, 3) * Fraction(yield_percent, 100)
        if produced == target:
            return Decimal(millimoles) / 1000
    raise AssertionError("no millimole input matches the variant")


PARAMS = {"target_diborane_mol": "0.210", "yield_percent": 70}
VARIANTS = [
    {"target_diborane_mol": "0.140", "yield_percent": 70},
    {"target_diborane_mol": "0.280", "yield_percent": 80},
    {"target_diborane_mol": "0.350", "yield_percent": 75},
]
ANSWER = Decimal("0.450")
