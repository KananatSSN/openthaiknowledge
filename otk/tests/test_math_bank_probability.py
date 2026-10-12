"""The probability sets built from the sheet bank's knowledge units.

Every solver in ``math_bank_probability`` is checked against brute-force
enumeration of the experiment it models, over the whole parameter range the
generators draw from. The exam questions the units came from are pinned as
spot checks with their printed answers.
"""

from __future__ import annotations

import itertools
import math
import random
from fractions import Fraction

import pytest

from otk.core import REGISTRY, generate
from otk.sets.math.m5 import probability as mb
from otk.sets._support.math_bank_probability import brute_digits, brute_routes

KEYS = ("math.probability_union_m5", "math.probability_two_way_table_m5",
        "math.probability_without_replacement_m5", "math.probability_digit_numbers_m5",
        "math.probability_random_arrangement_m5", "math.probability_grid_route_m5")


# ── Solvers vs brute force ───────────────────────────────────────────────────

@pytest.mark.parametrize("n", (20, 24, 25, 30, 36, 40, 50, 60))
def test_divisible_either(n):
    for a, b in itertools.permutations((2, 3, 4, 5, 6, 7), 2):
        brute = Fraction(sum(1 for k in range(1, n + 1) if k % a == 0 or k % b == 0), n)
        assert mb.divisible_either(n, a, b) == brute


def test_draw_sequence_matches_enumeration():
    counts = {"r": 3, "w": 2, "b": 4}
    balls = [c for c, k in counts.items() for _ in range(k)]
    orders = list(itertools.permutations(range(len(balls)), 3))
    for seq in itertools.product(counts, repeat=3):
        if any(seq.count(c) > counts[c] for c in counts):
            continue
        hits = sum(1 for o in orders if [balls[i] for i in o] == list(seq))
        assert mb.draw_sequence(counts, list(seq)) == Fraction(hits, len(orders))


@pytest.mark.parametrize("digits", (2, 3))
@pytest.mark.parametrize("condition", ("all_odd", "even_product", "has_k", "distinct"))
def test_digit_probability(digits, condition):
    for k in range(1, 10):
        assert mb.digit_probability(digits, condition, k) == brute_digits(digits, condition, k)


@pytest.mark.parametrize("n", range(1, 8))
def test_derangements(n):
    brute = sum(1 for p in itertools.permutations(range(n)) if all(p[i] != i for i in range(n)))
    assert mb.derangements(n) == brute


@pytest.mark.parametrize("a,b", [(2, 2), (2, 3), (3, 4), (4, 4)])
def test_grouped_together(a, b):
    row = ["x"] * a + ["y"] * b
    perms = list(itertools.permutations(range(a + b)))
    good = sum(1 for p in perms
               if sum(1 for i in range(1, a + b) if row[p[i]] != row[p[i - 1]]) == 1)
    assert mb.grouped_together(a, b) == Fraction(good, len(perms))


def test_route_through():
    for m in range(2, 6):
        for n in range(2, 5):
            for p in range(m + 1):
                for q in range(n + 1):
                    assert mb.route_through(m, n, p, q) == brute_routes(m, n, p, q)


# ── The exam questions the units came from ───────────────────────────────────

def test_exam_answers_reproduce():
    # O-NET (ก.พ. 2560/40): 1–25 divisible by 2 or 5 → 0.60
    assert mb.divisible_either(25, 2, 5) == Fraction(3, 5)
    # กสพท คณิต2 (ธ.ค. 2559/30): 100–999, product of digits even → 31/36
    assert mb.digit_probability(3, "even_product") == Fraction(31, 36)
    # A-level 2 (มี.ค. 2567/13): 4 phones, nobody gets their own → 3/8
    assert Fraction(mb.derangements(4), 24) == Fraction(3, 8)
    # O-NET (ก.พ. 2565/19): 4 plates, 3 bowls, kinds together → 2/35
    assert mb.grouped_together(4, 3) == Fraction(2, 35)
    # กสพท คณิต2 (มี.ค. 2562/10): 6 white, 7 red, 8 blue; two blue without replacement → 2/15
    assert mb.draw_sequence({"w": 6, "r": 7, "b": 8}, ["b", "b"]) == Fraction(2, 15)
    # กสพท คณิต2 (มี.ค. 2561/28): three dice all different → 5/9
    assert Fraction(math.perm(6, 3), 6 ** 3) == Fraction(5, 9)


# ── The generated items ──────────────────────────────────────────────────────

@pytest.mark.parametrize("key", KEYS)
def test_items_offer_full_distinct_choices_and_are_reproducible(key):
    # Foundation-stage sets offer three choices, the rest four (max_choices).
    want = REGISTRY[key].max_choices
    assert REGISTRY[key].topic == "ความน่าจะเป็น" and want in (3, 4)
    for seed in range(80):
        q = generate(key, rng=random.Random(seed))
        texts = [c.model_dump_json() for c in q.choices]
        assert len(texts) == want and len(set(texts)) == want, (key, seed)
        assert q.model_dump_json() == generate(key, rng=random.Random(seed)).model_dump_json()


def _value(choice) -> Fraction:
    tex = choice.content[0].tex
    if tex.startswith(r"\frac"):
        num, den = tex[6:-1].split("}{")
        return Fraction(int(num), int(den))
    return Fraction(tex)


@pytest.mark.parametrize("key", KEYS)
def test_every_choice_is_a_probability(key):
    for seed in range(80):
        q = generate(key, rng=random.Random(seed))
        for c in q.choices:
            assert 0 < _value(c) <= 1, (key, seed, c)
