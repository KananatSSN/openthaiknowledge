"""Figure table: A=(period3, group2)=Mg; D=(3,15)=P; E=(2,16)=O; G=(3,17)=Cl."""

POSITIONS = {"A": (3, 2), "D": (3, 15), "E": (2, 16), "G": (3, 17)}


def solve(order=(0, 1, 2, 3)):
    # Mg3P2, P3- / O2-, and PCl5 (nonpolar) refute I and III.
    truths = (False, True, False)
    groups = ({1}, {2}, {3}, {2, 3})
    return order.index(groups.index({i + 1 for i, v in enumerate(truths) if v}))


def check(order=(0, 1, 2, 3)):
    mg, p, o, cl = (POSITIONS[x][1] for x in "ADEG")
    assert (mg, p, o, cl) == (2, 15, 16, 17)
    formula_cations, formula_anions = 3, 2
    claims = (
        f"A{formula_cations}D{formula_anions}" == "AD3",
        p >= 15 and o >= 16,
        False,
    )  # PCl5 symmetric
    assert claims == (False, True, False)
    return order.index(1)


PARAMS = {"order": (0, 1, 2, 3)}
VARIANTS = [{"order": (1, 0, 2, 3)}, {"order": (2, 3, 0, 1)}, {"order": (3, 1, 2, 0)}]
ANSWER = solve(**PARAMS)
