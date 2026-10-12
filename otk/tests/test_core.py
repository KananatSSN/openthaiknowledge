"""Property tests for the core content model and question types.

The per-set safety net — every registered type yields a valid, well-formed
multiple-choice question whose public projection never leaks the answer — runs
in ``test_per_set.py``, which draws each set once for all the catalog-wide
rules. These tests check the content model itself and a few types by value;
the addition test checks arithmetic, so a broken assembly (wrong answer index)
is caught, not just a malformed shape.
"""

from __future__ import annotations

import random
import re


from otk.core import catalog, generate, search


def test_addition_answer_is_correct():
    rng = random.Random(7)
    for _ in range(500):
        q = generate("math.one_digit_plus_with_carry", rng)
        m = re.fullmatch(r"(\d+) \+ (\d+)", q.stem[0].tex)
        assert m, f"unexpected stem {q.stem[0].tex!r}"
        a, b = int(m.group(1)), int(m.group(2))
        assert q.choices[q.answer].content[0].tex == str(a + b)
        assert len(q.choices) == 4          # high-variety type fills all four


def test_anatomy_choices_are_thai_text():
    rng = random.Random(3)
    q = generate("anatomy.skeleton", rng)
    assert q.stem[0].kind == "image"
    for choice in q.choices:
        assert choice.content[0].kind == "text"   # not math — Thai labels
    assert len(q.choices) == 4


# ── Subject dimension & catalog search (README §3A) ──────────────────────────

def test_catalog_carries_subject_and_nav_dimensions():
    cat = catalog()
    by = {t["key"]: t for t in cat}
    assert by["math.one_digit_plus_with_carry"]["subject"] == "คณิตศาสตร์"      # default subject
    assert by["anatomy.skeleton"]["subject"] == "ชีวะ"  # the second subject
    # Every entry carries the navigation fields and additive curriculum metadata.
    for t in cat:
        assert {
            "subject", "level", "topic", "display_name", "course_type",
            "strand", "standard_code", "indicator_codes", "curriculum_node_id",
            "learning_stage", "learning_stage_key", "learning_stage_label", "source_key",
        } <= t.keys()


def test_search_matches_name_topic_and_subject():
    assert search("") == []                                    # empty query, no hits
    assert {t["key"] for t in search("บวก")} >= {"math.one_digit_plus_with_carry"}
    # Subject is searchable. Asserted as a property of the hits rather than by
    # naming one key: the result list is capped at ``limit``, so which biology set
    # lands inside the cap changes whenever biology grows.
    biology = search("ชีวะ")
    assert biology and all(t["subject"] == "ชีวะ" for t in biology)
    assert any(t["key"] == "anatomy.skeleton" for t in search("โครงกระดูก"))
    # results share the catalog entry shape, and the limit is respected
    assert all("key" in t and "subject" in t for t in search("การ"))
    assert len(search("การ", limit=3)) <= 3
