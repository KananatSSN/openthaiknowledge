"""Ice and dry ice are distinct molecular crystals; solid NaCl is not conductive."""


def solve(order=(0, 1, 2, 3)):
    claims = (False, True, False, False)
    return order.index(claims.index(True))


def check(order=(0, 1, 2, 3)):
    salt_ions_mobile = False
    crystal_units = ("H2O", "CO2")
    fullerene_conducts_like_graphite = False
    sulfur_formulas = ("S8", "S8")
    truths = (
        salt_ions_mobile,
        crystal_units[0] != crystal_units[1],
        fullerene_conducts_like_graphite,
        sulfur_formulas[0] != sulfur_formulas[1],
    )
    assert truths == (False, True, False, False)
    return order.index(1)


PARAMS = {"order": (0, 1, 2, 3)}
VARIANTS = [{"order": (1, 0, 2, 3)}, {"order": (2, 3, 0, 1)}, {"order": (3, 1, 2, 0)}]
ANSWER = solve(**PARAMS)
