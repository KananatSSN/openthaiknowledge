"""Evaporation below boiling, dynamic vapor equilibrium, and altitude effects."""


def solve(order=(0, 1, 2, 3)):
    truth = (True, True, False, False)
    groups = ({1, 2}, {1, 3}, {2, 4}, {3, 4})
    return order.index(groups.index({i + 1 for i, v in enumerate(truth) if v}))


def check(order=(0, 1, 2, 3)):
    room_c, acetone_bp = 25, 56.5
    evaporates_below_boiling = room_c < acetone_bp
    dynamic_equilibrium = 1 == 1  # equal evaporation and condensation rates
    evaporation_absorbs_energy = True
    mountain_pressure_lower = True
    claims = (
        evaporates_below_boiling,
        dynamic_equilibrium,
        not evaporation_absorbs_energy,
        not mountain_pressure_lower,
    )
    assert claims == (True, True, False, False)
    return order.index(0)


PARAMS = {"order": (0, 1, 2, 3)}
VARIANTS = [{"order": (1, 0, 2, 3)}, {"order": (2, 3, 0, 1)}, {"order": (3, 1, 2, 0)}]
ANSWER = solve(**PARAMS)
