"""Count coprime pairs making k·a(a²+b²)/(a²−b²) an integer."""

from __future__ import annotations

from math import gcd
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2562, ข้อ 2",)
)


def _pairs(k: int):
    # a² − b² is prime to a, and shares at most 2 with a² + b², so it divides
    # 2k; as a² − b² ≥ a + b, only a + b ≤ 2k can work.
    for total in range(3, 2 * k + 1):
        for b in range(1, (total + 1) // 2):
            yield total - b, b


def coprime_quotient_pairs(k: int) -> int:
    """Pairs a > b ≥ 1 with gcd 1 and (a² − b²) | k·a(a² + b²)."""
    if k < 1:
        raise ValueError("k must be positive")
    return sum(
        1
        for a, b in _pairs(k)
        if gcd(a, b) == 1 and k * a * (a * a + b * b) % (a * a - b * b) == 0
    )


def _divides_count(k: int) -> int:
    """Pairs with a² − b² | k: the slip of dropping the shared factor 2."""
    return sum(
        1 for a, b in _pairs(k) if gcd(a, b) == 1 and k % (a * a - b * b) == 0
    )


def _divides_twice_count(k: int) -> int:
    """Pairs with a² − b² | 2k for every parity: the slip of always sharing 2."""
    return sum(
        1 for a, b in _pairs(k) if gcd(a, b) == 1 and (2 * k) % (a * a - b * b) == 0
    )


@question_type(
    "math.coprime_square_difference_quotient_olympiad",
    display_name={"th": "คู่จำนวนเฉพาะสัมพัทธ์ที่ทำให้ผลหารเป็นจำนวนเต็ม"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="ทฤษฎีจำนวน: ห.ร.ม. และ ค.ร.น.",
)
class CoprimeSquareDifferenceQuotient(WordProblem):
    def expr(self, rng: Random):
        k = rng.randint(2, 60)
        answer = coprime_quotient_pairs(k)
        wrong = []
        for value in (
            _divides_count(k),
            _divides_twice_count(k),
            2 * answer,  # count (a, b) and (b, a) separately
            answer + 1,
            max(answer - 1, 0),
            answer + 2,
        ):
            if value != answer and value not in wrong:
                wrong.append(value)
        return MathDraw(
            rf"\frac{{{k}\,a\left(a^2+b^2\right)}}{{a^2-b^2}}",
            str(answer),
            prompt=(
                "จงหาจำนวนคู่อันดับ (a, b) ของจำนวนเต็มบวกซึ่ง a > b "
                "และ ห.ร.ม.(a, b) = 1 ที่ทำให้นิพจน์ต่อไปนี้เป็นจำนวนเต็ม"
            ),
            hint=(
                "a²−b² เป็นจำนวนเฉพาะสัมพัทธ์กับ a และมีตัวประกอบร่วมกับ a²+b² "
                "ได้ไม่เกิน 2 จึงต้องหาร 2k ลงตัว และ a²−b² ≥ a+b"
            ),
            distractors=[str(value) for value in wrong],
        )
