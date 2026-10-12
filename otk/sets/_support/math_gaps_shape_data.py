"""Primary geometry, fraction and data sets for indicators no set taught.

From the 2026-09 content audit: prisms at ป.5 (ค 2.2 ป.5/4); nets at ป.6
(ป.6/4); constructing rectangles, quadrilaterals, triangles and angles
(ป.4/2, ป.5/3, ป.6/2, ม.2/1); comparing, combining and applying fractions and
mixed numbers at ป.6 (ค 1.1 ป.6/1, 7, 8); and making a pictograph and a bar
chart rather than reading one (ค 3.1 ป.3/1, ป.5/2), with a line-graph
application set for ป.5.
"""

from __future__ import annotations

from random import Random

from otk.core.content import text
from otk.core.distractors import combine, fixed, label_pool
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType


def _choices(stem: list, correct: str, wrongs: list[str], topic: str) -> GeneratedQuestion:
    """Thai-text choices, hand-picked wrongs first."""
    wrongs = [w for w in dict.fromkeys(wrongs) if w != correct]
    return GeneratedQuestion(
        stem=stem, correct=[text(correct)],
        distractors=combine(fixed(*[[text(w)] for w in wrongs]), label_pool(wrongs)),
        topic=topic,
    )


# ── ป.5 ปริซึม (ค 2.2 ป.5/4) ──────────────────────────────────────────────────


# ── ป.6 รูปคลี่ (ค 2.2 ป.6/4) ─────────────────────────────────────────────────


# ── การสร้าง: ขั้นตอน (ป.4/2, ป.5/3, ป.6/2) ──────────────────────────────────

class _ConstructionSteps(QuestionType):
    """A construction as its ordered steps. The learner is shown one step and
    picks the one that comes next; a plausible but faulty step is among the
    wrong choices."""

    def procedures(self, rng: Random) -> tuple[str, list[str], list[str]]:
        """``(goal, steps, faulty steps)``."""
        raise NotImplementedError

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        goal, steps, faulty = self.procedures(rng)
        k = rng.randrange(len(steps) - 1)
        later = [s for i, s in enumerate(steps) if i > k + 1]
        earlier = [s for i, s in enumerate(steps) if i < k]
        stem = [text(f"{goal} ขั้นตอนที่ {k + 1} คือ “{steps[k]}” ขั้นตอนถัดไปคือข้อใด")]
        return _choices(stem, steps[k + 1], faulty + later + earlier, self.topic)


# ── ม.2 การสร้างมุมด้วยวงเวียนและสันตรง (ค 2.2 ม.2/1) ───────────────────────


# ── ป.6 เศษส่วนและจำนวนคละ (ค 1.1 ป.6/1, 7, 8) ──────────────────────────────


# ── ป.3 และ ป.5 การนำเสนอข้อมูล: เขียนแผนภูมิ (ค 3.1 ป.3/1, ป.5/2) ─────────────

_TALLY = (
    ("จำนวนนักเรียนที่ชอบผลไม้แต่ละชนิด", ("ส้ม", "มะม่วง", "กล้วย", "ทุเรียน"), "คน"),
    ("จำนวนต้นไม้ที่ปลูกในแต่ละสวน", ("สวนที่ 1", "สวนที่ 2", "สวนที่ 3", "สวนที่ 4"), "ต้น"),
    ("จำนวนหนังสือที่แต่ละห้องบริจาค", ("ห้อง 1", "ห้อง 2", "ห้อง 3", "ห้อง 4"), "เล่ม"),
)


def _table(title: str, rows, values, unit: str) -> str:
    return f"ตาราง{title}\n" + "\n".join(f"{r} | {v} {unit}" for r, v in zip(rows, values))


