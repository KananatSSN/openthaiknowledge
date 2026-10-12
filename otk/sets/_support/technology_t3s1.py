"""Phase 7 Technology wave T3, slice 1 — reading and debugging block programs, ป.1-ป.3.

The knowledge halves of three ``partial`` ``ว 4.2`` outcomes that ask a learner
to write a simple program "โดยใช้ซอฟต์แวร์หรือสื่อ" and to find its mistakes.
Writing needs a block editor the product does not have, so these sets *read*
programs drawn by ``block_programs.py``:

* ``ป.1/3`` — what one block does, where a short program ends, and which
  program reaches a star.
* ``ป.2/2`` — whether a program reaches the star, which block is wrong, and how
  to fix it.
* ``ป.3/2`` — the same outcome at more length: tracing a longer program part
  way, the block a program is missing, and the squares it passes.
"""

from __future__ import annotations

from random import Random

from otk.sets._support import block_programs as bp
from otk.sets._support.science_skills import diagram_question

P1, P2, P3 = {"th": "ป.1"}, {"th": "ป.2"}, {"th": "ป.3"}
DIRECTIONS = tuple(f"เดิน{bp.SAY[m]}" for m in "RLUD")
ARROW_TEXT = {"R": "→", "L": "←", "U": "↑", "D": "↓"}
READ_HINT = ("อ่านบล็อกจากบนลงล่างทีละบล็อก ลูกศรหนึ่งบล็อกพาตัวละครเดินหนึ่งช่อง "
             "คอลัมน์ A ถึง E เรียงจากซ้ายไปขวา แถว 1 ถึง 5 เรียงจากล่างขึ้นบน")


def _ask(rng: Random, spec, *, stem: str, correct: str, wrongs, hint: str, topic: str):
    return diagram_question(spec.asset_id, bp.alt(spec), stem=stem, correct=correct,
                            wrongs=tuple(wrongs), hint=hint, topic=topic)


def _other_cells(rng: Random, answer, near, count: int = 3) -> list[str]:
    """Wrong squares: the likely slips first, then squares next to the answer."""
    found: list[str] = []
    for pos in near:
        if bp.inside(pos) and pos != answer and bp.cell(pos) not in found:
            found.append(bp.cell(pos))
    ring = [(answer[0] + dx, answer[1] + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if dx or dy]
    rng.shuffle(ring)
    for pos in ring:
        if len(found) >= count + 2:
            break
        if bp.inside(pos) and bp.cell(pos) not in found:
            found.append(bp.cell(pos))
    return rng.sample(found, count)


# ══ ว 4.2 ป.1/3 ═══════════════════════════════════════════════════════════════


# ══ ว 4.2 ป.2/2 ═══════════════════════════════════════════════════════════════


# ══ ว 4.2 ป.3/2 ═══════════════════════════════════════════════════════════════


