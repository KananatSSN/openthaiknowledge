"""Compatibility facade for subject-specific curriculum placement.

The registry imports this module as its stable public boundary. Mathematics and
science keep independent explicit mappings behind it so either curriculum can be
reviewed without coupling their filing rules.
"""

from __future__ import annotations

from .curriculum_math import (
    ADDITIONAL,
    BASIC,
    COURSE_ORDER,
    CURRICULUM_VERSION,
    ENRICHMENT,
    MATH_SUBJECT,
    STRAND_ORDER,
    SUPPLEMENTAL,
    TERTIARY,
    CurriculumPlacement,
    curriculum_sort_fields as math_curriculum_sort_fields,
    placement_for as math_placement_for,
)
from .curriculum_science import (
    SCIENCE_KEYS,
    SCIENCE_SUBJECTS,
    SCIENCE_STRAND_ORDER,
    science_placement_for,
)

_ALL_STRAND_ORDER = (*STRAND_ORDER, *SCIENCE_STRAND_ORDER)


def curriculum_sort_fields(course: str, strand_code: str) -> tuple[int, int]:
    """Sort shared course labels and subject-specific strands deterministically."""
    course_rank, _ = math_curriculum_sort_fields(course, strand_code)
    strand_rank = (
        _ALL_STRAND_ORDER.index(strand_code)
        if strand_code in _ALL_STRAND_ORDER else len(_ALL_STRAND_ORDER)
    )
    return course_rank, strand_rank


def placement_for(*, key: str, subject: str, level: str,
                  topic: str) -> CurriculumPlacement:
    """Return the approved curriculum filing or a neutral legacy placement."""
    if subject == MATH_SUBJECT:
        return math_placement_for(key=key, subject=subject, level=level, topic=topic)
    if subject in SCIENCE_SUBJECTS and key in SCIENCE_KEYS:
        return science_placement_for(key=key, level=level, topic=topic)
    return CurriculumPlacement(
        "", "ทั่วไป", level, "", "", "", (), topic or "ทั่วไป", "",
        "not_applicable", level,
    )


def is_curriculum_filed(*, key: str, subject: str, level: str,
                        topic: str) -> bool:
    """Whether a registry entry participates in curriculum navigation/sorting."""
    placement = placement_for(key=key, subject=subject, level=level, topic=topic)
    return bool(placement.curriculum_node_id)


__all__ = [
    "ADDITIONAL", "BASIC", "COURSE_ORDER", "CURRICULUM_VERSION",
    "ENRICHMENT", "MATH_SUBJECT", "STRAND_ORDER", "SUPPLEMENTAL",
    "TERTIARY", "CurriculumPlacement", "curriculum_sort_fields",
    "is_curriculum_filed", "placement_for",
]
