"""Source p11, MC41: O2 takes 48 s where H2 takes 12 s (ง)."""

from math import sqrt


def solve(first_molar=2, second_molar=32, first_seconds=12):
    return round(first_seconds * sqrt(second_molar / first_molar), 1)


def check(first_molar=2, second_molar=32, first_seconds=12):
    # Graham's law: effusion rate is inverse to sqrt(M). Equal sample
    # amounts take time inversely proportional to their rates.
    first_rate = 1 / sqrt(first_molar)
    second_rate = 1 / sqrt(second_molar)
    return round(first_seconds * first_rate / second_rate, 1)


PARAMS = {"first_molar": 2, "second_molar": 32, "first_seconds": 12}
VARIANTS = [
    {"first_molar": 4, "second_molar": 16, "first_seconds": 10},
    {"first_molar": 2, "second_molar": 16, "first_seconds": 15},
    {"first_molar": 28, "second_molar": 32, "first_seconds": 12},
]
ANSWER = 48.0
