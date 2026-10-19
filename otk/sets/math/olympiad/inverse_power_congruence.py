"""p | n^(p − 4) + j³ means n⁻³ ≡ −j³, so n ≡ −1/j when 3 ∤ p − 1."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2549, วันแรก ข้อ 14",))


PRIMES = (503, 509, 521, 557, 563, 569, 587, 593, 599, 617, 641, 647, 653, 659, 677, 683, 701, 719, 743, 761, 773, 797, 809, 821, 827, 839, 857, 863, 881, 887, 911, 929, 941, 947, 953, 971, 977, 983, 1013, 1019, 2549)


def least_solution(p: int, j: int) -> int:
    """By Fermat n^(p − 4) ≡ n⁻³, so n⁻³ ≡ −j³ gives (−jn)³ ≡ 1, and cubing
    is a bijection when 3 ∤ p − 1: n ≡ −1/j (source: p = 2549, j = 2 → 1274)."""
    return -pow(j, -1, p) % p


@question_type(
    "math.inverse_power_congruence_olympiad",
    display_name={"th": "จำนวนนับน้อยสุดที่สอดคล้องสมภาคกำลังผกผัน"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="เลขคณิตมอดุลาร์",
)
class InversePowerCongruence(WordProblem):
    def expr(self, rng: Random):
        p = rng.choice(PRIMES)
        j = rng.randint(2, 7)
        answer = least_solution(p, j)
        c = p - j**3
        wrong = [v for v in dict.fromkeys([pow(j, -1, p), p - j, -pow(j**3, -1, p) % p, (p - 1) // j, answer + p]) if v != answer]
        return MathDraw(
            rf"{p}\mid n^{{{p - 4}}}-{c}",
            str(answer),
            prompt=f"จงหาจำนวนนับ n ที่น้อยที่สุดที่สอดคล้องเงื่อนไขต่อไปนี้ ({p} เป็นจำนวนเฉพาะ)",
            hint=f"โดยทฤษฎีบทแฟร์มาต์ n^{p - 4} ≡ n⁻³ และ {c} ≡ −{j**3} = −{j}³ ใช้ว่า 3 ไม่หาร {p - 1}",
            distractors=[str(v) for v in wrong],
        )
