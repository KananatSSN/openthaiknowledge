"""Source p18, written 7: incomplete two-step reaction gives D=12.0 g, E=4.5 g."""


def solve(initial_a_mol=0.25, a_reacted_percent=60.0,
          c_decomposed_percent=75.0, d_molar=80, e_molar=120):
    a_reacted = initial_a_mol * a_reacted_percent / 100
    c_formed = a_reacted * 2 / 3
    c_decomposed = c_formed * c_decomposed_percent / 100
    return round(c_decomposed * 2 * d_molar, 1), round(c_decomposed / 2 * e_molar, 1)


def check(initial_a_mol=0.25, a_reacted_percent=60.0,
          c_decomposed_percent=75.0, d_molar=80, e_molar=120):
    # Reaction extents: 3A+B->2C and 2C->4D+E.
    first_extent = initial_a_mol * a_reacted_percent / 100 / 3
    second_extent = 2 * first_extent * c_decomposed_percent / 100 / 2
    assert 0 < a_reacted_percent <= 100 and 0 < c_decomposed_percent <= 100
    return round(4 * second_extent * d_molar, 1), round(second_extent * e_molar, 1)


PARAMS = {"initial_a_mol": 0.25, "a_reacted_percent": 60.0,
          "c_decomposed_percent": 75.0, "d_molar": 80, "e_molar": 120}
VARIANTS = [
    {"initial_a_mol": 0.30, "a_reacted_percent": 50.0,
     "c_decomposed_percent": 80.0, "d_molar": 90, "e_molar": 100},
    {"initial_a_mol": 0.40, "a_reacted_percent": 75.0,
     "c_decomposed_percent": 50.0, "d_molar": 70, "e_molar": 150},
    {"initial_a_mol": 0.36, "a_reacted_percent": 50.0,
     "c_decomposed_percent": 75.0, "d_molar": 80, "e_molar": 120},
]
ANSWER = (12.0, 4.5)
