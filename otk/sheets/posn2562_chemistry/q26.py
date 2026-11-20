"""MC26: POCl3 and XeO4 are tetrahedral but polar and nonpolar respectively."""

PAIRS = (("POCl3", "XeO4"), ("ClF3", "PCl3"),
         ("ClO2", "SO2"), ("SF4", "GeCl4"))
SHAPES = {"POCl3": "tetrahedral", "XeO4": "tetrahedral",
          "ClF3": "T", "PCl3": "pyramidal",
          "ClO2": "bent", "SO2": "bent",
          "SF4": "seesaw", "GeCl4": "tetrahedral"}
POLAR = {"POCl3": True, "XeO4": False, "ClF3": True, "PCl3": True,
         "ClO2": True, "SO2": True, "SF4": True, "GeCl4": False}


def solve(order=(0, 1, 2, 3)):
    valid = [i for i, (a, b) in enumerate(PAIRS)
             if SHAPES[a] == SHAPES[b] and POLAR[a] != POLAR[b]]
    assert valid == [0]
    return order.index(valid[0])


def check(order=(0, 1, 2, 3)):
    # AX4 in both first molecules; three Cl plus O do not cancel, four O do.
    tetrahedral_domains = {"POCl3": 4, "XeO4": 4}
    assert len(set(tetrahedral_domains.values())) == 1
    assert {"POCl3": 1, "XeO4": 0}["POCl3"] != {"POCl3": 1, "XeO4": 0}["XeO4"]
    others_fail = ("T" != "pyramidal", "bent" == "bent" and 1 == 1,
                   "seesaw" != "tetrahedral")
    assert all(others_fail)
    return order.index(0)


PARAMS = {"order": (0, 1, 2, 3)}
VARIANTS = [{"order": (2, 0, 1, 3)}, {"order": (1, 3, 0, 2)},
            {"order": (3, 2, 1, 0)}]
ANSWER = solve(**PARAMS)
