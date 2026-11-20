"""Source p16, written 11: solvent evaporation from boiling-point elevation."""

from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction


def _rounded(value):
    return (Decimal(value.numerator) / Decimal(value.denominator)).quantize(
        Decimal("0.1"), rounding=ROUND_HALF_UP,
    )


def solve(solute_mol="0.10", pure_bp="73.0", initial_bp="75.0",
          final_bp="75.5", kb="2.0"):
    amount = Fraction(solute_mol)
    initial_kg = Fraction(kb) * amount / (Fraction(initial_bp) - Fraction(pure_bp))
    final_kg = Fraction(kb) * amount / (Fraction(final_bp) - Fraction(pure_bp))
    assert initial_kg > final_kg > 0
    return _rounded(1000 * (initial_kg - final_kg))


def check(solute_mol="0.10", pure_bp="73.0", initial_bp="75.0",
          final_bp="75.5", kb="2.0"):
    n = Fraction(solute_mol)
    initial_g = 1000 * Fraction(kb) * n / (Fraction(initial_bp) - Fraction(pure_bp))
    lost = min((Fraction(t, 10) for t in range(1, int(initial_g * 10))),
               key=lambda guess: abs(Fraction(pure_bp) + 1000 * Fraction(kb) * n /
                                     (initial_g - guess) - Fraction(final_bp)))
    return _rounded(lost)


PARAMS = {"solute_mol": "0.10", "pure_bp": "73.0", "initial_bp": "75.0",
          "final_bp": "75.5", "kb": "2.0"}
VARIANTS = [
    {"solute_mol": "0.20", "pure_bp": "80.0", "initial_bp": "82.0",
     "final_bp": "82.5", "kb": "2.0"},
    {"solute_mol": "0.15", "pure_bp": "60.0", "initial_bp": "61.5",
     "final_bp": "62.0", "kb": "2.0"},
    {"solute_mol": "0.10", "pure_bp": "70.0", "initial_bp": "71.0",
     "final_bp": "71.25", "kb": "2.0"},
]
ANSWER = Decimal("20.0")
