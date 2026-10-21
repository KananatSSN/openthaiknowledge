"""Source p10, MC41: NaN3 mass for N2 from both airbag reactions."""

from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction


R = Fraction("0.082")  # L atm mol-1 K-1, printed on the source constants page


def solve(nitrogen_l="31", temperature_c=37, pressure_mmhg=760):
    assert Fraction(nitrogen_l) > 0 and temperature_c > -273 and pressure_mmhg > 0
    nitrogen_mol = Fraction(pressure_mmhg, 760) * Fraction(nitrogen_l)
    nitrogen_mol /= R * (temperature_c + 273)
    # 2NaN3 -> 3N2 + 2Na; 10Na -> N2: 8/5 mol N2 per mol NaN3.
    mass_g = nitrogen_mol * Fraction(5, 8) * 65
    return (Decimal(mass_g.numerator) / Decimal(mass_g.denominator)).quantize(
        Decimal("0.1"), rounding=ROUND_HALF_UP,
    )


def check(nitrogen_l="31", temperature_c=37, pressure_mmhg=760):
    # Forward-predict gas volume for each tenth-gram loading and choose closest.
    target = Fraction(nitrogen_l)
    temperature = temperature_c + 273
    pressure = Fraction(pressure_mmhg, 760)
    def volume(tenths):
        azide_mol = Fraction(tenths, 650)
        decomposition = Fraction(3, 2) * azide_mol
        nitrate_reaction = azide_mol / 10
        return (decomposition + nitrate_reaction) * R * temperature / pressure
    best = min(range(1, 2001), key=lambda tenths: abs(volume(tenths) - target))
    return Decimal(best) / 10


PARAMS = {"nitrogen_l": "31", "temperature_c": 37, "pressure_mmhg": 760}
VARIANTS = [
    {"nitrogen_l": "25", "temperature_c": 27, "pressure_mmhg": 760},
    {"nitrogen_l": "40", "temperature_c": 37, "pressure_mmhg": 760},
    {"nitrogen_l": "31", "temperature_c": 37, "pressure_mmhg": 380},
]
ANSWER = Decimal("49.5")
