"""Source p16, written 12: mole fraction to mass and diluted molarity."""

from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction


def _rounded(value):
    return (Decimal(value.numerator) / Decimal(value.denominator)).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP,
    )


def solve(solution_g=1264, mole_fraction="0.0400", solute_molar_mass=200,
          water_molar_mass=18, added_water_g=136, final_density="1.400"):
    x = Fraction(mole_fraction)
    average_molar_mass = x * solute_molar_mass + (1 - x) * water_molar_mass
    solute_mol = Fraction(solution_g) * x / average_molar_mass
    solute_g = solute_mol * solute_molar_mass
    final_volume_l = Fraction(solution_g + added_water_g) / Fraction(final_density) / 1000
    return int(solute_g), _rounded(solute_mol / final_volume_l)


def check(solution_g=1264, mole_fraction="0.0400", solute_molar_mass=200,
          water_molar_mass=18, added_water_g=136, final_density="1.400"):
    x = Fraction(mole_fraction)
    n = next(n for n in range(1, 100)
             if n * solute_molar_mass + n * (1 - x) / x * water_molar_mass
             == solution_g)
    solute_g = n * solute_molar_mass
    final_ml = Fraction(solution_g + added_water_g) / Fraction(final_density)
    return solute_g, _rounded(Fraction(1000 * n, 1) / final_ml)


PARAMS = {"solution_g": 1264, "mole_fraction": "0.0400",
          "solute_molar_mass": 200, "water_molar_mass": 18,
          "added_water_g": 136, "final_density": "1.400"}
VARIANTS = [
    {**PARAMS, "solution_g": 1084, "mole_fraction": "0.0500",
     "added_water_g": 136, "final_density": "1.220"},
    {**PARAMS, "solution_g": 1804, "mole_fraction": "0.0250",
     "added_water_g": 196, "final_density": "1.250"},
    {**PARAMS, "solution_g": 1410, "mole_fraction": "0.0625",
     "added_water_g": 90, "final_density": "1.500"},
]
ANSWER = (400, Decimal("2.00"))
