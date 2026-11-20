"""Source p12, MC52: identify a false claim about crystalline solids."""

NONPOLAR = {"CO₂", "I₂", "N₂", "CCl₄"}


def solve(molecule="CO₂"):
    assert molecule in NONPOLAR
    # A nonpolar molecule has no permanent dipole for dipole–dipole forces.
    return 0


def check(molecule="CO₂"):
    properties = (
        molecule not in NONPOLAR,  # claimed permanent dipole attraction
        True,  # LiF ionic lattice
        True,  # solid Kr has dispersion attractions
        True,  # Au has delocalized metallic electrons
    )
    return properties.index(False)


PARAMS = {"molecule": "CO₂"}
VARIANTS = [{"molecule": "I₂"}, {"molecule": "N₂"}, {"molecule": "CCl₄"}]
ANSWER = 0
