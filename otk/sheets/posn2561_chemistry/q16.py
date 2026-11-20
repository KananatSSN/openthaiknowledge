"""Source p5, MC16: graph ก halves parent mass every 20 seconds."""


def graph_values(initial=80, half_life=20):
    assert initial > 0 and initial % 16 == 0 and half_life > 0
    return (
        (initial, initial // 2, initial // 4),
        (0, initial // 2, 3 * initial // 4),
        (initial, initial // 4, initial // 16),
        (0, 3 * initial // 4, 15 * initial // 16),
    )


def solve(initial=80, half_life=20):
    expected = tuple(round(initial * 2 ** (-time / half_life))
                     for time in (0, half_life, 2 * half_life))
    matches = [i for i, values in enumerate(graph_values(initial, half_life))
               if values == expected]
    assert len(matches) == 1
    return matches[0]


def check(initial=80, half_life=20):
    remaining = initial
    expected = [remaining]
    for _ in range(2):
        remaining //= 2
        expected.append(remaining)
    return graph_values(initial, half_life).index(tuple(expected))


PARAMS = {"initial": 80, "half_life": 20}
VARIANTS = [
    {"initial": 160, "half_life": 10},
    {"initial": 96, "half_life": 30},
    {"initial": 64, "half_life": 40},
]
ANSWER = 0
