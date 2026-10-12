"""Wave D, slice 21 — field-force diagrams and distance, then speed and displacement, at ม.2.

* ``ว 2.2 ม.2/12`` เขียนแผนภาพแสดงแรงแม่เหล็ก แรงไฟฟ้า และแรงโน้มถ่วงที่กระทำต่อวัตถุ — all three stages
* ``ว 2.2 ม.2/13`` ความสัมพันธ์ระหว่างขนาดของแรงกับระยะห่างจากแหล่งของสนาม — all three stages
* ``ว 2.2 ม.2/14`` อัตราเร็วและความเร็วของการเคลื่อนที่ — all three stages
* ``ว 2.2 ม.2/15`` เขียนแผนภาพแสดงการกระจัดและความเร็ว — all three stages

``ม.2/12`` and ``ม.2/15`` are ``เขียนแผนภาพ``: three sets each, no ``exact``, following
the rule Wave A set for ray diagrams and this wave has used since ``ป.5/2``.
``ม.2/13`` names its evidence, ``จากข้อมูลที่รวบรวมได้``, so only its Fluency set
is ``exact``, as with ``ม.2/11``. ``ม.2/14`` joins two free verbs — ``อธิบาย`` and
``คำนวณ...โดยใช้สมการจากหลักฐานเชิงประจักษ์`` — so both Foundation and Fluency are
``exact``, as with ``ม.2/10``.
"""

from __future__ import annotations

from random import Random

from otk.core.question import GeneratedQuestion
from otk.sets._support.science_wave_b14 import _labelled

# ══ ว 2.2 ม.2/12 — เขียนแผนภาพแสดงแรงแม่เหล็ก แรงไฟฟ้า และแรงโน้มถ่วง ══════════════


# ══ ว 2.2 ม.2/13 — ความสัมพันธ์ระหว่างขนาดของแรงกับระยะห่างจากแหล่งของสนาม ══════════


def _facts(rng: Random, facts: tuple, *, hint: str, topic: str) -> GeneratedQuestion:
    """One authored (stem, right, five wrongs) row, three wrongs drawn."""
    stem, right, wrongs = rng.choice(facts)
    return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), hint=hint, topic=topic)


# ══ ว 2.2 ม.2/14 — อัตราเร็วและความเร็วของการเคลื่อนที่ ═══════════════════════════


# ══ ว 2.2 ม.2/15 — เขียนแผนภาพแสดงการกระจัดและความเร็ว ══════════════════════════


