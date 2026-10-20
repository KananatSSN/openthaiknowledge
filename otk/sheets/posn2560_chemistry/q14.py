"""Source p6, MC14: MgHPO4, BaSO4 and BaHPO4 (choice ง)."""


def _formula(cation, anion):
    charge = 1 if cation in {"Na", "K"} else 2
    if charge == 2:
        return f"{cation}{anion}"
    if anion in {"SO4", "HPO4"}:
        return f"{cation}2{anion}"
    return f"{cation}{anion}"


def solve(cations=("Ba", "Mg", "Na"), anions=("Cl", "SO4", "HPO4")):
    # The supported pools only use group-1 ions, Ba2+ and Mg2+.
    # Chlorides/nitrates and group-1 salts dissolve; BaSO4 and
    # alkaline-earth hydrogen phosphates are sparingly soluble.
    return tuple(sorted(_formula(c, a) for c in cations for a in anions
                        if (a == "SO4" and c == "Ba")
                        or (a == "HPO4" and c in {"Ba", "Mg"})))


def check(cations=("Ba", "Mg", "Na"), anions=("Cl", "SO4", "HPO4")):
    # Explicit independently reviewed precipitate inventory, intersected
    # with the ion combinations present in this question.
    inventory = {"BaSO4": ("Ba", "SO4"),
                 "BaHPO4": ("Ba", "HPO4"),
                 "MgHPO4": ("Mg", "HPO4")}
    return tuple(sorted(formula for formula, pair in inventory.items()
                        if pair[0] in cations and pair[1] in anions))


PARAMS = {"cations": ("Ba", "Mg", "Na"),
          "anions": ("Cl", "SO4", "HPO4")}
VARIANTS = [
    {"cations": ("Ba", "Mg", "K"), "anions": ("Cl", "SO4", "HPO4")},
    {"cations": ("Ba", "Mg", "Na"), "anions": ("NO3", "SO4", "HPO4")},
    {"cations": ("Ba", "Mg", "K"), "anions": ("NO3", "SO4", "HPO4")},
]
ANSWER = ("BaHPO4", "BaSO4", "MgHPO4")
