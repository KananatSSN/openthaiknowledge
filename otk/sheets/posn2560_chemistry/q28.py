"""Source p9, MC28: KrO2H2 is AX4E, a seesaw (choice ค).

Use the stated Lewis model with terminal Kr=O and Kr-H bonds. This is a
formal VSEPR exercise, not a claim that isolated KrO2H2 is stable.
"""

_SHAPE = {
    "KrO2H2": "seesaw", "XeO2F2": "seesaw",
    "XeOF4": "square_pyramidal", "XeO3": "trigonal_pyramidal",
    "XeF4": "square_planar",
}
_BONDS = {
    "KrO2H2": (2, 2), "XeO2F2": (2, 2),
    "XeOF4": (1, 4), "XeO3": (3, 0), "XeF4": (0, 4),
}
_AXE_SHAPE = {
    (4, 1): "seesaw", (5, 1): "square_pyramidal",
    (3, 1): "trigonal_pyramidal", (4, 2): "square_planar",
}


def solve(formula="KrO2H2"):
    return _SHAPE[formula]


def check(formula="KrO2H2"):
    oxo, singles = _BONDS[formula]
    # Group 18 central atom: each terminal oxo double bond consumes two
    # central valence electrons; a single H/F bond consumes one.
    lone_pairs = (8 - 2 * oxo - singles) // 2
    assert 8 - 2 * oxo - singles >= 0
    return _AXE_SHAPE[(oxo + singles, lone_pairs)]


PARAMS = {"formula": "KrO2H2"}
VARIANTS = [
    {"formula": "XeO2F2"},
    {"formula": "XeOF4"},
    {"formula": "XeO3"},
    {"formula": "XeF4"},
]
ANSWER = "seesaw"
