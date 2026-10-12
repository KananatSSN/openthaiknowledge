"""Acceptance tests for Wave A slice 4 — the ม.3 optics cluster."""

from __future__ import annotations

import csv
import random
import re
from pathlib import Path

import pytest

from otk.core import catalog, generate
from otk.core.curriculum_science import SCIENCE_BASELINE_KEYS, SCIENCE_WAVE_KEYS
from otk.sets.physics.m3.optics import DEVICE_FACTS, LIGHT_PHENOMENA, VISION_DEFECTS
from otk.sets._support.science_wave_a4 import IMAGE_TYPES, _converging_image
from otk.sets.physics.m3.illuminance import LIGHTING_PLANS, STANDARD_LUX


NEW_KEYS = {
    "phys.mirror_image_foundation": ("ว 2.3 ม.3/14", 1),
    "phys.mirror_image_application": ("ว 2.3 ม.3/14", 3),
    "phys.lens_image_foundation": ("ว 2.3 ม.3/16", 1),
    "phys.lens_image_application": ("ว 2.3 ม.3/16", 3),
    "phys.optics_fluency": ("ว 2.3 ม.3/17", 2),
    "phys.optics_application": ("ว 2.3 ม.3/17", 3),
    "phys.illuminance_foundation": ("ว 2.3 ม.3/19", 1),
    "phys.illuminance_application": ("ว 2.3 ม.3/19", 3),
}
COMPLETED = ("ว 2.3 ม.3/14", "ว 2.3 ม.3/16", "ว 2.3 ม.3/17", "ว 2.3 ม.3/19")
ROOT = Path(__file__).resolve().parents[2]


def _text(blocks) -> str:
    return " ".join(block.text for block in blocks if block.kind == "text")


def _answer(question) -> str:
    return _text(question.choices[question.answer].content)


def test_slice_four_is_additive_and_correctly_staged():
    rows = {row["key"]: row for row in catalog()}
    assert set(NEW_KEYS) <= set(SCIENCE_WAVE_KEYS)
    assert not set(NEW_KEYS) & SCIENCE_BASELINE_KEYS
    for key, (indicator, stage) in NEW_KEYS.items():
        assert rows[key]["learning_stage"] == stage, key
        assert rows[key]["indicator_codes"] == [indicator], key


def test_each_completed_topic_holds_all_three_stages():
    rows = [row for row in catalog() if row["curriculum_node_id"]]
    for key, (indicator, _) in NEW_KEYS.items():
        node = next(row["curriculum_node_id"] for row in rows if row["key"] == key)
        stages = {r["learning_stage"] for r in rows if r["curriculum_node_id"] == node}
        assert stages == {1, 2, 3}, (indicator, sorted(stages))


def test_completed_outcomes_are_recorded_in_the_matrix():
    with (ROOT / "docs/for_admin/science_ipst_outcomes.csv").open(
        encoding="utf-8-sig", newline="",
    ) as handle:
        rows = {row["outcome_code"]: row for row in csv.DictReader(handle)}
    for indicator in COMPLETED:
        assert rows[indicator]["coverage_state"] == "complete", indicator
    for key, (indicator, _) in NEW_KEYS.items():
        assert key in rows[indicator]["current_set_keys"].split("; "), key


def test_converging_image_regions_follow_the_ray_diagram_rules():
    """The four regions a ม.3 diagram distinguishes, re-derived independently."""
    for focal in (5, 8, 12, 20):
        assert _converging_image(3 * focal, focal) == "ภาพจริง หัวกลับ ขนาดเล็กกว่าวัตถุ"
        assert _converging_image(2 * focal, focal) == "ภาพจริง หัวกลับ ขนาดเท่ากับวัตถุ"
        assert _converging_image(focal + 1, focal) == "ภาพจริง หัวกลับ ขนาดใหญ่กว่าวัตถุ"
        assert _converging_image(focal - 1, focal) == "ภาพเสมือน หัวตั้ง ขนาดใหญ่กว่าวัตถุ"


def test_mirror_and_lens_image_answers_match_the_object_position():
    """Every stated distance is re-classified from the stem, not from the generator."""
    checked = {"phys.mirror_image_application": 0, "phys.lens_image_application": 0}
    patterns = {
        "phys.mirror_image_application": r"กระจกเว้าที่มีความยาวโฟกัส (\d+) เซนติเมตร โดยวัตถุอยู่ห่างจากกระจก (\d+)",
        "phys.lens_image_application": r"เลนส์นูนที่มีความยาวโฟกัส (\d+) เซนติเมตร โดยวัตถุอยู่ห่างจากเลนส์ (\d+)",
    }
    for key, pattern in patterns.items():
        for seed in range(600):
            question = generate(key, random.Random(seed))
            stem = _text(question.stem)
            found = re.search(pattern, stem)
            if not found:
                continue
            checked[key] += 1
            focal, distance = (int(value) for value in found.groups())
            assert _answer(question) == _converging_image(distance, focal), stem
    assert all(checked.values()), checked


