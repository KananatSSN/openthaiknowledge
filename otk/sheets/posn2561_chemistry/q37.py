"""Source p9, MC37: carbonate remaining after silver-carbonate precipitation."""

from decimal import Decimal
from fractions import Fraction


def solve(carbonate_mm=80, carbonate_ml=75, silver_mm=200, silver_ml=25):
    carbonate = Fraction(carbonate_mm * carbonate_ml, 1000)  # mmol
    silver = Fraction(silver_mm * silver_ml, 1000)
    assert carbonate > silver / 2 > 0
    remainder = carbonate - silver / 2
    return Decimal(remainder.numerator) / Decimal(remainder.denominator) / (carbonate_ml + silver_ml)


def check(carbonate_mm=80, carbonate_ml=75, silver_mm=200, silver_ml=25):
    # Forward-reaction extent: every Ag2CO3 consumes two Ag+ and one CO3^2-.
    volume = carbonate_ml + silver_ml
    initial = Fraction(carbonate_mm, 1000) * carbonate_ml
    extent = Fraction(silver_mm, 1000) * silver_ml / 2
    assert initial > extent
    result = (initial - extent) / volume
    return Decimal(result.numerator) / Decimal(result.denominator)


PARAMS = {"carbonate_mm": 80, "carbonate_ml": 75, "silver_mm": 200, "silver_ml": 25}
VARIANTS = [
    {"carbonate_mm": 100, "carbonate_ml": 75, "silver_mm": 200, "silver_ml": 25},
    {"carbonate_mm": 80, "carbonate_ml": 50, "silver_mm": 120, "silver_ml": 50},
    {"carbonate_mm": 120, "carbonate_ml": 50, "silver_mm": 160, "silver_ml": 50},
]
ANSWER = Decimal("0.035")
