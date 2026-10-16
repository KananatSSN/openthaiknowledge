"""Check password endings independently from prefix omissions."""

from itertools import combinations
from random import Random

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.descending_password_suffix import (
    mistaken_suffixes,
    possible_suffixes,
)


def _brute_suffixes(target: int) -> set[str]:
    result = set()
    digits = set(range(10))
    for omitted_odd in (1, 3, 5, 7, 9):
        first_four = sorted({1, 3, 5, 7, 9} - {omitted_odd}, reverse=True)
        for even_middle in combinations((0, 2, 4, 6, 8), 3):
            middle = sorted(even_middle, reverse=True)
            last_three = sorted(digits - set(first_four) - set(middle), reverse=True)
            full_code = first_four + middle + last_three
            if sum(last_three) == target:
                result.add("".join(map(str, full_code[-5:])))
    return result


def test_suffixes_and_named_mistakes():
    for target in range(5, 22, 2):
        expected = _brute_suffixes(target)
        assert possible_suffixes(target) == expected
        for valid in expected:
            distractors = mistaken_suffixes(valid)
            assert len(distractors) == len(set(distractors)) == 4
            assert all(wrong not in expected for wrong in distractors)


def test_checked_source_case():
    assert sorted(possible_suffixes(15)) == [
        "20654", "20843", "20861", "40762", "40852", "42870", "42960", "60942",
    ]


def test_generated_draws():
    key = "math.descending_password_suffix_olympiad"
    for seed in range(100):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
