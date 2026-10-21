"""Source p6, MC18: calcium and rubidium oxides give basic water."""


ATOMIC_NUMBERS = (7, 16, 20, 37)  # N, S, Ca, Rb
PAIRS = ((0, 1), (0, 2), (1, 3), (2, 3))


def solve(options=(0, 1, 2, 3)):
    assert sorted(options) == [0, 1, 2, 3]
    basic = {20, 37}
    true = [i for i, option in enumerate(options)
            if all(ATOMIC_NUMBERS[index] in basic for index in PAIRS[option])]
    assert len(true) == 1
    return true[0]


def check(options=(0, 1, 2, 3)):
    # Oxide hydrolysis: N/S oxides are acidic or neutral; CaO and Rb2O
    # produce Ca(OH)2 and RbOH, respectively.
    hydroxide = {7: None, 16: None, 20: "Ca(OH)₂", 37: "RbOH"}
    true = [i for i, option in enumerate(options)
            if all(hydroxide[ATOMIC_NUMBERS[index]] is not None
                   for index in PAIRS[option])]
    assert len(true) == 1
    return true[0]


PARAMS = {"options": (0, 1, 2, 3)}
VARIANTS = [
    {"options": (3, 0, 1, 2)},
    {"options": (1, 3, 2, 0)},
    {"options": (2, 1, 0, 3)},
]
ANSWER = 3
