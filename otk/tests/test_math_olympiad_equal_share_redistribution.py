"""Check two-observation redistribution against direct sharing arithmetic."""

from math import gcd, lcm
from random import Random

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.equal_share_redistribution import original_population


def test_generated_parameter_grid():
    for ratio in range(4, 9):
        for added in range(2, 7):
            for scale in range(1, 4):
                cages = ratio * added
                each = lcm(ratio + 1, (ratio + 2) // gcd(2, ratio + 2)) * scale
                total = cages * each
                assert total % (cages + added) == total % (cages + 2 * added) == 0
                drop_a = each - total // (cages + added)
                drop_b = each - total // (cages + 2 * added)
                assert original_population(added, drop_a, 2 * added, drop_b) == (cages, each, total)


def test_checked_source_case():
    assert original_population(4, 8, 8, 14) == (24, 56, 1344)
    assert 24 * 56 == 28 * 48 == 32 * 42


def test_generated_draws():
    key = "math.equal_share_redistribution_olympiad"
    for seed in range(100):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
