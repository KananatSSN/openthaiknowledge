"""The proposition set: labels checked against the facts they state."""

from __future__ import annotations

import random

import pytest

from otk.core import REGISTRY, generate
from otk.sets.math.m4 import logic as tl

KEY = "math.proposition_identify_m4"


def test_mathematical_labels_match_their_checks():
    for sentence, kind, truth, check in tl.SENTENCES:
        if check:
            assert kind == tl.PROP and eval(check) is truth, sentence


def test_only_propositions_carry_a_truth_value():
    for sentence, kind, truth, _ in tl.SENTENCES:
        assert (truth is None) == (kind != tl.PROP), sentence


def test_textbook_items_reproduce():
    label = {s: (k, t) for s, k, t, _ in tl.SENTENCES}
    assert label["กรุณารักษาความสะอาด"][0] == tl.NONE            # แบบฝึกหัด 2.1 1.4
    assert label["π > 3"] == (tl.PROP, True)                      # 2.1 1.6
    assert label["9 เป็นจำนวนเฉพาะ"] == (tl.PROP, False)           # 2.1 1.7
    assert label["x² − 1"][0] == tl.NONE                          # 2.8 5
    assert label["−20 + 5 > −17"] == (tl.PROP, True)              # ท้ายบท 2.1


def _answer(q):
    return q.choices[q.answer].content[0].text


@pytest.mark.parametrize("seed", range(200))
def test_the_answer_fits_the_question_and_no_distractor_does(seed):
    q = generate(KEY, rng=random.Random(seed))
    ask = q.stem[0].text
    fits = dict(tl.ASKS)[ask]
    label = {s: (k, t) for s, k, t, _ in tl.SENTENCES}
    texts = [c.content[0].text for c in q.choices]
    assert [s for s in texts if fits(*label[s])] == [_answer(q)]


def test_items_offer_full_distinct_choices_and_are_reproducible():
    want = REGISTRY[KEY].max_choices
    for seed in range(200):
        q = generate(KEY, rng=random.Random(seed))
        texts = [c.model_dump_json() for c in q.choices]
        assert len(texts) == want and len(set(texts)) == want, seed
        assert q.model_dump_json() == generate(KEY, rng=random.Random(seed)).model_dump_json()
