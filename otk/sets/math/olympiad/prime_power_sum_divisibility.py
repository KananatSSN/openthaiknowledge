"""Prime triples with pq | rᵖ + r^q, by Fermat's little theorem."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2553, วันที่สอง ข้อ 6",)
)


def _primes(limit: int) -> list[int]:
    return [p for p in range(2, limit + 1) if all(p % d for d in range(2, int(p**0.5) + 1))]


def triple_count(limit: int) -> int:
    """Ordered prime triples (p, q, r) ≤ limit with pq | rᵖ + r^q. When
    p, q > r, Fermat gives rᵖ + r^q ≡ r + r^q (mod p), so r^{q−1} ≡ −1 and
    the orders of r force a contradiction: no such triple has p, q > r."""
    primes = _primes(limit)
    return sum(
        1
        for p in primes for q in primes for r in primes
        if (pow(r, p, p * q) + pow(r, q, p * q)) % (p * q) == 0
    )


@question_type(
    "math.prime_power_sum_divisibility_olympiad",
    display_name={"th": "สามสิ่งอันดับจำนวนเฉพาะที่ pq หาร rᵖ + r^q"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="ทฤษฎีจำนวน: ห.ร.ม. และ ค.ร.น.",
)
class PrimePowerSumDivisibility(WordProblem):
    def expr(self, rng: Random):
        limit = rng.choice([5, 7, 11, 13, 17, 19, 23, 29, 31])
        answer = triple_count(limit)
        wrong = [v for v in dict.fromkeys([answer + 1, max(answer - 1, 0), answer + 2, 2 * answer, answer + 4]) if v != answer]
        return MathDraw(
            rf"p,q,r\le {limit},\quad pq\mid r^{{p}}+r^{{q}}",
            str(answer),
            prompt="มีสามสิ่งอันดับ (p, q, r) ของจำนวนเฉพาะที่ไม่เกินค่าที่กำหนดกี่ชุดที่สอดคล้องเงื่อนไข",
            hint="ใช้ทฤษฎีบทเล็กของแฟร์มาต์ลดเลขชี้กำลังมอดุโล p และ q และพิจารณากรณี r เท่ากับ p หรือ q",
            distractors=[str(v) for v in wrong],
        )
