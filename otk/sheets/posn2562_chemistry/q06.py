"""Source MC6: identify the pair with half-filled highest p and d sublevels."""

OCCUPANCY = {11: ("s", 1), 15: ("p", 3), 25: ("d", 5), 26: ("d", 6),
             19: ("s", 1), 33: ("p", 3)}


def solve(alkali=11, pnictogen=15, manganese=25, iron=26):
    pairs = ((alkali, pnictogen), (alkali, iron),
             (pnictogen, manganese), (manganese, iron))
    good = [i for i, pair in enumerate(pairs)
            if all(OCCUPANCY[z] in (("p", 3), ("d", 5)) for z in pair)]
    assert len(good) == 1
    return good[0]


def check(alkali=11, pnictogen=15, manganese=25, iron=26):
    capacities = {"s": 2, "p": 6, "d": 10}
    half = {z for z in (alkali, pnictogen, manganese, iron)
            if OCCUPANCY[z][0] in ("p", "d")
            and 2 * OCCUPANCY[z][1] == capacities[OCCUPANCY[z][0]]}
    choices = ((alkali, pnictogen), (alkali, iron),
               (pnictogen, manganese), (manganese, iron))
    matches = [i for i, (a, b) in enumerate(choices) if a in half and b in half]
    return matches[0] if len(matches) == 1 else None


PARAMS = {"alkali": 11, "pnictogen": 15, "manganese": 25, "iron": 26}
VARIANTS = [
    {"alkali": 19, "pnictogen": 15, "manganese": 25, "iron": 26},
    {"alkali": 11, "pnictogen": 33, "manganese": 25, "iron": 26},
    {"alkali": 19, "pnictogen": 33, "manganese": 25, "iron": 26},
]
ANSWER = solve(**PARAMS)
