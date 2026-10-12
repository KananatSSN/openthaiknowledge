"""Acceptance tests for Wave A slice 7 — the last three Wave A topics."""

from __future__ import annotations

import csv
import random
import re
from pathlib import Path

import pytest

from otk.core import catalog, generate
from otk.core.curriculum_science import SCIENCE_BASELINE_KEYS, SCIENCE_WAVE_KEYS
from otk.sets.physics.m5.refraction import (
    CRITICAL_PAIRS,
    DEPTH_SETUPS,
    SNELL_SETUPS,
    RefractionIndexFoundation,
)
from otk.sets.physics.m3.em_spectrum import EM_BANDS, EM_NAMES, EM_SCENARIOS
from otk.sets.physics.m5.spherical_mirrors import (
    MIRROR_SETUPS,
    SphericalMirrorFoundation,
    image_distance,
)


NEW_KEYS = {
    "phys.em_spectrum_fluency": (["ว 2.3 ม.3/11", "ว 2.3 ม.3/12"], 2),
    "phys.em_spectrum_application": (["ว 2.3 ม.3/11", "ว 2.3 ม.3/12"], 3),
    "phys.spherical_mirror_foundation": (["ฟิสิกส์เพิ่มเติม 2 ม.5/9"], 1),
    "phys.spherical_mirror_application": (["ฟิสิกส์เพิ่มเติม 2 ม.5/9"], 3),
    "phys.refraction_index_foundation": (["ฟิสิกส์เพิ่มเติม 2 ม.5/10"], 1),
    "phys.refraction_index_application": (["ฟิสิกส์เพิ่มเติม 2 ม.5/10"], 3),
}
COMPLETED = ("ว 2.3 ม.3/11", "ว 2.3 ม.3/12",
             "ฟิสิกส์เพิ่มเติม 2 ม.5/9", "ฟิสิกส์เพิ่มเติม 2 ม.5/10")
ROOT = Path(__file__).resolve().parents[2]


def _text(blocks) -> str:
    return " ".join(block.text for block in blocks if block.kind == "text")


def _choice(choice) -> str:
    return _text(choice.content) or " ".join(
        block.tex for block in choice.content if block.kind == "math")


def _answer(question) -> str:
    return _choice(question.choices[question.answer])


def test_slice_seven_is_additive_and_correctly_staged():
    rows = {row["key"]: row for row in catalog()}
    assert set(NEW_KEYS) <= set(SCIENCE_WAVE_KEYS)
    assert not set(NEW_KEYS) & SCIENCE_BASELINE_KEYS
    for key, (outcomes, stage) in NEW_KEYS.items():
        assert rows[key]["learning_stage"] == stage, key
        assert rows[key]["indicator_codes"] == outcomes, key


def test_each_completed_topic_holds_all_three_stages():
    rows = [row for row in catalog() if row["curriculum_node_id"]]
    for key, (outcomes, _) in NEW_KEYS.items():
        node = next(row["curriculum_node_id"] for row in rows if row["key"] == key)
        stages = {r["learning_stage"] for r in rows if r["curriculum_node_id"] == node}
        assert stages == {1, 2, 3}, (outcomes, sorted(stages))


def test_completed_outcomes_are_recorded_in_the_matrix():
    with (ROOT / "docs/for_admin/science_ipst_outcomes.csv").open(
        encoding="utf-8-sig", newline="",
    ) as handle:
        rows = {row["outcome_code"]: row for row in csv.DictReader(handle)}
    for outcome in COMPLETED:
        assert rows[outcome]["coverage_state"] == "complete", outcome
    for key, (outcomes, _) in NEW_KEYS.items():
        for outcome in outcomes:
            assert key in rows[outcome]["current_set_keys"].split("; "), (key, outcome)


