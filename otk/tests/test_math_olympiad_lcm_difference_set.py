"""Exhaustively check small sets satisfying the LCM quotient rule."""

from itertools import combinations
from math import lcm
from random import Random

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.lcm_difference_set import (
    largest_lcm_difference_member,
)


def _closed(members: set[int]) -> bool:
    for smaller, larger in combinations(sorted(members), 2):
        quotient, remainder = divmod(lcm(smaller, larger), larger - smaller)
        if remainder or quotient not in members:
            return False
    return True


def test_exhaustive_small_sets_and_extrema():
    for minimum in range(1, 37):
        possible = [minimum + gap for gap in range(1, minimum + 1) if minimum % gap == 0]
        closed = []
        for mask in range(1, 1 << len(possible)):
            members = {minimum}
            members.update(value for bit, value in enumerate(possible) if mask & (1 << bit))
            if _closed(members):
                closed.append(members)
        assert all(len(members) == 2 for members in closed)
        expected = {
            largest_lcm_difference_member(index, False)
            for index in range(2, 7)
            if index * index == minimum
        } | {
            largest_lcm_difference_member(index, True)
            for index in range(2, 6)
            if index * (index + 1) == minimum
        }
        if minimum in (1, 2):
            assert closed  # the same classification also works at index 1
        else:
            assert {max(members) for members in closed} == expected


def test_generated_draws():
    key = "math.lcm_difference_set_olympiad"
    for seed in range(100):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
