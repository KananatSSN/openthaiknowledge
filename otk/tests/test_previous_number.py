"""``math.previous_number`` must say which number to count back from."""

from __future__ import annotations

from random import Random

from otk.core import generate


def _parts(blocks) -> list[str]:
    return [getattr(block, "text", getattr(block, "tex", "")) for block in blocks]


def test_the_stem_shows_the_number_and_the_answer_is_one_less():
    for seed in range(500):
        question = generate("math.previous_number", Random(seed))
        stem = _parts(question.stem)
        numbers = [part for part in stem if part.isdigit()]
        assert len(numbers) == 1, (seed, stem)
        choices = [" ".join(_parts(choice.content)) for choice in question.choices]
        assert choices[question.answer] == str(int(numbers[0]) - 1), (seed, stem, choices)


def test_no_choice_is_negative():
    for seed in range(500):
        question = generate("math.previous_number", Random(seed), lo=1, hi=1)
        choices = [" ".join(_parts(choice.content)) for choice in question.choices]
        assert len(set(choices)) == 4, (seed, choices)
        assert not any(choice.lstrip().startswith("-") for choice in choices), choices
