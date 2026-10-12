"""Wave E slice 5 — organic chemistry: hydrocarbons, polymers, and acid-base.

Three more core indicators under ``ว 2.1 ม.5``:

* ``ว 2.1 ม.5/14`` ระบุสารประกอบอินทรีย์ประเภทไฮโดรคาร์บอนว่าอิ่มตัวหรือไม่
  อิ่มตัวจากสูตรโครงสร้าง — single verb ระบุ, default filing.
* ``ว 2.1 ม.5/15`` สืบค้นข้อมูลและเปรียบเทียบสมบัติทางกายภาพระหว่างพอลิเมอร์
  และมอนอเมอร์ของพอลิเมอร์ชนิดนั้น — สืบค้นข้อมูล is not itself MCQ-assessable,
  so the record rides on เปรียบเทียบ alone, the same precedent already set for
  ``chem.element_use_effect`` in Wave D and ``chem.element_use_hazard`` in
  this wave's slice 2.
* ``ว 2.1 ม.5/16`` ระบุสมบัติความเป็นกรด-เบสจากโครงสร้างของสารประกอบอินทรีย์
  — single verb ระบุ, default filing.

Every fact bank is small and hand-checked against real organic chemistry
(real hydrocarbons, real polymer/monomer pairs, real functional groups).
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


# ══ ว 2.1 ม.5/14 — ไฮโดรคาร์บอนอิ่มตัวและไม่อิ่มตัว ═══════════════════════


# ══ ว 2.1 ม.5/15 — สมบัติทางกายภาพของพอลิเมอร์เทียบกับมอนอเมอร์ ═══════════


# ══ ว 2.1 ม.5/16 — สมบัติกรด-เบสจากโครงสร้างของสารประกอบอินทรีย์ ═════════


