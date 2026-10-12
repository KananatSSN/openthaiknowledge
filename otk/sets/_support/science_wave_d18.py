"""Wave D, slice 18 — resultant force and motion, liquid pressure, and buoyancy, at ม.2.

* ``ว 2.2 ม.2/1`` การพยากรณ์การเคลื่อนที่ของวัตถุจากแรงลัพธ์ — all three stages
* ``ว 2.2 ม.2/2`` แผนภาพแสดงแรงและแรงลัพธ์ในแนวเดียวกัน — all three stages
* ``ว 2.2 ม.2/3`` ปัจจัยที่มีผลต่อความดันของของเหลว — all three stages
* ``ว 2.2 ม.2/4`` แรงพยุงและการจมการลอยของวัตถุในของเหลว — all three stages

``ม.2/1`` is ``พยากรณ์`` with evidence: the Fluency set gives the forces and the
starting motion, and the answer predicts what follows. ``ม.2/2`` is ``เขียน
แผนภาพ``: three sets, no ``exact``. ``ม.2/3``'s experiment verb names the factors
as a class, so, as with ``ว 2.1 ม.2/4``, its Fluency set gives three
one-factor results and every answer explains all three. ``ม.2/4`` analyses
buoyancy from spring-scale readings in air and in water.
"""

from __future__ import annotations

from random import Random

from otk.core.question import GeneratedQuestion
from otk.sets._support.science_wave_b14 import _labelled

SECONDARY_TWO = {"th": "ม.2"}


# ══ ว 2.2 ม.2/1 — พยากรณ์การเคลื่อนที่จากแรงลัพธ์ ══════════════════════════════════════


def _facts(rng: Random, facts: tuple, *, hint: str, topic: str) -> GeneratedQuestion:
    """One authored (stem, right, five wrongs) row, three wrongs drawn."""
    stem, right, wrongs = rng.choice(facts)
    return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), hint=hint, topic=topic)


# ══ ว 2.2 ม.2/2 — แผนภาพแสดงแรงและแรงลัพธ์ ════════════════════════════════════════════


# ══ ว 2.2 ม.2/3 — ปัจจัยที่มีผลต่อความดันของของเหลว ════════════════════════════════════


# ══ ว 2.2 ม.2/4 — แรงพยุงและการจมการลอย ═══════════════════════════════════════════════


