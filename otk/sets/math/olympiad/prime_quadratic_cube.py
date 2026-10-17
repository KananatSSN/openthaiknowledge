"""Primes p making αp² − βp − 1 a perfect cube, built from the n + 1 = p case."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2557, ข้อ 6",)
)

LIMIT = 2000
PRIMES = tuple(p for p in range(2, LIMIT + 1) if all(p % d for d in range(2, int(p**0.5) + 1)))


def is_cube(value: int) -> bool:
    if value <= 0:
        return False
    root = round(value ** (1 / 3))
    return any((root + d) ** 3 == value for d in (-1, 0, 1))


def coefficients(first: int, second: int) -> tuple[int, int]:
    """With n + 1 = p, p(αp − β) = (n + 1)(n² − n + 1) becomes
    αp − β = p² − 3p + 3, so roots p₁, p₂ need α = p₁ + p₂ − 3, β = p₁p₂ − 3."""
    return first + second - 3, first * second - 3


def cube_primes(alpha: int, beta: int) -> tuple[int, ...]:
    return tuple(p for p in PRIMES if is_cube(alpha * p * p - beta * p - 1))


PAIRS = tuple(
    (p, q) for p in PRIMES[:11] for q in PRIMES[:11] if p < q and p + q > 3
)


@question_type(
    "math.prime_quadratic_cube_olympiad",
    display_name={"th": "จำนวนเฉพาะที่ทำให้พหุนามกำลังสองเป็นกำลังสาม"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="ทฤษฎีจำนวนเชิงพีชคณิต",
)
class PrimeQuadraticCube(WordProblem):
    def expr(self, rng: Random):
        first, second = rng.choice(PAIRS)
        alpha, beta = coefficients(first, second)
        found = cube_primes(alpha, beta)
        answer = sum(found)
        wrong = []
        for value in (
            first,  # stop at the first root
            second,
            first * second,
            first + second + 2,  # add a non-prime root
            answer + second,
            answer - 1,
        ):
            if value != answer and value > 0 and value not in wrong:
                wrong.append(value)
        lead = "" if alpha == 1 else str(alpha)
        return MathDraw(
            rf"{lead}p^2-{beta}p-1",
            str(answer),
            prompt=f"จงหาผลบวกของจำนวนเฉพาะ p ทั้งหมดที่ไม่เกิน {LIMIT} ซึ่งทำให้นิพจน์ต่อไปนี้เป็นกำลังสามของจำนวนเต็มบวก",
            hint="เขียนเป็น p(αp − β) = n³ + 1 = (n + 1)(n² − n + 1) แล้วพิจารณาว่า p หาร n + 1 หรือ n² − n + 1",
            distractors=[str(value) for value in wrong],
        )
