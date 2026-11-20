"""Source p10, MC42: acid volume to evolve both carbons from trona."""

from decimal import Decimal
from fractions import Fraction


def solve(trona_mg=452, acid_m="0.125"):
    assert trona_mg > 0 and Fraction(acid_m) > 0
    # One formula unit (226 g/mol) contains CO3^2- and HCO3-, using 3 H+.
    formula_mmol = Fraction(trona_mg, 226)
    acid_mmol = 3 * formula_mmol
    volume_ml = acid_mmol / Fraction(acid_m)
    return Decimal(volume_ml.numerator) / Decimal(volume_ml.denominator)


def check(trona_mg=452, acid_m="0.125"):
    # Forward-search mL of HCl that exactly supplies the two acid equivalents
    # for carbonate and one for bicarbonate in the given mass.
    target = Fraction(trona_mg, 226)
    for volume_ml in range(1, 301):
        supplied = Fraction(acid_m) * volume_ml
        if supplied / 2 == target * Fraction(3, 2):
            return Decimal(volume_ml)
    raise AssertionError("no integer-mL volume matches the variant")


PARAMS = {"trona_mg": 452, "acid_m": "0.125"}
VARIANTS = [
    {"trona_mg": 226, "acid_m": "0.125"},
    {"trona_mg": 678, "acid_m": "0.125"},
    {"trona_mg": 452, "acid_m": "0.150"},
]
ANSWER = Decimal("48.0")
