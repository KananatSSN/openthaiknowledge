"""At fixed pressure, volume and mean kinetic energy scale with kelvin temperature."""


def solve(t1=25, t2=50, order=(0, 1, 2, 3)):
    ratio = (t2 + 273.15) / (t1 + 273.15)
    false = (abs(ratio - 2) > 0.01, abs(1 / ratio - 0.5) > 0.01, round(ratio, 1) != 1.1)
    groups = ({1, 2}, {1, 3}, {2, 3}, {1, 2, 3})
    return order.index(groups.index({i + 1 for i, v in enumerate(false) if v}))


def check(t1=25, t2=50, order=(0, 1, 2, 3)):
    v1, v2 = t1 + 273.15, t2 + 273.15
    rho1, rho2 = 1 / v1, 1 / v2
    k1, k2 = v1, v2
    false = (v2 != 2 * v1, rho2 != rho1 / 2, round(k2 / k1, 1) != 1.1)
    assert false == (True, True, False)
    return order.index(0)


PARAMS = {"t1": 25, "t2": 50, "order": (0, 1, 2, 3)}
VARIANTS = [
    {"t1": 20, "t2": 45, "order": (1, 0, 2, 3)},
    {"t1": 30, "t2": 55, "order": (2, 3, 0, 1)},
    {"t1": 15, "t2": 40, "order": (3, 1, 2, 0)},
]
ANSWER = solve(**PARAMS)
