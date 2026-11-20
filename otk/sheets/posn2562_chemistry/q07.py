"""Source MC7: Si accepts an electron more favourably than Mg, Al, or P."""

# Approximate first electron affinities, kJ/mol; only the ordering is used.
EA = {12: -20, 13: 43, 14: 134, 15: 72}


def solve(options=(12, 13, 14, 15)):
    return max(range(4), key=lambda i: EA[options[i]])


def check(options=(12, 13, 14, 15)):
    # The half-filled p³ subshell of P resists attachment; Si is p².
    assert set(options) == {12, 13, 14, 15}
    configs = {12: ("s", 2), 13: ("p", 1), 14: ("p", 2), 15: ("p", 3)}
    winner = [i for i, z in enumerate(options) if configs[z] == ("p", 2)]
    return winner[0] if len(winner) == 1 else None


PARAMS = {"options": (12, 13, 14, 15)}
VARIANTS = [
    {"options": (15, 12, 13, 14)},
    {"options": (13, 15, 14, 12)},
    {"options": (14, 13, 12, 15)},
]
ANSWER = solve(**PARAMS)
