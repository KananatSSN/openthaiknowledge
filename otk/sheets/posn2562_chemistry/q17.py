"""MC17: Rh(A)+n -> Rh(A+1)+gamma, then beta-minus -> Pd(A+1)."""

PARTICLES = (((2, 1), (1, 1), (0, 1)),
             ((1, 1), (1, 0), (0, -1)),
             ((2, 0), (1, 0), (0, 1)),
             ((1, 0), (0, 0), (0, -1)))


def solve(mass=103, order=(0, 1, 2, 3)):
    matches = []
    for i, (a, b, c) in enumerate(PARTICLES):
        if (mass + a[0] == mass + 1 + b[0]
                and 45 + a[1] == 45 + b[1]
                and mass + 1 == mass + 1 + c[0]
                and 45 == 46 + c[1]):
            matches.append(i)
    assert matches == [3]
    return order.index(matches[0])


def check(mass=103, order=(0, 1, 2, 3)):
    assert mass > 0
    required_a = (1, 0)  # neutron capture raises A by one, not Z.
    required_b = (0, 0)  # photon carries neither nucleon nor charge.
    required_c = (0, -1)  # beta-minus raises nuclear Z by one.
    return order.index(PARTICLES.index((required_a, required_b, required_c)))


PARAMS = {"mass": 103, "order": (0, 1, 2, 3)}
VARIANTS = [
    {"mass": 101, "order": (3, 0, 1, 2)},
    {"mass": 102, "order": (1, 3, 2, 0)},
    {"mass": 105, "order": (2, 1, 0, 3)},
]
ANSWER = solve(**PARAMS)
