"""Effective contacts in dry ice exceed those in dilute CO2 gas."""

CLAIMS = (True, False, False)


def solve(order=(0, 1, 2, 3)):
    groups = ({1}, {2}, {3}, {1, 2, 3})
    return order.index(groups.index({i + 1 for i, v in enumerate(CLAIMS) if v}))


def check(order=(0, 1, 2, 3)):
    # Sublimation and evaporation overcome intermolecular contacts, not C-O/O-H bonds.
    contact = ("many", "few")
    water_covalent_bond_broken = False
    graphite_layer_covalent_bond_broken = False
    truths = (
        contact[0] != contact[1],
        water_covalent_bond_broken,
        graphite_layer_covalent_bond_broken,
    )
    assert truths == (True, False, False)
    return order.index(0)


PARAMS = {"order": (0, 1, 2, 3)}
VARIANTS = [{"order": (1, 0, 2, 3)}, {"order": (2, 3, 0, 1)}, {"order": (3, 1, 2, 0)}]
ANSWER = solve(**PARAMS)
