"""The indicators left out of coverage are real, and really uncovered."""

from __future__ import annotations

import json
from pathlib import Path

from otk.core import catalog
from otk.core.indicator_exclusions import NOT_ASSESSABLE_BY_MCQ

INDEX = Path(__file__).resolve().parents[2] / "docs" / "curriculum_sources" / "_md" / "indicators.jsonl"


def test_every_excluded_code_is_an_official_indicator():
    official = {json.loads(line)["code"] for line in INDEX.read_text("utf-8").splitlines()}
    assert set(NOT_ASSESSABLE_BY_MCQ) <= official


def test_no_set_practises_an_excluded_indicator():
    cited = {code for row in catalog() for code in row.get("indicator_codes") or []}
    assert not cited & set(NOT_ASSESSABLE_BY_MCQ)
