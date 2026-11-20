"""Source p12, MC51: solute mass from boiling-freezing temperature gap."""

from decimal import Decimal
from fractions import Fraction


KF = Fraction("1.86")
KB = Fraction("0.51")


def solve(gap_c="109.48", water_ml=100, solute_molar_mass=180):
    assert Fraction(gap_c) > 100 and water_ml > 0 and solute_molar_mass > 0
    # Tf=0-Kf*m and Tb=100+Kb*m, so gap=100+(Kf+Kb)*m.
    molality = (Fraction(gap_c) - 100) / (KF + KB)
    solute_g = molality * Fraction(water_ml, 1000) * solute_molar_mass
    return Decimal(solute_g.numerator) / Decimal(solute_g.denominator)


def check(gap_c="109.48", water_ml=100, solute_molar_mass=180):
    # Forward-search tenth-gram masses and compute both phase temperatures.
    target = Fraction(gap_c)
    solvent_kg = Fraction(water_ml, 1000)  # water density 1.00 g/mL
    for tenths in range(1, 10001):
        grams = Fraction(tenths, 10)
        molality = grams / solute_molar_mass / solvent_kg
        boiling = 100 + KB * molality
        freezing = -KF * molality
        if boiling - freezing == target:
            return Decimal(tenths) / 10
    raise AssertionError("no tenth-gram mass matches the variant")


PARAMS = {"gap_c": "109.48", "water_ml": 100, "solute_molar_mass": 180}
VARIANTS = [
    {"gap_c": "104.74", "water_ml": 100, "solute_molar_mass": 180},
    {"gap_c": "111.85", "water_ml": 200, "solute_molar_mass": 180},
    {"gap_c": "107.11", "water_ml": 100, "solute_molar_mass": 200},
]
ANSWER = Decimal("72")
