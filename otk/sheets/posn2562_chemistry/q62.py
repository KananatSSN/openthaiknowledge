"""Oxidation numbers N: nitrate +5, ammonium -3, hydrazine -2, N2O average +1."""


def solve(order=(0, 1, 2, 3)):
    values = (5, -3, -2, 1)
    choices = ((5, -3, -2, 1), (3, -3, -2, 1), (5, 3, -2, 1), (5, -3, -1, 2))
    return order.index(choices.index(values))


def check(order=(0, 1, 2, 3)):
    nitrate = -(3 * -2 + 1)
    ammonium = 1 - 4
    hydrazine = -4 / 2
    nitrous_oxide = 2 / 2
    assert (nitrate, ammonium, hydrazine, nitrous_oxide) == (5, -3, -2, 1)
    return order.index(0)


PARAMS = {"order": (0, 1, 2, 3)}
VARIANTS = [{"order": (1, 0, 2, 3)}, {"order": (2, 3, 0, 1)}, {"order": (3, 1, 2, 0)}]

ANSWER = solve(**PARAMS)
