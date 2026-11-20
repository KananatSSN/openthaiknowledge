"""Source p14, written 3: isotope-pair fraction at molecular mass 128."""

from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction


def solve(cl_light=3, cl_heavy=1, br_light=1, br_heavy=1):
    assert min(cl_light, cl_heavy, br_light, br_heavy) > 0
    fraction = Fraction(cl_light, cl_light + cl_heavy)
    fraction *= Fraction(br_light, br_light + br_heavy)
    percent = fraction * 100
    return (Decimal(percent.numerator) / Decimal(percent.denominator)).quantize(
        Decimal("0.1"), rounding=ROUND_HALF_UP,
    )


def check(cl_light=3, cl_heavy=1, br_light=1, br_heavy=1):
    chlorine = ((35, Fraction(cl_light, cl_light + cl_heavy)),
                (37, Fraction(cl_heavy, cl_light + cl_heavy)))
    bromine = ((79, Fraction(br_light, br_light + br_heavy)),
               (81, Fraction(br_heavy, br_light + br_heavy)))
    selected = sum((cl_prob * br_prob for cl_mass, cl_prob in chlorine
                    for br_mass, br_prob in bromine
                    if 12 + 2 + cl_mass + br_mass == 128), Fraction())
    result = selected * 100
    return (Decimal(result.numerator) / Decimal(result.denominator)).quantize(
        Decimal("0.1"), rounding=ROUND_HALF_UP,
    )


PARAMS = {"cl_light": 3, "cl_heavy": 1, "br_light": 1, "br_heavy": 1}
VARIANTS = [
    {"cl_light": 2, "cl_heavy": 1, "br_light": 3, "br_heavy": 1},
    {"cl_light": 4, "cl_heavy": 1, "br_light": 1, "br_heavy": 1},
    {"cl_light": 3, "cl_heavy": 2, "br_light": 2, "br_heavy": 1},
]
ANSWER = Decimal("37.5")
