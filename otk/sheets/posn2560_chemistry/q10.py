"""Source p5, MC10: B pairs two 2p electrons while a 2p box is empty.

Figure reading from the rendered page (2s count; three 2p occupations):
A=(2;1,1,1), B=(2;2,1,0), C=(1;2,1,1), D=(2;2,1,1).
All have paired 1s electrons. B alone violates Hund's rule; C is an
excited configuration but does not violate Pauli exclusion.
"""


def _valid(pattern):
    s, p = pattern
    if s not in (1, 2) or len(p) != 3 or any(n not in (0, 1, 2) for n in p):
        raise ValueError("invalid 2s/2p orbital diagram")
    electrons = sum(p)
    singly = p.count(1)
    return singly == min(electrons, 6 - electrons)


def solve(patterns=((2, (1, 1, 1)), (2, (2, 1, 0)),
                    (1, (2, 1, 1)), (2, (2, 1, 1)))):
    wrong = [i for i, pattern in enumerate(patterns) if not _valid(pattern)]
    if len(wrong) != 1:
        raise ValueError("expected exactly one Hund violation")
    return wrong[0]


def check(patterns=((2, (1, 1, 1)), (2, (2, 1, 0)),
                    (1, (2, 1, 1)), (2, (2, 1, 1)))):
    # Enumerate all Pauli-allowed occupations with the same number of 2p
    # electrons, and compare their maximum unpaired counts.
    from itertools import product

    violations = []
    for index, (_, orbitals) in enumerate(patterns):
        count = sum(orbitals)
        possible = (boxes for boxes in product(range(3), repeat=3)
                    if sum(boxes) == count)
        best = max(boxes.count(1) for boxes in possible)
        if orbitals.count(1) < best:
            violations.append(index)
    assert len(violations) == 1
    return violations[0]


PARAMS = {"patterns": ((2, (1, 1, 1)), (2, (2, 1, 0)),
                       (1, (2, 1, 1)), (2, (2, 1, 1)))}
VARIANTS = [
    {"patterns": ((2, (2, 1, 0)), (2, (1, 1, 1)),
                  (1, (2, 1, 1)), (2, (2, 1, 1)))},
    {"patterns": ((2, (1, 1, 1)), (1, (2, 1, 1)),
                  (2, (2, 1, 0)), (2, (2, 1, 1)))},
    {"patterns": ((2, (1, 1, 0)), (2, (2, 2, 0)),
                  (2, (1, 1, 1)), (1, (2, 1, 1)))},
]
ANSWER = 1
