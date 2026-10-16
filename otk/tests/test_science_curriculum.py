"""IPST science filing, compatibility, and mapping-integrity checks."""

from __future__ import annotations

import csv
from collections import Counter, defaultdict
from pathlib import Path

from otk.core import REGISTRY, catalog, generate, types_in
from otk.core.curriculum import ADDITIONAL, BASIC, CURRICULUM_VERSION, SUPPLEMENTAL
from otk.core.curriculum_science import (
    SCIENCE_BASELINE_KEYS,
    SCIENCE_BIOLOGY_CLOSURE_KEYS,
    SCIENCE_KEYS,
    SCIENCE_WAVE_C_KEYS,
    SCIENCE_WAVE_D_KEYS,
    SCIENCE_WAVE_E_KEYS,
    SCIENCE_WAVE_F_KEYS,
    SCIENCE_WAVE_G_KEYS,
    SCIENCE_WAVE_I_KEYS,
    SCIENCE_TECHNOLOGY_KEYS,
    SCIENCE_PILOT_KEYS,
    SCIENCE_PROCESS_SKILL_KEYS,
    SCIENCE_DIAGRAM_KEYS,
    SCIENCE_PLACEMENTS,
    SCIENCE_SUCCESSOR_KEYS,
    SCIENCE_WAVE_B_KEYS,
    SCIENCE_WAVE_KEYS,
)


ROOT = Path(__file__).resolve().parents[2]


def _science_catalog() -> list[dict]:
    return [row for row in catalog() if row["key"] in SCIENCE_KEYS]


def _approved_mapping() -> dict[str, dict]:
    """The reviewed filing in ``science_ipst_mapping.csv``, keyed by set key."""
    with (ROOT / "docs/for_admin/science_ipst_mapping.csv").open(
        encoding="utf-8-sig", newline="",
    ) as handle:
        return {row["key"]: row for row in csv.DictReader(handle)}


def test_every_approved_science_set_has_stable_curriculum_filing():
    rows = _science_catalog()
    # These three cohorts are closed and their sizes are the point: the 95 legacy
    # keys, the 11 successors Phase 2 split out of them, and the 15 Phase 3
    # pilots. Nothing may ever join them.
    assert len(SCIENCE_BASELINE_KEYS) == 95
    assert len(SCIENCE_SUCCESSOR_KEYS) == 11
    assert len(SCIENCE_PILOT_KEYS) == 15
    # The Wave A cohort grows a slice at a time, so its size is checked against
    # the reviewed mapping instead of a literal that would need hand-editing here
    # on every slice. That is also the stronger check: a literal only says how
    # many sets exist, while this fails if a set is registered in code and never
    # filed for review, or filed and never registered.
    assert set(SCIENCE_KEYS) == set(_approved_mapping())
    assert len(rows) == len(SCIENCE_KEYS)
    additive = (SCIENCE_SUCCESSOR_KEYS | SCIENCE_PILOT_KEYS | SCIENCE_WAVE_KEYS
                | SCIENCE_WAVE_B_KEYS | SCIENCE_BIOLOGY_CLOSURE_KEYS
                | SCIENCE_WAVE_C_KEYS | SCIENCE_WAVE_D_KEYS | SCIENCE_WAVE_E_KEYS
                | SCIENCE_WAVE_F_KEYS | SCIENCE_WAVE_G_KEYS
                | SCIENCE_TECHNOLOGY_KEYS | SCIENCE_WAVE_I_KEYS
                | SCIENCE_PROCESS_SKILL_KEYS | SCIENCE_DIAGRAM_KEYS)
    # Every additive cohort must be disjoint from every other, or a wave's review
    # gate could be read as covering sets from a wave that never went through one.
    cohorts = (SCIENCE_SUCCESSOR_KEYS, SCIENCE_PILOT_KEYS, SCIENCE_WAVE_KEYS,
               SCIENCE_WAVE_B_KEYS, SCIENCE_BIOLOGY_CLOSURE_KEYS,
               SCIENCE_WAVE_C_KEYS, SCIENCE_WAVE_D_KEYS, SCIENCE_WAVE_E_KEYS,
               SCIENCE_WAVE_F_KEYS, SCIENCE_WAVE_G_KEYS,
               SCIENCE_TECHNOLOGY_KEYS, SCIENCE_WAVE_I_KEYS,
               SCIENCE_PROCESS_SKILL_KEYS, SCIENCE_DIAGRAM_KEYS)
    assert sum(len(cohort) for cohort in cohorts) == len(additive)
    assert not SCIENCE_BASELINE_KEYS & additive
    assert SCIENCE_BASELINE_KEYS | additive == set(SCIENCE_KEYS)
    assert {row["key"] for row in rows} == set(SCIENCE_KEYS)
    assert set(SCIENCE_KEYS) <= set(REGISTRY)

    for row in rows:
        assert row["curriculum_node_id"].startswith("th-sci-2560-")
        assert row["legacy_level"]
        assert row["strand"]
        if row["course_type"] in {BASIC, ADDITIONAL}:
            assert row["curriculum_version"] == CURRICULUM_VERSION
            assert row["standard_code"]
            assert row["indicator_codes"]


