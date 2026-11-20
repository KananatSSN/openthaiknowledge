"""Source p9, MC35: air needed for complete combustion of a gas mixture."""

from fractions import Fraction


# Tenths of a percent, in source order: CO2, CO, H2, CH4, C2H4, Ar.
GAS_TENTHS = (120, 280, 30, 5, 5, 560)
GAS_NAMES = ("CO₂", "CO", "H₂", "CH₄", "C₂H₄", "Ar")
OXYGEN_PER_MOLE = (0, Fraction(1, 2), Fraction(1, 2), 2, 3, 0)


def solve(gas_volume_m3=200, air_oxygen_percent=20):
    assert sum(GAS_TENTHS) == 1000
    assert gas_volume_m3 > 0 and 0 < air_oxygen_percent <= 100
    oxygen_fraction = sum(Fraction(p, 1000) * required
                          for p, required in zip(GAS_TENTHS, OXYGEN_PER_MOLE))
    air_volume = gas_volume_m3 * oxygen_fraction * 100 / air_oxygen_percent
    assert air_volume.denominator == 1
    return int(air_volume)


def check(gas_volume_m3=200, air_oxygen_percent=20):
    # Independent O-atom balance per 1000 gas units: CO needs one O atom,
    # H2 one, CH4 four, and C2H4 six; CO2 and Ar need none.
    oxygen_atoms = 280 + 30 + 5 * 4 + 5 * 6
    assert oxygen_atoms == 360
    oxygen_molecules_per_thousand = Fraction(oxygen_atoms, 2)
    result = Fraction(gas_volume_m3 * oxygen_molecules_per_thousand, 1000)
    result *= Fraction(100, air_oxygen_percent)
    assert result.denominator == 1
    return int(result)


PARAMS = {"gas_volume_m3": 200, "air_oxygen_percent": 20}
VARIANTS = [
    {"gas_volume_m3": 100, "air_oxygen_percent": 20},
    {"gas_volume_m3": 200, "air_oxygen_percent": 16},
    {"gas_volume_m3": 400, "air_oxygen_percent": 20},
]
ANSWER = 180
