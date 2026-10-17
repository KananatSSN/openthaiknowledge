"""BD = DC = CF = t in a right triangle at A forces AC³ = 2t³."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2550, วันแรก ข้อ 5",))


def cube_root_side(t: int) -> int:
    """CF = AC²/BC = t and BD² = AB² + (AC − t)² = t² give BC² = 2t·AC and
    AC⁴ = t²BC² = 2t³·AC, so AC = t∛2. Returns the coefficient t."""
    return t


@question_type(
    "math.right_triangle_cube_root_olympiad",
    display_name={"th": "ความยาวด้านในรูปสามเหลี่ยมมุมฉากที่ได้รากที่สาม"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="เรขาคณิต: สามเหลี่ยมมุมฉาก",
)
class RightTriangleCubeRoot(WordProblem):
    def expr(self, rng: Random):
        t = rng.randint(1, 15)
        coef = cube_root_side(t)
        answer = ("" if coef == 1 else str(coef)) + r"\sqrt[3]{2}"
        wrong = [("" if t == 1 else str(t)) + r"\sqrt{2}", ("" if t == 1 else str(t)) + r"\sqrt[3]{4}", str(2 * t), ("" if t == 1 else str(t)) + r"\sqrt{3}", str(2 * t) + r"\sqrt[3]{2}"]
        return MathDraw(
            rf"BD=DC=CF={t}",
            answer,
            prompt="รูปสามเหลี่ยม ABC มีมุม A ฉาก D อยู่บน AC และ AF ตั้งฉากกับ BC ที่ F จงหา AC",
            hint="CF = AC²/BC จากรูปสามเหลี่ยมคล้าย และ BD² = AB² + AD²",
            distractors=wrong,
        )
