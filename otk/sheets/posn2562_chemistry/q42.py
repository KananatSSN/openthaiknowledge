"""E limits AD2E3 formation; product mass gives D atomic mass."""


def solve(a_g=2.4, d_atoms=2.408e22, e_mol=0.036, product_g=4.8, a_mass=60, e_mass=80):
    d_mol = d_atoms / (6.02e23)
    product_mol = min(a_g / a_mass, d_mol / 2, e_mol / 3)
    return round((product_g / product_mol - a_mass - 3 * e_mass) / 2)


def check(a_g=2.4, d_atoms=2.408e22, e_mol=0.036, product_g=4.8, a_mass=60, e_mass=80):
    d_mol = d_atoms / (6.02e23)
    for candidate in range(1, 201):
        made = min(a_g / a_mass, d_mol / 2, e_mol / 3) * (a_mass + 2 * candidate + 3 * e_mass)
        if abs(made - product_g) < 1e-8:
            return candidate
    raise ValueError("no atomic mass fits")


PARAMS = {
    "a_g": 2.4,
    "d_atoms": 2.408e22,
    "e_mol": 0.036,
    "product_g": 4.8,
    "a_mass": 60,
    "e_mass": 80,
}
VARIANTS = [
    {"a_g": 4.8, "d_atoms": 4.816e22, "e_mol": 0.072, "product_g": 9.6, "a_mass": 60, "e_mass": 80},
    {
        "a_g": 2.4,
        "d_atoms": 2.408e22,
        "e_mol": 0.036,
        "product_g": 5.04,
        "a_mass": 60,
        "e_mass": 80,
    },
    {
        "a_g": 2.4,
        "d_atoms": 2.408e22,
        "e_mol": 0.036,
        "product_g": 4.56,
        "a_mass": 60,
        "e_mass": 80,
    },
]
ANSWER = solve(**PARAMS)
