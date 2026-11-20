"""Source p14, MC58: 36 mmol chloride means X=6 mL, added water Y=12 mL (ก)."""


def solve(chloride_mmol=36, stock_molar=3.0, target_molar=1.0):
    # CdCl2 supplies two chloride ions per formula unit.
    stock_ml = chloride_mmol / (2 * stock_molar)
    final_ml = stock_ml * stock_molar / target_molar
    return round(stock_ml, 1), round(final_ml - stock_ml, 1)


def check(chloride_mmol=36, stock_molar=3.0, target_molar=1.0):
    # First count moles of salt, then independently derive both volumes.
    cdcl2_mmol = chloride_mmol / 2
    original_ml = cdcl2_mmol / stock_molar
    final_ml = cdcl2_mmol / target_molar
    assert stock_molar > target_molar > 0
    return round(original_ml, 1), round(final_ml - original_ml, 1)


PARAMS = {"chloride_mmol": 36, "stock_molar": 3.0, "target_molar": 1.0}
VARIANTS = [
    {"chloride_mmol": 36, "stock_molar": 2.0, "target_molar": 0.5},
    {"chloride_mmol": 48, "stock_molar": 4.0, "target_molar": 1.0},
    {"chloride_mmol": 30, "stock_molar": 2.5, "target_molar": 0.5},
]
ANSWER = (6.0, 12.0)
