"""|f(x + y) − f(x) − f(y)| < 1 gives |f(nx) − n f(x)| < n − 1, a sharp bound."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2551, วันแรก ข้อ 6",))


def scaling_bound(n: int) -> int:
    """Induction: f(kx) = f((k − 1)x) + f(x) + error with |error| < 1, so the
    total error after n − 1 steps is below n − 1; f = c⌊x⌋ with c → 1 shows
    the bound n − 1 cannot be lowered. Dividing by n (x → x/n) gives the
    source's |f(x/2008) − f(x)/2008| < 2007/2008 < 1."""
    return n - 1


@question_type(
    "math.almost_additive_scaling_bound_olympiad",
    display_name={"th": "ขอบเขตของฟังก์ชันที่เกือบบวกได้"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="สมการเชิงฟังก์ชัน",
)
class AlmostAdditiveScalingBound(WordProblem):
    def expr(self, rng: Random):
        n = rng.randint(3, 3000)
        answer = scaling_bound(n)
        wrong = [v for v in dict.fromkeys([n, 1, n - 2, 2 * (n - 1), n // 2]) if v != answer and v > 0]
        return MathDraw(
            rf"|f(x+y)-f(x)-f(y)|<1,\quad n={n}",
            str(answer),
            prompt="f : ℝ → ℝ สอดคล้องเงื่อนไขทุก x, y จงหาค่า K ที่น้อยที่สุดซึ่งรับประกันว่า |f(nx) − n·f(x)| < K ทุก x และทุก f ดังกล่าว",
            hint="ใช้อุปนัย f(kx) = f((k − 1)x) + f(x) + ความคลาดเคลื่อน แล้วลองฟังก์ชัน c⌊x⌋ ที่ c ใกล้ 1",
            distractors=[str(v) for v in wrong],
        )
