"""Source p3, MC1: the fourth group has three 18-electron species."""


def _groups(a, d, e, g):
    # (atomic number, charge); isotope mass numbers do not affect electrons.
    return (((a, 1), (a, -1), (d, 1)),
            ((e, -1), (e, 1), (g, 0)),
            ((e, -1), (a, -1), (d, 1)),
            ((e, -1), (g, 0), (a, 1)))


def solve(a=19, d=20, e=17, g=18):
    valid = [index for index, group in enumerate(_groups(a, d, e, g))
             if len({atomic - charge for atomic, charge in group}) == 1]
    assert len(valid) == 1
    return valid[0]


def check(a=19, d=20, e=17, g=18):
    # Independently fill shells for every ion, then compare configurations.
    def shells(atomic, charge):
        remaining = atomic - charge
        filled = []
        for capacity in (2, 8, 8, 18, 18):
            occupied = min(remaining, capacity)
            filled.append(occupied)
            remaining -= occupied
            if not remaining:
                return tuple(filled)
        raise ValueError("electron count outside supported shells")

    matches = [index for index, group in enumerate(_groups(a, d, e, g))
               if len({shells(*species) for species in group}) == 1]
    assert len(matches) == 1
    return matches[0]


PARAMS = {"a": 19, "d": 20, "e": 17, "g": 18}
VARIANTS = [
    {"a": 11, "d": 12, "e": 9, "g": 10},
    {"a": 37, "d": 38, "e": 35, "g": 36},
    {"a": 20, "d": 21, "e": 18, "g": 19},
]
ANSWER = 3
