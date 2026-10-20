"""Source p5, MC8: an ionic ACl2 points to a +2 metal ion with a noble-gas
configuration (choice ง). The adaptation names a group-2 element explicitly;
the source's bulk properties alone need not uniquely identify A.
"""

_NOBLE = ((10, "Ne"), (18, "Ar"), (36, "Kr"), (54, "Xe"))
_GROUP_TWO = (12, 20, 38, 56)


def solve(atomic=20, charge=2):
    if atomic not in _GROUP_TWO or charge != 2:
        raise ValueError("supported group-2 dichlorides only")
    electrons = atomic - charge
    return next(symbol for count, symbol in _NOBLE if electrons == count)


def check(atomic=20, charge=2):
    # Remove electrons individually from the neutral count, then compare
    # with independently listed closed-shell capacities.
    neutral = list(range(atomic))
    for _ in range(charge):
        neutral.pop()
    closed_shells = {"Ne": (2, 8), "Ar": (2, 8, 8),
                     "Kr": (2, 8, 18, 8), "Xe": (2, 8, 18, 18, 8)}
    return next(name for name, shells in closed_shells.items()
                if len(neutral) == sum(shells))


PARAMS = {"atomic": 20, "charge": 2}
VARIANTS = [
    {"atomic": 12, "charge": 2},
    {"atomic": 38, "charge": 2},
    {"atomic": 56, "charge": 2},
]
ANSWER = "Ar"
