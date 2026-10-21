"""Source p13, MC59: original-to-final volume ratio at fixed temperature."""

from fractions import Fraction


def solve(initial_mmhg=700, final_mmhg=200):
    assert initial_mmhg > final_mmhg > 0
    return Fraction(final_mmhg, initial_mmhg)


def check(initial_mmhg=700, final_mmhg=200):
    assert initial_mmhg > final_mmhg > 0
    expansion = Fraction(initial_mmhg, final_mmhg)
    return 1 / expansion


PARAMS = {"initial_mmhg": 700, "final_mmhg": 200}
VARIANTS = [
    {"initial_mmhg": 900, "final_mmhg": 300},
    {"initial_mmhg": 760, "final_mmhg": 190},
    {"initial_mmhg": 1000, "final_mmhg": 400},
]
ANSWER = Fraction(2, 7)
