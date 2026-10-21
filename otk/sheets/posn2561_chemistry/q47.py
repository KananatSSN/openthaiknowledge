"""Source p11, MC47: acetic-acid concentration after bicarbonate reaction."""

from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction


def solve(vinegar_ml=200, density="1.15", acid_percent="5.00", bicarbonate_g="4.200"):
    acid_g = Fraction(vinegar_ml) * Fraction(density) * Fraction(acid_percent) / 100
    initial_acid_mol = acid_g / 60
    bicarbonate_mol = Fraction(bicarbonate_g) / 84
    assert initial_acid_mol > bicarbonate_mol > 0
    residual = initial_acid_mol - bicarbonate_mol
    concentration = residual * 1000 / vinegar_ml
    return (Decimal(concentration.numerator) / Decimal(concentration.denominator)).quantize(
        Decimal("0.001"), rounding=ROUND_HALF_UP,
    )


def check(vinegar_ml=200, density="1.15", acid_percent="5.00", bicarbonate_g="4.200"):
    # Concentration balance: initial molarity minus NaHCO3 moles per litre.
    initial_molarity = Fraction(density) * 1000 * Fraction(acid_percent) / 100 / 60
    consumed_molarity = Fraction(bicarbonate_g) / 84 * 1000 / vinegar_ml
    result = initial_molarity - consumed_molarity
    assert result > 0
    return (Decimal(result.numerator) / Decimal(result.denominator)).quantize(
        Decimal("0.001"), rounding=ROUND_HALF_UP,
    )


PARAMS = {"vinegar_ml": 200, "density": "1.15", "acid_percent": "5.00",
          "bicarbonate_g": "4.200"}
VARIANTS = [
    {"vinegar_ml": 100, "density": "1.10", "acid_percent": "6.00", "bicarbonate_g": "4.200"},
    {"vinegar_ml": 250, "density": "1.20", "acid_percent": "5.00", "bicarbonate_g": "6.300"},
    {"vinegar_ml": 200, "density": "1.05", "acid_percent": "6.00", "bicarbonate_g": "4.200"},
]
ANSWER = Decimal("0.708")
