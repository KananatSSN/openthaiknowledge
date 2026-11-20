"""Source p10, MC35: NaCl lattice claims a and b are true (choice ค)."""

_TRUTH = {
    "coord_equal": True, "coord_unequal": False,
    "lattice_overcome": True, "lattice_unchanged": False,
    "crop_is_formula": False, "formula_one_to_one": True,
}


def solve(claims=("coord_equal", "lattice_overcome", "crop_is_formula")):
    return tuple(i for i, claim in enumerate(claims) if _TRUTH[claim])


def check(claims=("coord_equal", "lattice_overcome", "crop_is_formula")):
    # Rock salt has six oppositely charged nearest neighbors around either ion;
    # dissolution separates lattice ions; Na+ and Cl- charges require 1:1.
    sodium_neighbors = 6
    chloride_neighbors = 6
    visible_sodium, visible_chloride = 14, 13
    neutral_ratio = (1, 1)  # Na+ and Cl- charges balance at one each.
    facts = {
        "coord_equal": sodium_neighbors == chloride_neighbors,
        "coord_unequal": sodium_neighbors != chloride_neighbors,
        "lattice_overcome": True,
        "lattice_unchanged": False,
        "crop_is_formula": (visible_sodium, visible_chloride) == neutral_ratio,
        "formula_one_to_one": neutral_ratio == (1, 1),
    }
    true_claims = []
    for i, claim in enumerate(claims):
        if facts[claim]:
            true_claims.append(i)
    return tuple(true_claims)


PARAMS = {"claims": ("coord_equal", "lattice_overcome", "crop_is_formula")}
VARIANTS = [
    {"claims": ("coord_equal", "lattice_unchanged", "formula_one_to_one")},
    {"claims": ("coord_unequal", "lattice_overcome", "formula_one_to_one")},
    {"claims": ("coord_equal", "lattice_unchanged", "crop_is_formula")},
]
ANSWER = (0, 1)
