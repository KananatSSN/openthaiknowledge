"""Source MC1: compare protons, neutrons and electrons in two isotopes."""


def solve(a=120, z=50, charge=4, b=124, other_z=54):
    claims = (abs((a - z) - (b - other_z)) == 4,
              z > other_z,
              other_z - (z - charge) == 8,
              (a - z, z, z - charge) == (b - other_z, other_z, other_z))
    matches = [i for i, claim in enumerate(claims) if claim]
    assert len(matches) == 1
    return matches[0]


def check(a=120, z=50, charge=4, b=124, other_z=54):
    first = {"p": z, "n": a - z, "e": z - charge}
    second = {"p": other_z, "n": b - other_z, "e": other_z}
    tests = (abs(first["n"] - second["n"]) == 4,
             first["p"] > second["p"],
             second["e"] == first["e"] + 8,
             first == second)
    return tests.index(True) if tests.count(True) == 1 else None


PARAMS = {"a": 120, "z": 50, "charge": 4, "b": 124, "other_z": 54}
VARIANTS = [
    {"a": 112, "z": 48, "charge": 4, "b": 116, "other_z": 52},
    {"a": 116, "z": 49, "charge": 3, "b": 120, "other_z": 54},
    {"a": 122, "z": 51, "charge": 3, "b": 126, "other_z": 56},
]
ANSWER = solve(**PARAMS)
