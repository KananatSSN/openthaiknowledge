"""Source MC9: a group-16 trioxide is acidic; a group-2 monoxide is basic."""


def solve(nonmetal="S", metal="Ca"):
    assert nonmetal in ("S", "Se") and metal in ("Ca", "Mg", "Ba")
    claims = (False, False, False, True)
    return claims.index(True)


def check(nonmetal="S", metal="Ca"):
    assert nonmetal in ("S", "Se") and metal in ("Ca", "Mg", "Ba")
    # XO3 + H2O -> H2XO4; neutralisation needs 2 NaOH.
    sodium_count = 2
    chloride_count = 2  # MO + 2HCl -> MCl2 + H2O.
    blue_litmus_red = True
    truths = (False, sodium_count == 1, chloride_count == 1,
              blue_litmus_red)
    return truths.index(True) if truths.count(True) == 1 else None


PARAMS = {"nonmetal": "S", "metal": "Ca"}
VARIANTS = [
    {"nonmetal": "S", "metal": "Mg"},
    {"nonmetal": "Se", "metal": "Ca"},
    {"nonmetal": "Se", "metal": "Ba"},
]
ANSWER = solve(**PARAMS)
