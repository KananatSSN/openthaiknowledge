"""Wave E slice 13 — nuclear energy, renewable electricity, wave behaviour and resonance.

Four core indicators under ``ว 2.3 ม.5``:

* ``ว 2.3 ม.5/1`` สืบค้นข้อมูลและอธิบายพลังงานนิวเคลียร์ ฟิชชันและฟิวชัน และ
  ความสัมพันธ์ระหว่างมวลกับพลังงานที่ปลดปล่อยออกมาจากฟิชชันและฟิวชัน — one verb,
  several objects: default filing, and the ``exact`` bank reaches fission,
  fusion and the mass-energy relation. E = mc² with numbers is Application:
  the core indicator names the relation, not a calculation.
* ``ว 2.3 ม.5/2`` สืบค้นข้อมูล และอธิบายการเปลี่ยนพลังงานทดแทนเป็นพลังงานไฟฟ้า
  รวมทั้งสืบค้นและอภิปรายเกี่ยวกับเทคโนโลยี ... โดยเน้นด้านประสิทธิภาพและความคุ้มค่า
  ด้านค่าใช้จ่าย — ``รวมทั้ง`` joins two outcomes: Foundation (the energy
  conversions) and Fluency (efficiency and cost-effectiveness, judged from
  numbers) are both ``exact``.
* ``ว 2.3 ม.5/3`` สังเกตและอธิบายการสะท้อน การหักเห การเลี้ยวเบน และการรวมคลื่น —
  default filing; the ``exact`` bank spans all four behaviours.
* ``ว 2.3 ม.5/4`` สังเกตและอธิบายความถี่ธรรมชาติ การสั่นพ้อง และผลที่เกิดขึ้นจาก
  การสั่นพ้อง — default filing; the ``exact`` bank spans all three.
"""

from __future__ import annotations

from fractions import Fraction

from otk.core.content import text
from otk.core.distractors import fixed, label_pool
from otk.core.question import GeneratedQuestion

SUBJECT = "ฟิสิกส์"
UPPER_FIVE = {"th": "ม.5"}


def _labelled(*, stem: str, correct: str, wrongs: tuple[str, ...], topic: str,
              hint: str) -> GeneratedQuestion:
    return GeneratedQuestion(
        stem=[text(stem)],
        correct=[text(correct)],
        distractors=label_pool([correct, *wrongs]),
        topic=topic,
        hint=[text(hint)],
    )


def show(x) -> str:
    value = float(x)
    if value == int(value):
        return f"{int(value):,}"
    return f"{value:,.2f}".rstrip("0").rstrip(".")


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


# ══ ว 2.3 ม.5/1 — พลังงานนิวเคลียร์ ═══════════════════════════════════════════════


# ══ ว 2.3 ม.5/2 — พลังงานทดแทนเป็นพลังงานไฟฟ้า ═══════════════════════════════════


# ══ ว 2.3 ม.5/3 — พฤติกรรมของคลื่น ══════════════════════════════════════════════

REFLECT, REFRACT, DIFFRACT, SUPERPOSE = "การสะท้อน", "การหักเห", "การเลี้ยวเบน", "การรวมคลื่น"
BEHAVIOURS = (REFLECT, REFRACT, DIFFRACT, SUPERPOSE)


# ══ ว 2.3 ม.5/4 — ความถี่ธรรมชาติและการสั่นพ้อง ═══════════════════════════════════


