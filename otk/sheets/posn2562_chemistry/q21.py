"""MC21: nitrate resonates; ammonium bromide is ionic between its ions."""


def solve(order=(0, 1, 2, 3)):
    claims = (True, False, True)
    true = {i + 1 for i, value in enumerate(claims) if value}
    groups = ({1, 2}, {1, 3}, {2, 3}, {1, 2, 3})
    return order.index(groups.index(true))


def check(order=(0, 1, 2, 3)):
    nitrate_bond_positions = 3
    salt_has_ionic_interaction = True
    shared_triple_bond_electrons = 3 * 2
    true = tuple(i for i, value in enumerate((nitrate_bond_positions > 1,
                                              not salt_has_ionic_interaction,
                                              shared_triple_bond_electrons == 6), 1)
                 if value)
    groups = ((1, 2), (1, 3), (2, 3), (1, 2, 3))
    return order.index(groups.index(true))


PARAMS = {"order": (0, 1, 2, 3)}
VARIANTS = [{"order": (1, 0, 2, 3)}, {"order": (2, 3, 1, 0)},
            {"order": (3, 1, 0, 2)}]
ANSWER = solve(**PARAMS)
