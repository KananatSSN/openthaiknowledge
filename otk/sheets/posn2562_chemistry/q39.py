"""Page-10 figure shows connected NO and O2 vessels. Initial n ratios PV/RT = 2:3."""

FIGURE = {"NO": "large vessel", "O2": "small vessel", "valve": "closed initially"}


def solve(no_volume=2, o2_volume=1, no_pressure=1, o2_pressure=3, order=(0, 1, 2, 3)):
    no = no_volume * no_pressure
    o2 = o2_volume * o2_pressure
    used = min(no, 2 * o2)
    remaining_no = no - used
    remaining_o2 = o2 - used / 2
    produced_no2 = used
    if remaining_no == 0 and remaining_o2 == 0:
        answer = 0
    elif remaining_no == produced_no2 and remaining_o2 == 0:
        answer = 1
    elif remaining_o2 == produced_no2 and remaining_no == 0:
        answer = 2
    elif produced_no2 == 2 * remaining_o2 and remaining_no == 0:
        answer = 3
    else:
        raise ValueError("unsupported product ratio")
    return order.index(answer)


def check(no_volume=2, o2_volume=1, no_pressure=1, o2_pressure=3, order=(0, 1, 2, 3)):
    initial_no = no_volume * no_pressure
    initial_o2 = o2_volume * o2_pressure
    extent = min(initial_no / 2, initial_o2)
    final = (initial_no - 2 * extent, initial_o2 - extent, 2 * extent)
    candidates = (
        (final[0] == 0 and final[1] == 0),
        (final[0] == final[2] and final[1] == 0),
        (final[1] == final[2] and final[0] == 0),
        (final[2] == 2 * final[1] and final[0] == 0),
    )
    assert sum(candidates) == 1
    return order.index(candidates.index(True))


PARAMS = {"no_volume": 2, "o2_volume": 1, "no_pressure": 1, "o2_pressure": 3, "order": (0, 1, 2, 3)}
VARIANTS = [
    {"no_volume": 4, "o2_volume": 2, "no_pressure": 1, "o2_pressure": 3, "order": (1, 0, 2, 3)},
    {"no_volume": 2, "o2_volume": 1, "no_pressure": 2, "o2_pressure": 6, "order": (2, 3, 0, 1)},
    {"no_volume": 6, "o2_volume": 3, "no_pressure": 1, "o2_pressure": 3, "order": (3, 1, 2, 0)},
]
ANSWER = solve(**PARAMS)
