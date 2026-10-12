"""The correct number's sorted position must not give the answer away.

See docs/for_admin/MCQ_GUESSABILITY.md (workstream 1).
"""

from __future__ import annotations

from collections import Counter
from random import Random

import pytest

from otk.core import generate, math, text
from otk.core.distractors import _plain_number, fixed, rank_balanced


def _rank_share(key: str, draws: int = 120) -> float:
    ranks: Counter = Counter()
    for seed in range(draws):
        q = generate(key, Random(seed))
        numbers = [_plain_number(c.content) for c in q.choices]
        if None in numbers:
            continue                      # a set may mix in non-numeric shapes
        order = sorted(range(len(numbers)), key=lambda i: numbers[i][0])
        ranks[order.index(q.answer)] += 1
    assert sum(ranks.values()) >= 30, key
    return max(ranks.values()) / sum(ranks.values())


# Each was always the same rank before rank balancing (smallest, second
# smallest, or third) because every listed mistake erred the same way.
@pytest.mark.parametrize("key", [
    "math.subtract_within_20_p1",
    "math.division_word_problem_p2",
    "math.multiplication_word_problem_p2",
    "math.polygon_sides",
    "math.subtract_word_p1",
    "phys.shm_foundation",
])
def test_numeric_answer_rank_is_not_a_cue(key):
    assert _rank_share(key) < 0.6


def test_first_listed_mistake_is_always_offered():
    strategy = rank_balanced(fixed(*[[math(str(v))] for v in (23, 13, 8, 6, 5)]))
    for seed in range(50):
        chosen = strategy([math("7")], Random(seed), 3)
        assert chosen[0][0].tex == "23"
        assert len(chosen) == 3


def test_invented_values_keep_the_unit_and_stay_non_negative():
    strategy = rank_balanced(fixed([text("20 cm")]), invent=True)
    for seed in range(50):
        chosen = strategy([text("1 cm")], Random(seed), 3)
        assert all(c[0].text.endswith(" cm") for c in chosen)
        assert all(float(c[0].text.split()[0]) >= 0 for c in chosen)


def test_non_numeric_choices_pass_through():
    pool = [[text("ไนโตรเจน")], [text("ออกซิเจน")], [text("ฮีเลียม")]]
    chosen = rank_balanced(fixed(*pool))([text("ไฮโดรเจน")], Random(0), 3)
    assert chosen == pool
