"""Source p13, MC55: classify phases from melting and boiling points."""


BASE_ROWS = (
    ((-188, -42), (-91, 98), (40, 330)),
    ((-188, -42), (32, 330), (-91, 98)),
    ((-91, 98), (-8.8, -42), (40, 330)),
    ((32, 330), (-91, 98), (-188, -42)),
)


def rows(offset=0):
    assert offset in (-10, -5, 0, 5)
    return tuple(tuple((mp + offset, bp + offset) for mp, bp in row)
                 for row in BASE_ROWS)


def solve(offset=0):
    def phase(mp, bp):
        if 25 < mp:
            return "solid"
        if 25 > bp:
            return "gas"
        return "liquid"

    matches = [i for i, row in enumerate(rows(offset))
               if tuple(phase(*pair) for pair in row) == ("gas", "liquid", "solid")]
    assert len(matches) == 1
    return matches[0]


def check(offset=0):
    valid = []
    for row in rows(offset):
        (a_mp, a_bp), (b_mp, b_bp), (c_mp, c_bp) = row
        valid.append(a_mp < a_bp < 25 and b_mp < 25 < b_bp
                     and 25 < c_mp < c_bp)
    return valid.index(True) if valid.count(True) == 1 else None


PARAMS = {"offset": 0}
VARIANTS = [{"offset": -10}, {"offset": -5}, {"offset": 5}]
ANSWER = 0
