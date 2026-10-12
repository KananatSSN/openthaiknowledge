"""Phase 5 Wave I: the four indicators the task queue found with no set."""

from __future__ import annotations

import re
from random import Random

import pytest

from otk.core import REGISTRY, generate
from otk.core.curriculum_science import (REVIEW_PENDING, SCIENCE_PLACEMENTS,
                                         SCIENCE_WAVE_I_APPROVED_KEYS, SCIENCE_WAVE_I_KEYS)
from otk.core.provenance import provenance
from otk.sets.chemistry.m6.plastic_test import BURNING, IN_BRINE, IN_WATER
from otk.sets.biology.m1.microscope_use import DIRECTIONS, MICROSCOPE_PARTS
from otk.sets.chemistry.m6.ester_test import ESTER_SMELLS

SEEDS = 200
STAGES = ("foundation", "fluency", "application")
INDICATORS = {
    "ว 1.2 ม.1/2": "cell.microscope_use",
    "เคมีเพิ่มเติม 2 ม.5/4": "chem.rate_experiment",
    "เคมีเพิ่มเติม 1 ม.6/9": "chem.ester_test",
    "เคมีเพิ่มเติม 1 ม.6/13": "chem.plastic_test",
}
KEYS = [f"{prefix}_{stage}" for prefix in INDICATORS.values() for stage in STAGES]


def _text(blocks) -> str:
    return " ".join(getattr(b, "text", getattr(b, "tex", "")) for b in blocks)


def _draws(key):
    for seed in range(SEEDS):
        q = generate(key, Random(seed))
        yield _text(q.stem), _text(q.choices[q.answer].content), [_text(c.content) for c in q.choices]


# ── filing ────────────────────────────────────────────────────────────────────

def test_the_cohort_is_exactly_these_sets_and_awaits_review():
    assert set(KEYS) == SCIENCE_WAVE_I_KEYS
    pending = set().union(*REVIEW_PENDING.values())
    assert SCIENCE_WAVE_I_KEYS - SCIENCE_WAVE_I_APPROVED_KEYS <= pending


@pytest.mark.parametrize("code,prefix", INDICATORS.items())
def test_each_indicator_holds_three_stages_in_one_unit(code, prefix):
    specs = [SCIENCE_PLACEMENTS[f"{prefix}_{stage}"] for stage in STAGES]
    assert {spec.indicator_codes for spec in specs} == {(code,)}
    assert len({spec.unit for spec in specs}) == 1
    assert [REGISTRY[f"{prefix}_{stage}"].learning_stage for stage in STAGES] == [1, 2, 3]


@pytest.mark.parametrize("key", KEYS)
def test_every_set_is_original_and_draws_distinct_choices(key):
    assert provenance(key).kind == "original"
    for _, _, choices in _draws(key):
        assert len(choices) == len(set(choices)) >= 3


# ── ว 1.2 ม.1/2 ────────────────────────────────────────────────────────────────

def test_microscope_parts_and_jobs_match():
    jobs = {job: part for part, job in MICROSCOPE_PARTS.items()}
    for stem, answer, _ in _draws("cell.microscope_use_foundation"):
        if answer in MICROSCOPE_PARTS:
            assert MICROSCOPE_PARTS[answer] in stem
        else:
            assert jobs[answer] in stem


def test_total_magnification_is_the_product():
    for stem, answer, _ in _draws("cell.microscope_use_fluency"):
        numbers = [int(n) for n in re.findall(r"\d+", stem)]
        value = int(answer.replace(",", "").split()[0]) if re.match(r"\d", answer) else None
        if "ทั้งหมดกี่เท่า" in stem:
            assert value == numbers[0] * numbers[1]
        elif "เลนส์ใกล้วัตถุกำลังขยายกี่เท่า" in stem:
            assert value * numbers[1] == numbers[0]


def test_the_image_moves_against_the_slide_and_cell_counts_shrink():
    for stem, answer, _ in _draws("cell.microscope_use_application"):
        if "ต้องเลื่อนสไลด์ไปทางใด" in stem:
            seen = next(d for d in DIRECTIONS if f"อยู่ทาง{d}ของภาพ" in stem)
            assert answer == f"ไปทาง{seen}"
        elif "ภาพที่เห็นจะเคลื่อนไปทางใด" in stem:
            moved = next(d for d in DIRECTIONS if f"เลื่อนสไลด์ไปทาง{d} " in stem)
            assert answer == f"ไปทาง{DIRECTIONS[moved]}"
        elif "กี่เซลล์" in stem:
            low, count, high = (int(n) for n in re.findall(r"\d+", stem))
            factor = high // low
            expected = count // factor if "เรียงเป็นแถว" in stem else count // factor ** 2
            assert int(re.findall(r"\d+", answer)[0]) == expected


# ── เคมีเพิ่มเติม 2 ม.5/4 ──────────────────────────────────────────────────────────

def test_the_fastest_run_is_the_shortest_time_and_hotter_is_faster():
    for stem, answer, _ in _draws("chem.rate_experiment_fluency"):
        runs = re.findall(r"การทดลอง ([ABC]): (\d+) °C ใช้เวลา (\d+) s", stem)
        by_temp = sorted(runs, key=lambda r: int(r[1]))
        assert [int(r[2]) for r in by_temp] == sorted((int(r[2]) for r in runs), reverse=True)
        if "สูงที่สุด" in stem:
            assert answer == f"การทดลอง {min(runs, key=lambda r: int(r[2]))[0]}"


# ── เคมีเพิ่มเติม 1 ม.6/9 ──────────────────────────────────────────────────────────

def test_an_ester_comes_from_its_own_acid_and_alcohol():
    for stem, answer, _ in _draws("chem.ester_test_application"):
        for acid, alcohol, ester, smell in ESTER_SMELLS:
            if f"กลิ่น{smell} ต้องใช้" in stem:
                assert answer == f"{acid} กับ{alcohol}"
            if f"อุ่น{acid}กับ{alcohol}โดย" in stem:
                assert answer == f"{ester} กลิ่นคล้าย{smell}"


# ── เคมีเพิ่มเติม 1 ม.6/13 ─────────────────────────────────────────────────────────

def test_plastics_are_named_by_their_tests():
    for stem, answer, choices in _draws("chem.plastic_test_foundation"):
        for plastic, flame in BURNING.items():
            if flame in stem:
                assert answer == plastic
                assert "PET" not in " ".join(choices)  # it burns like PS: never offered
    words = {True: "ลอย", False: "จม"}
    for stem, answer, _ in _draws("chem.plastic_test_fluency"):
        if "ลอยหรือจม" in stem:
            plastic = next(p for p in IN_WATER if p in stem)
            table = IN_BRINE if "น้ำเกลือ" in stem else IN_WATER
            assert answer == words[table[plastic]]
        else:
            fits = [p for p in IN_WATER if f"{words[IN_WATER[p]]}ในน้ำ และ{words[IN_BRINE[p]]}ในน้ำเกลือ" in stem]
            assert answer == " หรือ ".join(sorted(fits))
