"""Source p12, MC45: 3.94 g for 0.020 mol is BaCO3 (ง)."""

_MOLAR_MASS = {"Na2CO3": 106, "MgCO3": 84, "CaCO3": 100, "BaCO3": 197}


def solve(carbonate_g=3.94, acid_molar=0.2, acid_ml=200, co2_ml=448):
    carbonate_from_acid = acid_molar * acid_ml / 1000 / 2
    carbonate_from_gas = co2_ml / 22400
    assert abs(carbonate_from_acid - carbonate_from_gas) < 1e-8
    molar_mass = carbonate_g / carbonate_from_gas
    matches = [formula for formula, value in _MOLAR_MASS.items()
               if abs(value - molar_mass) < 1e-7]
    assert len(matches) == 1
    return matches[0]


def check(carbonate_g=3.94, acid_molar=0.2, acid_ml=200, co2_ml=448):
    acid_moles = acid_molar * acid_ml / 1000
    gas_moles = co2_ml / 1000 / 22.4
    assert abs(acid_moles - 2 * gas_moles) < 1e-8
    cation_masses = {"Na2CO3": 2 * 23, "MgCO3": 24, "CaCO3": 40, "BaCO3": 137}
    carbonate_mass = 12 + 3 * 16
    return next(formula for formula, metal_mass in cation_masses.items()
                if abs((metal_mass + carbonate_mass) * gas_moles - carbonate_g) < 1e-7)


PARAMS = {"carbonate_g": 3.94, "acid_molar": 0.2, "acid_ml": 200, "co2_ml": 448}
VARIANTS = [
    {"carbonate_g": 2.12, "acid_molar": 0.2, "acid_ml": 200, "co2_ml": 448},
    {"carbonate_g": 1.68, "acid_molar": 0.2, "acid_ml": 200, "co2_ml": 448},
    {"carbonate_g": 2.00, "acid_molar": 0.2, "acid_ml": 200, "co2_ml": 448},
]
ANSWER = "BaCO3"
