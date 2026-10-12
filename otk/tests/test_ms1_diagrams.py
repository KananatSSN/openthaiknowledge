"""The drawn ม.1 ความร้อน and ลมฟ้าอากาศ diagrams, and the sets that read them.

Three of these sets promised a picture and shipped a sentence instead — a graph
described in prose, a thermometer whose reading was stated in the stem it was
meant to be read from, and a "แบบจำลอง" that was four numbers in a list. What
has to hold now is that the drawing exists, that the answer is derived from the
same spec the picture was drawn from, and that the alt text stops short of the
value being asked for.
"""

from __future__ import annotations

import re
from random import Random

import pytest

from otk.core import generate
from otk.sets._support.ms1_diagrams import (
    ATMOSPHERE,
    ATMOSPHERE_ALT,
    ATMOSPHERE_ASSET,
    HEAT_SCENES,
    HEATING_CURVES,
    MODE_LABELS,
    THERMOMETERS,
    WEATHER_CHARTS,
    heat_scene_alt,
    heating_curve_alt,
    thermometer_alt,
    weather_chart_alt,
)
from otk.sets.earth_science.m1.atmosphere_layers import LAYERS


from otk.core.render.assets import is_diagram

SEEDS = 300

DIAGRAM_KEYS = (
    "phys.heat_quantity_foundation",
    "phys.thermometer_fluency",
    "geo.atmosphere_layers_foundation",
    "geo.weather_chart_foundation",
    "geo.weather_chart_fluency",
    "geo.weather_chart_application",
    "phys.heat_transfer_diagram_foundation",
    "phys.heat_transfer_diagram_fluency",
    "phys.heat_transfer_diagram_application",
)


def _stem_image(question):
    return next(b for b in question.stem if b.kind == "image")


def _answer(question) -> str:
    return " ".join(b.text for b in question.choices[question.answer].content)


# ── the specs and their rendered assets ──────────────────────────────────────

def test_every_spec_is_a_drawable_diagram():
    specs = [*HEATING_CURVES, *THERMOMETERS, *WEATHER_CHARTS, *HEAT_SCENES]
    missing = [s.asset_id for s in specs
               if not is_diagram(s.asset_id)]
    assert not missing
    assert is_diagram(ATMOSPHERE_ASSET)


def test_asset_ids_are_unique_and_ascii():
    """ASCII because they name files, and because nothing Thai may be drawn."""
    ids = [s.asset_id for s in
           (*HEATING_CURVES, *THERMOMETERS, *WEATHER_CHARTS, *HEAT_SCENES)]
    assert len(set(ids)) == len(ids)
    assert all(i.isascii() for i in ids)


def test_a_heating_curve_really_has_a_flat_stretch():
    """Without one there is no change of state to interpret."""
    for spec in HEATING_CURVES:
        assert spec.hold > 0, spec.asset_id
        assert spec.start < spec.plateau < spec.end, spec.asset_id
        assert spec.plateau_end == spec.plateau_start + spec.hold
        assert spec.total == spec.warm_to + spec.hold + spec.after


def test_every_thermometer_reading_sits_on_its_own_scale():
    for spec in THERMOMETERS:
        assert spec.lo <= spec.reading <= spec.hi, spec.asset_id
        assert (spec.reading - spec.lo) % spec.step == 0, spec.asset_id
        assert spec.label_every % spec.step == 0, spec.asset_id


def test_the_thermometer_pool_is_not_all_one_degree_per_division():
    """A learner who counts divisions is only caught by a coarser scale."""
    assert {spec.step for spec in THERMOMETERS} > {1}


def test_a_high_is_always_higher_than_the_low_beside_it():
    for spec in WEATHER_CHARTS:
        assert spec.high_hpa > spec.low_hpa, spec.asset_id
        assert spec.difference > 0
        assert {spec.high_side, spec.low_side} == {"left", "right"}


def test_the_chart_pool_puts_the_high_on_both_sides():
    """Otherwise "the wind blows right" answers every draw without the picture."""
    assert {spec.high_side for spec in WEATHER_CHARTS} == {"left", "right"}


