"""Consolidated math topics: the code and the rename table agree.

Consumers that key data by topic (TutorRank's ratings) migrate it with
``MATH_TOPIC_RENAMES``; their own tests check their migrations against it.
"""

from __future__ import annotations

from otk.core import REGISTRY
from otk.core.curriculum_math import (
    MATH_SUBJECT, MATH_TOPIC_ASSIGNMENTS, MATH_TOPIC_RENAMES, RETIRED_TOPIC_NAMES,
)

MATH = {k: s for k, s in REGISTRY.items() if s.subject == MATH_SUBJECT}
IN_USE = {s.topic for s in REGISTRY.values()}


def test_no_set_is_filed_under_a_renamed_topic():
    left = [(k, s.level_for(), s.topic) for k, s in MATH.items()
            if (s.level_for(), s.topic) in MATH_TOPIC_RENAMES]
    assert not left


def test_topicless_sets_have_their_topic():
    assert all(MATH[k].topic == t for k, t in MATH_TOPIC_ASSIGNMENTS.items())


def test_every_rename_target_is_a_live_topic():
    assert set(MATH_TOPIC_RENAMES.values()) <= IN_USE


def test_no_set_brings_back_a_retired_topic_name():
    """At any level: a consumer keys ratings by the name and migrated it away."""
    assert not RETIRED_TOPIC_NAMES & IN_USE


def test_every_retired_name_was_renamed():
    assert RETIRED_TOPIC_NAMES <= {old for (_, old) in MATH_TOPIC_RENAMES}
