"""Source MC4: 2s/2p degeneracy holds only for a one-electron atom."""


def solve(multielectron_z=16, metal_z=28, halogen_z=35):
    assert multielectron_z > 2 and metal_z > 2 and halogen_z > 2
    # Hydrogen is one-electron, while the other atoms have electron screening.
    claims = (False, True, False, False)
    return claims.index(True)


def check(multielectron_z=16, metal_z=28, halogen_z=35):
    assert all(z > 2 for z in (multielectron_z, metal_z, halogen_z))
    # Hydrogenic energy depends on n alone; for screened atoms, 3s < 3p.
    # Madelung orders the other comparison 3d < 4p (same n+l, lower n).
    rankings = {"H2s": 2, "H2p": 2, "3s": 3, "3p": 4,
                "3d": 5, "4p": 6}
    statements = (rankings["H2p"] > rankings["H2s"],
                  rankings["3p"] > rankings["3s"],
                  rankings["3d"] > rankings["4p"],
                  rankings["3d"] > rankings["4p"])
    return statements.index(True) if statements.count(True) == 1 else None


PARAMS = {"multielectron_z": 16, "metal_z": 28, "halogen_z": 35}
VARIANTS = [
    {"multielectron_z": 15, "metal_z": 27, "halogen_z": 35},
    {"multielectron_z": 17, "metal_z": 26, "halogen_z": 35},
    {"multielectron_z": 14, "metal_z": 29, "halogen_z": 35},
]
ANSWER = solve(**PARAMS)
