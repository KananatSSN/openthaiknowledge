"""98-55 gives Tc Z=43; Tc(III) loses 5s2 then one 4d electron."""


def solve(mass=98, neutrons=55, charge=3, order=(0, 1, 2, 3)):
    z = mass - neutrons
    assert z == 43 and charge == 3
    d, s = 5, 2
    removed_s = min(charge, s)
    removed_d = charge - removed_s
    config = (d - removed_d, s - removed_s)
    choices = ((5, 0), (3, 1), (4, 0), (2, 2))
    return order.index(choices.index(config))


def check(mass=98, neutrons=55, charge=3, order=(0, 1, 2, 3)):
    assert mass - neutrons == 43
    electrons = 43 - charge
    krypton_core = 36
    valence = electrons - krypton_core
    assert valence == 4
    choices = ((5, 0), (3, 1), (4, 0), (2, 2))
    return order.index(choices.index((valence, 0)))


PARAMS = {"mass": 98, "neutrons": 55, "charge": 3, "order": (0, 1, 2, 3)}
VARIANTS = [
    {"mass": 100, "neutrons": 57, "charge": 3, "order": (1, 0, 2, 3)},
    {"mass": 99, "neutrons": 56, "charge": 3, "order": (2, 3, 0, 1)},
    {"mass": 101, "neutrons": 58, "charge": 3, "order": (3, 1, 2, 0)},
]

ANSWER = solve(**PARAMS)
