"""Source p13, MC54: 4.06 g MgCl2·6H2O gives 62.5 mL stock (ข)."""


def solve(hydrate_g=4.06, stock_ml=250, target_molar=0.0100, target_ml=500):
    hydrate_molar = 24 + 2 * 35.5 + 6 * 18
    stock_molar = hydrate_g / hydrate_molar / (stock_ml / 1000)
    return round(target_molar * target_ml / stock_molar, 1)


def check(hydrate_g=4.06, stock_ml=250, target_molar=0.0100, target_ml=500):
    # The stock contains one mole MgCl2 per mole of hydrate. Use a direct
    # portion of its total moles, avoiding an intermediate stock molarity.
    total_mgcl2_mol = hydrate_g / 203
    wanted_mgcl2_mol = target_molar * target_ml / 1000
    assert 0 < wanted_mgcl2_mol <= total_mgcl2_mol
    return round(stock_ml * wanted_mgcl2_mol / total_mgcl2_mol, 1)


PARAMS = {"hydrate_g": 4.06, "stock_ml": 250, "target_molar": 0.0100,
          "target_ml": 500}
VARIANTS = [
    {"hydrate_g": 2.03, "stock_ml": 250, "target_molar": 0.0100,
     "target_ml": 500},
    {"hydrate_g": 4.06, "stock_ml": 200, "target_molar": 0.0200,
     "target_ml": 500},
    {"hydrate_g": 8.12, "stock_ml": 400, "target_molar": 0.0250,
     "target_ml": 200},
]
ANSWER = 62.5
