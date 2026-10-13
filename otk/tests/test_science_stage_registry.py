"""Learning-stage bookkeeping for every science subject, checked in one place.

This used to be five near-identical copies, one per subject, each in its own
``test_<subject>_content_review.py``. They drifted: a wave that added sets to a
subject bumped that subject's copy and left the others, and a wave that touched
two subjects bumped one and was caught by the other only by luck. Wave G slice 2
hit exactly that — the physics copy was updated, the earth-science copy was not,
and the full suite was the first thing to notice.

So the subject list is **derived from the registry** rather than written down.
Adding a sixth science subject fails ``test_every_science_subject_has_a_reviewed
_stage_map`` with the subject's name, instead of silently checking four of five.

**There are no literal totals here.** A number like ``len(physics) == 301`` has
to be hand-edited on every slice, and it cannot tell a genuine re-filing from a
typo — both just move it. Every check below is structural: the maps must cover
exactly the registry, agree with the reviewed mapping CSV, and agree with the
catalog. ``test_science_curriculum.py`` made the same move for the same reason,
and ``test_refactor_characterization.py`` keeps the one deliberate literal —
``len(REGISTRY)`` — which exists to make any registry change visible at all.

Subject-specific content checks stay in their own files; only this bookkeeping
moved.
"""

from __future__ import annotations

import csv
from functools import lru_cache
from pathlib import Path

import pytest

from otk.core import REGISTRY, catalog
from otk.sets._support.science_stages import (
    REVIEWED_ASTRONOMY_STAGES,
    REVIEWED_BIOLOGY_STAGES,
    REVIEWED_CHEMISTRY_STAGES,
    REVIEWED_COMPUTING_STAGES,
    REVIEWED_EARTH_SCIENCE_STAGES,
    REVIEWED_GENERAL_SCIENCE_STAGES,
    REVIEWED_PHYSICS_STAGES,
    REVIEWED_TECHNOLOGY_DESIGN_STAGES,
)


ROOT = Path(__file__).resolve().parents[2]

#: Every subject that goes through the IPST science review, and the map that
#: records its reviewed stages.
REVIEWED_BY_SUBJECT = {
    "ฟิสิกส์": REVIEWED_PHYSICS_STAGES,
    "เคมี": REVIEWED_CHEMISTRY_STAGES,
    "ชีวะ": REVIEWED_BIOLOGY_STAGES,
    "ธรณีวิทยา": REVIEWED_EARTH_SCIENCE_STAGES,
    "ดาราศาสตร์": REVIEWED_ASTRONOMY_STAGES,
    # Added with Wave G slice 4. ทักษะกระบวนการทางวิทยาศาสตร์ is not a content
    # science; this row is the deliberate edit that
    # test_every_science_subject_has_a_reviewed_stage_map exists to demand.
    "วิทยาศาสตร์ทั่วไป": REVIEWED_GENERAL_SCIENCE_STAGES,
    # Phase 7 — ว 4.1 as its own course.
    "การออกแบบและเทคโนโลยี": REVIEWED_TECHNOLOGY_DESIGN_STAGES,
    # ... and ว 4.2 as the second.
    "วิทยาการคำนวณ": REVIEWED_COMPUTING_STAGES,
}

#: Subjects outside the science expansion, which have no reviewed-stage map.
#: Listed rather than inferred so that adding one is a deliberate edit here.
NON_SCIENCE_SUBJECTS = frozenset({"คณิตศาสตร์", "ภูมิศาสตร์"})

SUBJECTS = sorted(REVIEWED_BY_SUBJECT)


def _keys_for(subject: str) -> set[str]:
    return {key for key, spec in REGISTRY.items() if spec.subject == subject}


@lru_cache(maxsize=1)
def _approved_stages() -> dict[str, dict[str, int]]:
    """The reviewed ``proposed_stage`` per subject, from the mapping CSV.

    Read once: the file is a thousand rows and every subject wants a slice of it.
    """
    by_subject: dict[str, dict[str, int]] = {}
    with (ROOT / "docs/for_admin/science_ipst_mapping.csv").open(
        encoding="utf-8-sig", newline="",
    ) as handle:
        for row in csv.DictReader(handle):
            by_subject.setdefault(row["legacy_subject"], {})[row["key"]] = (
                int(row["proposed_stage"]))
    return by_subject


@lru_cache(maxsize=1)
def _catalog_stages() -> dict[str, int]:
    return {row["key"]: row["learning_stage"] for row in catalog()}


# ── the subject list itself ──────────────────────────────────────────────────

def test_every_science_subject_has_a_reviewed_stage_map():
    """The check the five separate copies could not make.

    A new science subject appearing in the registry fails here by name, rather
    than being quietly skipped by tests that each know one subject.
    """
    registry_subjects = {spec.subject for spec in REGISTRY.values()}
    unreviewed = registry_subjects - set(REVIEWED_BY_SUBJECT) - NON_SCIENCE_SUBJECTS
    assert not unreviewed, f"no reviewed-stage map for {sorted(unreviewed)}"
    assert set(REVIEWED_BY_SUBJECT) <= registry_subjects


def test_the_mapping_csv_covers_the_same_subjects():
    """A subject filed for review but never registered would be invisible otherwise."""
    assert set(_approved_stages()) == set(REVIEWED_BY_SUBJECT)


def test_the_reviewed_maps_partition_the_science_registry():
    """Every science set has exactly one reviewed stage — no gaps, no doubles."""
    science = {key for key, spec in REGISTRY.items()
               if spec.subject not in NON_SCIENCE_SUBJECTS}
    reviewed = [set(stages) for stages in REVIEWED_BY_SUBJECT.values()]
    assert set().union(*reviewed) == science
    assert sum(len(keys) for keys in reviewed) == len(science)


# ── per subject ──────────────────────────────────────────────────────────────

@pytest.mark.parametrize("subject", SUBJECTS)
def test_a_subjects_reviewed_map_is_exactly_its_registry_keys(subject):
    assert set(REVIEWED_BY_SUBJECT[subject]) == _keys_for(subject)


@pytest.mark.parametrize("subject", SUBJECTS)
def test_every_reviewed_stage_matches_the_approved_mapping(subject):
    assert _approved_stages()[subject] == REVIEWED_BY_SUBJECT[subject]


@pytest.mark.parametrize("subject", SUBJECTS)
def test_every_reviewed_stage_reaches_the_catalog(subject):
    """What a learner is served must be the stage that was reviewed."""
    published = _catalog_stages()
    for key, stage in REVIEWED_BY_SUBJECT[subject].items():
        assert published[key] == stage, key


@pytest.mark.parametrize("subject", SUBJECTS)
def test_every_stage_is_one_of_the_three(subject):
    assert set(REVIEWED_BY_SUBJECT[subject].values()) <= {1, 2, 3}
