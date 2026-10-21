"""MC15: cobalt's NH3 and Br ligands bind by coordination, not ionic bonds."""


def solve(order=(0, 1, 2, 3)):
    complex_charge = 2  # sulfate counterion is SO4(2-)
    cobalt_oxidation = complex_charge + 1  # coordinated bromide is Br-
    claims = (True, cobalt_oxidation == 3, complex_charge == 2, False)
    return order.index(claims.index(False))


def check(order=(0, 1, 2, 3)):
    # Independently total formal charges in [Co(NH3)5Br]SO4.
    sulfate = -2
    bromide = -1
    ammine = 0
    cobalt = -(sulfate + bromide + 5 * ammine)
    false_claims = (False, cobalt != 3, cobalt + bromide != 2, True)
    assert false_claims.count(True) == 1
    return order.index(false_claims.index(True))


PARAMS = {"order": (0, 1, 2, 3)}
VARIANTS = [{"order": (3, 0, 1, 2)}, {"order": (1, 3, 2, 0)},
            {"order": (2, 1, 0, 3)}]
ANSWER = solve(**PARAMS)
