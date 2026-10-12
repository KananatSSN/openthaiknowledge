"""Named mistakes: the ledger, the assembler's labelling, and the labelled sets.

The per-set test checks every set's labels line up and never sit on the answer.
This file checks the mechanism itself, and that each labelled set's names reach
its choices: a value named as an int but shown with a unit, say, would match no
choice and silently label nothing.
"""

from __future__ import annotations

from random import Random

import pytest

import otk.sets  # noqa: F401  registers every type
from otk.core import mistakes
from otk.core.content import math as content_math, text
from otk.core.mistakes import MISTAKES, label_for, named, recording
from otk.core.registry import REGISTRY

# The sets that name their mistakes. Grow this as sets are labelled; the test
# below holds each one to "every mistake it names is seen on a choice".
LABELLED = (
    "math.fraction_of_amount_p5",
    "math.fraction_word_addsub_p5",
    "math.fraction_word_muldiv_p5",
    "math.decimal_multiply_p5",
    "math.decimal_divide_p5",
    "math.fraction_to_decimal_p5",
    "math.decimal_word_problem_p5",
    "math.unit_price_p5",
    "math.rate_word_problem_p5",
    "math.recipe_scaling_p5",
    "math.percent_of_quantity_p5",
    "math.find_percent_p5",
    "math.percent_two_step_p5",
    "math.volume_capacity_p5",
    "math.cube_units_p5",
    "math.rhombus_kite_area_p5",
)
DRAWS = 200


def test_named_returns_the_value_and_rejects_unknown_keys():
    value = [content_math("3")]
    assert named("proportion.no_divide", 12) == 12
    assert named("proportion.no_divide", value) is value
    with pytest.raises(KeyError):
        named("proportion.not_a_mistake", 12)


def test_named_records_only_inside_a_recording():
    named("proportion.no_divide", 12)  # outside: a no-op
    with recording() as ledger:
        named("proportion.no_divide", 12)
        named("proportion.unit_rate_only", 12)  # the first naming of a value wins
        named("fraction.add_across", [text("ห้า")])
    assert label_for(ledger, [content_math("12")]) == "proportion.no_divide"
    assert label_for(ledger, [text("12")]) == "proportion.no_divide"
    assert label_for(ledger, [text("ห้า")]) == "fraction.add_across"
    assert label_for(ledger, [content_math("13")]) is None
    assert label_for(ledger, [content_math("12"), text("บาท")]) is None


def test_every_mistake_has_both_names():
    for key, names in MISTAKES.items():
        assert set(names) == {"th", "en"} and all(names.values()), key
        assert key == key.lower() and "." in key, key
    assert mistakes.mistake_names() == {key: MISTAKES[key] for key in sorted(MISTAKES)}


@pytest.mark.parametrize("key", LABELLED)
def test_a_labelled_set_shows_every_mistake_it_names(key):
    question_type = REGISTRY[key]
    named_keys: set[str] = set()
    seen: set[str] = set()
    for seed in range(DRAWS):
        with recording() as ledger:
            question_type.build(Random(seed))
        named_keys.update(ledger.values())
        question = question_type.generate(Random(seed))
        seen.update(label for label in question.mistakes if label)
    assert named_keys, f"{key} names no mistakes; remove it from LABELLED"
    assert named_keys <= seen, f"{key} names {sorted(named_keys - seen)} but no choice shows them"


def test_labelling_never_changes_a_draw():
    # The assembler labels after the shuffle without touching the generator, so a
    # labelled set's public question is the same draw it always was.
    for key in LABELLED:
        first = REGISTRY[key].generate(Random(7))
        again = REGISTRY[key].generate(Random(7))
        assert first.model_dump() == again.model_dump()
        assert first.mistakes == again.mistakes


def test_sibling_draws_do_not_label_this_question():
    # WordProblem fills spare choices with sibling draws' answers, which calls the
    # type again; their named mistakes are not this question's. Each choice of a
    # draw is distinct, so no mistake can label two of them.
    for seed in range(DRAWS):
        question = REGISTRY["math.rate_word_problem_p5"].generate(Random(seed))
        labels = [label for label in question.mistakes if label]
        assert len(labels) == len(set(labels)), (seed, question.mistakes)
