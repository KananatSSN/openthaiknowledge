"""Check code counts by enumerating complete small-alphabet strings."""

from itertools import product
from random import Random

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.leading_digit_passwords import count_leading_digit_codes


def _direct_count(letters: int, pool: int, digits: int) -> int:
    alphabet = [*(f"L{i}" for i in range(pool)), *(f"D{i}" for i in range(digits))]
    count = 0
    for code in product(alphabet, repeat=letters + 2):
        digit_positions = [i for i, symbol in enumerate(code) if symbol.startswith("D")]
        if len(digit_positions) != 2 or digit_positions[0] != 0:
            continue
        if digit_positions[1] == 1:
            continue
        used_letters = [symbol for symbol in code if symbol.startswith("L")]
        count += len(set(used_letters)) == letters
    return count


def test_matches_direct_strings():
    for letters in range(2, 5):
        for pool in range(letters, min(5, letters + 1) + 1):
            for digits in range(1, 4):
                assert count_leading_digit_codes(letters, pool, digits) == _direct_count(letters, pool, digits)


def test_checked_source_case_and_repeated_digits():
    assert count_leading_digit_codes(4, 5, 10) == 48000
    assert count_leading_digit_codes(2, 2, 1) == 4


def test_generated_draws():
    key = "math.leading_digit_nonadjacent_codes_olympiad"
    for seed in range(100):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
