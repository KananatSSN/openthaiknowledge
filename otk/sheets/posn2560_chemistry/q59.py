"""Source p14, MC59: mixed CaCl2 solution is 35.5 g/L (ง)."""


def solve(first_molar=1.00, first_ml=20.0, second_molar=0.200,
          second_ml=60.0, final_ml=100.0):
    ca_moles = (first_molar * first_ml + second_molar * second_ml) / 1000
    molar_mass = 40 + 2 * 35.5
    return round(ca_moles * molar_mass / (final_ml / 1000), 1)


def check(first_molar=1.00, first_ml=20.0, second_molar=0.200,
          second_ml=60.0, final_ml=100.0):
    # Count mass from each stock separately, then divide by final volume.
    first_g = first_molar * first_ml * 111 / 1000
    second_g = second_molar * second_ml * 111 / 1000
    assert final_ml >= first_ml + second_ml
    return round(1000 * (first_g + second_g) / final_ml, 1)


PARAMS = {"first_molar": 1.00, "first_ml": 20.0,
          "second_molar": 0.200, "second_ml": 60.0, "final_ml": 100.0}
VARIANTS = [
    {"first_molar": 1.00, "first_ml": 10.0,
     "second_molar": 0.200, "second_ml": 50.0, "final_ml": 100.0},
    {"first_molar": 0.500, "first_ml": 40.0,
     "second_molar": 0.200, "second_ml": 20.0, "final_ml": 100.0},
    {"first_molar": 0.800, "first_ml": 25.0,
     "second_molar": 0.300, "second_ml": 50.0, "final_ml": 125.0},
]
ANSWER = 35.5
