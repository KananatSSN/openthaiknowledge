"""Phase 7 Technology wave T1, slice 4 — ว 4.2 วิทยาการคำนวณ ป.2-ป.3.

* ``ว 4.2 ป.2/1`` — the same outcome text as ``ป.1/2``, taken a step further:
  steps shown as *symbols*, the arrows ``→ ← ↑ ↓`` that move a robot one square.
  Translating, following and fixing an arrow sequence.
* ``ว 4.2 ป.3/1`` — an algorithm shown in text: spotting a repeated block,
  counting what a repeat does, and following a ``ถ้า…`` rule.
* ``ว 4.2 ป.2/4`` — the ``ป.1/5`` outcome again, here about looking after each
  device and the agreements of a shared computer room.
* ``ว 4.2 ป.3/5`` — the agreements for using the internet: personal
  information, the reasons behind each rule, and what to do online.

Everything is text. The arrows are characters, not drawings, so they need no
new capability.
"""

from __future__ import annotations

SECOND, THIRD = {"th": "ป.2"}, {"th": "ป.3"}


# ══ ว 4.2 ป.2/1 — ลำดับขั้นตอนด้วยลูกศร ═══════════════════════════════════════


# ══ ว 4.2 ป.3/1 — อัลกอริทึม: การทำซ้ำและเงื่อนไข ════════════════════════════════


def _near(answer: int, candidates) -> list[int]:
    """Three distinct non-negative wrong counts, topped up from nearby numbers."""
    found = [c for c in dict.fromkeys(candidates) if c >= 0 and c != answer]
    step = 1
    while len(found) < 3:
        for c in (answer + step, answer - step):
            if c >= 0 and c != answer and c not in found:
                found.append(c)
        step += 1
    return found


# ══ ว 4.2 ป.2/4 — ดูแลรักษาอุปกรณ์และข้อตกลงในห้องคอมพิวเตอร์ ═══════════════════


# ══ ว 4.2 ป.3/5 — ข้อตกลงในการใช้อินเทอร์เน็ต ════════════════════════════════════


