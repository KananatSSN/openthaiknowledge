"""SO2 diffuses slower but liquefies more readily than O2."""


def solve(order=(0, 1, 2, 3)):
    truths = (64 < 32, True, False)
    groups = ({1}, {2}, {3}, {2, 3})
    return order.index(groups.index({i + 1 for i, v in enumerate(truths) if v}))


def check(order=(0, 1, 2, 3)):
    from math import sqrt

    relative_diffusion = sqrt(32 / 64)
    boiling_so2, boiling_o2 = -10, -183
    molecular_speeds_identical = False
    claims = (relative_diffusion > 1, boiling_so2 > boiling_o2, molecular_speeds_identical)
    assert claims == (False, True, False)
    return order.index(1)


PARAMS = {"order": (0, 1, 2, 3)}
VARIANTS = [{"order": (1, 0, 2, 3)}, {"order": (2, 3, 0, 1)}, {"order": (3, 1, 2, 0)}]
ANSWER = solve(**PARAMS)
