"""Source p11, MC48: NaOH stock volume after accounting for ppm Ba(OH)2."""

from decimal import Decimal
from fractions import Fraction


def solve(target_oh_m="0.4016", final_ml=500, barium_ppm=342,
          barium_density="1.00", barium_ml=200,
          sodium_percent="32.0", sodium_density="1.25"):
    assert Fraction(target_oh_m) > 0 and final_ml > 0
    # ppm is solute mass/solution mass times 10^6.
    barium_g = Fraction(barium_density) * barium_ml * barium_ppm / 1_000_000
    barium_oh_mmol = barium_g / 171 * 2 * 1000
    target_oh_mmol = Fraction(target_oh_m) * final_ml
    sodium_oh_mmol = target_oh_mmol - barium_oh_mmol
    assert sodium_oh_mmol > 0
    sodium_mmol_per_ml = Fraction(sodium_density) * Fraction(sodium_percent) / 100 / 40 * 1000
    volume = sodium_oh_mmol / sodium_mmol_per_ml
    return Decimal(volume.numerator) / Decimal(volume.denominator)


def check(target_oh_m="0.4016", final_ml=500, barium_ppm=342,
          barium_density="1.00", barium_ml=200,
          sodium_percent="32.0", sodium_density="1.25"):
    # Forward-predict final OH molarity for hundredth-mL stock additions.
    target = Fraction(target_oh_m)
    barium_mass = Fraction(barium_density) * barium_ml * barium_ppm / 1_000_000
    barium_oh_mmol = 2 * barium_mass / 171 * 1000
    sodium_mmol_per_ml = Fraction(sodium_density) * Fraction(sodium_percent) / 100 / 40 * 1000
    for hundredths in range(1, 10001):
        sodium_ml = Fraction(hundredths, 100)
        final_oh = (barium_oh_mmol + sodium_ml * sodium_mmol_per_ml) / final_ml
        if final_oh == target:
            return Decimal(hundredths) / 100
    raise AssertionError("no hundredth-mL stock volume matches the variant")


PARAMS = {"target_oh_m": "0.4016", "final_ml": 500, "barium_ppm": 342,
          "barium_density": "1.00", "barium_ml": 200,
          "sodium_percent": "32.0", "sodium_density": "1.25"}
VARIANTS = [
    {**PARAMS, "target_oh_m": "0.2016"},
    {**PARAMS, "target_oh_m": "0.6016"},
    {**PARAMS, "target_oh_m": "0.4032", "barium_ppm": 684},
]
ANSWER = Decimal("20")
