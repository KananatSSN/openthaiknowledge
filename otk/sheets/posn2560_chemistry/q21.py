"""Source p8, MC21: NO+ has the shortest N-O bond (choice ก)."""

from fractions import Fraction


_BOND_ORDER = {
    "NO+": Fraction(3), "NO": Fraction(5, 2),
    "NO2+": Fraction(2), "NO2-": Fraction(3, 2),
    "NO3-": Fraction(4, 3),
}

# Approximate experimental N-O distances in angstrom, adequate to separate
# every possible shortest candidate in the supported pools.
_LENGTH_ANGSTROM = {
    "NO+": 1.06, "NO": 1.15, "NO2+": 1.116,
    "NO2-": 1.24, "NO3-": 1.26,
}


def solve(species=("NO+", "NO2-", "NO2+", "NO3-")):
    return max(species, key=lambda item: _BOND_ORDER[item])


def check(species=("NO+", "NO2-", "NO2+", "NO3-")):
    return min(species, key=lambda item: _LENGTH_ANGSTROM[item])


PARAMS = {"species": ("NO+", "NO2-", "NO2+", "NO3-")}
VARIANTS = [
    {"species": ("NO+", "NO", "NO2+", "NO3-")},
    {"species": ("NO+", "NO", "NO2+", "NO2-")},
    {"species": ("NO+", "NO", "NO2-", "NO3-")},
]
ANSWER = "NO+"
