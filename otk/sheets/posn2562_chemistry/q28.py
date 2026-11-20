"""MC28: COCl2 is trigonal planar, BrF3 T-shaped with ten S-domain electrons."""


def solve(order=(0, 1, 2, 3)):
    claims = (False, True, 5 * 2 == 10)
    true = tuple(i for i, value in enumerate(claims, 1) if value)
    groups = ((1, 2), (1, 3), (2, 3), (1, 2, 3))
    return order.index(groups.index(true))


def check(order=(0, 1, 2, 3)):
    # SO3 and COCl2 have AX3; BrF3 is AX3E2, with 3 bonds + 2 lone pairs.
    so3, cocl2, brf3 = "trigonal planar", "trigonal planar", "T"
    all_120 = len({so3, cocl2, brf3}) == 1
    different = cocl2 != brf3
    central_electrons = 2 * (3 + 2)
    true = tuple(i for i, value in enumerate((all_120, different,
                                              central_electrons == 10), 1) if value)
    groups = ((1, 2), (1, 3), (2, 3), (1, 2, 3))
    return order.index(groups.index(true))


PARAMS = {"order": (0, 1, 2, 3)}
VARIANTS = [{"order": (2, 0, 1, 3)}, {"order": (1, 3, 2, 0)},
            {"order": (3, 2, 1, 0)}]
ANSWER = solve(**PARAMS)
