"""Source p9, MC34: identify A in ASO₄ from BaSO₄ precipitate mass."""

from fractions import Fraction


METALS = (("Ti", 48), ("Cu", 64), ("Zn", 65), ("Zr", 91))


def solve(salt_centigrams=322, precip_centigrams=466):
    assert salt_centigrams > 0 and precip_centigrams > 0
    # ASO4 + BaCl2 -> BaSO4 + ACl2; one mole of each sulfate.
    sulfate_molar_mass = Fraction(salt_centigrams * 233, precip_centigrams)
    metal_mass = sulfate_molar_mass - 96
    matches = [i for i, (_, mass) in enumerate(METALS) if mass == metal_mass]
    assert len(matches) == 1
    return matches[0]


def check(salt_centigrams=322, precip_centigrams=466):
    # Independently predict BaSO4 mass from every candidate ASO4 mass.
    possibilities = [i for i, (_, mass) in enumerate(METALS)
                     if Fraction(salt_centigrams * 233, mass + 96)
                     == precip_centigrams]
    assert len(possibilities) == 1
    return possibilities[0]


PARAMS = {"salt_centigrams": 322, "precip_centigrams": 466}
VARIANTS = [
    {"salt_centigrams": 288, "precip_centigrams": 466},
    {"salt_centigrams": 320, "precip_centigrams": 466},
    {"salt_centigrams": 374, "precip_centigrams": 466},
]
ANSWER = 2
