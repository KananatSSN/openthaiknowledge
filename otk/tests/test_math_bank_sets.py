"""The เซต sets built from the sheet bank's knowledge units.

Every counting solver sees only the numbers a stem states. Each is checked
against brute force over Venn-region counts: every assignment of counts to
the regions, pushed through the solver, must come back as the hidden value.
Truth for the "always true" set is checked on a bigger universe than the one
it uses. The source exams' printed answers are pinned.
"""

from __future__ import annotations

import itertools
import random

import pytest

from otk.core import REGISTRY, generate
from otk.sets.math.m4 import sets as ms

KEYS = ("math.set_expression_eval_m4", "math.set_expression_match_m4",
        "math.set_always_true_m4", "math.set_two_set_word_m4", "math.set_exactly_k_m4",
        "math.set_region_algebra_m4", "math.set_multiples_count_m4", "math.set_extremal_m4")
SMALL = range(0, 5)


# ── Solvers vs brute force over Venn regions ─────────────────────────────────

def test_two_set_solvers():
    for a_only, both, b_only, neither in itertools.product(SMALL, repeat=4):
        n_a, n_b = a_only + both, b_only + both
        union = a_only + both + b_only
        total = union + neither
        assert ms.solve_b_from_only_a(total, a_only, neither) == n_b
        assert ms.solve_b_from_difference(union, both, n_a - n_b) == n_b
        assert ms.solve_both(total, n_a, n_b, neither) == both
        if a_only == b_only:
            assert ms.solve_only_when_equal(union, both) == a_only


def test_three_set_solvers():
    for regions in itertools.product(range(3), repeat=7):
        a, b, c, ab, bc, ac, abc = regions
        for neither in (0, 2):
            n = [a + ab + ac + abc, b + ab + bc + abc, c + bc + ac + abc]
            e1, e2 = a + b + c, ab + bc + ac
            total = sum(regions) + neither
            assert ms.solve_exactly_two(total, neither, n, abc) == e2
            assert ms.solve_exactly_one(total, neither, n, abc) == e1
            assert ms.solve_third_set(total, neither, e2, abc, n[0], n[1]) == n[2]
            assert ms.solve_all_three(total, neither, a + ac, b + ab, c + bc) == abc


@pytest.mark.parametrize("n", (50, 60, 80, 100, 120, 150, 200))
def test_multiples(n):
    for a, b in itertools.permutations((2, 3, 4, 5, 6, 7), 2):
        xs = range(1, n + 1)
        assert ms.count_either(n, a, b) == sum(1 for x in xs if x % a == 0 or x % b == 0)
        assert ms.count_only_first(n, a, b) == sum(1 for x in xs if x % a == 0 and x % b)
        assert ms.count_either_not_both(n, a, b) == sum(
            1 for x in xs if (x % a == 0) != (x % b == 0))


def test_extremes():
    for n_u, both, neither, a_min in itertools.product((20, 30), (3, 6), (1, 4), (8, 12, 15)):
        best = max((n_u - neither - both - a_only) + both
                   for a_only in range(n_u + 1)
                   if n_u - neither - both - a_only >= 0 and a_only + both >= a_min)
        assert ms.max_b(n_u, both, neither, a_min) == best
    for total, only_z, both, y_max in itertools.product((40, 50), (10, 15), (3, 5), (10, 14)):
        rest = total - only_z
        best = min(x_only + both for x_only in range(rest + 1)
                   if 0 <= rest - both - x_only and rest - x_only <= y_max)
        assert ms.min_x(total, only_z, both, y_max) == best


def test_three_elements_decide_always_true():
    # A four-element universe gives the same verdicts as the three-element one.
    world4 = [frozenset(s) for r in range(5) for s in itertools.combinations(range(4), r)]

    def always4(premise, conclusion):
        ws = [(A, B, C) for A in world4 for B in world4 for C in world4
              if A and B and C and premise(A, B, C)]
        return bool(ws) and all(conclusion(*w) for w in ws)

    for _, p in ms._PREMISES:
        for _, c in ms._CONCLUSIONS:
            assert ms.always(p, c) == always4(p, c)


# ── The exam questions the units came from ───────────────────────────────────

def test_exam_answers_reproduce():
    # O-NET (มี.ค. 2561/31): n(B ∩ (A ∪ C)) = 4
    A, B, C = {2, "a", "d"}, {2, 3, "b", "c", "d"}, {3, "b"}
    assert len(ms.evaluate(r"B \cap (A \cup C)", A, B, C, A | B | C)) == 4
    assert ms.solve_b_from_only_a(50, 8, 12) == 30            # O-NET (มี.ค. 2564/25)
    assert ms.solve_b_from_difference(166, 74, 12) == 114      # กสพท คณิต2 (มี.ค. 2565/2)
    assert ms.solve_only_when_equal(168, 48) == 60             # A-level 2 (มี.ค. 2566/28)
    assert ms.solve_both(40, 25, 9, 12) == 6                   # กสพท คณิต2 (มี.ค. 2563/17)
    assert ms.solve_exactly_two(46, 0, [37, 13, 19], 3) == 17  # O-NET (ก.พ. 2565/5)
    assert ms.solve_exactly_two(300, 120, [38, 155, 62], 13) == 49   # กสพท คณิต2 (มี.ค. 2562/17)
    assert ms.solve_third_set(50, 7, 22, 5, 30, 25) == 20      # กสพท คณิต2 (ธ.ค. 2558/18)
    assert ms.solve_all_three(800, 20, 230, 270, 200) == 80    # O-NET (ก.พ. 2563/35)
    assert ms.count_either_not_both(100, 2, 5) == 50           # กสพท คณิต2 (ธ.ค. 2558/17)
    assert ms.count_only_first(50, 2, 3) == 17                 # O-NET (ก.พ. 2565/4)
    assert ms.max_b(100, 35, 9, 61) == 65                      # A-level 1 (มี.ค. 2566/26)
    assert ms.min_x(500, 220, 90, 100) == 270                  # กสพท คณิต2 (ธ.ค. 2559/18)


# ── The generated items ──────────────────────────────────────────────────────

@pytest.mark.parametrize("key", KEYS)
def test_items_offer_full_distinct_choices_and_are_reproducible(key):
    want = REGISTRY[key].max_choices
    assert REGISTRY[key].topic == "เซต" and want in (3, 4)
    for seed in range(120):
        q = generate(key, rng=random.Random(seed))
        texts = [c.model_dump_json() for c in q.choices]
        assert len(texts) == want and len(set(texts)) == want, (key, seed)
        assert q.model_dump_json() == generate(key, rng=random.Random(seed)).model_dump_json()
