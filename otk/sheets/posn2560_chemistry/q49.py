"""Source p12, MC49: C4H10 combustion gives 100 cm3 water vapor (ง)."""


def solve(hydrocarbon_ml=20, oxygen_ml=130, carbon_dioxide_ml=80):
    carbon = round(carbon_dioxide_ml / hydrocarbon_ml)
    hydrogen = round(4 * (oxygen_ml / hydrocarbon_ml - carbon))
    assert carbon_dioxide_ml == carbon * hydrocarbon_ml
    assert oxygen_ml == (carbon + hydrogen / 4) * hydrocarbon_ml
    return carbon, hydrogen, round(hydrogen / 2 * hydrocarbon_ml)


def check(hydrocarbon_ml=20, oxygen_ml=130, carbon_dioxide_ml=80):
    # Search integer hydrocarbons whose C and O atom balances match the
    # measured equal-condition gas volumes; H2O follows H balance.
    candidates = []
    for carbon in range(1, 9):
        for hydrogen in range(2, 19, 2):
            if (carbon * hydrocarbon_ml == carbon_dioxide_ml
                    and (4 * carbon + hydrogen) * hydrocarbon_ml == 4 * oxygen_ml):
                candidates.append((carbon, hydrogen, hydrogen * hydrocarbon_ml // 2))
    assert len(candidates) == 1
    return candidates[0]


PARAMS = {"hydrocarbon_ml": 20, "oxygen_ml": 130, "carbon_dioxide_ml": 80}
VARIANTS = [
    {"hydrocarbon_ml": 20, "oxygen_ml": 40, "carbon_dioxide_ml": 20},
    {"hydrocarbon_ml": 20, "oxygen_ml": 70, "carbon_dioxide_ml": 40},
    {"hydrocarbon_ml": 20, "oxygen_ml": 100, "carbon_dioxide_ml": 60},
]
ANSWER = (4, 10, 100)
