"""MC20: ozone-health and heavy-metal superoxide claims are false.

The source's fourth claim is overbroad: oxygen can have a non--2 state with
fluorine or an O-O bond. The adaptation explicitly restricts conventional
oxoanions to no fluorine and no peroxide linkage.
"""


def solve(order=(0, 1, 2, 3)):
    statements = (False, False, True, True)
    false = {i + 1 for i, truth in enumerate(statements) if not truth}
    groups = ({1, 2}, {3, 4}, {1, 3}, {2, 4})
    return order.index(groups.index(false))


def check(order=(0, 1, 2, 3)):
    # Ground-level O3 irritates the respiratory tract. Group-1 cations
    # stabilise superoxides; H2O2 disinfects. In NO3-, O is -2.
    wrong = (True, True, False, (5 + 3 * (-2) != -1))
    assert wrong == (True, True, False, False)
    combinations = ((1, 2), (3, 4), (1, 3), (2, 4))
    return order.index(combinations.index((1, 2)))


PARAMS = {"order": (0, 1, 2, 3)}
VARIANTS = [{"order": (2, 0, 1, 3)}, {"order": (1, 3, 0, 2)},
            {"order": (3, 2, 1, 0)}]
ANSWER = solve(**PARAMS)
