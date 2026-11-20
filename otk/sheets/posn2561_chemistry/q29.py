"""Source p8, MC29: SO₂ is bent, unlike three linear molecules."""


MOLECULES = ("SO₂", "CO₂", "XeF₂", "BeCl₂")


def solve(options=(0, 1, 2, 3)):
    assert sorted(options) == [0, 1, 2, 3]
    domains = {"SO₂": (2, 1), "CO₂": (2, 0),
               "XeF₂": (2, 3), "BeCl₂": (2, 0)}
    shapes = {formula: "linear" if lone_pairs in (0, 3) else "bent"
              for formula, (_, lone_pairs) in domains.items()}
    distinct = [i for i, option in enumerate(options)
                if shapes[MOLECULES[option]] != "linear"]
    assert len(distinct) == 1
    return distinct[0]


def check(options=(0, 1, 2, 3)):
    # Independent bond-angle check: SO2 is approximately 119°, while
    # CO2, XeF2 and gas-phase BeCl2 each have 180° bond angles.
    angles = (119, 180, 180, 180)
    odd = [i for i, option in enumerate(options) if angles[option] < 180]
    assert len(odd) == 1
    return odd[0]


PARAMS = {"options": (0, 1, 2, 3)}
VARIANTS = [
    {"options": (1, 0, 2, 3)},
    {"options": (2, 3, 1, 0)},
    {"options": (3, 2, 0, 1)},
]
ANSWER = 0
