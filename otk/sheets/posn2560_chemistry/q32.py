"""Source p9, MC32: formal ClH3 and TeF4 are both polar (choice ค).

ClH3 is treated as the printed Lewis/VSEPR model AX3E2. This is not an
assertion that an isolated chlorine trihydride molecule is stable.
"""

_POLAR = {
    "HCN": True, "KrF4": False, "AsI5": False, "SBr2": True,
    "ClH3": True, "TeF4": True, "SO3": False, "PBr3": True,
    "NH3": True, "H2O": True, "CO2": False, "XeF4": False,
    "BF3": False, "PCl3": True, "SF4": True,
}

# Independent shape/symmetry assessment from Lewis structures.
_GEOMETRY = {
    "HCN": ("linear", False), "KrF4": ("square_planar", True),
    "AsI5": ("trigonal_bipyramidal", True), "SBr2": ("bent", True),
    "ClH3": ("t_shaped", True), "TeF4": ("seesaw", True),
    "SO3": ("trigonal_planar", True), "PBr3": ("pyramidal", True),
    "NH3": ("pyramidal", True), "H2O": ("bent", True),
    "CO2": ("linear", True), "XeF4": ("square_planar", True),
    "BF3": ("trigonal_planar", True), "PCl3": ("pyramidal", True),
    "SF4": ("seesaw", True),
}
_CANCEL = {"linear", "square_planar", "trigonal_bipyramidal", "trigonal_planar"}


def solve(pairs=(("HCN", "KrF4"), ("AsI5", "SBr2"),
                 ("ClH3", "TeF4"), ("SO3", "PBr3"))):
    matches = [pair for pair in pairs if all(_POLAR[item] for item in pair)]
    assert len(matches) == 1
    return matches[0]


def check(pairs=(("HCN", "KrF4"), ("AsI5", "SBr2"),
                 ("ClH3", "TeF4"), ("SO3", "PBr3"))):
    def polar(formula):
        shape, equivalent_ligands = _GEOMETRY[formula]
        return not (equivalent_ligands and shape in _CANCEL)

    matches = [pair for pair in pairs if all(polar(item) for item in pair)]
    assert len(matches) == 1
    return matches[0]


PARAMS = {"pairs": (("HCN", "KrF4"), ("AsI5", "SBr2"),
                    ("ClH3", "TeF4"), ("SO3", "PBr3"))}
VARIANTS = [
    {"pairs": (("NH3", "H2O"), ("CO2", "PCl3"),
               ("BF3", "SF4"), ("XeF4", "HCN"))},
    {"pairs": (("AsI5", "TeF4"), ("PBr3", "SBr2"),
               ("SO3", "NH3"), ("HCN", "KrF4"))},
    {"pairs": (("XeF4", "H2O"), ("ClH3", "PCl3"),
               ("BF3", "TeF4"), ("CO2", "PBr3"))},
]
ANSWER = ("ClH3", "TeF4")
