"""MC24: only Cl2O is correctly named and bent in the printed table."""


def solve(order=(0, 1, 2, 3)):
    entries = (("dichlorine monoxide", "bent", "dichlorine monoxide", "bent"),
               ("oxygen difluoride", "linear", "oxygen difluoride", "bent"),
               ("sulfur tetrafluoride", "seesaw", "silicon tetrafluoride", "tetrahedral"))
    good = tuple(i + 1 for i, (name, shape, actual_name, actual_shape)
                 in enumerate(entries) if name == actual_name and shape == actual_shape)
    groups = ((1,), (2,), (3,), (1, 2))
    return order.index(groups.index(good))


def check(order=(0, 1, 2, 3)):
    # Central O in Cl2O and OF2 is AX2E2; SiF4 is AX4.
    oxygen_shape = "bent"
    silicon_shape = "tetrahedral"
    true = (oxygen_shape == "bent", oxygen_shape == "linear",
            silicon_shape == "seesaw")
    assert true == (True, False, False)
    return order.index(0)


PARAMS = {"order": (0, 1, 2, 3)}
VARIANTS = [{"order": (2, 0, 1, 3)}, {"order": (1, 3, 0, 2)},
            {"order": (3, 2, 1, 0)}]
ANSWER = solve(**PARAMS)
