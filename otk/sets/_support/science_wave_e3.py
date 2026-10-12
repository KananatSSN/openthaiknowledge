"""Wave E slice 3 — covalent bonding: bond order, polarity, and hydrogen bonds.

Three more core indicators under ``ว 2.1 ม.5``:

* ``ว 2.1 ม.5/8`` ระบุว่าพันธะโคเวเลนต์เป็นพันธะเดี่ยว พันธะคู่ หรือพันธะสาม
  และระบุจำนวนคู่อิเล็กตรอนระหว่างอะตอมคู่ร่วมพันธะจากสูตรโครงสร้าง — verb ระบุ
  repeated over two joined facts that always move together (bond order fixes
  the shared-pair count), so the default filing applies: only Fluency (both
  facts at once) is exact.
* ``ว 2.1 ม.5/9`` ระบุสภาพขั้วของสารที่โมเลกุลประกอบด้วย 2 อะตอม — single verb
  ระบุ, same default filing.
* ``ว 2.1 ม.5/10`` ระบุสารที่เกิดพันธะไฮโดรเจนได้จากสูตรโครงสร้าง — single verb
  ระบุ, same default filing.

Every fact bank here is deliberately small and hand-checked (real bonds in
real molecules), the same discipline used for the periodic-table banks in
``science_wave_e1.py``/``science_wave_e2.py``.
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


# ══ ว 2.1 ม.5/8 — พันธะเดี่ยว/คู่/สาม และจำนวนคู่อิเล็กตรอนร่วมพันธะ ═══════


# ══ ว 2.1 ม.5/9 — สภาพขั้วของโมเลกุลที่ประกอบด้วย 2 อะตอม ═════════════════


# ══ ว 2.1 ม.5/10 — การเกิดพันธะไฮโดรเจนจากสูตรโครงสร้าง ═══════════════════

H_BOND_FILLERS = ("เกิดพันธะไฮโดรเจนได้เฉพาะในสถานะของแข็ง", "ไม่สามารถระบุได้จากสูตรโครงสร้าง",
                  "เกิดพันธะไฮโดรเจนได้เฉพาะเมื่อร้อนจัด", "เกิดพันธะไฮโดรเจนกับโลหะเท่านั้น")


