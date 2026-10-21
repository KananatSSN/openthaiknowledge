"""Source MC10: a group-13 trichloride forms covalent bonds and hydrolyses."""


def solve(z=5, order=(0, 1, 2, 3)):
    assert z in (5, 13, 31)
    claims = tuple((False, True, False, False)[i] for i in order)
    return claims.index(True)


def check(z=5, order=(0, 1, 2, 3)):
    configurations = {5: (2, 3), 13: (2, 8, 3), 31: (2, 8, 18, 3)}
    assert configurations[z][-1] == 3
    # Three valence bonds to Cl; BCl3, AlCl3 and GaCl3 hydrolyse to acidic media.
    formula_subscript = configurations[z][-1]
    covalent = z in configurations
    water_neutral = False
    claims = (formula_subscript == 2, covalent,
              z == 5 and water_neutral, water_neutral)
    ordered = [claims[i] for i in order]
    return ordered.index(True) if ordered.count(True) == 1 else None


PARAMS = {"z": 5, "order": (0, 1, 2, 3)}
VARIANTS = [
    {"z": 13, "order": (1, 0, 2, 3)},
    {"z": 31, "order": (2, 1, 3, 0)},
    {"z": 5, "order": (3, 2, 0, 1)},
]
ANSWER = solve(**PARAMS)
