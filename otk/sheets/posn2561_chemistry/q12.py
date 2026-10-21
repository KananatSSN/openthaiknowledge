"""Source p4, MC12: dichromate and iron(III) chloride both color water.

The original Cl2O distractor can be colored when dissolved at sufficient
concentration. It is replaced by NaCl in the adaptation for a unique answer.
"""


PAIRS = (("K₂SO₄", "MnCl₂"), ("NaCl", "Co(NO₃)₂"),
         ("K₂Cr₂O₇", "FeCl₃"), ("[Ni(NH₃)₆]Cl₂", "RbCl"))
COLORED = {"MnCl₂", "Co(NO₃)₂", "K₂Cr₂O₇", "FeCl₃", "[Ni(NH₃)₆]Cl₂"}


def solve(options=(0, 1, 2, 3)):
    assert sorted(options) == [0, 1, 2, 3]
    true = [i for i, option in enumerate(options)
            if all(compound in COLORED for compound in PAIRS[option])]
    assert len(true) == 1
    return true[0]


def check(options=(0, 1, 2, 3)):
    colors = {"K₂SO₄": None, "MnCl₂": "pale pink", "NaCl": None,
              "Co(NO₃)₂": "pink", "K₂Cr₂O₇": "orange", "FeCl₃": "yellow",
              "[Ni(NH₃)₆]Cl₂": "blue-violet", "RbCl": None}
    true = [i for i, option in enumerate(options)
            if all(colors[compound] for compound in PAIRS[option])]
    assert len(true) == 1
    return true[0]


PARAMS = {"options": (0, 1, 2, 3)}
VARIANTS = [
    {"options": (2, 0, 1, 3)},
    {"options": (1, 3, 2, 0)},
    {"options": (3, 2, 0, 1)},
]
ANSWER = 2
