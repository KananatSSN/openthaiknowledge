"""Source p12, MC46: CO limits methanol synthesis to 400 g (ก)."""


def solve(co_g=350, hydrogen_g=65.0):
    # CO + 2H2 -> CH3OH; molar masses 28, 2 and 32 g/mol.
    extent = min(co_g / 28, hydrogen_g / 4)
    return round(extent * 32, 1)


def check(co_g=350, hydrogen_g=65.0):
    possible_from_carbon = co_g * 32 / 28
    possible_from_hydrogen = hydrogen_g * 32 / 4
    return round(min(possible_from_carbon, possible_from_hydrogen), 1)


PARAMS = {"co_g": 350, "hydrogen_g": 65.0}
VARIANTS = [
    {"co_g": 280, "hydrogen_g": 30.0},
    {"co_g": 140, "hydrogen_g": 20.0},
    {"co_g": 224, "hydrogen_g": 24.0},
]
ANSWER = 400.0
