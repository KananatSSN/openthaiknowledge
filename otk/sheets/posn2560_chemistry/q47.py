"""Source p12, MC47: 47.0% water in 50.0 g has 1.57e24 H atoms (ค)."""

_AVOGADRO = 6.02e23


def solve(water_percent=47.0, sample_g=50.0):
    water_g = sample_g * water_percent / 100
    hydrogen_atoms = 2 * water_g / 18 * _AVOGADRO
    return round(hydrogen_atoms / 1e24, 2)


def check(water_percent=47.0, sample_g=50.0):
    # From Na2SO4·xH2O with M(Na2SO4)=142, infer the integral hydration
    # number, then count its 2x hydrogens per formula unit.
    fraction = water_percent / 100
    hydration = round(142 * fraction / (18 * (1 - fraction)))
    assert hydration > 0
    actual_percent = 100 * 18 * hydration / (142 + 18 * hydration)
    assert abs(actual_percent - water_percent) < 0.06
    formula_units = sample_g / (142 + 18 * hydration) * _AVOGADRO
    return round(2 * hydration * formula_units / 1e24, 2)


PARAMS = {"water_percent": 47.0, "sample_g": 50.0}
VARIANTS = [
    {"water_percent": 38.8, "sample_g": 50.0},  # x=5
    {"water_percent": 55.9, "sample_g": 40.0},  # x=10
    {"water_percent": 47.0, "sample_g": 30.0},  # x=7
]
ANSWER = 1.57
