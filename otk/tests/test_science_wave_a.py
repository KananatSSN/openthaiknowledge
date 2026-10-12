"""Acceptance tests for the Phase 5 Wave A chemistry and physical-science paths."""

from __future__ import annotations

import csv
import random
import re
from fractions import Fraction
from pathlib import Path

from otk.core import catalog, generate
from otk.core.curriculum_science import SCIENCE_BASELINE_KEYS, SCIENCE_WAVE_KEYS
from otk.sets.chemistry.m1.pure_substances_and_mixtures import PURE_EXAMPLES
from otk.sets.chemistry.p6.separating_mixtures import (
    SEPARATION_CASES,
    SEPARATION_METHODS,
    SEPARATION_PROBLEMS,
)
from otk.sets.physics.m3.series_and_parallel_circuits import SeriesParallelFluency


PATHS = {
    "ว 2.3 ม.3/4": (
        "elec.circuit_series_parallel_foundation",
        "elec.circuit_series_parallel_fluency",
        "elec.circuit_series_parallel_application",
    ),
    "ว 2.1 ม.1/4": (
        "chem.pure_mixture_foundation",
        "chem.pure_mixture_fluency",
        "chem.pure_mixture_application",
    ),
    "ว 2.1 ป.6/1": (
        "chem.separation_choice_foundation",
        "chem.separation_choice_fluency",
        "chem.separation_choice_application",
    ),
}
ROOT = Path(__file__).resolve().parents[2]


def _text(blocks) -> str:
    return " ".join(block.text for block in blocks if block.kind == "text")


def _answer(question) -> str:
    return _text(question.choices[question.answer].content)


def test_wave_a_is_additive_and_preserves_the_baseline():
    keys = {key for path in PATHS.values() for key in path}
    assert keys <= set(SCIENCE_WAVE_KEYS)
    assert len(SCIENCE_BASELINE_KEYS) == 95
    assert not keys & SCIENCE_BASELINE_KEYS


def test_each_wave_a_path_is_one_node_with_three_real_stages():
    rows = {row["key"]: row for row in catalog()}
    for indicator, path in PATHS.items():
        entries = [rows[key] for key in path]
        assert [row["learning_stage"] for row in entries] == [1, 2, 3], indicator
        assert len({row["curriculum_node_id"] for row in entries}) == 1, indicator
        assert all(row["indicator_codes"] == [indicator] for row in entries), indicator
        assert entries[1]["mapping_status"] == entries[2]["mapping_status"] == "exact"


def test_wave_a_outcomes_are_recorded_as_complete():
    with (ROOT / "docs/for_admin/science_ipst_outcomes.csv").open(
        encoding="utf-8-sig", newline="",
    ) as handle:
        rows = {row["outcome_code"]: row for row in csv.DictReader(handle)}
    for indicator, path in PATHS.items():
        row = rows[indicator]
        assert row["coverage_state"] == "complete", indicator
        keys = set(row["current_set_keys"].split("; "))
        assert set(path) <= keys, indicator
        assert row["current_set_count"] == str(len(keys)), indicator


def test_every_resistor_pair_has_a_whole_ohm_parallel_combination():
    """No question may depend on rounding a parallel combination."""
    for first, second in SeriesParallelFluency._PAIRS:
        assert Fraction(first * second, first + second).denominator == 1, (first, second)


def test_circuit_answers_are_independently_correct():
    seen = {"series": 0, "parallel": 0, "current": 0}
    for seed in range(600):
        question = generate(PATHS["ว 2.3 ม.3/4"][1], random.Random(seed))
        stem = _text(question.stem)
        answer = _answer(question)
        first, second = (int(value) for value in re.findall(r"(\d+) โอห์ม", stem))
        if "แหล่งกำเนิด" in stem:
            voltage = int(re.search(r"(\d+) V", stem).group(1))
            assert voltage % (first + second) == 0
            assert answer == f"{voltage // (first + second)} A"
            seen["current"] += 1
        elif "แบบอนุกรม" in stem:
            assert answer == f"{first + second} โอห์ม"
            seen["series"] += 1
        else:
            assert answer == f"{Fraction(first * second, first + second)} โอห์ม"
            seen["parallel"] += 1
    assert all(seen.values()), seen


def test_separation_foundation_only_offers_the_six_official_methods():
    """ว 2.1 ป.6/1 names exactly six methods; no question may invent a seventh."""
    assert len(SEPARATION_METHODS) == 6
    for seed in range(400):
        question = generate(PATHS["ว 2.1 ป.6/1"][0], random.Random(seed))
        choices = {_text(choice.content) for choice in question.choices}
        assert choices <= set(SEPARATION_METHODS)
    answers = {
        _answer(generate(PATHS["ว 2.1 ป.6/1"][0], random.Random(seed)))
        for seed in range(400)
    }
    assert answers == {method for _, method, _ in SEPARATION_CASES}


def test_separation_paths_reach_every_authored_case_and_problem():
    stems = [
        _text(generate(PATHS["ว 2.1 ป.6/1"][0], random.Random(seed)).stem)
        for seed in range(400)
    ]
    for case, _, _ in SEPARATION_CASES:
        assert any(case in stem for stem in stems), case
    problems = [
        _text(generate(PATHS["ว 2.1 ป.6/1"][2], random.Random(seed)).stem)
        for seed in range(500)
    ]
    for problem, _, _ in SEPARATION_PROBLEMS:
        assert any(problem in stem for stem in problems), problem


def test_pure_and_mixture_classification_matches_the_authored_table():
    answers: dict[str, set[str]] = {}
    for seed in range(500):
        question = generate(PATHS["ว 2.1 ม.1/4"][0], random.Random(seed))
        stem = _text(question.stem)
        for material, kind in PURE_EXAMPLES:
            if stem.startswith(material):
                answers.setdefault(material, set()).add(_answer(question))
                assert _answer(question) == kind, material
    assert len(answers) == len(PURE_EXAMPLES)


def test_fluency_and_application_read_measured_evidence():
    fluency = [
        _text(generate(PATHS["ว 2.1 ม.1/4"][1], random.Random(seed)).stem)
        for seed in range(300)
    ]
    assert any("อุณหภูมิคงที่ที่" in stem for stem in fluency)
    assert any("ค่อย ๆ เพิ่มจาก" in stem for stem in fluency)
    application = [
        _answer(generate(PATHS["ว 2.1 ม.1/4"][2], random.Random(seed)))
        for seed in range(300)
    ]
    assert any("ก เป็นสารบริสุทธิ์ และ ข เป็นสารผสม" == answer for answer in application)
    assert any("ไม่ถูกต้อง" in answer for answer in application)


def test_six_hundred_seed_quality_gate_has_four_distinct_choices_each():
    minimums = {
        "elec.circuit_series_parallel_foundation": 10,
        "elec.circuit_series_parallel_fluency": 40,
        "elec.circuit_series_parallel_application": 40,
        "chem.pure_mixture_foundation": 14,
        "chem.pure_mixture_fluency": 16,
        "chem.pure_mixture_application": 40,
        "chem.separation_choice_foundation": 12,
        "chem.separation_choice_fluency": 10,
        "chem.separation_choice_application": 16,
    }
    for key in minimums:
        signatures = set()
        for seed in range(600):
            question = generate(key, random.Random(seed))
            choices = [_text(choice.content) for choice in question.choices]
            assert len(choices) == len(set(choices)) == 4, (key, seed)
            assert choices[question.answer]
            assert question.hint
            signatures.add((_text(question.stem), choices[question.answer]))
        assert len(signatures) >= minimums[key], (key, len(signatures))
