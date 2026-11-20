"""MC18: Bh is group 7; alpha decay gives Z=105 and A-4 nucleons.

BhO2 is presented as a possible +4 oxide by group analogy, not as an
experimentally isolated compound.
"""


def solve(mass=274, order=(0, 1, 2, 3)):
    daughter_z = 107 - 2
    daughter_neutrons = mass - 4 - daughter_z
    claims = (daughter_z == 105 and daughter_neutrons == mass - 107,
              True, 2 * (-2) + 4 == 0)
    correct = {i + 1 for i, yes in enumerate(claims) if yes}
    groups = ({1, 2}, {2, 3}, {1, 3}, {2})
    return order.index(groups.index(correct))


def check(mass=274, order=(0, 1, 2, 3)):
    # Alpha particle removes 2p+2n. Bh parallels group-7 Mn, whose +4 oxide exists.
    parent_neutrons = mass - 107
    daughter = (105, parent_neutrons - 2)
    first = daughter == (105, parent_neutrons)
    second = 107 in (25, 43, 75, 107)
    third = 4 + 2 * (-2) == 0
    groups = ((1, 2), (2, 3), (1, 3), (2,))
    truths = tuple(i for i, yes in enumerate((first, second, third), 1) if yes)
    return order.index(groups.index(truths))


PARAMS = {"mass": 274, "order": (0, 1, 2, 3)}
VARIANTS = [
    {"mass": 272, "order": (1, 0, 2, 3)},
    {"mass": 270, "order": (2, 1, 3, 0)},
    {"mass": 268, "order": (3, 0, 1, 2)},
]
ANSWER = solve(**PARAMS)
