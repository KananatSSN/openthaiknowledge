"""Source p15, written 8: aluminum per pancake from additive mass fractions."""

from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction


def solve(flour_g=500, additive_pct="1.00", alumina_pct="10.2", pieces=40):
    assert flour_g > 0 and pieces > 0
    aluminum_mg = (Fraction(flour_g) * Fraction(additive_pct) / 100
                   * Fraction(alumina_pct) / 100 * Fraction(54, 102)
                   * Fraction(1000, pieces))
    return (Decimal(aluminum_mg.numerator) / Decimal(aluminum_mg.denominator)).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP,
    )


def check(flour_g=500, additive_pct="1.00", alumina_pct="10.2", pieces=40):
    additive_g = Fraction(flour_g) * Fraction(additive_pct) / 100
    alumina_g = additive_g * Fraction(alumina_pct) / 100
    alumina_mol = alumina_g / 102
    aluminum_mol = 2 * alumina_mol
    each_mg = aluminum_mol * 27 * 1000 / pieces
    return (Decimal(each_mg.numerator) / Decimal(each_mg.denominator)).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP,
    )


PARAMS = {"flour_g": 500, "additive_pct": "1.00",
          "alumina_pct": "10.2", "pieces": 40}
VARIANTS = [
    {"flour_g": 400, "additive_pct": "1.50", "alumina_pct": "17.0", "pieces": 40},
    {"flour_g": 600, "additive_pct": "0.50", "alumina_pct": "20.4", "pieces": 30},
    {"flour_g": 300, "additive_pct": "2.00", "alumina_pct": "10.2", "pieces": 36},
]
ANSWER = Decimal("6.75")
