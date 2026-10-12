"""Acceptance tests for the Phase 3 moon-phase and tide learning-path pilot."""

from __future__ import annotations

import csv
import random
import re
from pathlib import Path

from otk.core import catalog, generate
from otk.core.curriculum_science import SCIENCE_BASELINE_KEYS, SCIENCE_PILOT_KEYS
from otk.sets.astronomy.m3.moon_phases_and_tides import (
    MOON_CALENDAR,
    MOON_CLAIMS,
    MOON_GEOMETRY,
    MOON_PHASES,
    MOON_RISE_TIMES,
    MOON_TIDE_TYPES,
)
from otk.sets._support.science_pilots import MOON_CAUSE_FACTS


PILOT_KEYS = (
    "astro.moon_phase_foundation",
    "astro.moon_phase_fluency",
    "astro.moon_phase_application",
)
ROOT = Path(__file__).resolve().parents[2]
CLOCK = re.compile(r"(\d{2}):(\d{2}) น\.")


def _text(blocks) -> str:
    return " ".join(block.text for block in blocks if block.kind == "text")


def _answer(question) -> str:
    return _text(question.choices[question.answer].content)


def _minutes(value: str) -> int:
    hour, minute = CLOCK.fullmatch(value).groups()
    return int(hour) * 60 + int(minute)


def test_moon_phase_pilot_is_additive_and_preserves_the_baseline():
    assert set(PILOT_KEYS) <= SCIENCE_PILOT_KEYS
    assert len(SCIENCE_BASELINE_KEYS) == 95
    assert {"astro.moon_phases", "astro.tides"} <= SCIENCE_BASELINE_KEYS
    assert not set(PILOT_KEYS) & SCIENCE_BASELINE_KEYS


def test_moon_phase_pilot_shares_one_curriculum_node_with_three_real_stages():
    rows = {row["key"]: row for row in catalog()}
    pilot = [rows[key] for key in PILOT_KEYS]
    assert [row["learning_stage"] for row in pilot] == [1, 2, 3]
    assert len({row["curriculum_node_id"] for row in pilot}) == 1
    assert all(row["indicator_codes"] == ["ว 3.1 ม.3/3"] for row in pilot)
    assert all(row["unit"] == "ข้างขึ้นข้างแรมและน้ำขึ้นน้ำลง" for row in pilot)
    assert pilot[1]["mapping_status"] == pilot[2]["mapping_status"] == "exact"


def test_moon_phase_outcome_is_complete_with_all_contributing_keys():
    with (ROOT / "docs/for_admin/science_ipst_outcomes.csv").open(
        encoding="utf-8-sig", newline="",
    ) as handle:
        row = next(item for item in csv.DictReader(handle) if item["outcome_code"] == "ว 3.1 ม.3/3")
    assert row["coverage_state"] == "complete"
    assert row["current_set_count"] == "6"
    assert set(row["current_set_keys"].split("; ")) == {
        "astro.moon_phases", "astro.phenomena", "astro.tides", *PILOT_KEYS,
    }


def test_authored_moon_banks_are_internally_consistent():
    assert {phase for _, phase in MOON_GEOMETRY} == set(MOON_PHASES)
    assert {phase for _, phase in MOON_CALENDAR} == set(MOON_PHASES)
    assert {phase for phase, _ in MOON_RISE_TIMES} == set(MOON_PHASES)
    spring = {phase for phase, tide, _ in MOON_TIDE_TYPES if tide == "น้ำเกิด"}
    assert spring == {"จันทร์เต็มดวง", "จันทร์ดับ"}
    neap = {phase for phase, tide, _ in MOON_TIDE_TYPES if tide == "น้ำตาย"}
    assert neap == {"ครึ่งดวงข้างขึ้น", "ครึ่งดวงข้างแรม"}


