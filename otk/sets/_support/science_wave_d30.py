"""Wave D, slice 30 — work, power, and simple machines, opening ว 2.3 ม.2.

* ``ว 2.3 ม.2/1`` การคำนวณงานและกำลังโดยใช้สมการ W = Fs และ P = W/t — all three stages
* ``ว 2.3 ม.2/2`` หลักการทำงานของเครื่องกลอย่างง่าย — all three stages
* ``ว 2.3 ม.2/3`` ประโยชน์ของเครื่องกลอย่างง่าย — all three stages

``ม.2/1`` joins two free verbs — ``วิเคราะห์สถานการณ์`` (Foundation) and
``คำนวณ...โดยใช้สมการ...จากข้อมูลที่รวบรวมได้`` (Fluency) — both ``exact``.
``ม.2/2`` and ``ม.2/3`` are each one verb with evidence, so only their
Fluency set is ``exact``.

Wave H slice 1 widened every set here: work and no-work cases, power drawn
from generated force, distance and time, more machines and tools, and lever
and ramp calculations using the rules stated in the stem (the moment rule
and ideal F × L = W × h). The authored rows are kept inside the banks.
"""

from __future__ import annotations

from random import Random

from otk.core.question import GeneratedQuestion
from otk.sets._support.science_wave_b14 import _labelled

SECOND_SECONDARY = {"th": "ม.2"}


def _facts(rng: Random, facts: tuple, *, hint: str, topic: str) -> GeneratedQuestion:
    """One authored (stem, right, five wrongs) row, three wrongs drawn."""
    stem, right, wrongs = rng.choice(facts)
    return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), hint=hint, topic=topic)


# ══ ว 2.3 ม.2/1 — การคำนวณงานและกำลังโดยใช้สมการ W = Fs และ P = W/t ═══════════════


# ══ ว 2.3 ม.2/2 — หลักการทำงานของเครื่องกลอย่างง่าย ═══════════════════════════════


# ══ ว 2.3 ม.2/3 — ประโยชน์ของเครื่องกลอย่างง่าย ═══════════════════════════════════


