"""Source p14, MC57: 0.505 g KNO3 and 0.828 g Pb(NO3)2 (ง)."""


def solve(volume_ml=100, potassium_molar=0.0500, lead_molar=0.0250):
    volume_litre = volume_ml / 1000
    potassium_molar_mass = 39 + 14 + 3 * 16
    lead_molar_mass = 207 + 2 * (14 + 3 * 16)
    return (round(potassium_molar * volume_litre * potassium_molar_mass, 3),
            round(lead_molar * volume_litre * lead_molar_mass, 3))


def check(volume_ml=100, potassium_molar=0.0500, lead_molar=0.0250):
    # Each gram mass must yield the requested number of formula units.
    potassium_g = potassium_molar * volume_ml * 101 / 1000
    lead_g = lead_molar * volume_ml * 331 / 1000
    assert potassium_g > 0 and lead_g > 0
    return round(potassium_g, 3), round(lead_g, 3)


PARAMS = {"volume_ml": 100, "potassium_molar": 0.0500,
          "lead_molar": 0.0250}
VARIANTS = [
    {"volume_ml": 200, "potassium_molar": 0.0250, "lead_molar": 0.0100},
    {"volume_ml": 250, "potassium_molar": 0.0400, "lead_molar": 0.0200},
    {"volume_ml": 100, "potassium_molar": 0.0800, "lead_molar": 0.0400},
]
ANSWER = (0.505, 0.828)
