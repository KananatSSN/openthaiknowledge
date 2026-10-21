"""Source p3, MC5: fluorine is the most reactive nonmetal among C, F, Na, Cl."""


def solve(options=(6, 9, 11, 17)):
    # Restricted pool: each option group contains two halogens. Their
    # elemental reactivity decreases down group 17.
    halogens = [z for z in options if z in (9, 17, 35)]
    assert len(options) == 4 and len(halogens) == 2
    return min(halogens)


def check(options=(6, 9, 11, 17)):
    # An independent numeric electronegativity comparison confirms the
    # intended winner for every chosen option pool.
    electronegativity = {6: 2.55, 8: 3.44, 9: 3.98, 11: 0.93,
                         12: 1.31, 17: 3.16, 20: 1.00, 35: 2.96}
    winner = max(options, key=lambda z: electronegativity[z])
    assert len(set(options)) == 4
    return winner


PARAMS = {"options": (6, 9, 11, 17)}
VARIANTS = [
    {"options": (6, 17, 11, 35)},
    {"options": (8, 9, 12, 17)},
    {"options": (6, 17, 20, 35)},
]
ANSWER = 9
