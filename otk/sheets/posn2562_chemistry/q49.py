"""Pyrite supplies two SO2 molecules per FeS2 unit."""


def solve(sample_g=480, pyrite_percent=5):
    return round(sample_g * pyrite_percent / 100 / 120 * 2 * 64, 2)


def check(sample_g=480, pyrite_percent=5):
    # 4FeS2 + 11O2 -> 2Fe2O3 + 8SO2; mass ratio 8*64/(4*120).
    return round(sample_g * (pyrite_percent / 100) * (8 * 64) / (4 * 120), 2)


PARAMS = {"sample_g": 480, "pyrite_percent": 5}
VARIANTS = [
    {"sample_g": 600, "pyrite_percent": 4},
    {"sample_g": 600, "pyrite_percent": 10},
    {"sample_g": 300, "pyrite_percent": 8},
]

ANSWER = solve(**PARAMS)
