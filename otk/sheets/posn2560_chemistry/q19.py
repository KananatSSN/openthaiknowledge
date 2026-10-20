"""Source p8, MC19: Pb2+ + SO4(2-) -> PbSO4(s), choice ข."""

from math import gcd


_CATIONS = {"Pb": 2, "Ba": 2, "Ag": 1, "Ca": 2}
_ANIONS = {"SO4": 2, "Cl": 1, "CO3": 2}


def _formula(metal, anion):
    positive, negative = _CATIONS[metal], _ANIONS[anion]
    divisor = gcd(positive, negative)
    metal_count = negative // divisor
    anion_count = positive // divisor
    metal_part = metal + (str(metal_count) if metal_count > 1 else "")
    anion_part = (f"({anion})" if anion_count > 1 and len(anion) > 2 else anion)
    return metal_part + anion_part + (str(anion_count) if anion_count > 1 else "")


def solve(metal="Pb", anion="SO4"):
    return _CATIONS[metal], _ANIONS[anion], _formula(metal, anion)


def check(metal="Pb", anion="SO4"):
    # Independent reviewed precipitation inventory for the four supported
    # solution pairs, rather than the charge-balancing formula builder.
    known = {
        ("Pb", "SO4"): (2, 2, "PbSO4"),
        ("Ba", "SO4"): (2, 2, "BaSO4"),
        ("Ag", "Cl"): (1, 1, "AgCl"),
        ("Ca", "CO3"): (2, 2, "CaCO3"),
    }
    return known[(metal, anion)]


PARAMS = {"metal": "Pb", "anion": "SO4"}
VARIANTS = [
    {"metal": "Ba", "anion": "SO4"},
    {"metal": "Ag", "anion": "Cl"},
    {"metal": "Ca", "anion": "CO3"},
]
ANSWER = (2, 2, "PbSO4")
