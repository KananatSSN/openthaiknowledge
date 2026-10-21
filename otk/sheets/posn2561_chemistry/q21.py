"""Source p6, MC21: cyanogen N≡C–C≡N has one single and two triples."""


OPTIONS = (
    (1, 0, 1, 1),
    (1, 0, 2, 2),
    (1, 2, 0, 2),
    (2, 1, 2, 2),
)


def solve(options=(0, 1, 2, 3)):
    assert sorted(options) == [0, 1, 2, 3]
    # Octet-satisfying neutral cyanogen: N≡C–C≡N. Each terminal N has
    # one lone pair; each C has four bonding pairs.
    orders = (3, 1, 3)
    counts = (orders.count(1), orders.count(2), orders.count(3), 2)
    matches = [i for i, option in enumerate(options) if OPTIONS[option] == counts]
    assert len(matches) == 1
    return matches[0]


def check(options=(0, 1, 2, 3)):
    # Independently enumerate N-C-C-N bond orders under neutral-octet
    # constraints: N has 3 bonds and one lone pair; C has 4 bonds.
    valid = []
    for left in range(1, 4):
        for middle in range(1, 4):
            for right in range(1, 4):
                if left == right == 3 and left + middle == middle + right == 4:
                    bonds = (left, middle, right)
                    valid.append((bonds.count(1), bonds.count(2), bonds.count(3), 2))
    assert valid == [(1, 0, 2, 2)]
    return [OPTIONS[option] for option in options].index(valid[0])


PARAMS = {"options": (0, 1, 2, 3)}
VARIANTS = [
    {"options": (1, 0, 2, 3)},
    {"options": (2, 3, 1, 0)},
    {"options": (3, 2, 0, 1)},
]
ANSWER = 1
