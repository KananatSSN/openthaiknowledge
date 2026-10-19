"""x² + ax − n has integer roots iff n = r(r + a) for an integer r ≥ 1."""

from __future__ import annotations

from math import isqrt
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2549, วันแรก ข้อ 15",))


def root_count(a: int, bound: int) -> int:
    """Roots r and −a − r with product −n, so n = r(r + a); for n ≥ 1 take
    r ≥ 1 (r ≤ −a − 1 gives the same n). r(r + a) is increasing, so count
    r with r(r + a) < N (source: a = 1, N = 2549 → 49)."""
    r = 0
    while (r + 1) * (r + 1 + a) < bound:
        r += 1
    return r


@question_type(
    "math.integer_root_quadratic_count_olympiad",
    display_name={"th": "จำนวนค่า n ที่ทำให้สมการกำลังสองมีรากเป็นจำนวนเต็ม"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="สมการกำลังสอง",
)
class IntegerRootQuadraticCount(WordProblem):
    def expr(self, rng: Random):
        a, bound = rng.randint(1, 9), rng.randint(200, 6000)
        answer = root_count(a, bound)
        wrong = [v for v in dict.fromkeys([2 * answer, answer + 1, isqrt(bound), answer - 1, root_count(a, bound + 1) + 1]) if v != answer]
        lead = "x" if a == 1 else f"{a}x"
        return MathDraw(
            rf"x^2+{lead}-n=0,\quad n<{bound}",
            str(answer),
            prompt="มีจำนวนนับ n กี่จำนวนที่ทำให้สมการต่อไปนี้มีรากเป็นจำนวนเต็ม",
            hint="ถ้ารากหนึ่งเป็น r อีกรากเป็น −a − r ผลคูณของรากคือ −n จึง n = r(r + a)",
            distractors=[str(v) for v in wrong],
        )
