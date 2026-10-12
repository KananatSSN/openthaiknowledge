"""Wave E slice 4 — boiling points, ionic formulas, and electrolytes.

Three more core indicators under ``ว 2.1 ม.5``:

* ``ว 2.1 ม.5/11`` อธิบายความสัมพันธ์ระหว่างจุดเดือดของสารโคเวเลนต์กับแรงดึงดูด
  ระหว่างโมเลกุลตามสภาพขั้วหรือการเกิดพันธะไฮโดรเจน — single verb อธิบาย,
  default filing: only Fluency is exact.
* ``ว 2.1 ม.5/12`` เขียนสูตรเคมีของไอออนและสารประกอบไอออนิก — verb เขียน
  repeated over two joined objects (an ion's formula; an ionic compound's
  formula). Writing a chemical formula is a discrete symbolic answer an MCQ
  item can offer as a choice — unlike freehand diagrams or graphs — so this
  follows the same default filing as ``chem.periodic_position`` (ม.5/5):
  only Fluency (both formulas together) is exact.
* ``ว 2.1 ม.5/13`` ระบุว่าสารเกิดการละลายแบบแตกตัวหรือไม่แตกตัว พร้อมให้
  เหตุผลและระบุว่าสารละลายที่ได้เป็นสารละลายอิเล็กโทรไลต์หรือนอนอิเล็กโทรไลต์
  — dissociation type fixes the electrolyte classification, the same
  correlated-fact shape as ``chem.covalent_bond_order`` (ม.5/8); default
  filing.

Every fact bank is small and hand-checked against real chemistry (real ionic
compounds and their actual Thai names, real electrolytes and nonelectrolytes),
the same discipline used throughout this wave.
"""

from __future__ import annotations

from otk.core.content import text
from otk.core.distractors import label_pool
from otk.core.question import GeneratedQuestion

SUBJECT = "เคมี"


def _labelled(*, stem: str, correct: str, wrongs: tuple[str, ...], topic: str,
              hint: str) -> GeneratedQuestion:
    return GeneratedQuestion(
        stem=[text(stem)],
        correct=[text(correct)],
        distractors=label_pool([correct, *wrongs]),
        topic=topic,
        hint=[text(hint)],
    )


# ══ ว 2.1 ม.5/11 — จุดเดือดของสารโคเวเลนต์กับแรงดึงดูดระหว่างโมเลกุล ═══════


# ══ ว 2.1 ม.5/12 — สูตรเคมีของไอออนและสารประกอบไอออนิก ═══════════════════


# ══ ว 2.1 ม.5/13 — การแตกตัวของสารและสารละลายอิเล็กโทรไลต์ ═══════════════


DISSOCIATION_FILLERS = ("แตกตัวได้ครึ่งเดียว", "ขึ้นกับอุณหภูมิเท่านั้น", "แตกตัวเป็นอะตอม", "ระเหยเป็นแก๊สทันที")