def test_every_heat_mode_is_drawn_at_least_twice():
    """One scene per mode would let a student memorise the picture, not the idea."""
    counts = {mode: sum(s.mode == mode for s in HEAT_SCENES)
              for mode in ("conduction", "convection", "radiation")}
    assert all(count >= 2 for count in counts.values()), counts
    assert {s.thai_mode for s in HEAT_SCENES} == set(MODE_LABELS)


def test_the_drawn_atmosphere_matches_the_layers_the_questions_name():
    """One table: the picture and the wording must not drift apart."""
    assert len(ATMOSPHERE) == 4
    for drawn, described in zip(ATMOSPHERE, LAYERS):
        assert drawn.name == described.name
        # Checked against the plotted numbers rather than the wording: the two
        # describe the same trend in different words, and it is the direction
        # the line actually goes that must match what the choice says.
        rising = drawn.top_c > drawn.base_c
        assert rising == (drawn.trend == "เพิ่มขึ้น"), drawn.name
        assert rising != ("ลดลง" in described.trend), drawn.name
        assert str(drawn.base_km) in described.span or drawn.base_km == 0
        assert str(drawn.top_km) in described.span


# ── what the alt text may and may not say ────────────────────────────────────

def test_the_curve_alt_never_gives_away_the_values_being_read():
    for spec in HEATING_CURVES:
        described = heating_curve_alt(spec)
        assert str(spec.plateau) not in described
        assert str(spec.hold) not in described


def test_the_thermometer_alt_never_gives_away_the_reading():
    for spec in THERMOMETERS:
        described = thermometer_alt(spec)
        numbers = [int(n) for n in re.findall(r"-?\d+", described)]
        assert spec.reading not in numbers or spec.reading in (spec.lo, spec.hi,
                                                               spec.step,
                                                               spec.label_every)
        # The scale itself must be there, or the drawing cannot be read at all.
        assert spec.lo in numbers and spec.hi in numbers
        assert spec.step in numbers


def test_the_chart_alt_names_the_letters_but_not_which_side_wins():
    for spec in WEATHER_CHARTS:
        described = weather_chart_alt(spec)
        assert "H" in described and "L" in described
        assert "ซ้าย" not in described and "ขวา" not in described


def test_the_heat_scene_alt_never_names_the_mode():
    for spec in HEAT_SCENES:
        described = heat_scene_alt(spec)
        for label in MODE_LABELS:
            assert label not in described, spec.asset_id


def test_the_atmosphere_alt_numbers_the_layers_without_naming_them():
    for layer in ATMOSPHERE:
        assert layer.name not in ATMOSPHERE_ALT


# ── the questions built from them ────────────────────────────────────────────

@pytest.mark.parametrize("key", DIAGRAM_KEYS)
def test_every_draw_shows_a_diagram_and_offers_four_distinct_choices(key):
    for seed in range(SEEDS):
        question = generate(key, Random(seed))
        image = _stem_image(question)
        assert is_diagram(image.asset_id), (key, seed)
        assert image.alt, (key, seed)
        assert len({c.model_dump_json() for c in question.choices}) == 4, (key, seed)


def test_the_thermometer_answer_is_the_value_drawn():
    by_id = {s.asset_id: s for s in THERMOMETERS}
    for seed in range(SEEDS):
        question = generate("phys.thermometer_fluency", Random(seed))
        spec = by_id[_stem_image(question).asset_id]
        assert _answer(question) == f"{spec.reading} องศาเซลเซียส"


