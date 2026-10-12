"""The drawn ป.6 circuit schematics and the sets that read them.

``ว 2.3 ป.6/2`` is about แผนภาพ, so these sets *show* one. What has to hold is
that every spec the generators can draw has a PNG on disk, that the picture and
the answer come from the same row of one table, and that the alt text gives away
neither more nor less than it should — a set whose answer is the layout must not
state the layout in words an image-less reader would see.
"""

from __future__ import annotations

from random import Random

import pytest

from otk.core import generate
from otk.sets._support.circuit_symbols import (
    FAULT_CIRCUITS,
    MULTI_BULB_CIRCUITS,
    P6_CIRCUIT_SPECS,
    SYMBOL_CARDS,
    card_alt,
    full_alt,
    layout_alt,
)


from otk.core.render.assets import is_diagram

SEEDS = 300

DIAGRAM_KEYS = (
    "phys.circuit_symbol_foundation",
    "phys.circuit_symbol_fluency",
    "phys.circuit_symbol_application",
    "phys.circuit_diagram_fluency",
)


def _stem_image(question):
    return next(b for b in question.stem if b.kind == "image")


def _answer(question) -> str:
    return " ".join(b.text for b in question.choices[question.answer].content)


# ── the specs and their rendered assets ──────────────────────────────────────

def test_every_spec_is_a_drawable_diagram():
    """A missing PNG would render as a broken image in front of a student."""
    missing = [s.asset_id for s in (*SYMBOL_CARDS, *P6_CIRCUIT_SPECS)
               if not is_diagram(s.asset_id)]
    assert not missing


def test_asset_ids_are_unique():
    ids = [s.asset_id for s in (*SYMBOL_CARDS, *P6_CIRCUIT_SPECS)]
    assert len(set(ids)) == len(ids)


def test_a_circuit_is_complete_exactly_when_nothing_breaks_the_loop():
    for spec in P6_CIRCUIT_SPECS:
        assert spec.lights == (spec.switch == "closed" and not spec.gap)


def test_the_pool_covers_every_case_the_sets_ask_about():
    # Something to fix, and something that needs no fixing.
    assert any(s.gap for s in P6_CIRCUIT_SPECS)
    assert any(s.switch == "open" for s in P6_CIRCUIT_SPECS)
    assert any(s.lights for s in P6_CIRCUIT_SPECS)
    # Both wirings, readable — otherwise the Fluency set has one answer.
    assert {s.wiring for s in MULTI_BULB_CIRCUITS} == {"series", "parallel"}
    assert all(s.lights and s.bulbs >= 2 for s in MULTI_BULB_CIRCUITS)
    # Cell counts a student can actually tell apart in a picture.
    assert {s.cells for s in P6_CIRCUIT_SPECS} <= {1, 2, 3}


def test_no_thai_is_drawn_into_a_diagram():
    """These schematics carry no text at all — the symbols are the content.

    The bundled matplotlib font has no Thai glyphs, so the Thai lives in the
    stem, the choices and the alt text. Asset ids are ASCII for the same reason
    they are stable: they name files.
    """
    for spec in (*SYMBOL_CARDS, *P6_CIRCUIT_SPECS):
        assert spec.asset_id.isascii()


# ── what the alt text may and may not say ────────────────────────────────────

def test_a_symbol_card_alt_describes_the_shape_without_naming_the_device():
    """Naming it is the answer to the Foundation set."""
    for card in SYMBOL_CARDS:
        described = card_alt(card)
        assert card.shape in described
        assert card.device not in described


def test_layout_alt_never_says_how_the_circuit_is_connected():
    """Reading the layout, or finding the fault in it, is the question."""
    for spec in P6_CIRCUIT_SPECS:
        described = layout_alt(spec)
        assert "อนุกรม" not in described
        assert "ขนาน" not in described
        assert str(spec.cells) not in described
        assert "ไม่ต่อ" not in described


