"""Diluted NaOH molarity from stock mass fraction, density and additive volumes."""


def solve(stock_percent=40, density=1.5, stock_ml=50, water_ml=450):
    moles = stock_ml * density * stock_percent / 100 / 40
    return round(moles / ((stock_ml + water_ml) / 1000), 2)


def check(stock_percent=40, density=1.5, stock_ml=50, water_ml=450):
    total_volume_l = (stock_ml + water_ml) / 1000
    solution_g = stock_ml * density
    naoh_g = solution_g * (stock_percent / 100)
    return round((naoh_g / 40) / total_volume_l, 2)


PARAMS = {"stock_percent": 40, "density": 1.5, "stock_ml": 50, "water_ml": 450}
VARIANTS = [
    {"stock_percent": 20, "density": 1.5, "stock_ml": 50, "water_ml": 450},
    {"stock_percent": 40, "density": 1.2, "stock_ml": 50, "water_ml": 450},
    {"stock_percent": 40, "density": 1.5, "stock_ml": 100, "water_ml": 400},
]

ANSWER = solve(**PARAMS)