def test_image_questions_only_offer_real_image_types():
    for key in ("phys.mirror_image_application", "phys.lens_image_application",
                "phys.optics_fluency"):
        for seed in range(400):
            question = generate(key, random.Random(seed))
            choices = {_text(choice.content) for choice in question.choices}
            if choices <= set(IMAGE_TYPES):
                continue
            # Non-image branches are allowed; image branches must use the table only.
            assert not choices & set(IMAGE_TYPES), (key, seed, choices)


def test_lamp_counts_are_illuminance_times_area_over_flux():
    for area, lux, lumens, lamps in LIGHTING_PLANS:
        assert lux * area == lamps * lumens, (area, lux, lumens, lamps)
    checked = 0
    for seed in range(800):
        question = generate("phys.illuminance_application", random.Random(seed))
        stem = _text(question.stem)
        if "ต้องใช้หลอดไฟอย่างน้อยกี่หลอด" not in stem:
            continue
        checked += 1
        area = int(re.search(r"พื้นที่ (\d+) ตารางเมตร", stem).group(1))
        lux = int(re.search(r"ความสว่างบนพื้นที่ (\d+) ลักซ์", stem).group(1))
        lumens = int(re.search(r"ฟลักซ์ส่องสว่าง (\d+) ลูเมน", stem).group(1))
        assert _answer(question) == f"{lux * area // lumens} หลอด", stem
    assert checked


def test_measured_illuminance_never_falls_to_an_implausible_reading():
    """A proportional shortfall keeps 100 lx from becoming 0 lx."""
    standards = dict(STANDARD_LUX)
    checked = 0
    for seed in range(800):
        question = generate("phys.illuminance_application", random.Random(seed))
        stem = _text(question.stem)
        if "ค่ามาตรฐานคือ" not in stem:
            continue
        checked += 1
        measured = int(re.search(r"ได้ (\d+) ลักซ์", stem).group(1))
        standard = int(re.search(r"ค่ามาตรฐานคือ (\d+) ลักซ์", stem).group(1))
        assert standard in standards.values()
        assert 0 < measured < standard, stem
        assert measured >= standard * 6 // 10, stem
        assert _answer(question).startswith(f"เพิ่มความสว่างให้ถึงประมาณ {standard} ลักซ์")
    assert checked


def test_device_and_phenomenon_answers_come_from_the_authored_tables():
    elements = {device: element for device, element, _ in DEVICE_FACTS}
    images = {device: image for device, _, image in DEVICE_FACTS}
    seen = set()
    for seed in range(600):
        question = generate("phys.optics_fluency", random.Random(seed))
        stem = _text(question.stem)
        device = next(name for name in elements if name in stem)
        seen.add(device)
        expected = elements[device] if "ตัวสร้างภาพ" in stem else images[device]
        assert _answer(question) == expected, stem
    assert seen == set(elements)

    causes = dict(LIGHT_PHENOMENA)
    lenses = {name: (lens, reason) for name, _, lens, reason in VISION_DEFECTS}
    for seed in range(600):
        question = generate("phys.optics_application", random.Random(seed))
        stem = _text(question.stem)
        phenomenon = next((name for name in causes if name in stem), None)
        if phenomenon is not None:
            assert _answer(question) == causes[phenomenon], stem
            continue
        defect = next(name for name in lenses if f"ภาวะ{name}" in stem)
        lens, reason = lenses[defect]
        assert _answer(question) == f"{lens} เพราะ{reason}", stem


@pytest.mark.slow
def test_thousand_seed_quality_gate_has_four_distinct_choices_each():
    minimums = {
        "phys.mirror_image_foundation": 8,
        "phys.mirror_image_application": 100,
        "phys.lens_image_foundation": 8,
        "phys.lens_image_application": 100,
        "phys.optics_fluency": 12,
        "phys.optics_application": 8,
        "phys.illuminance_foundation": 10,
        "phys.illuminance_application": 20,
    }
    for key, minimum in minimums.items():
        signatures = set()
        for seed in range(1000):
            question = generate(key, random.Random(seed))
            choices = [_text(choice.content) for choice in question.choices]
            assert len(choices) == len(set(choices)) == 4, (key, seed)
            assert choices[question.answer]
            assert question.hint
            signatures.add((_text(question.stem), choices[question.answer]))
        assert len(signatures) >= minimum, (key, len(signatures))