def test_wave_a_leaves_no_incomplete_core_chemistry_or_physical_science_topic():
    """The closing condition for Wave A, asserted rather than asserted about."""
    rows = [row for row in catalog() if row["curriculum_node_id"]]
    stages: dict[str, set[int]] = {}
    course: dict[str, str] = {}
    strand: dict[str, str] = {}
    unit: dict[str, str] = {}
    for row in rows:
        node = row["curriculum_node_id"]
        stages.setdefault(node, set()).add(row["learning_stage"])
        course[node] = row["course_type"]
        strand[node] = row["strand_code"]
        unit[node] = row["unit"]
    physical = {"ว 2", "เคมีเพิ่มเติม", "ฟิสิกส์เพิ่มเติม"}
    incomplete = sorted(
        unit[node] for node, seen in stages.items()
        if strand[node] in physical and seen != {1, 2, 3}
    )
    assert incomplete == [], incomplete


def test_the_spectrum_is_ordered_once_and_read_the_same_way_everywhere():
    order = {name: index for index, name in enumerate(EM_NAMES)}
    assert len(order) == len(EM_BANDS) == 7
    assert EM_NAMES[0] == "คลื่นวิทยุ" and EM_NAMES[-1] == "รังสีแกมมา"
    checked = {"extreme": 0, "higher": 0, "hazard": 0}
    hazards = {hazard: name for name, _, hazard in EM_BANDS}
    for seed in range(900):
        question = generate("phys.em_spectrum_fluency", random.Random(seed))
        stem = _text(question.stem)
        names = [_choice(choice) for choice in question.choices]
        assert set(names) <= set(order), stem
        answer = _answer(question)
        if "คลื่นใดมี" in stem:
            checked["extreme"] += 1
            positions = [order[name] for name in names]
            wanted = min(positions) if "ความยาวคลื่น" in stem else max(positions)
            assert order[answer] == wanted, stem
        elif "มีความถี่สูงกว่า" in stem:
            checked["higher"] += 1
            reference = next(name for name in order if f"สูงกว่า{name}" in stem)
            higher = [name for name in names if order[name] > order[reference]]
            assert higher == [answer], stem
        else:
            checked["hazard"] += 1
            hazard = next(text for text in hazards if text in stem)
            assert answer == hazards[hazard], stem
    assert all(checked.values()), checked


def test_every_em_scenario_is_settled_by_a_real_band():
    for stem, correct, wrongs in EM_SCENARIOS:
        assert len(wrongs) >= 3 and len(set(wrongs)) == len(wrongs), stem
        assert correct not in wrongs, stem
        # Either the item asks which band to use — then every choice names one —
        # or it names the band in the stem and asks what that band does.
        named = [choice for choice in (correct, *wrongs)
                 if any(name in choice for name in EM_NAMES)]
        assert len(named) == 4 or any(name in stem for name in EM_NAMES), stem


def test_every_mirror_setup_puts_a_real_image_at_a_whole_distance():
    for focal, distance in MIRROR_SETUPS:
        assert distance > focal, (focal, distance)
        assert focal * distance % (distance - focal) == 0, (focal, distance)
        image = image_distance(focal, distance)
        assert image != distance, (focal, distance)
        # 1/f = 1/s + 1/s', re-derived rather than trusted.
        assert distance * image == focal * (distance + image), (focal, distance)


