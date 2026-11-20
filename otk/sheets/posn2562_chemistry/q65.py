"""128 to 2 mg in 12 months is six halvings: 2 months, 0.25 mg at 18 months."""


def solve(start_mg=128, after_12_mg=2):
    from math import log2

    halvings = log2(start_mg / after_12_mg)
    half_life_months = 12 / halvings
    after_18 = start_mg * 0.5 ** (18 / half_life_months)
    return (round(half_life_months, 2), round(after_18, 3))


def check(start_mg=128, after_12_mg=2):
    for half_life in (1, 1.5, 2, 3, 4, 6):
        if abs(start_mg * (0.5 ** (12 / half_life)) - after_12_mg) < 1e-8:
            return (half_life, round(start_mg * (0.5 ** (18 / half_life)), 3))
    raise ValueError("no half-life found")


PARAMS = {"start_mg": 128, "after_12_mg": 2}
VARIANTS = [
    {"start_mg": 256, "after_12_mg": 4},
    {"start_mg": 64, "after_12_mg": 1},
    {"start_mg": 128, "after_12_mg": 8},
]

ANSWER = solve(**PARAMS)
