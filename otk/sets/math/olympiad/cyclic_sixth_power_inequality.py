"""Minimize a cyclic sixth-power expression under a fixed sum."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2563, ข้อ 8",)
)


def cyclic_sixth_power_minimum(scale: int) -> int:
    """Normalize a+b+c=3t to a/t+b/t+c/t=3."""
    if scale < 1:
        raise ValueError("scale must be positive")
    return scale**4


@question_type(
    "math.cyclic_sixth_power_inequality_olympiad",
    display_name={"th": "ค่าน้อยสุดของผลบวกเศษส่วนกำลังหกแบบวนรอบ"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="อสมการ",
)
class CyclicSixthPowerInequality(WordProblem):
    def expr(self, rng: Random):
        scale = rng.randint(2, 8)
        answer = cyclic_sixth_power_minimum(scale)
        return MathDraw(
            (
                rf"t={scale},\quad a+b+c=3t,\quad "
                r"\frac{a^6}{c^2+(2/t)b^3}"
                r"+\frac{b^6}{a^2+(2/t)c^3}"
                r"+\frac{c^6}{b^2+(2/t)a^3}"
            ),
            str(answer),
            prompt="เมื่อ a,b,c>0 จงหาค่าน้อยที่สุดของนิพจน์ที่กำหนด",
            hint=(
                "หาร a,b,c ด้วย t แล้วใช้คอชี–ชวาร์ซให้เหลือผลรวมกำลังสอง"
                "และกำลังสาม; ค่าน้อยสุดเกิดเมื่อ a=b=c=t"
            ),
            distractors=[
                str(scale**3),  # lose one power while rescaling
                str(scale**6),  # rescale numerator but not denominator
                str(answer // 3),  # count just one equal-value term
                str(3 * answer),  # keep three terms after summing
                str(answer + scale),  # add the scale after normalization
                str(2 * answer),  # miss one denominator contribution
            ],
        )
