"""Source p13, MC51: Zn + 2HCl gives true claims a and b (ก)."""


def _actual(zn_g=1.30, acid_molar=6.0, acid_ml=100):
    zinc_mol = zn_g / 65
    acid_initial = acid_molar * acid_ml / 1000
    assert acid_initial >= 2 * zinc_mol
    hydrogen_l = zinc_mol * 22.4
    zinc_chloride_percent = zinc_mol * 136 / acid_ml * 100
    consumed_acid = 2 * zinc_mol
    remaining_acid = acid_initial - consumed_acid
    return hydrogen_l, zinc_chloride_percent, consumed_acid, remaining_acid


def solve(zn_g=1.30, acid_molar=6.0, acid_ml=100,
          claim_hydrogen_l=0.448, claim_zinc_chloride_percent=2.72,
          claim_acid_used_mol=0.020, claim_acid_left_mol=0.58):
    actual = _actual(zn_g, acid_molar, acid_ml)
    return tuple(i for i, valid in enumerate((
        abs(actual[0] - claim_hydrogen_l) < 1e-7,
        abs(actual[1] - claim_zinc_chloride_percent) < 1e-7,
        abs(actual[2] - claim_acid_used_mol) < 1e-7
        and abs(actual[3] - claim_acid_left_mol) < 1e-7,
    )) if valid)


def check(zn_g=1.30, acid_molar=6.0, acid_ml=100,
          claim_hydrogen_l=0.448, claim_zinc_chloride_percent=2.72,
          claim_acid_used_mol=0.020, claim_acid_left_mol=0.58):
    # Direct mass and atom balance: ZnCl2 incorporates Zn and two Cl,
    # while the two released H atoms make one H2 molecule.
    reaction_extent = zn_g / 65
    grams_product = reaction_extent * (65 + 2 * 35.5)
    initial_hcl = acid_molar * acid_ml / 1000
    measurements = (
        reaction_extent * 22.4,
        grams_product / acid_ml * 100,
        2 * reaction_extent,
        initial_hcl - 2 * reaction_extent,
    )
    return tuple(i for i, valid in enumerate((
        abs(measurements[0] - claim_hydrogen_l) < 1e-7,
        abs(measurements[1] - claim_zinc_chloride_percent) < 1e-7,
        abs(measurements[2] - claim_acid_used_mol) < 1e-7
        and abs(measurements[3] - claim_acid_left_mol) < 1e-7,
    )) if valid)


PARAMS = {"zn_g": 1.30, "acid_molar": 6.0, "acid_ml": 100,
          "claim_hydrogen_l": 0.448, "claim_zinc_chloride_percent": 2.72,
          "claim_acid_used_mol": 0.020, "claim_acid_left_mol": 0.58}
VARIANTS = [
    {"zn_g": 0.65, "acid_molar": 2.0, "acid_ml": 100,
     "claim_hydrogen_l": 0.224, "claim_zinc_chloride_percent": 1.36,
     "claim_acid_used_mol": 0.020, "claim_acid_left_mol": 0.18},
    {"zn_g": 1.30, "acid_molar": 2.0, "acid_ml": 100,
     "claim_hydrogen_l": 0.448, "claim_zinc_chloride_percent": 1.36,
     "claim_acid_used_mol": 0.040, "claim_acid_left_mol": 0.16},
    {"zn_g": 1.95, "acid_molar": 2.0, "acid_ml": 100,
     "claim_hydrogen_l": 0.448, "claim_zinc_chloride_percent": 4.08,
     "claim_acid_used_mol": 0.060, "claim_acid_left_mol": 0.14},
]
ANSWER = (0, 1)
