"""Source p15, written 9: phosphate by silver precipitation/back titration."""

from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction


def _sci(value):
    assert 0 < value < 1
    exponent = 0
    coefficient = value
    while coefficient < 1:
        coefficient *= 10
        exponent -= 1
    superscript = str(-exponent).translate(str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹"))
    return f"{float(coefficient):.2f}×10⁻{superscript} mol"


def solve(sample_g="1.4200", ag_m="0.0840", ag_ml="50.00",
          scn_m="0.0600", scn_ml="3.00"):
    initial_ag = Fraction(ag_m) * Fraction(ag_ml) / 1000
    leftover_ag = Fraction(scn_m) * Fraction(scn_ml) / 1000
    assert initial_ag > leftover_ag > 0
    p2o5_mol = (initial_ag - leftover_ag) / 6
    percentage = p2o5_mol * 142 / Fraction(sample_g) * 100
    rounded = (Decimal(percentage.numerator) / Decimal(percentage.denominator)).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP,
    )
    return _sci(leftover_ag), f"{rounded:.2f}%"


def check(sample_g="1.4200", ag_m="0.0840", ag_ml="50.00",
          scn_m="0.0600", scn_ml="3.00"):
    leftover = Fraction(scn_m) * Fraction(scn_ml) / 1000
    supplied = Fraction(ag_m) * Fraction(ag_ml) / 1000
    # Forward-search the hundredth-percent P2O5 whose required six Ag+ ions
    # per formula unit leave the measured silver remainder.
    def mismatch(hundredth_pct):
        p2o5_mol = Fraction(sample_g) * Fraction(hundredth_pct, 10000) / 142
        return abs(supplied - 6 * p2o5_mol - leftover)

    best = min(range(1, 10001), key=lambda value: (mismatch(value), -value))
    return _sci(leftover), f"{best / 100:.2f}%"


PARAMS = {"sample_g": "1.4200", "ag_m": "0.0840", "ag_ml": "50.00",
          "scn_m": "0.0600", "scn_ml": "3.00"}
VARIANTS = [
    {"sample_g": "1.0000", "ag_m": "0.0600", "ag_ml": "50.00",
     "scn_m": "0.0500", "scn_ml": "4.00"},
    {"sample_g": "2.0000", "ag_m": "0.1000", "ag_ml": "50.00",
     "scn_m": "0.0500", "scn_ml": "10.00"},
    {"sample_g": "1.5000", "ag_m": "0.0800", "ag_ml": "75.00",
     "scn_m": "0.0600", "scn_ml": "5.00"},
]
ANSWER = ("1.80×10⁻⁴ mol", "6.70%")
