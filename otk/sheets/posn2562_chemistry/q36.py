"""Page-9 figure: A rises/concave, B depressed/convex; B droplet sinks in A."""

FIGURE = {"A": "concave rise", "B": "convex depression", "B_drop_in_A": "sinks spherical"}


def solve(order=(0, 1, 2, 3)):
    false = (True, False, False)
    groups = ({1}, {3}, {1, 2}, {1, 3})
    return order.index(groups.index({i + 1 for i, v in enumerate(false) if v}))


def check(order=(0, 1, 2, 3)):
    a_adhesion_exceeds_cohesion = FIGURE["A"] == "concave rise"
    b_denser_than_a = "sinks" in FIGURE["B_drop_in_A"]
    reciprocal_drop_floats = b_denser_than_a
    claims = (not a_adhesion_exceeds_cohesion, b_denser_than_a, reciprocal_drop_floats)
    assert claims == (False, True, True)
    return order.index(0)


PARAMS = {"order": (0, 1, 2, 3)}
VARIANTS = [{"order": (1, 0, 2, 3)}, {"order": (2, 3, 0, 1)}, {"order": (3, 1, 2, 0)}]
ANSWER = solve(**PARAMS)
