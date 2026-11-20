"""Source p11, MC42: 2.72 g ZnCl2 means 74.0% Cu in a 5.00 g alloy (ง)."""

from decimal import Decimal, ROUND_HALF_UP

_ZN = Decimal("65.0")
_CL = Decimal("35.5")
_ZNCL2 = _ZN + 2 * _CL


def solve(alloy_g=5.00, zinc_chloride_g=2.72):
    zinc_g = Decimal(str(zinc_chloride_g)) * _ZN / _ZNCL2
    percent_copper = 100 * (Decimal(str(alloy_g)) - zinc_g) / Decimal(str(alloy_g))
    return float(percent_copper.quantize(Decimal("0.1"), rounding=ROUND_HALF_UP))


def check(alloy_g=5.00, zinc_chloride_g=2.72):
    chloride_mass_fraction = (2 * 35.5) / 136.0
    zinc_mass = zinc_chloride_g * (1 - chloride_mass_fraction)
    copper_mass = alloy_g - zinc_mass
    return round(100 * copper_mass / alloy_g, 1)


PARAMS = {"alloy_g": 5.00, "zinc_chloride_g": 2.72}
VARIANTS = [
    {"alloy_g": 5.00, "zinc_chloride_g": 1.36},
    {"alloy_g": 8.00, "zinc_chloride_g": 6.80},
    {"alloy_g": 10.00, "zinc_chloride_g": 4.08},
]
ANSWER = 74.0
