"""Source p11, MC40: STP density 1.25 g/L gives 140 g for 5 mol (ข)."""

from decimal import Decimal, ROUND_HALF_UP


def solve(density_g_l=1.25, amount_mol=5):
    value = Decimal(str(density_g_l)) * Decimal("22.4") * Decimal(str(amount_mol))
    return float(value.quantize(Decimal("0.1"), rounding=ROUND_HALF_UP))


def check(density_g_l=1.25, amount_mol=5):
    sample_volume_l = 22.4 * amount_mol
    return round(density_g_l * sample_volume_l, 1)


PARAMS = {"density_g_l": 1.25, "amount_mol": 5}
VARIANTS = [
    {"density_g_l": 1.50, "amount_mol": 3},
    {"density_g_l": 0.75, "amount_mol": 4},
    {"density_g_l": 2.00, "amount_mol": 2},
]
ANSWER = 140.0
