"""Check conditional switch passes by set algebra on the switch numbers."""

from itertools import permutations
from random import Random

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.conditional_switch_passes import switches_on


def _set_count(total: int, first: int, second: int, third: int) -> int:
    """Pass 1 adds every multiple of the first divisor to the on set, pass 2 removes
    every multiple of the second, pass 3 adds every multiple of the third."""
    multiples = lambda divisor: set(range(divisor, total + 1, divisor))
    on = set(range(1, total // 2 + 1))
    on = ((on | multiples(first)) - multiples(second)) | multiples(third)
    return len(on)


def test_matches_set_algebra():
    for total in range(20, 102, 2):
        for first, second, third in permutations(range(2, 7), 3):
            assert switches_on(total, first, second, third) == _set_count(total, first, second, third)


def test_checked_source_case():
    # สอวน. ค่าย 1 2569 ข้อ 29: เปิด (หาร 2) ปิด (หาร 3) เปิด (หาร 4) เฉพาะสวิตช์ในสถานะตรงข้าม
    assert switches_on(2026, 2, 3, 4) == _set_count(2026, 2, 3, 4) == 1182


def test_generated_draws():
    key = "math.conditional_switch_passes_olympiad"
    for seed in range(100):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
