"""Source p8, MC18: HCl < HBr < HI < HF boiling points (choice ก)."""

# Normal boiling points, degrees Celsius, rounded from reference values.
_BOILING_C = {"HCl": -85.1, "HBr": -66.8, "HI": -35.4, "HF": 19.5}


def solve(molecules=("HCl", "HBr", "HI", "HF")):
    return tuple(sorted(molecules, key=lambda molecule: _BOILING_C[molecule]))


def check(molecules=("HCl", "HBr", "HI", "HF")):
    # Independent physical trend: dispersion grows HCl -> HBr -> HI;
    # hydrogen bonding places HF above all three.
    rank = ("HCl", "HBr", "HI", "HF")
    return tuple(compound for compound in rank if compound in molecules)


PARAMS = {"molecules": ("HCl", "HBr", "HI", "HF")}
VARIANTS = [
    {"molecules": ("HCl", "HBr", "HI")},
    {"molecules": ("HCl", "HBr", "HF")},
    {"molecules": ("HCl", "HI", "HF")},
]
ANSWER = ("HCl", "HBr", "HI", "HF")
