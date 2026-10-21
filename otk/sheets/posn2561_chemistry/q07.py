"""Source p4, MC7: the Na > Na+ > Cl comparison is convention-dependent.

The adaptation supplies a consistent radius table in pm, so the mixed
atomic/ionic comparison has a definite answer. Values are representative
metallic/covalent atomic and six-coordinate ionic radii.
"""


SPECIES = ("Na", "Na⁺", "Cl", "Ca", "Br", "Br⁻")


def solve(radii=(186, 102, 99, 197, 114, 196)):
    na, na_ion, cl, ca, br, br_ion = radii
    claims = (
        na > na_ion > cl,
        ca > cl > na_ion,
        br_ion > br > ca,
        br > cl > na,
    )
    true = [i for i, claim in enumerate(claims) if claim]
    assert len(true) == 1
    return true[0]


def check(radii=(186, 102, 99, 197, 114, 196)):
    sizes = dict(zip(SPECIES, radii))
    chains = (("Na", "Na⁺", "Cl"), ("Ca", "Cl", "Na⁺"),
              ("Br⁻", "Br", "Ca"), ("Br", "Cl", "Na"))
    valid = [i for i, chain in enumerate(chains)
             if list(chain) == sorted(chain, key=lambda species: sizes[species],
                                      reverse=True)]
    assert len(valid) == 1
    return valid[0]


PARAMS = {"radii": (186, 102, 99, 197, 114, 196)}
VARIANTS = [
    {"radii": (190, 102, 79, 197, 114, 196)},
    {"radii": (185, 99, 79, 197, 114, 196)},
    {"radii": (186, 102, 100, 197, 114, 196)},
]
ANSWER = 0
