"""Source p16, written 13: rank vapor pressures of four pure substances."""


SPECIES = ("CH4", "C2H5OH", "C2H5OC2H5", "SiH4")
ORDER = ("C2H5OH", "C2H5OC2H5", "SiH4", "CH4")


def solve(sequence=SPECIES):
    assert set(sequence) == set(SPECIES) and len(sequence) == 4
    # Ethanol hydrogen-bonds; ether is polar; the nonpolar hydrides differ
    # by dispersion, with larger SiH4 holding its molecules more strongly.
    interaction_rank = {"C2H5OH": 0, "C2H5OC2H5": 1,
                        "SiH4": 2, "CH4": 3}
    return tuple(sorted(sequence, key=lambda name: interaction_rank[name]))


def check(sequence=SPECIES):
    assert set(sequence) == set(SPECIES) and len(sequence) == 4
    # Independent NIST normal boiling points (K), high to low. At a common
    # temperature, the lower-boiling liquid has the greater vapor pressure.
    # Methane 111.7, silane ~161.7, ethyl ether 307.7, ethanol 351.5.
    boiling_k = {"CH4": 111.7, "SiH4": 161.7,
                 "C2H5OC2H5": 307.7, "C2H5OH": 351.5}
    return tuple(sorted(sequence, key=lambda name: boiling_k[name], reverse=True))


PARAMS = {"sequence": SPECIES}
VARIANTS = [
    {"sequence": tuple(reversed(SPECIES))},
    {"sequence": ("SiH4", "CH4", "C2H5OC2H5", "C2H5OH")},
    {"sequence": ("C2H5OC2H5", "SiH4", "C2H5OH", "CH4")},
]
ANSWER = ORDER
