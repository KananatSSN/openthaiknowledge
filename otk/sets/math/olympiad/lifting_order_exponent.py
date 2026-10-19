"""Smallest n with p^k | aⁿ − bⁿ; it exists for every k once p | a^m − b^m."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2552, วันที่สอง ข้อ 1",))


def smallest_exponent(a: int, b: int, p: int, k: int, limit: int = 100000) -> int:
    """If p | a^m − b^m with p ∤ b, then a^m ≡ b^m and (a^m)^{p^{k−1}} ≡
    (b^m)^{p^{k−1}} (mod p^k) by lifting, so n = m·p^{k−1} works."""
    modulus = p**k
    for n in range(1, limit):
        if (pow(a, n, modulus) - pow(b, n, modulus)) % modulus == 0:
            return n
    raise ValueError("no exponent below the limit")


CASES = tuple(
    (a, b, p)
    for p in (3, 5, 7)
    for a in range(2, 12) for b in range(2, 12)
    if a != b and a % p and b % p
)


@question_type(
    "math.lifting_order_exponent_olympiad",
    display_name={"th": "เลขชี้กำลังน้อยสุดที่ pᵏ หาร aⁿ − bⁿ"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="เลขคณิตมอดุลาร์",
)
class LiftingOrderExponent(WordProblem):
    def expr(self, rng: Random):
        a, b, p = rng.choice(CASES)
        k = rng.randint(2, 4)
        answer = smallest_exponent(a, b, p, k)
        first = smallest_exponent(a, b, p, 1)
        wrong = [v for v in dict.fromkeys([first, first * k, first * p**k, answer * p, (p - 1) * p ** (k - 1), answer + 1]) if v != answer]
        return MathDraw(
            rf"{p}^{{{k}}}\mid {a}^n-{b}^n",
            str(answer),
            prompt="จงหาจำนวนนับ n ที่น้อยที่สุดที่ทำให้เงื่อนไขต่อไปนี้เป็นจริง",
            hint="หา n ที่น้อยที่สุดสำหรับ p ก่อน แล้วพิจารณาการยกกำลัง p เพื่อยกระดับไปยัง p², p³, …",
            distractors=[str(v) for v in wrong],
        )
