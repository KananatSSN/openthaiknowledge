"""Wave E slice 6 — solubility, thermoplastic/thermoset, and polymer impact.

Three more core indicators under ``ว 2.1 ม.5``:

* ``ว 2.1 ม.5/17`` อธิบายสมบัติการละลายในตัวทำละลายชนิดต่าง ๆ ของสาร — single
  verb อธิบาย, default filing.
* ``ว 2.1 ม.5/18`` วิเคราะห์และอธิบายความสัมพันธ์ระหว่างโครงสร้างกับสมบัติ
  เทอร์มอพลาสติกและเทอร์มอเซตของพอลิเมอร์ และการนำพอลิเมอร์ไปใช้ประโยชน์ —
  วิเคราะห์ and อธิบาย both act on the *same* relationship (structure vs
  property), unlike the ``TWO_FREE_VERBS`` pattern where each verb has its
  own separate object; this stays under the default filing.
* ``ว 2.1 ม.5/19`` สืบค้นข้อมูลและนำเสนอผลกระทบของการใช้ผลิตภัณฑ์พอลิเมอร์ที่มี
  ต่อสิ่งมีชีวิตและสิ่งแวดล้อม พร้อมแนวทางป้องกันหรือแก้ไข — สืบค้นข้อมูล is
  not itself MCQ-assessable, so the record rides on นำเสนอ alone, the same
  precedent already set for ``chem.element_use_effect``/``chem.element_use_hazard``.

Every fact bank is small and hand-checked (real solute/solvent pairs under
"like dissolves like", real thermoplastic/thermoset polymers, real polymer
environmental impacts and mitigations).
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


# ══ ว 2.1 ม.5/17 — สมบัติการละลายในตัวทำละลายชนิดต่าง ๆ ═══════════════════


# ══ ว 2.1 ม.5/18 — โครงสร้างกับสมบัติเทอร์มอพลาสติกและเทอร์มอเซต ═══════════


# ══ ว 2.1 ม.5/19 — ผลกระทบของผลิตภัณฑ์พอลิเมอร์ต่อสิ่งมีชีวิตและสิ่งแวดล้อม ═


