"""Source p8, MC33: recover initial H₂ fraction after photochemical HCl formation."""

from fractions import Fraction


def solve(final_chlorine=30, final_hydrogen=50, final_hcl=20,
          chlorine_consumed_percent=25):
    assert final_chlorine + final_hydrogen + final_hcl == 100
    assert 0 < chlorine_consumed_percent < 100
    initial_chlorine = Fraction(final_chlorine * 100,
                                100 - chlorine_consumed_percent)
    consumed_chlorine = initial_chlorine - final_chlorine
    assert 2 * consumed_chlorine == final_hcl
    initial_hydrogen = 100 - initial_chlorine
    assert initial_hydrogen.denominator == 1
    return int(initial_hydrogen)


def check(final_chlorine=30, final_hydrogen=50, final_hcl=20,
          chlorine_consumed_percent=25):
    # Independent hydrogen balance: one mole H2 becomes two moles HCl;
    # the reaction conserves the total number of gas molecules.
    initial_hydrogen = Fraction(final_hydrogen) + Fraction(final_hcl, 2)
    initial_chlorine = Fraction(final_chlorine) + Fraction(final_hcl, 2)
    assert initial_hydrogen + initial_chlorine == 100
    assert Fraction(final_hcl, 2) / initial_chlorine * 100 == chlorine_consumed_percent
    return int(initial_hydrogen)


PARAMS = {"final_chlorine": 30, "final_hydrogen": 50, "final_hcl": 20,
          "chlorine_consumed_percent": 25}
VARIANTS = [
    {"final_chlorine": 15, "final_hydrogen": 75, "final_hcl": 10,
     "chlorine_consumed_percent": 25},
    {"final_chlorine": 45, "final_hydrogen": 25, "final_hcl": 30,
     "chlorine_consumed_percent": 25},
    {"final_chlorine": 30, "final_hydrogen": 10, "final_hcl": 60,
     "chlorine_consumed_percent": 50},
]
ANSWER = 60
