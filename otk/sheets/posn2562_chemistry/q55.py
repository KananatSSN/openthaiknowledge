"""Equal mass percent means molality ranks inversely with molar mass."""


def solve(percent=20, order=(0, 1, 2, 3)):
    solute_g = percent
    water_kg = (100 - percent) / 1000
    m = {
        "acid": solute_g / 60 / water_kg,
        "ethanol": solute_g / 46 / water_kg,
        "naoh": solute_g / 40 / water_kg,
    }
    ranks = tuple(sorted(m, key=m.get, reverse=True))
    choices = (
        ("acid", "ethanol", "naoh"),
        ("ethanol", "naoh", "acid"),
        ("naoh", "acid", "ethanol"),
        ("naoh", "ethanol", "acid"),
    )
    return order.index(choices.index(ranks))


def check(percent=20, order=(0, 1, 2, 3)):
    assert 0 < percent < 100
    inverse_order = sorted((("acid", 60), ("ethanol", 46), ("naoh", 40)), key=lambda t: t[1])
    assert tuple(x for x, _ in inverse_order) == ("naoh", "ethanol", "acid")
    return order.index(3)


PARAMS = {"percent": 20, "order": (0, 1, 2, 3)}
VARIANTS = [
    {"percent": 10, "order": (1, 0, 2, 3)},
    {"percent": 30, "order": (2, 3, 0, 1)},
    {"percent": 40, "order": (3, 1, 2, 0)},
]

ANSWER = solve(**PARAMS)
