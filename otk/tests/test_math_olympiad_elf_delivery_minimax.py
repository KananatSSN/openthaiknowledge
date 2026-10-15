"""Exhaustively check the minimum maximum delivery time on small instances."""

from itertools import permutations
from random import Random

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.elf_delivery_minimax import minimum_elf_delivery_time


def test_assignment_enumeration_and_source_case():
    for houses in range(1, 9):
        brute = min(
            max(elf * distance for elf, distance in enumerate(assignment, 1))
            for assignment in permutations(range(1, houses + 1))
        )
        assert brute == minimum_elf_delivery_time(houses)
    assert minimum_elf_delivery_time(63) == 1024
    assert max(elf * (64 - elf) for elf in range(1, 64)) == 1024


def test_generated_draws():
    key = "math.elf_delivery_minimax_olympiad"
    for seed in range(100):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
