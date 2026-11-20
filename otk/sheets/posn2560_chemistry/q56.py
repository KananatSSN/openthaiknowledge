"""Source p13, MC56: 14.9% w/v NaClO diluted 2.50 to 10.00 mL is 0.500 M (ก)."""


def solve(percent_wv=14.9, aliquot_ml=2.50, final_ml=10.00):
    # Percent w/v is grams solute per 100 mL of original solution.
    stock_molar = (percent_wv / 74.5) / 0.100
    return round(stock_molar * aliquot_ml / final_ml, 3)


def check(percent_wv=14.9, aliquot_ml=2.50, final_ml=10.00):
    # Count the actual solute mass in the pipetted aliquot.
    solute_g = percent_wv * aliquot_ml / 100
    final_litre = final_ml / 1000
    return round((solute_g / (23 + 16 + 35.5)) / final_litre, 3)


PARAMS = {"percent_wv": 14.9, "aliquot_ml": 2.50, "final_ml": 10.00}
VARIANTS = [
    {"percent_wv": 14.9, "aliquot_ml": 5.00, "final_ml": 10.00},
    {"percent_wv": 7.45, "aliquot_ml": 2.00, "final_ml": 20.00},
    {"percent_wv": 22.35, "aliquot_ml": 4.00, "final_ml": 20.00},
]
ANSWER = 0.500
