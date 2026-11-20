"""Source p5, MC14: among coordination complexes Cr(III) > Fe(II)."""


COMPOUNDS = ("MnO₂", "NiSO₄", "K₄[Fe(CN)₆]", "[Cr(NH₃)₆]Cl₃")
OXIDATION = (4, 2, 2, 3)
IS_COMPLEX = (False, False, True, True)


def solve(options=(0, 1, 2, 3)):
    assert sorted(options) == [0, 1, 2, 3]
    eligible = [i for i, option in enumerate(options) if IS_COMPLEX[option]]
    return max(eligible, key=lambda i: OXIDATION[options[i]])


def check(options=(0, 1, 2, 3)):
    # Charge balance: [Fe(CN)6]4− has Fe +2; [Cr(NH3)6]3+ has Cr +3.
    charge = {"K₄[Fe(CN)₆]": -4, "[Cr(NH₃)₆]Cl₃": 3}
    ligand = {"K₄[Fe(CN)₆]": -1, "[Cr(NH₃)₆]Cl₃": 0}
    eligible = [(i, compound) for i, option in enumerate(options)
                if (compound := COMPOUNDS[option]) in charge]
    winner = max(eligible, key=lambda row: charge[row[1]] - 6 * ligand[row[1]])
    return winner[0]


PARAMS = {"options": (0, 1, 2, 3)}
VARIANTS = [
    {"options": (3, 0, 1, 2)},
    {"options": (1, 3, 2, 0)},
    {"options": (2, 1, 3, 0)},
]
ANSWER = 3
