"""Source p12, MC50: a and b require exact stoichiometric BaCl2 addition.

The source only says all sulfate precipitates, which also permits excess
BaCl2. The generated prompt explicitly states exact stoichiometric mixing.
"""


def _actual(sulfate_percent=14.2, sulfate_ml=10, barium_molar=0.25):
    # Percent w/v is grams Na2SO4 per 100 mL. M(Na2SO4)=142,
    # M(BaSO4)=233 and M(Na)=23 g/mol.
    sulfate_mol = sulfate_percent * sulfate_ml / 100 / 142
    barium_ml = sulfate_mol / barium_molar * 1000
    precipitate_g = sulfate_mol * 233
    sodium_g = 2 * sulfate_mol * 23
    sodium_percent = sodium_g / (sulfate_ml + barium_ml) * 100
    return barium_ml, precipitate_g, sodium_percent


def solve(sulfate_percent=14.2, sulfate_ml=10, barium_molar=0.25,
          claim_x_ml=40, claim_precipitate_g=2.33, claim_sodium_percent=4.6):
    actual = _actual(sulfate_percent, sulfate_ml, barium_molar)
    claims = (claim_x_ml, claim_precipitate_g, claim_sodium_percent)
    return tuple(i for i, (value, expected) in enumerate(zip(claims, actual))
                 if abs(value - expected) < 0.011)


def check(sulfate_percent=14.2, sulfate_ml=10, barium_molar=0.25,
          claim_x_ml=40, claim_precipitate_g=2.33, claim_sodium_percent=4.6):
    # Mass balance in the aliquot, then charge/atom balance in the filtrate.
    sodium_sulfate_g = sulfate_percent * sulfate_ml / 100
    molar_sulfate = 2 * 23 + 32 + 4 * 16
    reacted_moles = sodium_sulfate_g / molar_sulfate
    barium_solution_ml = reacted_moles * 1000 / barium_molar
    solid_g = reacted_moles * (137 + 32 + 4 * 16)
    filtrate_sodium_g = reacted_moles * 2 * 23
    filtrate_ml = sulfate_ml + barium_solution_ml
    measured = (barium_solution_ml, solid_g, filtrate_sodium_g * 100 / filtrate_ml)
    stated = (claim_x_ml, claim_precipitate_g, claim_sodium_percent)
    return tuple(i for i in range(3) if abs(measured[i] - stated[i]) < 0.011)


PARAMS = {"sulfate_percent": 14.2, "sulfate_ml": 10, "barium_molar": 0.25,
          "claim_x_ml": 40, "claim_precipitate_g": 2.33, "claim_sodium_percent": 4.6}
VARIANTS = [
    {"sulfate_percent": 14.2, "sulfate_ml": 20, "barium_molar": 0.5,
     "claim_x_ml": 40, "claim_precipitate_g": 2.33, "claim_sodium_percent": 4.6},
    {"sulfate_percent": 7.1, "sulfate_ml": 20, "barium_molar": 0.25,
     "claim_x_ml": 20, "claim_precipitate_g": 2.33, "claim_sodium_percent": 4.6},
    {"sulfate_percent": 14.2, "sulfate_ml": 10, "barium_molar": 0.25,
     "claim_x_ml": 20, "claim_precipitate_g": 2.33, "claim_sodium_percent": 0.92},
]
ANSWER = (0, 1)
