"""Spare choices borrowed from sibling draws keep to the draw's own story.

A type that mixes several stories can mark each draw's ``MathDraw.variant``;
spare choices then come only from siblings of the same variant, so a cube's
volume is never offered the answer of a cubic-metre conversion.
"""

from __future__ import annotations

from random import Random

import otk.sets  # noqa: F401  registers every type
from otk.core.registry import REGISTRY
from otk.kit.math_problems import MathDraw, WordProblem


def _value(choice) -> float:
    return float(" ".join(b.tex for b in choice.content).replace("{,}", "").replace(",", ""))


def test_a_cube_volume_never_borrows_a_conversion_answer():
    question_type = REGISTRY["math.cube_units_p5"]
    for seed in range(400):
        question = question_type.generate(Random(seed))
        stem = " ".join(getattr(block, "text", "") for block in question.stem)
        if "ลูกบาศก์เมตร" in stem:
            continue  # the conversion story, whose answers are millions
        # The volume stories go up to 12 cm a side: nothing near a million.
        assert all(_value(c) < 100_000 for c in question.choices), (seed, stem)


class _TwoStories(WordProblem):
    """Draws alternate between a story answered in units and one in millions."""

    key = "test.two_stories"
    topic = "test"

    def expr(self, rng: Random):
        n = rng.randint(2, 9)
        if rng.random() < 0.5:
            return MathDraw("", str(n), prompt="units", variant="units")
        return MathDraw("", str(n * 1_000_000), prompt="millions", variant="millions")


class _OneStoryOnly(WordProblem):
    """Every sibling is of another variant, so none can ever be borrowed."""

    key = "test.lonely"
    topic = "test"
    _first = True

    def expr(self, rng: Random):
        if self._first:
            self._first = False
            return MathDraw("", "7", prompt="first", variant="first")
        return MathDraw("", "7000000", prompt="other", variant="other")


def test_spare_choices_come_only_from_the_same_variant():
    question_type = _TwoStories()
    for seed in range(200):
        question = question_type.generate(Random(seed))
        values = [_value(c) for c in question.choices]
        answer = values[question.answer]
        assert all((v >= 100_000) == (answer >= 100_000) for v in values), (seed, values)


def test_without_a_same_variant_sibling_other_fillers_complete_the_choices():
    question = _OneStoryOnly().generate(Random(1))
    assert len(question.choices) >= 3
    assert all(_value(c) < 100 for c in question.choices), [_value(c) for c in question.choices]
