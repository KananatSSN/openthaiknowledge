"""Wave D, slice 19 — forces in liquids drawn, and static and kinetic friction, at ม.2.

* ``ว 2.2 ม.2/5`` แผนภาพแสดงแรงที่กระทำต่อวัตถุในของเหลว — all three stages
* ``ว 2.2 ม.2/6`` แรงเสียดทานสถิตและแรงเสียดทานจลน์ — all three stages
* ``ว 2.2 ม.2/7`` ปัจจัยที่มีผลต่อขนาดของแรงเสียดทาน — all three stages

``ม.2/5`` is ``เขียนแผนภาพ``: three sets, no ``exact``. ``ม.2/6`` explains both
kinds of friction from a spring-scale record, so its Fluency answer covers the
static friction before sliding, the largest static friction, and the kinetic
friction while sliding. ``ม.2/7``, like ``ม.2/3``, gives three one-factor
results and every answer explains all three factors.
"""

from __future__ import annotations

from random import Random

from otk.core.question import GeneratedQuestion
from otk.sets._support.science_wave_b14 import _labelled


def _facts(rng: Random, facts: tuple, *, hint: str, topic: str) -> GeneratedQuestion:
    """One authored (stem, right, five wrongs) row, three wrongs drawn."""
    stem, right, wrongs = rng.choice(facts)
    return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), hint=hint, topic=topic)


# ══ ว 2.2 ม.2/5 — แผนภาพแสดงแรงที่กระทำต่อวัตถุในของเหลว ══════════════════════════════


# ══ ว 2.2 ม.2/6 — แรงเสียดทานสถิตและแรงเสียดทานจลน์ ═════════════════════════════════


def _facts(rng: Random, facts: tuple, *, hint: str, topic: str) -> GeneratedQuestion:
    """One authored (stem, right, five wrongs) row, three wrongs drawn."""
    stem, right, wrongs = rng.choice(facts)
    return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), hint=hint, topic=topic)


# ══ ว 2.2 ม.2/7 — ปัจจัยที่มีผลต่อขนาดของแรงเสียดทาน ═══════════════════════════════════


