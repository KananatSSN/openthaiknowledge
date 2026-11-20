"""Source p6, MC19: the observations identify gallium, so VA is false."""


CLAIMS = (
    "X อยู่ในหมู่ 15 (VA)",
    "X อยู่ในคาบที่ 4",
    "แก๊ส Y เป็นแก๊สไฮโดรเจน",
    "X อยู่ในหมู่เดียวกับ Al",
)


def solve(options=(0, 1, 2, 3)):
    assert sorted(options) == [0, 1, 2, 3]
    # 2Ga + 3Cl2 -> 2GaCl3; Ga is the water-inert period-4 group-13
    # metal that yields a colorless trivalent solution with acid.
    gallium_group, gallium_period = 13, 4
    claims = (gallium_group == 15, gallium_period == 4,
              True, gallium_group == 13)
    false = [i for i, option in enumerate(options) if not claims[option]]
    assert len(false) == 1
    return false[0]


def check(options=(0, 1, 2, 3)):
    # Independent periodic-table route: Ga Z=31 is [Ar]3d10 4s2 4p1.
    z = 31
    valence = (2, 1)
    period = 4
    group = 10 + sum(valence)
    assert z in range(19, 37) and group == 13
    truth = (group == 15, period == 4, "H₂" == "H₂", group == 13)
    false = [i for i, option in enumerate(options) if not truth[option]]
    assert len(false) == 1
    return false[0]


PARAMS = {"options": (0, 1, 2, 3)}
VARIANTS = [
    {"options": (1, 0, 2, 3)},
    {"options": (2, 3, 0, 1)},
    {"options": (3, 2, 1, 0)},
]
ANSWER = 0
