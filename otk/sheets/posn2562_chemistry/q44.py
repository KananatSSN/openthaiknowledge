"""MnO2 gives one Cl2; hot base consumes two NaOH per Cl2."""


def solve(naoh_mol=1.5, mno2_molar=87):
    # 3Cl2 + 6NaOH -> 5NaCl + NaClO3 + 3H2O.
    return round(naoh_mol / 2 * mno2_molar, 1)


def check(naoh_mol=1.5, mno2_molar=87):
    # MnO2 + 4HCl -> MnCl2 + 2H2O + Cl2; chain the extents.
    chlorine_required = naoh_mol * 3 / 6
    return round(chlorine_required * mno2_molar, 1)


PARAMS = {"naoh_mol": 1.5, "mno2_molar": 87}
VARIANTS = [
    {"naoh_mol": 1.0, "mno2_molar": 87},
    {"naoh_mol": 2.0, "mno2_molar": 87},
    {"naoh_mol": 3.0, "mno2_molar": 87},
]
ANSWER = solve(**PARAMS)
