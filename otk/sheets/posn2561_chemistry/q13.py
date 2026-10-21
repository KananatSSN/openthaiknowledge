"""Source p5, MC13: carbonate/sulfate tests identify Mg, K, Ba."""


OPTIONS = (
    ("KNO₃", "MgCl₂", "BaCl₂"),
    ("Mg(NO₃)₂", "Ba(NO₃)₂", "KCl"),
    ("BaCl₂", "KNO₃", "Mg(NO₃)₂"),
    ("MgCl₂", "KCl", "Ba(NO₃)₂"),
)
CATIONS = {
    "KNO₃": "K", "MgCl₂": "Mg", "BaCl₂": "Ba",
    "Mg(NO₃)₂": "Mg", "Ba(NO₃)₂": "Ba", "KCl": "K",
}
OBSERVED = ((False, True, False), (False, False, False),
            (False, True, True))  # NaCl, Na2CO3, Na2SO4


def solve(options=(0, 1, 2, 3)):
    assert sorted(options) == [0, 1, 2, 3]
    expected = {"Mg": (False, True, False), "K": (False, False, False),
                "Ba": (False, True, True)}
    matches = [i for i, option in enumerate(options)
               if tuple(expected[CATIONS[compound]] for compound in OPTIONS[option])
               == OBSERVED]
    assert len(matches) == 1
    return matches[0]


def check(options=(0, 1, 2, 3)):
    # Independent product-solubility route. All listed chlorides stay soluble;
    # K2CO3/K2SO4 and MgSO4 stay dissolved, while MgCO3, BaCO3, BaSO4 do not.
    insoluble = {"MgCO₃", "BaCO₃", "BaSO₄"}
    products = {
        "K": ("KCl", "K₂CO₃", "K₂SO₄"),
        "Mg": ("MgCl₂", "MgCO₃", "MgSO₄"),
        "Ba": ("BaCl₂", "BaCO₃", "BaSO₄"),
    }
    matches = []
    for i, option in enumerate(options):
        pattern = tuple(tuple(product in insoluble for product in products[CATIONS[salt]])
                        for salt in OPTIONS[option])
        if pattern == OBSERVED:
            matches.append(i)
    assert len(matches) == 1
    return matches[0]


PARAMS = {"options": (0, 1, 2, 3)}
VARIANTS = [
    {"options": (3, 0, 1, 2)},
    {"options": (1, 3, 2, 0)},
    {"options": (2, 1, 0, 3)},
]
ANSWER = 3