def test_thermometer_choices_are_far_enough_apart_to_see():
    """One small division is about five pixels on the dense scales, too close to judge on a phone."""
    from otk.sets._support.ms1_diagrams import min_option_gap, thermometer_wrongs

    for spec in THERMOMETERS:
        gap = min_option_gap(spec)
        assert gap >= 2 * spec.step or spec.step >= 5, spec.asset_id
        wrongs = thermometer_wrongs(spec)
        assert len(wrongs) == 3, spec.asset_id
        values = (spec.reading, *wrongs)
        assert all(spec.lo <= v <= spec.hi for v in values), spec.asset_id
        assert all(abs(a - b) >= gap for i, a in enumerate(values) for b in values[i + 1:]), spec.asset_id
    by_id = {s.asset_id: s for s in THERMOMETERS}
    for seed in range(SEEDS):
        question = generate("phys.thermometer_fluency", Random(seed))
        spec = by_id[_stem_image(question).asset_id]
        values = [int(" ".join(b.text for b in c.content).split()[0]) for c in question.choices]
        gap = min_option_gap(spec)
        assert all(abs(a - b) >= gap for i, a in enumerate(values) for b in values[i + 1:]), (spec.asset_id, values)


def test_the_heating_curve_answer_is_read_off_the_plotted_curve():
    by_id = {s.asset_id: s for s in HEATING_CURVES}
    asked_values = False
    for seed in range(SEEDS):
        question = generate("phys.heat_quantity_foundation", Random(seed))
        spec = by_id[_stem_image(question).asset_id]
        answer = _answer(question)
        if "องศาเซลเซียส" in answer:
            asked_values = True
            assert answer == f"{spec.plateau} องศาเซลเซียส เป็นเวลา {spec.hold} นาที"
        else:
            assert "เปลี่ยนสถานะ" in answer
    assert asked_values, "the value-reading half of the set never came up"


def test_the_chart_sets_answer_from_the_side_the_high_is_drawn_on():
    by_id = {s.asset_id: s for s in WEATHER_CHARTS}
    for key in ("geo.weather_chart_foundation", "geo.weather_chart_fluency",
                "geo.weather_chart_application"):
        for seed in range(SEEDS):
            question = generate(key, Random(seed))
            spec = by_id[_stem_image(question).asset_id]
            answer = _answer(question)
            high = "ซ้าย" if spec.high_side == "left" else "ขวา"
            low = "ขวา" if spec.high_side == "left" else "ซ้าย"
            if key == "geo.weather_chart_foundation":
                assert answer.startswith(f"ความกดอากาศสูงอยู่ด้าน{high}")
            elif key == "geo.weather_chart_fluency":
                assert answer.startswith(f"เคลื่อนจากด้าน{high}ไปยังด้าน{low}")
            else:
                assert answer.startswith(f"บริเวณด้าน{low}")


def test_the_heat_scene_answer_is_the_mode_that_scene_shows():
    by_id = {s.asset_id: s for s in HEAT_SCENES}
    for seed in range(SEEDS):
        question = generate("phys.heat_transfer_diagram_foundation", Random(seed))
        spec = by_id[_stem_image(question).asset_id]
        assert _answer(question) == spec.thai_mode


def test_the_heat_scene_reason_matches_the_mode_drawn():
    by_id = {s.asset_id: s for s in HEAT_SCENES}
    for seed in range(SEEDS):
        question = generate("phys.heat_transfer_diagram_fluency", Random(seed))
        spec = by_id[_stem_image(question).asset_id]
        assert _answer(question) == spec.because


def test_the_atmosphere_set_asks_only_about_layers_the_picture_numbers():
    """เอกโซสเฟียร์ lies above the plotted range, so it may distract, never answer."""
    names = [layer.name for layer in ATMOSPHERE]
    for seed in range(SEEDS):
        question = generate("geo.atmosphere_layers_foundation", Random(seed))
        assert _stem_image(question).asset_id == ATMOSPHERE_ASSET
        answer = _answer(question)
        assert any(answer.startswith(name) for name in names), answer
        assert not answer.startswith("เอกโซสเฟียร์")


def test_the_humidity_trio_never_shows_a_picture():
    """A ratio is an idea; drawing it would suggest there is something to read."""
    for key in ("geo.humidity_foundation", "geo.humidity_fluency",
                "geo.humidity_application"):
        for seed in range(60):
            question = generate(key, Random(seed))
            assert all(b.kind != "image" for b in question.stem), (key, seed)
            assert len({c.model_dump_json() for c in question.choices}) == 4
