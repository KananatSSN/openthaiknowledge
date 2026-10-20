"""Source p9, MC31: IF4+ has 10 electrons around iodine (choice ง)."""


def solve(species=(("I", 1, 0), ("I", 2, 1), ("I", 3, 2), ("I", 4, 1))):
    # For XF_n^(q+), the central-atom electron count after filling the
    # terminal F octets is 7+n-q.
    matches = [item for item in species if 7 + item[1] - item[2] != 8]
    assert len(matches) == 1
    return matches[0]


def check(species=(("I", 1, 0), ("I", 2, 1), ("I", 3, 2), ("I", 4, 1))):
    matches = []
    for item in species:
        _, bonded, charge = item
        total_valence = 7 + 7 * bonded - charge
        terminal_lone_electrons = 6 * bonded
        bonding_electrons = 2 * bonded
        central_lone_electrons = (total_valence - terminal_lone_electrons
                                  - bonding_electrons)
        assert central_lone_electrons >= 0 and central_lone_electrons % 2 == 0
        central_shell = bonding_electrons + central_lone_electrons
        if central_shell != 8:
            matches.append(item)
    assert len(matches) == 1
    return matches[0]


PARAMS = {"species": (("I", 1, 0), ("I", 2, 1), ("I", 3, 2), ("I", 4, 1))}
VARIANTS = [
    {"species": (("I", 5, 0), ("I", 2, 1), ("I", 3, 2), ("I", 4, 3))},
    {"species": (("I", 1, 0), ("Br", 4, 1), ("Br", 3, 2), ("I", 2, 1))},
    {"species": (("Cl", 3, 0), ("I", 2, 1), ("Br", 3, 2), ("I", 4, 3))},
]
ANSWER = ("I", 4, 1)