def test_mirror_answers_are_rebuilt_from_the_numbers_in_the_stem():
    checked = {"distance": 0, "height": 0, "focal": 0}
    for seed in range(900):
        question = generate("phys.spherical_mirror_application", random.Random(seed))
        stem = _text(question.stem)
        found = re.search(
            r"วางวัตถุห่างจากกระจกเงาเว้าที่มีความยาวโฟกัส (\d+) เซนติเมตร "
            r"เป็นระยะ (\d+) เซนติเมตร", stem)
        if found:
            checked["distance"] += 1
            focal, distance = (int(value) for value in found.groups())
            assert _answer(question) == str(image_distance(focal, distance)), stem
            continue
        found = re.search(
            r"วางวัตถุสูง (\d+) เซนติเมตร .*?ความยาวโฟกัส (\d+) เซนติเมตร "
            r"เป็นระยะ (\d+) เซนติเมตร", stem)
        if found:
            checked["height"] += 1
            height, focal, distance = (int(value) for value in found.groups())
            image = image_distance(focal, distance)
            assert height * image % distance == 0, stem
            assert _answer(question) == str(height * image // distance), stem
            continue
        found = re.search(
            r"ห่างจากกระจกเงาเว้า (\d+) เซนติเมตร และเกิดภาพจริง "
            r"ห่างจากกระจก (\d+) เซนติเมตร", stem)
        assert found, stem
        checked["focal"] += 1
        distance, image = (int(value) for value in found.groups())
        assert _answer(question) == str(
            distance * image // (distance + image)), stem
    assert all(checked.values()), checked


def test_no_refraction_row_states_an_index_below_one_or_a_repeating_decimal():
    """No medium slows light less than a vacuum, and 1.33333 is not a measurement."""
    for (top, bottom), real in DEPTH_SETUPS:
        assert top > bottom >= 1, (top, bottom)
        assert real * bottom % top == 0, (top, bottom, real)
        assert (top / bottom) == round(top / bottom, 2), (top, bottom)
    for dense, sparse in CRITICAL_PAIRS:
        assert dense > sparse >= 1.0, (dense, sparse)
        # Compared with a tolerance: 1.2/1.5 is 0.7999999999999999 in binary
        # floating point, and what matters is that it prints as a short decimal.
        assert abs(sparse / dense - round(sparse / dense, 4)) < 1e-9, (dense, sparse)
    for first, sine_in, second in SNELL_SETUPS:
        assert first >= 1.0 and second >= 1.0, (first, second)
        refracted = first * sine_in / second
        assert 0 < refracted <= 1, (first, sine_in, second)
        assert abs(refracted - round(refracted, 4)) < 1e-9, (first, sine_in, second)


def test_refraction_answers_are_rebuilt_from_the_numbers_in_the_stem():
    checked = {"depth": 0, "critical": 0, "snell": 0}
    for seed in range(900):
        question = generate("phys.refraction_index_application", random.Random(seed))
        stem = _text(question.stem)
        found = re.search(
            r"ดรรชนีหักเห ([\d.]+) ลึกจริง (\d+) เซนติเมตร", stem)
        if found:
            checked["depth"] += 1
            index, real = float(found.group(1)), int(found.group(2))
            assert _answer(question) == f"{round(real / index):g}", stem
            continue
        found = re.search(
            r"ดรรชนีหักเห ([\d.]+) และจะออกสู่ตัวกลางที่มีดรรชนีหักเห ([\d.]+)", stem)
        if found:
            checked["critical"] += 1
            dense, sparse = (float(value) for value in found.groups())
            assert _answer(question) == f"{sparse / dense:g}", stem
            continue
        found = re.search(
            r"ดรรชนีหักเห ([\d.]+) เข้าสู่ตัวกลางที่มีดรรชนีหักเห ([\d.]+) "
            r"ถ้าไซน์ของมุมตกกระทบเท่ากับ ([\d.]+)", stem)
        assert found, stem
        checked["snell"] += 1
        first, second, sine_in = (float(value) for value in found.groups())
        assert _answer(question) == f"{round(first * sine_in / second, 4):g}", stem
    assert all(checked.values()), checked


def test_concept_banks_offer_three_distractors_and_no_repeated_stem():
    for cls in (SphericalMirrorFoundation, RefractionIndexFoundation):
        stems = [item.stem for item in cls.ITEMS]
        assert len(stems) == len(set(stems)) >= 6, cls.__name__
        for item in cls.ITEMS:
            assert len(item.distractors) >= 3, item.stem
            assert item.correct not in item.distractors, item.stem
            assert len(set(item.distractors)) == len(item.distractors), item.stem


@pytest.mark.slow
def test_thousand_seed_quality_gate_has_four_distinct_choices_each():
    minimums = {
        "phys.em_spectrum_fluency": 18,
        "phys.em_spectrum_application": 6,
        "phys.spherical_mirror_foundation": 7,
        "phys.spherical_mirror_application": 100,
        "phys.refraction_index_foundation": 7,
        "phys.refraction_index_application": 25,
    }
    for key, minimum in minimums.items():
        signatures = set()
        for seed in range(1000):
            question = generate(key, random.Random(seed))
            choices = [_choice(choice) for choice in question.choices]
            assert len(choices) == len(set(choices)) == 4, (key, seed)
            assert choices[question.answer]
            signatures.add((_text(question.stem), choices[question.answer]))
        assert len(signatures) >= minimum, (key, len(signatures))
