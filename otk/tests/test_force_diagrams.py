"""The drawn free-body diagrams behind the ``ว 2.2`` แผนภาพแสดงแรง sets.

These four indicators used to describe their diagram in words and ask the
student to pick the right description. They now *show* the drawing, so what has
to hold is different: every spec the generators can draw must have a PNG on
disk, the picture and the answer must come from the same numbers, and nothing
Thai may be baked into an image the bundled font cannot render.
"""

from __future__ import annotations

from random import Random

import pytest

from otk.core import generate
from otk.sets._support.force_diagrams import (
    ALL_FORCE_DIAGRAM_SPECS,
    FIELD_SPECS,
    FRICTION_SPECS,
    LIQUID_SPECS,
    NETFORCE_SPECS,
    SYMBOL_NAMES,
    alt_text,
)


from otk.core.render.assets import is_diagram

SEEDS = 300

DIAGRAM_KEYS = (
    "phys.net_force_diagram_fluency",
    "phys.liquid_force_diagram_fluency",
    "phys.friction_forces_diagram_fluency",
    "phys.field_force_diagram_fluency",
)


def _stem_image(question):
    return next(b for b in question.stem if b.kind == "image")


def _answer(question) -> str:
    return " ".join(b.text for b in question.choices[question.answer].content)


# ── the specs and their rendered assets ──────────────────────────────────────

def test_every_spec_is_a_drawable_diagram():
    """A missing PNG would render as a broken image in front of a student."""
    missing = [spec.asset_id for spec in ALL_FORCE_DIAGRAM_SPECS
               if not is_diagram(spec.asset_id)]
    assert not missing


def test_asset_ids_are_unique():
    ids = [spec.asset_id for spec in ALL_FORCE_DIAGRAM_SPECS]
    assert len(set(ids)) == len(ids)


def test_no_thai_is_drawn_into_a_diagram():
    """Arrow labels are ASCII symbols — the bundled matplotlib font has no Thai.

    The Thai belongs in the stem, the choices and the alt text instead.
    """
    for spec in ALL_FORCE_DIAGRAM_SPECS:
        for arrow in spec.arrows:
            assert arrow.symbol.isascii(), spec.asset_id
            assert arrow.symbol in SYMBOL_NAMES


def test_alt_text_names_every_arrow_in_thai():
    """A reader who cannot see the picture still gets all of its content."""
    for spec in ALL_FORCE_DIAGRAM_SPECS:
        described = alt_text(spec)
        for arrow in spec.arrows:
            assert arrow.name in described, spec.asset_id
            assert f"{arrow.newtons} นิวตัน" in described, spec.asset_id


def test_each_pool_covers_the_cases_its_indicator_needs():
    # A resultant each way and one that cancels exactly.
    nets = {spec.horizontal for spec in NETFORCE_SPECS}
    assert 0 in nets and any(n > 0 for n in nets) and any(n < 0 for n in nets)
    # Boxes that are balanced and boxes that accelerate.
    horizontals = {spec.horizontal for spec in FRICTION_SPECS}
    assert 0 in horizontals and any(h > 0 for h in horizontals)
    # Floating at rest and sinking.
    verticals = {spec.vertical for spec in LIQUID_SPECS}
    assert 0 in verticals and any(v < 0 for v in verticals)
    # Both field kinds, pulling both ways.
    symbols = {a.symbol for spec in FIELD_SPECS for a in spec.arrows}
    assert {"FM", "FE"} <= symbols
    assert {a.direction for spec in FIELD_SPECS for a in spec.arrows
            if a.symbol in ("FM", "FE")} == {"left", "right"}


def test_a_resting_object_never_has_an_unbalanced_vertical_pair():
    """W and N are drawn equal wherever the object sits on something solid."""
    for spec in FRICTION_SPECS + FIELD_SPECS:
        assert spec.vertical == 0, spec.asset_id


# ── the questions built from them ────────────────────────────────────────────

@pytest.mark.parametrize("key", DIAGRAM_KEYS)
def test_every_draw_shows_a_diagram_and_offers_four_distinct_choices(key):
    for seed in range(SEEDS):
        question = generate(key, Random(seed))
        image = _stem_image(question)
        assert is_diagram(image.asset_id), (key, seed)
        assert image.alt, (key, seed)
        assert len({c.model_dump_json() for c in question.choices}) == 4, (key, seed)


@pytest.mark.parametrize("key", DIAGRAM_KEYS)
def test_the_question_draws_only_from_its_own_pool(key):
    pools = {
        "phys.net_force_diagram_fluency": NETFORCE_SPECS,
        "phys.liquid_force_diagram_fluency": LIQUID_SPECS,
        "phys.friction_forces_diagram_fluency": FRICTION_SPECS,
        "phys.field_force_diagram_fluency": FIELD_SPECS,
    }[key]
    allowed = {spec.asset_id for spec in pools}
    for seed in range(SEEDS):
        assert _stem_image(generate(key, Random(seed))).asset_id in allowed


def test_net_force_answer_matches_the_drawn_arrows():
    by_id = {spec.asset_id: spec for spec in NETFORCE_SPECS}
    for seed in range(SEEDS):
        question = generate("phys.net_force_diagram_fluency", Random(seed))
        spec = by_id[_stem_image(question).asset_id]
        answer = _answer(question)
        if spec.horizontal == 0:
            assert answer == "แรงลัพธ์เป็นศูนย์"
        else:
            side = "ขวา" if spec.horizontal > 0 else "ซ้าย"
            assert f"{abs(spec.horizontal)} นิวตัน ไปทาง{side}" in answer


def test_liquid_answer_matches_the_drawn_arrows():
    by_id = {spec.asset_id: spec for spec in LIQUID_SPECS}
    for seed in range(SEEDS):
        question = generate("phys.liquid_force_diagram_fluency", Random(seed))
        spec = by_id[_stem_image(question).asset_id]
        answer = _answer(question)
        if spec.vertical == 0:
            assert "ลอยนิ่ง" in answer
        else:
            assert "จมลง" in answer
            assert f"{abs(spec.vertical)} นิวตัน" in answer


def test_friction_answer_matches_the_drawn_arrows():
    by_id = {spec.asset_id: spec for spec in FRICTION_SPECS}
    for seed in range(SEEDS):
        question = generate("phys.friction_forces_diagram_fluency", Random(seed))
        spec = by_id[_stem_image(question).asset_id]
        answer = _answer(question)
        if spec.horizontal == 0:
            assert "เป็นศูนย์" in answer
        else:
            assert f"{spec.horizontal} นิวตัน ไปทางขวา" in answer


def test_field_answer_names_the_right_force_and_direction():
    by_id = {spec.asset_id: spec for spec in FIELD_SPECS}
    for seed in range(SEEDS):
        question = generate("phys.field_force_diagram_fluency", Random(seed))
        spec = by_id[_stem_image(question).asset_id]
        field = next(a for a in spec.arrows if a.symbol in ("FM", "FE"))
        answer = _answer(question)
        assert answer.startswith(field.name), spec.asset_id
        assert f"{field.newtons} นิวตัน" in answer
        assert ("ขวา" if field.direction == "right" else "ซ้าย") in answer
