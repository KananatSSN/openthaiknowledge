"""Check the diagonal-area invariant independently from sampled sides."""

from random import Random

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.equiangular_hexagon_diagonals import pair_product_square


def test_matches_direct_side_products():
    for a in range(2, 12):
        for b in range(2, 12):
            for c in range(2, 12):
                ac_sq = a * a + a * b + b * b
                ce_sq = a * a + a * c + c * c
                ea_sq = b * b + b * c + c * c
                assert pair_product_square(ac_sq, ce_sq, ea_sq) == (a * b + b * c + c * a) ** 2


def test_checked_source_case():
    assert pair_product_square(15**2, 17**2, 8**2) == 19200
    assert 15**2 + 8**2 == 17**2
    assert 16 * 60**2 // 3 == 19200


def test_generated_draws():
    key = "math.equiangular_hexagon_diagonals_olympiad"
    for seed in range(100):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
