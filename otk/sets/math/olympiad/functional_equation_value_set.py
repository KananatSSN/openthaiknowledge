"""Classify a cubic functional equation after scaling its coefficient."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("original")


def possible_values(scale: int, point: int) -> tuple[int, int, int]:
    """The only functions are zero and the two scaled identity maps."""
    if scale <= 0 or point == 0:
        raise ValueError("expected positive scale and nonzero point")
    magnitude = scale * abs(point)
    return -magnitude, 0, magnitude


def _set(values: tuple[int, ...]) -> str:
    return "{" + ", ".join(map(str, values)) + "}"


@question_type(
    "math.functional_equation_value_set_olympiad",
    display_name={"th": "ค่าที่เป็นไปได้ของสมการเชิงฟังก์ชัน"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="สมการเชิงฟังก์ชัน",
)
class FunctionalEquationValueSet(WordProblem):
    def expr(self, rng: Random):
        scale = rng.randint(2, 12)
        point = rng.choice(tuple(range(-9, 0)) + tuple(range(1, 10)))
        values = possible_values(scale, point)
        magnitude = values[2]
        return MathDraw(
            rf"c={scale**2},\quad t={point}",
            _set(values),
            prompt=(
                "ฟังก์ชัน f:ℝ→ℝ สอดคล้องกับ "
                "f(x)f(y)f(x−y)=c[x²f(y)−y²f(x)] สำหรับทุก x,y∈ℝ "
                "จงหาเซตของค่าที่เป็นไปได้ของ f(t)"
            ),
            hint="ถ้า f ไม่เป็นศูนย์ทุกจุด จงหารสมการด้วย f(x)f(y) แล้วเทียบ x กับ 2x",
            distractors=[
                _set((-magnitude, magnitude)),  # omit the zero function
                _set((0, magnitude)),  # discard the negative linear solution
                _set((-scale**2 * abs(point), 0, scale**2 * abs(point))),  # use c, not sqrt(c)
                _set((-abs(point), 0, abs(point))),  # forget the coefficient
                _set((0,)),  # assume no nonzero solution
            ],
        )
