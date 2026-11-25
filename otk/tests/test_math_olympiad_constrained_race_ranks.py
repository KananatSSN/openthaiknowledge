"""Cross-check rank-pair backtracking against all finish orders."""

from itertools import permutations
from random import Random

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.constrained_race_ranks import possible_rank_pairs


def _direct_pairs(competitors, separation, b_not_first, d_before_f, a_before_f, f_before_c):
    labels = "ABCDEFG"[:competitors]
    pairs = set()
    for order in permutations(labels):
        position = {label: order.index(label) for label in labels}
        if position["B"] >= position["A"] or abs(position["E"] - position["A"]) != separation:
            continue
        if b_not_first and position["B"] == 0:
            continue
        if d_before_f and position["D"] >= position["F"]:
            continue
        if a_before_f and position["A"] >= position["F"]:
            continue
        if f_before_c and position["F"] >= position["C"]:
            continue
        pairs.add((order[0], order[2]))
    return frozenset(pairs)


def test_matches_full_permutation_enumeration():
    for competitors in (6, 7):
        for separation in range(2, competitors - 1):
            for omit in (None, "b", "d", "a", "c"):
                flags = (omit != "b", omit != "d", omit != "a", omit != "c")
                assert possible_rank_pairs(
                    competitors, separation, b_not_first=flags[0], d_before_f=flags[1],
                    a_before_f=flags[2], f_before_c=flags[3],
                ) == _direct_pairs(competitors, separation, *flags)


def test_checked_source_case():
    # สอวน. ค่าย 1 2569 ข้อ 26: "F เข้าเส้นชัยหลัง D และ A แต่เข้าเส้นชัยก่อน C"
    assert possible_rank_pairs(6, 3) == frozenset({("D", "A"), ("E", "B"), ("E", "D")})


def test_generated_draws():
    key = "math.constrained_race_rank_pairs_olympiad"
    for seed in range(100):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
