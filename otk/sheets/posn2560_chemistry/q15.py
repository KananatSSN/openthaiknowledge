"""Source p7, MC15: X=Cl, Y=I, Z=Br; EN order X>Z>Y (choice ค).

The printed stem does not explicitly say X, Y and Z are distinct. The
adaptation states this assumption to make the deduction unique.
"""

_ELECTRONEGATIVITY = {"Cl": 3.16, "Br": 2.96, "I": 2.66}


def solve(assignment=("Cl", "I", "Br")):
    if set(assignment) != set(_ELECTRONEGATIVITY):
        raise ValueError("X, Y and Z must be distinct Cl, Br and I")
    return tuple(sorted("XYZ", key=lambda label:
                        -_ELECTRONEGATIVITY[assignment["XYZ".index(label)]]))


def check(assignment=("Cl", "I", "Br")):
    # Independent group trend: electronegativity decreases down group 17.
    positions = {symbol: label for label, symbol in zip("XYZ", assignment)}
    return tuple(positions[symbol] for symbol in ("Cl", "Br", "I"))


PARAMS = {"assignment": ("Cl", "I", "Br")}
VARIANTS = [
    {"assignment": ("Br", "I", "Cl")},
    {"assignment": ("I", "Cl", "Br")},
    {"assignment": ("Br", "Cl", "I")},
]
ANSWER = ("X", "Z", "Y")
