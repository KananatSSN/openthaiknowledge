"""Source p16, written 3: after 75% of 50 g I-131 decays, 12.5 g remains at 16.2 d."""

from math import log2


def solve(half_life_days=8.1, initial_g=50.0, decayed_percent=75.0):
    remaining_fraction = 1 - decayed_percent / 100
    assert 0 < remaining_fraction <= 1
    elapsed_days = half_life_days * log2(1 / remaining_fraction)
    return round(elapsed_days, 1), round(initial_g * remaining_fraction, 1)


def check(half_life_days=8.1, initial_g=50.0, decayed_percent=75.0):
    # Repeatedly halve the initial mass until the stated decay fraction is met.
    target_g = initial_g * (100 - decayed_percent) / 100
    remaining_g = initial_g
    periods = 0
    while remaining_g > target_g + 1e-9:
        remaining_g /= 2
        periods += 1
    assert abs(remaining_g - target_g) < 1e-9
    return round(periods * half_life_days, 1), round(remaining_g, 1)


PARAMS = {"half_life_days": 8.1, "initial_g": 50.0, "decayed_percent": 75.0}
VARIANTS = [
    {"half_life_days": 8.1, "initial_g": 100.0, "decayed_percent": 75.0},
    {"half_life_days": 4.5, "initial_g": 40.0, "decayed_percent": 87.5},
    {"half_life_days": 6.0, "initial_g": 72.0, "decayed_percent": 93.75},
]
ANSWER = (16.2, 12.5)
