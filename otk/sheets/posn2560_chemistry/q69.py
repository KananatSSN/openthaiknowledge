"""Source p19, written 9: 277 g KClO4 needs 568 g Cl2 and yields 1043 g KCl."""


def solve(perchlorate_g=277.0):
    kclo4_mol = perchlorate_g / (39 + 35.5 + 4 * 16)
    # 4KClO3->3KClO4+KCl; 3KClO->2KCl+KClO3;
    # Cl2+2KOH->KCl+KClO+H2O.
    chlorate_mol = 4 * kclo4_mol / 3
    hypochlorite_mol = 3 * chlorate_mol
    chlorine_mol = hypochlorite_mol
    kcl_mol = (chlorine_mol + 2 * hypochlorite_mol / 3
               + chlorate_mol / 4)
    return round(chlorine_mol * 71, 1), round(kcl_mol * 74.5, 1)


def check(perchlorate_g=277.0):
    # Independently balance the overall reaction from the three printed
    # steps: 4Cl2+8KOH -> KClO4+7KCl+4H2O.
    product_mol = perchlorate_g / 138.5
    chlorine_g = 4 * product_mol * (2 * 35.5)
    potassium_chloride_g = 7 * product_mol * (39 + 35.5)
    assert 4 * 2 == 1 + 7  # chlorine atoms
    assert 8 == 1 + 7  # potassium atoms
    assert 8 == 4 + 4  # oxygen atoms, including the water
    return round(chlorine_g, 1), round(potassium_chloride_g, 1)


PARAMS = {"perchlorate_g": 277.0}
VARIANTS = [
    {"perchlorate_g": 138.5},
    {"perchlorate_g": 415.5},
    {"perchlorate_g": 554.0},
]
ANSWER = (568.0, 1043.0)
