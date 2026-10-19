"""The least positive integer with exactly d divisors, over exponent patterns."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2550, วันแรก ข้อ 16",))


SMALL_PRIMES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29)
COUNTS = (6, 8, 10, 12, 14, 15, 16, 18, 20, 24, 28, 30, 32, 36, 40, 42, 45, 48, 60)


def patterns(d: int, largest: int) -> list[list[int]]:
    """Non-increasing factorisations d = f₁f₂… with every fᵢ ≥ 2 and ≤ largest."""
    if d == 1:
        return [[]]
    out = []
    for f in range(min(d, largest), 1, -1):
        if d % f == 0:
            out += [[f] + rest for rest in patterns(d // f, f)]
    return out


def value(factors: list[int], ascending: bool = False) -> int:
    exps = sorted((f - 1 for f in factors), reverse=not ascending)
    out = 1
    for p, e in zip(SMALL_PRIMES, exps):
        out *= p ** e
    return out


def least_with_divisors(d: int) -> int:
    """τ(n) = Π(eᵢ + 1); the largest exponents go on the smallest primes
    (source: d = 24 gives 2³·3²·5 = 360)."""
    return min(value(f) for f in patterns(d, d))


def prime_split(d: int) -> list[int]:
    out, f = [], 2
    while d > 1:
        while d % f == 0:
            out.append(f)
            d //= f
        f += 1
    return out


@question_type(
    "math.smallest_with_divisor_count_olympiad",
    display_name={"th": "จำนวนเต็มบวกที่น้อยที่สุดที่มีจำนวนตัวหารตามกำหนด"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="ตัวประกอบของจำนวนเต็ม",
)
class SmallestWithDivisorCount(WordProblem):
    def expr(self, rng: Random):
        d = rng.choice(COUNTS)
        answer = least_with_divisors(d)
        best = min(patterns(d, d), key=value)
        wrong = [v for v in dict.fromkeys([value(prime_split(d)), value(best, ascending=True), min(value(f) for f in patterns(d, d) if len(f) <= 2), least_with_divisors(d + 1), sorted({value(f) for f in patterns(d, d)})[1]]) if v != answer]
        return MathDraw(
            rf"\tau(n)={d}",
            str(answer),
            prompt=f"จงหาจำนวนเต็มบวก n ที่น้อยที่สุดที่มีจำนวนตัวหารที่เป็นบวกเท่ากับ {d} ตัว",
            hint="ถ้า n = p₁^e₁ p₂^e₂ … แล้ว τ(n) = (e₁ + 1)(e₂ + 1)… ลองทุกวิธีแยก d เป็นผลคูณ และให้เลขชี้กำลังมากอยู่กับจำนวนเฉพาะน้อย",
            distractors=[str(v) for v in wrong],
        )