def test_foundation_covers_geometry_calendar_days_and_causes():
    stems = []
    answers = []
    for seed in range(500):
        question = generate(PILOT_KEYS[0], random.Random(seed))
        stems.append(_text(question.stem))
        answers.append(_answer(question))
        assert question.hint
    for position, _ in MOON_GEOMETRY:
        assert any(position in stem for stem in stems)
    for day, _ in MOON_CALENDAR:
        assert any(f"คืนวัน{day}" in stem for stem in stems)
    for question_text, correct, _ in MOON_CAUSE_FACTS:
        assert any(question_text in stem for stem in stems)
        assert correct in answers
    assert set(MOON_PHASES) <= set(answers)


def test_fluency_links_phase_rise_time_and_tide_type():
    stems = []
    answers = []
    for seed in range(500):
        question = generate(PILOT_KEYS[1], random.Random(seed))
        stems.append(_text(question.stem))
        answers.append(_answer(question))
        assert question.hint
    for phase, rise in MOON_RISE_TIMES:
        assert any(f"คืนที่เห็น{phase} ดวงจันทร์ขึ้นเวลาใด" in stem for stem in stems)
    assert {rise for _, rise in MOON_RISE_TIMES} <= set(answers)
    for phase, tide, reason in MOON_TIDE_TYPES:
        assert f"{tide} เพราะ{reason}" in answers
    assert any("ขึ้นช้าลง" in stem for stem in stems)


def test_fluency_moonrise_shift_is_exactly_fifty_minutes_later():
    checked = 0
    for seed in range(500):
        question = generate(PILOT_KEYS[1], random.Random(seed))
        stem = _text(question.stem)
        if "คืนพรุ่งนี้" not in stem:
            continue
        checked += 1
        start = _minutes(CLOCK.search(stem).group(0))
        assert (_minutes(_answer(question)) - start) % (24 * 60) == 50
    assert checked


def test_application_uses_tide_ranges_multi_day_timing_and_claims():
    stems = []
    answers = []
    for seed in range(600):
        question = generate(PILOT_KEYS[2], random.Random(seed))
        stems.append(_text(question.stem))
        answers.append(_answer(question))
        assert question.hint
    assert any("บันทึกพิสัยน้ำขึ้นน้ำลง" in stem for stem in stems)
    assert any("จันทร์เต็มดวงหรือจันทร์ดับ ส่วนวันที่ 8" in answer for answer in answers)
    for claim, correct, _ in MOON_CLAIMS:
        assert any(claim in stem for stem in stems)
        assert correct in answers
    assert any("ดวงอาทิตย์ตกพอดี" in stem for stem in stems)
    assert any("โลกอยู่ระหว่างดวงอาทิตย์กับดวงจันทร์" in answer for answer in answers)


def test_application_multi_day_timing_scales_with_the_number_of_nights():
    checked = 0
    for seed in range(600):
        question = generate(PILOT_KEYS[2], random.Random(seed))
        stem = _text(question.stem)
        if "อีก " not in stem:
            continue
        checked += 1
        days = int(re.search(r"อีก (\d+) คืน", stem).group(1))
        start = _minutes(CLOCK.search(stem).group(0))
        assert (_minutes(_answer(question)) - start) % (24 * 60) == 50 * days
    assert checked


def test_application_tide_range_evidence_always_orders_spring_above_neap():
    for seed in range(600):
        stem = _text(generate(PILOT_KEYS[2], random.Random(seed)).stem)
        if "บันทึกพิสัยน้ำขึ้นน้ำลง" not in stem:
            continue
        large, small = (float(value) for value in re.findall(r"([\d.]+) m", stem))
        assert large > small


def test_two_hundred_seed_quality_gate_has_four_distinct_choices_each():
    for key in PILOT_KEYS:
        signatures = set()
        for seed in range(200):
            question = generate(key, random.Random(seed))
            choices = [_text(choice.content) for choice in question.choices]
            assert len(choices) == len(set(choices)) == 4
            assert choices[question.answer]
            signatures.add((_text(question.stem), choices[question.answer]))
        minimum = 12 if key == PILOT_KEYS[0] else 25 if key == PILOT_KEYS[1] else 80
        assert len(signatures) >= minimum
