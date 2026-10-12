"""Wave E slice 14 — sound: its wave behaviour, loudness and hearing, and
echo, beats, the Doppler effect and resonance.

Three core indicators under ``ว 2.3 ม.5``:

* ``ว 2.3 ม.5/5`` สังเกตและอธิบายการสะท้อน การหักเห การเลี้ยวเบน และการรวมคลื่นของ
  คลื่นเสียง — default filing; the ``exact`` bank spans all four.
* ``ว 2.3 ม.5/6`` สืบค้นข้อมูลและอธิบายความสัมพันธ์ระหว่างความเข้มเสียงกับระดับเสียง
  และผลของความถี่กับระดับเสียงที่มีต่อการได้ยินเสียง — one verb, two objects:
  default filing, and the ``exact`` set reaches both. ระดับเสียง is the level in
  decibels, as at ``ป.5/4``. The logarithm itself is Application: the core
  indicator asks for the relationship, and คำนวณ appears only in
  ``ฟิสิกส์เพิ่มเติม 2 ม.5/6``.
* ``ว 2.3 ม.5/7`` สังเกตและอธิบายการเกิดเสียงสะท้อนกลับ บีต ดอปเพลอร์ และการสั่นพ้อง
  ของเสียง — default filing; the ``exact`` bank spans all four.

The speed of sound in air is taken as 340 m/s, and in water as 1,500 m/s.
"""

from __future__ import annotations

from fractions import Fraction

from otk.core.content import text
from otk.core.distractors import fixed, label_pool
from otk.core.question import GeneratedQuestion
from otk.sets._support.science_wave_e13 import show

SUBJECT = "ฟิสิกส์"
UPPER_FIVE = {"th": "ม.5"}

V_AIR, V_WATER = 340, 1500


def _labelled(*, stem: str, correct: str, wrongs: tuple[str, ...], topic: str,
              hint: str) -> GeneratedQuestion:
    return GeneratedQuestion(
        stem=[text(stem)],
        correct=[text(correct)],
        distractors=label_pool([correct, *wrongs]),
        topic=topic,
        hint=[text(hint)],
    )


def _numeric(*, stem: str, answer, wrongs, unit: str, topic: str, hint: str) -> GeneratedQuestion:
    seen = [Fraction(answer)]
    # Slips on both sides; the registry's rank balancing picks among them.
    for w in [*wrongs, answer / 2, answer * 2, answer - 1, answer + 1, answer / 10, answer * 10, answer - 2, answer + 2, answer * 3]:
        w = Fraction(w)
        if w > 0 and w not in seen and show(w) not in {show(s) for s in seen}:
            seen.append(w)
    return GeneratedQuestion(
        stem=[text(stem)], correct=[text(f"{show(seen[0])} {unit}")],
        distractors=fixed(*[[text(f"{show(w)} {unit}")] for w in seen[1:]]),
        topic=topic, hint=[text(hint)],
    )


# ══ ว 2.3 ม.5/5 — พฤติกรรมของคลื่นเสียง ═════════════════════════════════════════


# ══ ว 2.3 ม.5/6 — ความเข้มเสียงและระดับเสียง ═══════════════════════════════════


# ══ ว 2.3 ม.5/7 — เสียงสะท้อนกลับ บีต ดอปเพลอร์ และการสั่นพ้อง ═══════════════════