def test_full_alt_states_everything_the_picture_shows():
    """It is only used where the layout is given and the answer follows from it."""
    for spec in P6_CIRCUIT_SPECS:
        described = full_alt(spec)
        assert f"{spec.cells} เซลล์" in described
        assert f"{spec.bulbs} ดวง" in described
        assert spec.wiring_word in described


# ── the questions built from them ────────────────────────────────────────────

@pytest.mark.parametrize("key", DIAGRAM_KEYS)
def test_every_draw_shows_a_diagram_and_offers_four_distinct_choices(key):
    for seed in range(SEEDS):
        question = generate(key, Random(seed))
        image = _stem_image(question)
        assert is_diagram(image.asset_id), (key, seed)
        assert image.alt, (key, seed)
        assert len({c.model_dump_json() for c in question.choices}) == 4, (key, seed)


def test_the_symbol_set_answers_with_the_device_the_card_draws():
    by_id = {c.asset_id: c for c in SYMBOL_CARDS}
    for seed in range(SEEDS):
        question = generate("phys.circuit_symbol_foundation", Random(seed))
        card = by_id[_stem_image(question).asset_id]
        assert _answer(question) == card.device


def test_reading_the_circuit_matches_the_drawn_cells_and_wiring():
    by_id = {s.asset_id: s for s in P6_CIRCUIT_SPECS}
    for seed in range(SEEDS):
        question = generate("phys.circuit_symbol_fluency", Random(seed))
        spec = by_id[_stem_image(question).asset_id]
        answer = _answer(question)
        assert f"เซลล์ไฟฟ้า {spec.cells} เซลล์" in answer
        assert f"หลอดไฟ {spec.bulbs} ดวง" in answer
        assert answer.endswith(spec.wiring_word)


def test_reading_the_circuit_only_ever_uses_a_circuit_worth_reading():
    allowed = {s.asset_id for s in MULTI_BULB_CIRCUITS}
    for seed in range(SEEDS):
        question = generate("phys.circuit_symbol_fluency", Random(seed))
        assert _stem_image(question).asset_id in allowed


def test_the_fix_matches_what_is_actually_wrong_with_the_drawing():
    by_id = {s.asset_id: s for s in FAULT_CIRCUITS}
    for seed in range(SEEDS):
        question = generate("phys.circuit_symbol_application", Random(seed))
        spec = by_id[_stem_image(question).asset_id]
        answer = _answer(question)
        if spec.gap:
            assert "ครบเป็นวงปิด" in answer
        elif spec.switch == "open":
            assert "กดสวิตช์" in answer
        else:
            assert "ไม่ต้องแก้ไข" in answer


def test_a_working_circuit_is_sometimes_the_answer():
    """Otherwise "something is broken" answers the Application set unread."""
    answers = {_answer(generate("phys.circuit_symbol_application", Random(s)))
               for s in range(SEEDS)}
    assert any(a.startswith("ไม่ต้องแก้ไข") for a in answers)
    assert any(not a.startswith("ไม่ต้องแก้ไข") for a in answers)


def test_whether_the_bulb_lights_matches_the_drawn_circuit():
    by_id = {s.asset_id: s for s in FAULT_CIRCUITS}
    for seed in range(SEEDS):
        question = generate("phys.circuit_diagram_fluency", Random(seed))
        spec = by_id[_stem_image(question).asset_id]
        answer = _answer(question)
        assert answer.startswith("สว่าง" if spec.lights else "ไม่สว่าง")
        if not spec.lights:
            assert ("สวิตช์" in answer) == (spec.switch == "open")


def test_the_closed_circuit_trio_never_shows_a_picture():
    """It is the half of the topic that has to work without one."""
    for key in ("phys.closed_circuit_foundation", "phys.closed_circuit_fluency",
                "phys.closed_circuit_application"):
        for seed in range(60):
            question = generate(key, Random(seed))
            assert all(b.kind != "image" for b in question.stem), (key, seed)
            assert len({c.model_dump_json() for c in question.choices}) == 4
