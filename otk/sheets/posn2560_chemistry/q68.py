"""Source p19, written 8: combustion analysis gives empirical formula C3H6O."""

from fractions import Fraction
from math import gcd, lcm


def _formula(carbon, hydrogen, oxygen):
    return ("C" + (str(carbon) if carbon > 1 else "")
            + "H" + (str(hydrogen) if hydrogen > 1 else "")
            + "O" + (str(oxygen) if oxygen > 1 else ""))


def solve(sample_g=23.2, carbon_dioxide_g=52.8, water_g=21.6):
    sample = Fraction(str(sample_g))
    carbon_mol = Fraction(str(carbon_dioxide_g)) / 44
    hydrogen_mol = 2 * Fraction(str(water_g)) / 18
    oxygen_mol = (sample - 12 * carbon_mol - hydrogen_mol) / 16
    assert oxygen_mol > 0
    scale = lcm(carbon_mol.denominator, hydrogen_mol.denominator,
                oxygen_mol.denominator)
    counts = (int(carbon_mol * scale), int(hydrogen_mol * scale),
              int(oxygen_mol * scale))
    divisor = gcd(*counts)
    return _formula(*(count // divisor for count in counts))


def check(sample_g=23.2, carbon_dioxide_g=52.8, water_g=21.6):
    # Independent bounded search for the smallest integral CHO formula whose
    # combustion reproduces both product masses and the sample mass.
    carbon_mol = carbon_dioxide_g / 44
    solutions = []
    for carbon in range(1, 13):
        units_mol = carbon_mol / carbon
        for hydrogen in range(1, 25):
            predicted_water = units_mol * hydrogen / 2 * 18
            if abs(predicted_water - water_g) > 1e-7:
                continue
            for oxygen in range(1, 13):
                predicted_sample = units_mol * (12 * carbon + hydrogen + 16 * oxygen)
                if abs(predicted_sample - sample_g) < 1e-7 and gcd(carbon, hydrogen, oxygen) == 1:
                    solutions.append((carbon, hydrogen, oxygen))
    assert len(solutions) == 1
    return _formula(*solutions[0])


PARAMS = {"sample_g": 23.2, "carbon_dioxide_g": 52.8, "water_g": 21.6}
VARIANTS = [
    {"sample_g": 8.8, "carbon_dioxide_g": 17.6, "water_g": 7.2},
    {"sample_g": 9.2, "carbon_dioxide_g": 17.6, "water_g": 10.8},
    {"sample_g": 9.0, "carbon_dioxide_g": 13.2, "water_g": 5.4},
]
ANSWER = "C3H6O"
