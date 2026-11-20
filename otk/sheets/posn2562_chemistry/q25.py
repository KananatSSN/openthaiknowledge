"""MC25: the first pictured NCO- structure gives central C five bond pairs."""

BONDS = ((3, 2), (3, 1), (2, 2), (1, 3))


def solve(order=(0, 1, 2, 3)):
    impossible = [i for i, (n_bond, o_bond) in enumerate(BONDS)
                  if n_bond + o_bond > 4]
    assert impossible == [0]
    return order.index(impossible[0])


def check(order=(0, 1, 2, 3)):
    # Carbon has no lone pairs here; each bond order contributes two electrons.
    carbon_electrons = [2 * (n + o) for n, o in BONDS]
    invalid = [i for i, electrons in enumerate(carbon_electrons) if electrons != 8]
    assert invalid == [0]
    return order.index(invalid[0])


PARAMS = {"order": (0, 1, 2, 3)}
VARIANTS = [{"order": (1, 0, 2, 3)}, {"order": (2, 3, 0, 1)},
            {"order": (3, 1, 2, 0)}]
ANSWER = solve(**PARAMS)
