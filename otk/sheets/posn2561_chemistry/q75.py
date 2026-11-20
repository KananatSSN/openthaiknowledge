"""Source p16, written 15: molar mass from Graham-law effusion rates."""

from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction


def _rounded(value):
    return (Decimal(value.numerator) / Decimal(value.denominator)).quantize(
        Decimal("0.1"), rounding=ROUND_HALF_UP,
    )


def solve(sample_mol="0.000235", sample_s="100.0", argon_mol="0.000105",
          argon_s="50.0", argon_mass=40):
    sample_rate = Fraction(sample_mol) / Fraction(sample_s)
    argon_rate = Fraction(argon_mol) / Fraction(argon_s)
    mass = Fraction(argon_mass) * (argon_rate / sample_rate) ** 2
    return _rounded(mass)


def check(sample_mol="0.000235", sample_s="100.0", argon_mol="0.000105",
          argon_s="50.0", argon_mass=40):
    # Forward-search masses in tenths: the mass whose Graham-law prediction
    # is closest to the measured sample/argon effusion-rate ratio wins.
    observed = float(Fraction(sample_mol) * Fraction(argon_s) /
                     (Fraction(sample_s) * Fraction(argon_mol)))
    nearest = min(range(1, 1001),
                  key=lambda tenth: abs((argon_mass / (tenth / 10)) ** 0.5
                                        - observed))
    return Decimal(nearest) / 10


PARAMS = {"sample_mol": "0.000235", "sample_s": "100.0",
          "argon_mol": "0.000105", "argon_s": "50.0", "argon_mass": 40}
VARIANTS = [
    {**PARAMS, "sample_mol": "0.000240"},
    {**PARAMS, "sample_mol": "0.000280"},
    {**PARAMS, "sample_mol": "0.000420"},
]
ANSWER = Decimal("31.9")
