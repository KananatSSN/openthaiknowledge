"""Source p8, MC27: central-atom octets in NO₂, BF₄⁻, XeF₄, CO₃²⁻."""


PAIRS = (
    ("NO₂", "BF₄⁻"),
    ("NO₂", "CO₃²⁻"),
    ("BF₄⁻", "XeF₄"),
    ("BF₄⁻", "CO₃²⁻"),
)
CENTRAL_ELECTRONS = {"NO₂": 7, "BF₄⁻": 8, "XeF₄": 12, "CO₃²⁻": 8}


def solve(options=(0, 1, 2, 3)):
    assert sorted(options) == [0, 1, 2, 3]
    valid = [i for i, option in enumerate(options)
             if all(CENTRAL_ELECTRONS[species] == 8 for species in PAIRS[option])]
    assert len(valid) == 1
    return valid[0]


def check(options=(0, 1, 2, 3)):
    # Lewis structures: NO2 has 17 total valence electrons (radical);
    # BF4- has four B-F bonds; XeF4 has four bonds and two lone pairs;
    # carbonate has one C=O and two C-O bonds in each resonance form.
    total_valence = {"NO₂": 5 + 2 * 6, "BF₄⁻": 3 + 4 * 7 + 1,
                     "XeF₄": 8 + 4 * 7, "CO₃²⁻": 4 + 3 * 6 + 2}
    assert total_valence == {"NO₂": 17, "BF₄⁻": 32, "XeF₄": 36, "CO₃²⁻": 24}
    octet = {"BF₄⁻", "CO₃²⁻"}
    return [set(PAIRS[i]) for i in options].index(octet)


PARAMS = {"options": (0, 1, 2, 3)}
VARIANTS = [
    {"options": (3, 0, 1, 2)},
    {"options": (1, 3, 2, 0)},
    {"options": (2, 1, 0, 3)},
]
ANSWER = 3
