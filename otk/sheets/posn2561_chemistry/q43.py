"""Source p10, MC43: limiting reagent in KO2 and CO2 oxygen production."""

from fractions import Fraction


def solve(superoxide_mg=710, carbon_dioxide_cm3=336):
    assert superoxide_mg > 0 and carbon_dioxide_cm3 > 0
    # 4KO2 + 2CO2 -> 2K2CO3 + 3O2; KO2 molar mass 71 g/mol.
    ko2_mmol = Fraction(superoxide_mg, 71)
    co2_mmol = Fraction(carbon_dioxide_cm3, 22400) * 1000
    oxygen_mmol = min(Fraction(3, 4) * ko2_mmol, Fraction(3, 2) * co2_mmol)
    oxygen_cm3 = oxygen_mmol * Fraction(224, 10)
    assert oxygen_cm3.denominator == 1
    return int(oxygen_cm3)


def check(superoxide_mg=710, carbon_dioxide_cm3=336):
    # Test candidate oxygen volumes against both reactant budgets independently.
    ko2_mmol = Fraction(superoxide_mg, 71)
    co2_mmol = Fraction(carbon_dioxide_cm3, 22400) * 1000
    feasible = [oxygen for oxygen in range(1, 2001)
                if Fraction(oxygen, 22400) * 1000 * Fraction(4, 3) <= ko2_mmol
                and Fraction(oxygen, 22400) * 1000 * Fraction(2, 3) <= co2_mmol]
    return max(feasible)


PARAMS = {"superoxide_mg": 710, "carbon_dioxide_cm3": 336}
VARIANTS = [
    {"superoxide_mg": 1420, "carbon_dioxide_cm3": 560},
    {"superoxide_mg": 1065, "carbon_dioxide_cm3": 448},
    {"superoxide_mg": 2840, "carbon_dioxide_cm3": 224},
]
ANSWER = 168
