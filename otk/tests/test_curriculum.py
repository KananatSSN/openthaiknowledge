"""IPST curriculum filing and backward-compatibility checks."""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

from otk.core import REGISTRY, catalog, generate, types_in
from otk.core.curriculum import (
    ADDITIONAL, BASIC, CURRICULUM_VERSION, ENRICHMENT, TERTIARY,
)


def _math_catalog() -> list[dict]:
    return [row for row in catalog() if row["subject"] == "คณิตศาสตร์"]


def test_every_math_set_has_a_stable_curriculum_filing():
    rows = _math_catalog()
    assert len(rows) == len({row["key"] for row in rows})
    assert len(rows) == sum(1 for key in REGISTRY if key.startswith("math."))
    for row in rows:
        assert row["course_type"]
        assert row["strand"]
        assert row["curriculum_node_id"].startswith("th-math-2560-")
        assert row["legacy_level"]
        if row["course_type"] in {BASIC, ADDITIONAL}:
            assert row["curriculum_version"] == CURRICULUM_VERSION
            assert row["strand_code"] in {"ค 1", "ค 2", "ค 3"}
            assert row["standard_code"].startswith(row["strand_code"])


def test_basic_sets_have_indicator_coverage_and_extras_are_separate():
    rows = _math_catalog()
    for row in rows:
        if row["course_type"] == BASIC:
            # no_indicator: taught at a grade the 2560 book gives no indicator.
            assert bool(row["indicator_codes"]) == (row["mapping_status"] != "no_indicator"), row["key"]
    counts = Counter(row["course_type"] for row in rows)
    assert counts[BASIC] > 0
    assert counts[ADDITIONAL] > 0
    assert counts[ENRICHMENT] == 469  # seven สอวน. sheets of 30, plus 259 further sets
    assert counts[TERTIARY] == 89


def test_known_ipst_standard_and_grade_corrections():
    by_key = {row["key"]: row for row in _math_catalog()}
    assert by_key["math.one_digit_plus_with_carry"]["standard_code"] == "ค 1.1"

    system = next(row for row in _math_catalog() if row["legacy_level"] == "ม.2" and row["topic"] == "ระบบสมการ")
    assert system["level"] == "ม.3"
    assert system["standard_code"] == "ค 1.3"
    assert system["indicator_codes"] == ["ค 1.3 ม.3/3"]

    assert all(row["level"] == "ม.5" for row in _math_catalog() if row["topic"] == "เวกเตอร์")
    assert all(
        row["level"] == "ม.6" for row in _math_catalog()
        if row["topic"] == "อนุพันธ์" and row["legacy_level"] in {"ม.5", "ม.6"}
    )


def test_effective_level_is_used_by_generation_and_pool_selection():
    key = next(
        row["key"] for row in _math_catalog()
        if row["legacy_level"] == "ม.2" and row["topic"] == "ระบบสมการ"
    )
    assert key in types_in(subject="คณิตศาสตร์", level="ม.3", topic="ระบบสมการ")
    assert key not in types_in(subject="คณิตศาสตร์", level="ม.2", topic="ระบบสมการ")
    assert generate(key).level == "ม.3"


def test_curriculum_node_id_groups_sets_without_replacing_topic_identity():
    rows = [row for row in _math_catalog() if row["level"] == "ป.1" and row["topic"] == "การบวก"]
    assert len(rows) > 1
    assert len({row["curriculum_node_id"] for row in rows}) == 1
    assert {row["topic"] for row in rows} == {"การบวก"}


_INDEX = Path(__file__).resolve().parents[2] / "docs/curriculum_sources/_md/indicators.jsonl"


def _official_codes() -> set[str]:
    with _INDEX.open(encoding="utf-8") as handle:
        return {json.loads(line)["code"] for line in handle if line.strip()}


def test_every_cited_indicator_exists_in_the_2560_books():
    """Each code, and each ``/*`` scope, must name indicators the book prints.

    The index is rebuilt from the official PDFs by scripts/curriculum_index.py.
    """
    official = _official_codes()
    wrong = set()
    for row in catalog():
        for code in row["indicator_codes"] or ():
            if code.endswith("/*"):
                if not any(c.startswith(code[:-1]) for c in official):
                    wrong.add(code)
            elif code not in official:
                wrong.add(code)
    assert not wrong, sorted(wrong)


def test_cited_indicators_sit_at_the_grade_they_are_filed_at():
    for row in catalog():
        for code in row["indicator_codes"] or ():
            grade = re.search(r"([ปม]\.\d)/", code)
            if row["course_type"] == BASIC and grade:
                assert grade.group(1) == row["level"], (row["key"], code)


def test_a_set_can_cite_an_exact_indicator_outside_its_topic_scope():
    """The protractor set cites ค 2.1 ป.4/2 but stays in its topic's node."""
    rows = {row["key"]: row for row in _math_catalog()}
    protractor = rows["math.construct_angle_protractor_p4"]
    neighbour = rows["math.classify_angle"]
    assert protractor["indicator_codes"] == ["ค 2.1 ป.4/2"]
    assert protractor["mapping_status"] == "exact"
    assert protractor["curriculum_node_id"] == neighbour["curriculum_node_id"]
    assert protractor["standard_code"] == neighbour["standard_code"] == "ค 2.2"
