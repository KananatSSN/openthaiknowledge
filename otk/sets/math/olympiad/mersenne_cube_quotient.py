"""x·yᵏ/(x + y) = pᵏ: only x = 2, y = 2p with p = 2ᵏ − 1 prime."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2556, ข้อ 10",)
)

EXPONENTS = (2, 3, 5, 7, 13)  # 2ᵏ − 1 prime


def unique_solution(k: int) -> tuple[int, int, int]:
    """x = du, y = dv, gcd(u, v) = 1 gives dᵏuvᵏ = pᵏ(u + v), so uvᵏ | pᵏ and
    u + v | dᵏ. Only u = 1, v = p survives, with dᵏ = p + 1, so d = 2."""
    p = 2**k - 1
    return 2, 2 * p, p


@question_type(
    "math.mersenne_cube_quotient_olympiad",
    display_name={"th": "คู่ x, y ที่ xyᵏ/(x + y) เป็นกำลังของจำนวนเฉพาะ"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="ทฤษฎีจำนวนเชิงพีชคณิต",
)
class MersenneCubeQuotient(WordProblem):
    def expr(self, rng: Random):
        k = rng.choice(EXPONENTS)
        x, y, p = unique_solution(k)
        words = {2: "กำลังสอง", 3: "กำลังสาม"}.get(k, f"กำลัง {k}")
        if rng.randrange(2):
            answer, asked = x + y, "x + y"
            candidates = [2**k, 2 ** (k + 1) - 2, p, 2 ** (k + 1) + 2, 3 * p]
        else:
            answer, asked = p, "จำนวนเฉพาะ p ดังกล่าว"
            candidates = [2**k + 1, 2 ** (k + 1) - 1, 2**k, p + 2, y]
        wrong = [v for v in dict.fromkeys(candidates) if v != answer]
        return MathDraw(
            rf"\frac{{xy^{{{k}}}}}{{x+y}}=p^{{{k}}}",
            str(answer),
            prompt=f"จำนวนเต็มบวก x, y คู่เดียวที่ทำให้ xy^{k}/(x + y) เป็น{words}ของจำนวนเฉพาะ p จงหา{asked}",
            hint="ให้ d = ห.ร.ม.(x, y), x = du, y = dv แล้ว u + v เป็นจำนวนเฉพาะสัมพัทธ์กับ uv",
            distractors=[str(v) for v in wrong],
            variant=asked,
        )
