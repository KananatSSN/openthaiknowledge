"""Source p9, MC25: symmetric PF5 is nonpolar (choice ง)."""

_POLAR = {
    "SF4": True, "SCl2": True, "PCl3": True, "PF5": False,
    "H2O": True, "NH3": True, "CO2": False, "BF3": False,
    "CF4": False, "XeF4": False, "ClF3": True,
}

# Independent VSEPR route: an identical-ligand arrangement cancels bond
# dipoles only in the symmetric molecular geometries listed here.
_GEOMETRY = {
    "SF4": ("seesaw", True), "SCl2": ("bent", True),
    "PCl3": ("pyramidal", True), "PF5": ("trigonal_bipyramidal", True),
    "H2O": ("bent", True), "NH3": ("pyramidal", True),
    "CO2": ("linear", True), "BF3": ("trigonal_planar", True),
    "CF4": ("tetrahedral", True), "XeF4": ("square_planar", True),
    "ClF3": ("t_shaped", True),
}
_CANCEL = {"linear", "trigonal_planar", "tetrahedral",
           "trigonal_bipyramidal", "square_planar"}


def solve(species=("SF4", "SCl2", "PCl3", "PF5")):
    matches = [item for item in species if not _POLAR[item]]
    assert len(matches) == 1
    return matches[0]


def check(species=("SF4", "SCl2", "PCl3", "PF5")):
    matches = [item for item in species if _GEOMETRY[item][1]
               and _GEOMETRY[item][0] in _CANCEL]
    assert len(matches) == 1
    return matches[0]


PARAMS = {"species": ("SF4", "SCl2", "PCl3", "PF5")}
VARIANTS = [
    {"species": ("H2O", "CO2", "NH3", "SF4")},
    {"species": ("PCl3", "BF3", "SCl2", "ClF3")},
    {"species": ("XeF4", "NH3", "SF4", "H2O")},
]
ANSWER = "PF5"
