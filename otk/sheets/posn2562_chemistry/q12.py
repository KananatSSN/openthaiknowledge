"""Source MC12: Br2 oxidises K but cannot oxidise Cl-; I2 cannot oxidise Br-."""


def solve(alkali="K", bromide="KBr", chloride="NaCl"):
    assert alkali in ("K", "Na", "Li")
    assert bromide in ("KBr", "NaBr") and chloride in ("NaCl", "KCl")
    reactions = (True, False, False)
    choices = ((0, 1), (1, 2), (0, 2), (0,))
    valid = tuple(i for i, reacts in enumerate(reactions) if reacts)
    return choices.index(valid)


def check(alkali="K", bromide="KBr", chloride="NaCl"):
    assert alkali in ("K", "Na", "Li")
    assert bromide in ("KBr", "NaBr") and chloride in ("NaCl", "KCl")
    # Oxidising strength Cl2 > Br2 > I2; displacement requires stronger halogen.
    strengths = {"Cl2": 3, "Br2": 2, "I2": 1}
    first = True  # elemental alkali + Br2 -> bromide
    second = strengths["I2"] > strengths["Br2"]
    third = strengths["Br2"] > strengths["Cl2"]
    return 3 if (first, second, third) == (True, False, False) else None


PARAMS = {"alkali": "K", "bromide": "KBr", "chloride": "NaCl"}
VARIANTS = [
    {"alkali": "Na", "bromide": "KBr", "chloride": "NaCl"},
    {"alkali": "Li", "bromide": "NaBr", "chloride": "KCl"},
    {"alkali": "K", "bromide": "NaBr", "chloride": "KCl"},
]
ANSWER = solve(**PARAMS)
