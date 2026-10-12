"""Wave E slice 11 — Newton's laws, accelerated motions, and gravity round the Earth.

Four core indicators under ``ว 2.2 ม.5``:

* ``ว 2.2 ม.5/3`` สังเกต วิเคราะห์ และอธิบายความสัมพันธ์ระหว่างความเร่งของวัตถุ
  กับแรงลัพธ์ที่กระทำต่อวัตถุและมวลของวัตถุ — three verbs on one relationship:
  default filing (Foundation ``standard_scope``, Fluency ``exact``, Application
  ``standard_scope``).
* ``ว 2.2 ม.5/4`` สังเกตและอธิบายแรงกิริยาและแรงปฏิกิริยาระหว่างวัตถุคู่หนึ่ง ๆ —
  default filing.
* ``ว 2.2 ม.5/5`` สังเกตและอธิบายผลของความเร่งที่มีต่อการเคลื่อนที่แบบต่าง ๆ
  ได้แก่ แนวตรง โพรเจกไทล์ วงกลม และการสั่น — default filing, and by the
  multi-object rule the ``exact`` set's bank spans all four motions.
* ``ว 2.2 ม.5/6`` สืบค้นข้อมูลและอธิบายแรงโน้มถ่วงที่เกี่ยวกับการเคลื่อนที่ของวัตถุ
  ต่าง ๆ รอบโลก — สืบค้นข้อมูล is not assessable in a choice, so อธิบาย carries
  the record: default filing.

Take g = 10 m/s² throughout, as the core textbook does for calculation.
"""

from __future__ import annotations

from fractions import Fraction

from otk.core.content import text
from otk.core.distractors import fixed, label_pool
from otk.core.question import GeneratedQuestion

SUBJECT = "ฟิสิกส์"
UPPER_FIVE = {"th": "ม.5"}

G = 10


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
    """Four distinct positive values in ``unit``; slips first, neighbours after."""
    seen = [Fraction(answer)]
    # Slips on both sides; the registry's rank balancing picks among them.
    extra = [answer / 2, answer * 2, answer - 1, answer + 1, answer / 10, answer * 10, answer - 2, answer + 2, answer * 3]
    for w in [*wrongs, *extra]:
        w = Fraction(w)
        if w > 0 and w not in seen and show(w) not in {show(s) for s in seen}:
            seen.append(w)
    return GeneratedQuestion(
        stem=[text(stem)], correct=[text(f"{show(seen[0])} {unit}")],
        distractors=fixed(*[[text(f"{show(w)} {unit}")] for w in seen[1:]]),
        topic=topic, hint=[text(hint)],
    )


# ══ ว 2.2 ม.5/3 — กฎการเคลื่อนที่ข้อที่สองของนิวตัน ═════════════════════════════════


# ══ ว 2.2 ม.5/4 — แรงกิริยาและแรงปฏิกิริยา ══════════════════════════════════════


# ══ ว 2.2 ม.5/5 — ความเร่งกับการเคลื่อนที่แบบต่าง ๆ ═══════════════════════════════


# ══ ว 2.2 ม.5/6 — แรงโน้มถ่วงกับการเคลื่อนที่รอบโลก ════════════════════════════════


