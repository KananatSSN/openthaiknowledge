"""Source p9, MC29: all four printed formula–name pairs are correct.

The printed 'which is incorrect?' item has no correct choice. The adapted
generator asks how many pairs are wrong, with 0 for the source data.
"""

FORMULAS = ("CrO3", "Na2S2O3", "Hg2Cl2", "Ba(NO2)2")
_CANONICAL = {
    "CrO3": "chromium_trioxide", "Na2S2O3": "sodium_thiosulfate",
    "Hg2Cl2": "mercury_i_chloride", "Ba(NO2)2": "barium_nitrite",
}

# Independent reverse lookup, including plausible near-miss names.
_NAMED_FORMULA = {
    "chromium_trioxide": "CrO3", "chromium_dioxide": "CrO2",
    "sodium_thiosulfate": "Na2S2O3", "sodium_sulfite": "Na2SO3",
    "mercury_i_chloride": "Hg2Cl2", "mercury_ii_chloride": "HgCl2",
    "barium_nitrite": "Ba(NO2)2", "barium_nitrate": "Ba(NO3)2",
}


def solve(names=("chromium_trioxide", "sodium_thiosulfate",
                     "mercury_i_chloride", "barium_nitrite")):
    return sum(name != _CANONICAL[formula] for formula, name in zip(FORMULAS, names))


def check(names=("chromium_trioxide", "sodium_thiosulfate",
                     "mercury_i_chloride", "barium_nitrite")):
    assert len(names) == len(FORMULAS)
    return sum(_NAMED_FORMULA[name] != formula
               for name, formula in zip(names, FORMULAS))


PARAMS = {"names": ("chromium_trioxide", "sodium_thiosulfate",
                    "mercury_i_chloride", "barium_nitrite")}
VARIANTS = [
    {"names": ("chromium_trioxide", "sodium_thiosulfate",
               "mercury_i_chloride", "barium_nitrate")},
    {"names": ("chromium_dioxide", "sodium_thiosulfate",
               "mercury_ii_chloride", "barium_nitrite")},
    {"names": ("chromium_dioxide", "sodium_sulfite",
               "mercury_i_chloride", "barium_nitrate")},
]
ANSWER = 0
