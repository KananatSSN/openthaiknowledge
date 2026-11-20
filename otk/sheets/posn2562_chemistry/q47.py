"""O2 limits ammonia oxidation; measured NO gives percent yield."""


def solve(nh3_g=85, o2_g=96, no_g=54):
    theoretical = min(nh3_g / 17, o2_g / 32 * 4 / 5) * 30
    return round(no_g / theoretical * 100)


def check(nh3_g=85, o2_g=96, no_g=54):
    extent = min(nh3_g / (4 * 17), o2_g / (5 * 32))
    no_possible = 4 * extent * 30
    return round(100 * no_g / no_possible)


PARAMS = {"nh3_g": 85, "o2_g": 96, "no_g": 54}
VARIANTS = [
    {"nh3_g": 85, "o2_g": 96, "no_g": 36},
    {"nh3_g": 85, "o2_g": 96, "no_g": 43.2},
    {"nh3_g": 85, "o2_g": 96, "no_g": 72},
]
ANSWER = solve(**PARAMS)
