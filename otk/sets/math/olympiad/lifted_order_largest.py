"""q² | 3^(3n + 3) − 27 iff 27ⁿ ≡ 1 (mod q²), i.e. the order of 27 mod q² divides n."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2547, วันแรก ข้อ 15",))


PRIMES = (5, 7, 11, 13, 17, 19, 23)


def order(base: int, modulus: int) -> int:
    k, x = 1, base % modulus
    while x != 1:
        x = x * base % modulus
        k += 1
    return k


def largest(q: int, bound: int) -> int:
    """3^(3n + 3) − 27 = 27(27ⁿ − 1) and q ∤ 27, so n must be a multiple of
    the order of 27 mod q² (source: q = 13: order 39, so 13 | n → 2002)."""
    d = order(27, q * q)
    return bound - bound % d


@question_type(
    "math.lifted_order_largest_olympiad",
    display_name={"th": "จำนวนเต็มมากสุดที่ทำให้กำลังสองของจำนวนเฉพาะหารลงตัว"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="เลขคณิตมอดุลาร์",
)
class LiftedOrderLargest(WordProblem):
    def expr(self, rng: Random):
        q = rng.choice(PRIMES)
        bound = rng.randint(500, 3000)
        answer = largest(q, bound)
        d1 = order(27, q)
        wrong = [v for v in dict.fromkeys([bound - bound % d1, bound - bound % (q * (q - 1)), bound - bound % (q * q), bound - bound % order(3, q * q), bound]) if v != answer]
        return MathDraw(
            rf"n\le {bound},\quad {q * q}\mid 3^{{3n+3}}-27",
            str(answer),
            prompt="จงหาจำนวนเต็ม n ที่มากที่สุดที่สอดคล้องเงื่อนไขต่อไปนี้",
            hint=f"3^(3n+3) − 27 = 27(27ⁿ − 1) จึงต้องการ 27ⁿ ≡ 1 (mod {q * q}) หาอันดับของ 27 มอดุโล {q * q}",
            distractors=[str(v) for v in wrong],
        )
