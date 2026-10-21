"""Source p3, MC4: only the second-shell claim is certain for every X.

X may be any period-2 element, Z has six more protons. The source asks for
the most reliable statement. The adaptation says "always" explicitly.
"""


def _period(z):
    return 2 if z <= 10 else 3


def _second_shell(z):
    return min(z - 2, 8)


def _outer_shell(z):
    return z - (2 if z <= 10 else 10)


def solve(x_min=3, x_max=10, offset=6):
    values = range(x_min, x_max + 1)
    assert 3 <= x_min < x_max <= 10
    assert all(9 <= x + offset <= 18 for x in values)
    claims = (
        all(_period(x) == _period(x + offset) for x in values),
        all(_second_shell(x + offset) > 6 for x in values),
        False,  # neutron numbers are unspecified; nucleon difference is not fixed
        all(_outer_shell(x + offset) - _outer_shell(x) == offset for x in values),
    )
    true = [index for index, claim in enumerate(claims) if claim]
    assert len(true) == 1
    return true[0]


def check(x_min=3, x_max=10, offset=6):
    # Independently use a period-two/three occupancy table, and enumerate
    # isotope neutron counts to falsify the nuclear-particle statement.
    table = {
        3: (2, 1, 1), 4: (2, 2, 2), 5: (2, 3, 3), 6: (2, 4, 4),
        7: (2, 5, 5), 8: (2, 6, 6), 9: (2, 7, 7), 10: (2, 8, 8),
        11: (3, 8, 1), 12: (3, 8, 2), 13: (3, 8, 3), 14: (3, 8, 4),
        15: (3, 8, 5), 16: (3, 8, 6), 17: (3, 8, 7), 18: (3, 8, 8),
    }
    cases = [(table[x], table[x + offset]) for x in range(x_min, x_max + 1)]
    claims = (
        all(first[0] == second[0] for first, second in cases),
        all(second[1] > 6 for _, second in cases),
        all((x + offset + n_z) - (x + n_x) == offset
            for x in range(x_min, x_max + 1)
            for n_x in (x, x + 1) for n_z in (x + offset, x + offset + 1)),
        all(second[2] - first[2] == offset for first, second in cases),
    )
    true = [index for index, claim in enumerate(claims) if claim]
    assert len(true) == 1
    return true[0]


PARAMS = {"x_min": 3, "x_max": 10, "offset": 6}
VARIANTS = [
    {"x_min": 4, "x_max": 9, "offset": 6},
    {"x_min": 3, "x_max": 8, "offset": 7},
    {"x_min": 5, "x_max": 10, "offset": 4},
]
ANSWER = 1