def test_science_filing_preserves_registry_identity_and_content_metadata():
    by_key = {row["key"]: row for row in _science_catalog()}
    for key, spec in REGISTRY.items():
        if key not in SCIENCE_KEYS:
            continue
        row = by_key[key]
        assert row["key"] == key
        assert row["display_name"] == spec.display_name_for("th")
        assert row["subject"] == spec.subject
        assert row["legacy_level"] == spec.level_for()
        assert row["topic"] == spec.topic
        assert row["params"] == spec.params()
        assert row["learning_stage"] == spec.learning_stage
        assert row["learning_stage_key"] == spec.learning_stage_key
        assert row["source_key"] == (spec.source_key or key)


COURSE_TYPE_FROM_CSV = {
    "core": BASIC, "additional": ADDITIONAL, "supplemental": SUPPLEMENTAL,
}


def test_science_course_and_mapping_status_counts_match_the_approved_mapping():
    """Every set is filed under the course type and mapping status it was reviewed under.

    Counted against the CSV rather than against literals. Literal totals here had
    to be hand-edited on every Wave A slice, and they could not tell a genuine
    re-filing from a typo — both just move a number.
    """
    rows = _science_catalog()
    approved = _approved_mapping()
    assert Counter(row["course_type"] for row in rows) == Counter(
        COURSE_TYPE_FROM_CSV[row["course_type"]] for row in approved.values())
    assert Counter(row["mapping_status"] for row in rows) == Counter(
        row["mapping_status"] for row in approved.values())
    # Every course type in use is one of the three, so a new value cannot slip
    # through by matching itself on both sides of the comparison above.
    assert set(Counter(row["course_type"] for row in rows)) == {
        BASIC, ADDITIONAL, SUPPLEMENTAL}
    assert set(row["mapping_status"] for row in rows) == {
        "exact", "standard_scope", "additional_outcome", "outside_scope"}


def test_known_science_grade_and_course_corrections_are_effective():
    by_key = {row["key"]: row for row in _science_catalog()}
    assert by_key["chem.phase_change"]["level"] == "ป.5"
    assert by_key["chem.phase_change"]["legacy_level"] == "ป.6"
    assert by_key["ecology.symbiosis"]["level"] == "ม.3"
    assert by_key["ecology.symbiosis"]["legacy_level"] == "ป.6"
    assert by_key["chem.nuclide"]["course_type"] == ADDITIONAL
    assert by_key["chem.nuclide"]["level"] == "ม.4"
    assert by_key["elec.resistivity"]["course_type"] == ADDITIONAL
    assert by_key["elec.resistivity"]["level"] == "ม.5"


def test_effective_science_level_drives_generation_and_pool_selection():
    key = "ecology.symbiosis"
    assert key in types_in(subject="ชีวะ", level="ม.3", topic="สิ่งมีชีวิตกับสิ่งแวดล้อม")
    assert key not in types_in(subject="ชีวะ", level="ป.6", topic="สิ่งมีชีวิตกับสิ่งแวดล้อม")
    assert generate(key).level == "ม.3"


def test_science_node_ids_group_only_identical_curriculum_nodes():
    nodes: dict[str, set[tuple]] = defaultdict(set)
    for row in _science_catalog():
        nodes[row["curriculum_node_id"]].add((
            row["course_type"], row["level"], row["strand_code"],
            row["standard_code"], row["unit"],
        ))
    assert all(len(placements) == 1 for placements in nodes.values())

    by_key = {row["key"]: row for row in _science_catalog()}
    assert (
        by_key["chem.symbol_to_name"]["curriculum_node_id"]
        == by_key["chem.name_to_symbol"]["curriculum_node_id"]
    )


def test_code_mapping_matches_approved_csv_and_official_outcome_index():
    approved = _approved_mapping()
    with (ROOT / "docs/for_admin/science_ipst_outcomes.csv").open(
        encoding="utf-8-sig", newline="",
    ) as handle:
        official_codes = {row["outcome_code"] for row in csv.DictReader(handle)}

    assert set(approved) == set(SCIENCE_PLACEMENTS)
    for key, spec in SCIENCE_PLACEMENTS.items():
        row = approved[key]
        assert spec.course_type == COURSE_TYPE_FROM_CSV[row["course_type"]], key
        assert spec.level == row["mapped_level"], key
        assert spec.strand_code == row["strand_code"], key
        assert spec.standard_code == row["standard_code"], key
        assert spec.unit == row["curriculum_topic"], key
        assert spec.mapping_status == row["mapping_status"], key
        # Compared against the CSV, not merely against the official index. A code
        # can be perfectly official and still not be the one this set was
        # reviewed under, which a subset check against the index cannot see.
        listed = [code for code in row["indicator_codes"].split("; ") if code]
        assert list(spec.indicator_codes) == listed, key
        assert set(spec.indicator_codes) <= official_codes, key
