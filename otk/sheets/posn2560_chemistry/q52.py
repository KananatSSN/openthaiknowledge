"""Source p13, MC52: C has molar mass 44 g/mol (ข)."""


def solve(a_g=20.8, b_g=80.5, c_g=70.4, a_molar=52, b_molar=32):
    # A + 5B -> 4C + 2D.
    extent = min(a_g / a_molar, b_g / (5 * b_molar))
    assert extent > 0
    return round(c_g / (4 * extent), 1)


def check(a_g=20.8, b_g=80.5, c_g=70.4, a_molar=52, b_molar=32):
    # Independently calculate the C yield allowed by each feedstock.
    c_moles_from_a = 4 * a_g / a_molar
    c_moles_from_b = 4 / 5 * b_g / b_molar
    produced_c_moles = min(c_moles_from_a, c_moles_from_b)
    return round(c_g / produced_c_moles, 1)


PARAMS = {"a_g": 20.8, "b_g": 80.5, "c_g": 70.4,
          "a_molar": 52, "b_molar": 32}
VARIANTS = [
    {"a_g": 10.4, "b_g": 40.0, "c_g": 28.8, "a_molar": 52, "b_molar": 32},
    {"a_g": 20.8, "b_g": 32.0, "c_g": 40.8, "a_molar": 52, "b_molar": 32},
    {"a_g": 15.6, "b_g": 48.0, "c_g": 100.8, "a_molar": 52, "b_molar": 32},
]
ANSWER = 44.0
