"""Source p8, MC23: ClF3 has the smallest bond angle (choice ก)."""

# Smallest bond angle in each molecule, degrees. Experimental values where
# available; near-ideal values for the symmetric molecules suffice here.
_MIN_ANGLE = {
    "ClF5": 86.5, "ClF3": 87.45, "H2O": 104.5,
    "NH3": 106.7, "NCl3": 107.1, "SiF4": 109.5,
    "OCl2": 110.88, "BF3": 120.0,
}


def solve(molecules=("ClF3", "SiF4", "NCl3", "OCl2")):
    return min(molecules, key=lambda molecule: _MIN_ANGLE[molecule])


def check(molecules=("ClF3", "SiF4", "NCl3", "OCl2")):
    # Independently rank by the VSEPR shape and observed distortions:
    # square-pyramidal ClF5 and T-shaped ClF3 have sub-90-degree angles;
    # the other supported candidates have minimum angles above 104 degrees.
    priority = ("ClF5", "ClF3", "H2O", "NH3", "NCl3", "SiF4", "OCl2", "BF3")
    return next(molecule for molecule in priority if molecule in molecules)


PARAMS = {"molecules": ("ClF3", "SiF4", "NCl3", "OCl2")}
VARIANTS = [
    {"molecules": ("ClF5", "SiF4", "NCl3", "OCl2")},
    {"molecules": ("ClF3", "BF3", "NH3", "H2O")},
    {"molecules": ("ClF5", "BF3", "SiF4", "H2O")},
]
ANSWER = "ClF3"
