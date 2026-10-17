"""n! modulo a prime p from Wilson's theorem when n is close to p."""

from __future__ import annotations

from math import factorial
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2562, ข้อ 10",)
)

PRIMES = tuple(
    p for p in range(53, 500) if all(p % d for d in range(2, int(p**0.5) + 1))
)


def wilson_reflection(p: int, n: int) -> int:
    """(p−1)! = n!·(n+1)⋯(p−1) ≡ n!·(−1)^k·k! ≡ −1 with k = p − 1 − n."""
    k = p - 1 - n
    if not 0 <= k < p - 1:
        raise ValueError("n must lie in 1..p−1")
    return (-1) ** (k + 1) * pow(factorial(k), -1, p) % p


@question_type(
    "math.wilson_reflection_factorial_olympiad",
    display_name={"th": "เศษของแฟกทอเรียลใกล้จำนวนเฉพาะด้วยทฤษฎีบทวิลสัน"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="ทฤษฎีจำนวน: ห.ร.ม. และ ค.ร.น.",
)
class WilsonReflectionFactorial(WordProblem):
    def expr(self, rng: Random):
        p = rng.choice(PRIMES)
        k = rng.randint(2, 6)
        n = p - 1 - k
        answer = wilson_reflection(p, n)
        wrong = []
        for value in (
            (-answer) % p,  # drop the sign (−1)^k
            factorial(k) % p,  # use k! instead of its inverse
            (-factorial(k)) % p,
            p - 1,  # quote Wilson's theorem for (p−1)! itself
            (answer + 1) % p,
            (answer - 1) % p,
        ):
            if value != answer and value not in wrong:
                wrong.append(value)
        return MathDraw(
            rf"{n}!\ \bmod\ {p}",
            str(answer),
            prompt=f"{p} เป็นจำนวนเฉพาะ จงหาเศษเหลือจากการหาร {n}! ด้วย {p}",
            hint=f"ใช้ ({p - 1})! ≡ −1 (mod {p}) และ {n + 1}·{n + 2}⋯{p - 1} ≡ (−1)^{k}·{k}! (mod {p})",
            distractors=[str(value) for value in wrong],
        )
