"""A=O, D=Al, E=excited Sc, G=Na; D group 13, A highest IE1."""

ELEMENTS = {"A": (8, 16, 1314), "D": (13, 13, 578), "E": (21, 3, 633), "G": (11, 1, 496)}


def solve(order=(0, 1, 2, 3)):
    group13 = next(k for k, v in ELEMENTS.items() if v[1] == 13)
    high_ie = max(ELEMENTS, key=lambda k: ELEMENTS[k][2])
    pairs = (("A", "D"), ("D", "A"), ("E", "A"), ("D", "G"))
    return order.index(pairs.index((group13, high_ie)))


def check(order=(0, 1, 2, 3)):
    electrons = {
        "A": 2 + 2 + 4,
        "D": 2 + 2 + 6 + 2 + 1,
        "E": 2 + 2 + 6 + 2 + 6 + 2 + 1,
        "G": 2 + 2 + 6 + 1,
    }
    assert electrons == {"A": 8, "D": 13, "E": 21, "G": 11}
    # Only Al belongs to group 13; O has much higher first ionization energy.
    return order.index(1)


PARAMS = {"order": (0, 1, 2, 3)}
VARIANTS = [{"order": (1, 0, 2, 3)}, {"order": (2, 3, 0, 1)}, {"order": (3, 1, 2, 0)}]

ANSWER = solve(**PARAMS)
