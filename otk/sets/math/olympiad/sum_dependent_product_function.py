"""If f(m)f(n) depends only on m + n, then f is geometric."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2554, ข้อ 2",)
)


def geometric_value(first: int, ratio: int, k: int) -> int:
    """f(1)f(n) = f(2)f(n − 1) gives f(n)/f(n − 1) = f(2)/f(1). In the source,
    f(2m + 2n) = f(m)f(n) makes f(m)f(n) depend on m + n, and then
    r^{m+n+1} = f(1) for every m + n forces r = 1 and f ≡ 1."""
    return first * ratio ** (k - 1)


@question_type(
    "math.sum_dependent_product_function_olympiad",
    display_name={"th": "ฟังก์ชันที่ f(m)f(n) ขึ้นกับ m + n เท่านั้น"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="สมการเชิงฟังก์ชัน",
)
class SumDependentProductFunction(WordProblem):
    def expr(self, rng: Random):
        first = rng.randint(1, 6)
        ratio = rng.randint(2, 5)
        k = rng.randint(4, 9)
        answer = geometric_value(first, ratio, k)
        wrong = [v for v in dict.fromkeys([
            first * ratio**k,  # off by one in the exponent
            first * ratio ** (k - 2),
            first + (k - 1) * ratio,  # arithmetic instead of geometric
            (first * ratio) ** (k - 1),
            ratio ** (k - 1),
        ]) if v != answer]
        return MathDraw(
            rf"f(1)={first},\quad f(2)={first * ratio}",
            str(answer),
            prompt=(
                "f : ℕ → ℕ มีสมบัติว่า f(m)f(n) = f(m′)f(n′) ทุกครั้งที่ m + n = m′ + n′ "
                f"จงหา f({k})"
            ),
            hint="เทียบ f(1)f(n) กับ f(2)f(n − 1) จะได้อัตราส่วน f(n)/f(n − 1) คงตัว",
            distractors=[str(v) for v in wrong],
        )
