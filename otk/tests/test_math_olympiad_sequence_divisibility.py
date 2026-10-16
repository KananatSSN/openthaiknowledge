"""Check recurrence-period counts against direct modular iteration."""

from random import Random

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.sequence_divisibility import divisible_terms_through


def test_period_count_matches_direct_modular_iteration():
    for exponent in (2, 3):
        value = 1
        for index in range(2, 7):
            value = value**exponent + 1
            residue = 1 % value
            hits = 0
            for q in range(1, 31):
                if q > 1:
                    residue = (residue**exponent + 1) % value
                hits += residue == 0
                assert hits == divisible_terms_through(index, q)


def test_generated_choices_are_distinct_and_reproducible():
    key = "math.recurrence_divisibility_olympiad"
    for seed in range(100):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices
        assert len(choices) == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
