"""Source p12, MC54: compare vapor-pressure curves at equal temperature."""


def solve(a=480, b=280, c=110):
    assert a > b > c > 0
    true_claims = (a > b > c, c > a and c > b, a > b and a > c)
    return (1, 3) if true_claims == (True, False, True) else ()


def check(a=480, b=280, c=110):
    pressures = {"A": a, "B": b, "C": c}
    rank = sorted(pressures, key=pressures.get, reverse=True)
    # At one temperature, larger vapor pressure means lower boiling point
    # and weaker effective intermolecular attraction.
    assertions = (rank == ["A", "B", "C"], rank[0] == "C", rank[0] == "A")
    return tuple(i for i, true in enumerate(assertions, 1) if true)


PARAMS = {"a": 480, "b": 280, "c": 110}
VARIANTS = [
    {"a": 600, "b": 410, "c": 190},
    {"a": 520, "b": 260, "c": 90},
    {"a": 340, "b": 200, "c": 80},
]
ANSWER = (1, 3)
