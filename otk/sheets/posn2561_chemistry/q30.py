"""Source p8, MC30: compare each molecule's *smallest* bond angle."""


MOLECULES = ("NCl₃", "PCl₅", "SOCl₂", "CH₂Cl₂")
# Degrees, gas-phase molecular structures. NCl3 ~107.1, SOCl2
# Cl-S-Cl 96.1, CH2Cl2 H-C-Cl 108.15; PCl5 axial-equatorial 90.
MIN_ANGLES = (107.1, 90.0, 96.1, 108.15)


def solve(options=(0, 1, 2, 3)):
    assert sorted(options) == [0, 1, 2, 3]
    minimum = min(MIN_ANGLES)
    matches = [i for i, option in enumerate(options)
               if MIN_ANGLES[option] == minimum]
    assert len(matches) == 1
    return matches[0]


def check(options=(0, 1, 2, 3)):
    # Independent VSEPR geometry: AX5 includes axial-equatorial 90°;
    # the other three have three/four domains with angles above 90°.
    geometries = {"NCl₃": "trigonal pyramidal", "PCl₅": "trigonal bipyramidal",
                  "SOCl₂": "trigonal pyramidal", "CH₂Cl₂": "tetrahedral"}
    assert geometries["PCl₅"] == "trigonal bipyramidal"
    assert all(geometries[name] != "trigonal bipyramidal"
               for name in MOLECULES if name != "PCl₅")
    return [MOLECULES[i] for i in options].index("PCl₅")


PARAMS = {"options": (0, 1, 2, 3)}
VARIANTS = [
    {"options": (1, 0, 2, 3)},
    {"options": (2, 3, 1, 0)},
    {"options": (3, 2, 0, 1)},
]
ANSWER = 1
