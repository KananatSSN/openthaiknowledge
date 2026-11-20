"""MC22: CO3(2-) is trigonal planar; NO2- is bent and wider than NH2-."""


def solve(order=(0, 1, 2, 3)):
    central_lone_pairs = {"CO3": 0, "NO2": 1, "SO3": 1, "ClO3": 1}
    shapes = {"CO3": "trigonal planar", "NO2": "bent",
              "SO3": "trigonal pyramidal", "ClO3": "trigonal pyramidal"}
    claims = (all(central_lone_pairs.values()),
              len({shapes[x] for x in ("CO3", "SO3", "ClO3")}) == 1,
              shapes["NO2"] == "bent" and 115 > 104)
    groups = ((1,), (2,), (3,), (2, 3))
    truths = tuple(i for i, yes in enumerate(claims, 1) if yes)
    return order.index(groups.index(truths))


def check(order=(0, 1, 2, 3)):
    # Electron-domain counts: CO3 AX3, NO2 AX2E, SO3/ClO3 AX3E.
    carbon_lone = 0
    carbonate_shape = "planar"
    other_shapes = ("pyramidal", "pyramidal")
    no2_angle, nh2_angle = 115, 104
    valid = (carbon_lone > 0,
             carbonate_shape == other_shapes[0] == other_shapes[1],
             no2_angle > nh2_angle)
    assert valid == (False, False, True)
    return order.index(2)


PARAMS = {"order": (0, 1, 2, 3)}
VARIANTS = [{"order": (2, 0, 1, 3)}, {"order": (1, 3, 2, 0)},
            {"order": (3, 2, 1, 0)}]
ANSWER = solve(**PARAMS)
