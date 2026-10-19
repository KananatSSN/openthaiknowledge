"""Pigeonhole into classes, then a monochromatic triangle by Ramsey numbers."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2553, วันที่สอง ข้อ 2",)
)

RAMSEY = {2: 6, 3: 17}  # R(3, 3) and R(3, 3, 3)


def threshold(classes: int, topics: int) -> int:
    """(R − 1)·classes people can avoid it (R − 1 per class with a
    triangle-free colouring); one more puts R people in some class, where the
    colouring of their pairs has a one-colour triangle."""
    return (RAMSEY[topics] - 1) * classes + 1


@question_type(
    "math.ramsey_class_threshold_olympiad",
    display_name={"th": "จำนวนคนน้อยสุดที่รับประกันสามเหลี่ยมสีเดียวในกลุ่มเดียวกัน"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="การจัดหมู่",
)
class RamseyClassThreshold(WordProblem):
    def expr(self, rng: Random):
        regions = rng.randint(2, 9)
        topics = rng.choice((2, 3))
        classes = 12 * 2 * regions
        answer = threshold(classes, topics)
        r = RAMSEY[topics]
        wrong = [v for v in dict.fromkeys([r * classes, (r - 1) * classes, 2 * classes + 1, (r - 2) * classes + 1, (6 if topics == 3 else 17) * classes]) if v != answer]
        return MathDraw(
            rf"12\times 2\times {regions}={24 * regions}",
            str(answer),
            prompt=(
                f"นักเรียนมาจาก {regions} ภูมิภาค แต่ละคนมีเพศ (2 แบบ) และเดือนเกิด (12 เดือน) "
                f"ทุกคู่เลือกถกปัญหาร่วมกันหนึ่งหัวข้อจาก {topics} หัวข้อ "
                "ต้องมีนักเรียนอย่างน้อยกี่คนจึงรับประกันว่ามี 3 คนที่เกิดเดือนเดียวกัน เพศเดียวกัน ภูมิภาคเดียวกัน "
                "และทุกคู่ใน 3 คนนี้ถกหัวข้อเดียวกัน"
            ),
            hint="นับกลุ่ม (เดือน, เพศ, ภูมิภาค) แล้วใช้หลักรังนกพิราบกับจำนวนแรมซีย์ R(3, 3) = 6, R(3, 3, 3) = 17",
            distractors=[str(v) for v in wrong],
            variant=str(topics),
        )
