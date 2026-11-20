"""Source p9, MC38: aluminium fraction from alloy mass and hydrogen volume."""

from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction


def solve(alloy_mg=1000, residue_mg=350, hydrogen_cm3="448"):
    reactive_mg = alloy_mg - residue_mg
    hydrogen_mmol = Fraction(hydrogen_cm3) / Fraction("22.4")
    # 27a + 65z = reactive mass (mg); (3/2)a + z = H2 (mmol).
    aluminium_mmol = (65 * hydrogen_mmol - reactive_mg) / Fraction(141, 2)
    zinc_mmol = hydrogen_mmol - Fraction(3, 2) * aluminium_mmol
    assert aluminium_mmol > 0 and zinc_mmol > 0
    percent = Fraction(2700 * aluminium_mmol, alloy_mg)
    return (Decimal(percent.numerator) / Decimal(percent.denominator)).quantize(
        Decimal("0.1"), rounding=ROUND_HALF_UP,
    )


def check(alloy_mg=1000, residue_mg=350, hydrogen_cm3="448"):
    # Eliminate Al instead: z = (reactive - 18 H2) / 47 mg per mmol.
    hydrogen = Fraction(hydrogen_cm3) / Fraction("22.4")
    zinc = Fraction(alloy_mg - residue_mg, 1) - 18 * hydrogen
    zinc /= 47
    aluminium_mg = alloy_mg - residue_mg - 65 * zinc
    assert aluminium_mg > 0 and zinc > 0
    percent = Fraction(100 * aluminium_mg, alloy_mg)
    return (Decimal(percent.numerator) / Decimal(percent.denominator)).quantize(
        Decimal("0.1"), rounding=ROUND_HALF_UP,
    )


PARAMS = {"alloy_mg": 1000, "residue_mg": 350, "hydrogen_cm3": "448"}
VARIANTS = [
    {"alloy_mg": 1000, "residue_mg": 405, "hydrogen_cm3": "448"},
    {"alloy_mg": 1200, "residue_mg": 415, "hydrogen_cm3": "392"},
    {"alloy_mg": 900, "residue_mg": 294, "hydrogen_cm3": "403.2"},
]
ANSWER = Decimal("24.9")
