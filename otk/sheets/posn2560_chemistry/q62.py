"""Source p16, written 2: NaIO4 has iodine +7; OF2 has fluorine -1."""


OXIDATION = {"HBrO3": 5, "KClO2": 3, "NaIO4": 7, "Cl2O": 1, "OF2": -1}


def solve(formulas=("HBrO3", "KClO2", "NaIO4", "Cl2O", "OF2")):
    ordered = sorted(formulas, key=lambda formula: OXIDATION[formula])
    highest, lowest = ordered[-1], ordered[0]
    return highest, OXIDATION[highest], lowest, OXIDATION[lowest]


def check(formulas=("HBrO3", "KClO2", "NaIO4", "Cl2O", "OF2")):
    # Charge balance for the halogen in each compound; fluorine is -1 in OF2.
    balance = {
        "HBrO3": 3 * 2 - 1, "KClO2": 2 * 2 - 1,
        "NaIO4": 4 * 2 - 1, "Cl2O": 2 / 2, "OF2": -1,
    }
    maximum = max(formulas, key=lambda formula: balance[formula])
    minimum = min(formulas, key=lambda formula: balance[formula])
    return maximum, int(balance[maximum]), minimum, int(balance[minimum])


PARAMS = {"formulas": ("HBrO3", "KClO2", "NaIO4", "Cl2O", "OF2")}
VARIANTS = [
    {"formulas": ("HBrO3", "KClO2", "Cl2O", "OF2")},
    {"formulas": ("HBrO3", "KClO2", "NaIO4", "Cl2O")},
    {"formulas": ("KClO2", "Cl2O", "OF2")},
]
ANSWER = ("NaIO4", 7, "OF2", -1)
