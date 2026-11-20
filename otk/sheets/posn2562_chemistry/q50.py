"""NH3 limits urea synthesis; 4 mol NH3 give 2 mol urea, 120 g."""


def solve(nh3_g=68, co2_mol=2.5, order=(0, 1, 2, 3)):
    nh3 = nh3_g / 17
    urea = min(nh3 / 2, co2_mol)
    claims = (nh3 == 4, (co2_mol - urea) * 44 == 22, urea * 60 == 75, nh3 / 2 < co2_mol)
    return order.index(claims.index(False))


def check(nh3_g=68, co2_mol=2.5, order=(0, 1, 2, 3)):
    extent = min(nh3_g / (2 * 17), co2_mol)
    spent_nh3 = 2 * extent
    left_co2 = (co2_mol - extent) * 44
    made_urea = extent * 60
    false = (spent_nh3 != 4, left_co2 != 22, made_urea != 75, nh3_g / (2 * 17) >= co2_mol)
    assert false == (False, False, True, False)
    return order.index(2)


PARAMS = {"nh3_g": 68, "co2_mol": 2.5, "order": (0, 1, 2, 3)}
VARIANTS = [
    {"nh3_g": 68, "co2_mol": 2.5, "order": (1, 0, 2, 3)},
    {"nh3_g": 68, "co2_mol": 2.5, "order": (2, 3, 0, 1)},
    {"nh3_g": 68, "co2_mol": 2.5, "order": (3, 1, 2, 0)},
]

ANSWER = solve(**PARAMS)
