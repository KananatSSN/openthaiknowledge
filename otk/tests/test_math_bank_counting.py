"""The counting sets built from the sheet bank's knowledge units.

Every closed form is recounted by brute-force enumeration over small cases,
and the source exams' answers are pinned.
"""

from __future__ import annotations

import random
from itertools import combinations, permutations, product
from math import factorial

import pytest

from otk.core import REGISTRY, generate
from otk.sets.math.m5 import counting_principles as mc
from otk.sets._support.math_bank_counting import one_extra_surjection, path_edges
from otk.sets.math.m5.permutations import alternating, blocks, no_two_adjacent_seats
from otk.sets.math.m5.combinations import multinomial, two_baskets

KEYS = ("math.counting_complement_m5", "math.coloring_regions_m5", "math.arrangement_blocks_gaps_m5",
        "math.distribute_to_groups_m5")


def test_at_least_one():
    for d in range(2, 6):
        for n in range(1, 5):
            brute = sum(1 in s for s in product(range(1, d + 1), repeat=n))
            assert mc.at_least_one(d, n) == brute


def test_above_power_of_ten():
    for b in range(2, 5):
        for n in range(2, 5):
            # The digit strings are read as ordinary (decimal) numbers, as in the stem.
            brute = sum(1 for s in product(range(b), repeat=n)
                        if s[0] and int("".join(map(str, s))) > int("1" + "0" * (n - 1)))
            assert mc.above_power_of_ten(b, n) == brute, (b, n)


def _proper(edges, n, k):
    return sum(all(c[i] != c[j] for i, j in edges) for c in product(range(k), repeat=n))


def test_colourings():
    for k in range(2, 7):
        for n in range(2, 6):
            assert mc.colourings("path", k, n) == _proper(path_edges(n), n, k)
        for name, (_, edges, _) in mc.LAYOUTS.items():
            if edges:
                assert mc.colourings(name, k) == _proper(edges, 4, k), (name, k)


def test_blocks():
    for sizes in ([2, 2], [2, 3], [1, 2, 2], [2, 2, 2], [3, 2]):
        labels = [g for g, s in enumerate(sizes) for _ in range(s)]
        items = list(range(len(labels)))
        brute = 0
        for order in permutations(items):
            groups = [labels[i] for i in order]
            runs = [g for i, g in enumerate(groups) if i == 0 or g != groups[i - 1]]
            brute += len(runs) == len(sizes)
        assert blocks(sizes) == brute, sizes


def test_alternating():
    for a in range(1, 4):
        for b in range(1, 5):
            labels = [0] * a + [1] * b
            brute = sum(all(labels[o[i]] != labels[o[i + 1]] for i in range(a + b - 1))
                        for o in permutations(range(a + b)))
            assert alternating(a, b) == brute, (a, b)


def test_no_two_adjacent_seats():
    for n in range(3, 10):
        for p in range(1, 5):
            brute = sum(all(s[i + 1] - s[i] > 1 for i in range(p - 1)) for s in combinations(range(n), p))
            assert no_two_adjacent_seats(n, p) == brute * factorial(p)


def test_distributions():
    for sizes in ([2, 2], [2, 2, 2], [1, 2, 3], [3, 3]):
        n = sum(sizes)
        brute = sum(all(a.count(g) == s for g, s in enumerate(sizes)) for a in product(range(len(sizes)), repeat=n))
        assert multinomial(sizes) == brute
    for n in range(4, 8):
        for a in range(1, 3):
            for b in range(1, n - a):
                brute = sum(a_.count(1) == a and a_.count(2) == b for a_ in product(range(3), repeat=n))
                assert two_baskets(n, a, b) == brute
    for n in range(2, 6):
        brute = sum(len(set(f)) == n for f in product(range(n), repeat=n + 1))
        assert one_extra_surjection(n) == brute


def test_exam_answers_reproduce():
    assert mc.at_least_one(4, 4) == 175                    # กสพท คณิต2 (มี.ค. 2563/29)
    assert mc.at_least_one(9, 3) == 217                    # กสพท คณิต2 (มี.ค. 2562/30)
    assert mc.at_least_one(4, 5) == 781                    # กสพท คณิต2 (ธ.ค. 2558/25)
    assert mc.above_power_of_ten(2, 5) == 15               # กสพท คณิต2 (มี.ค. 2561/29)
    assert mc.colourings("path", 3, 5) == 48               # A-level 2 (มี.ค. 2566/13)
    assert mc.colourings("triangle_plus", 5) == 180        # A-level 2 (มี.ค. 2567/10)
    assert mc.colourings("triangle_plus", 6) == 480        # A-level 1 (มี.ค. 2566/27)
    assert blocks([2, 3, 3]) == 432                     # กสพท คณิต1 (มี.ค. 2562/9)
    assert alternating(3, 4) == 144                     # กสพท คณิต2 (มี.ค. 2565/23)
    assert no_two_adjacent_seats(11, 5) == factorial(7) // 2  # กสพท คณิต1 (เม.ย. 2564/20)
    assert multinomial([2, 2, 2]) == 90                 # A-level 1 (มี.ค. 2567/24)
    assert two_baskets(8, 3, 4) == 280                  # O-NET (ก.พ. 2565/20)
    assert one_extra_surjection(99) == 50 * 99 * factorial(99)  # A-level 2 (มี.ค. 2567/11)


@pytest.mark.parametrize("key", KEYS)
def test_items_offer_full_distinct_choices_and_are_reproducible(key):
    want = REGISTRY[key].max_choices
    assert want in (3, 4)
    for seed in range(120):
        q = generate(key, rng=random.Random(seed))
        texts = [c.model_dump_json() for c in q.choices]
        assert len(texts) == want and len(set(texts)) == want, (key, seed)
        assert q.model_dump_json() == generate(key, rng=random.Random(seed)).model_dump_json()
