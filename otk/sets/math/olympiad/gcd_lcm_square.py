"""Square least common multiples under a fixed gcd."""

from __future__ import annotations

from math import gcd, isqrt
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("original")


def squarefree_kernel(value: int) -> int:
    """Return the product of primes with odd exponent in a positive integer."""
    if value < 1:
        raise ValueError("value must be positive")
    remaining, kernel, prime = value, 1, 2
    while prime * prime <= remaining:
        odd = False
        while remaining % prime == 0:
            remaining //= prime
            odd = not odd
        if odd:
            kernel *= prime
        prime += 1
    return kernel * remaining


def sum_fixed_gcd_square_lcm(modulus: int, fixed_gcd: int, limit: int) -> int:
    """Sum positive n<=limit with gcd(n,modulus)=fixed_gcd and square lcm.

    Write n=G*t and M=G*m. The gcd condition is gcd(t,m)=1, and the
    least common multiple is M*t. If the squarefree kernel s of M shares a
    prime with m, no t works. Otherwise t=s*u² with gcd(u,m)=1.
    """
    if modulus < 1 or fixed_gcd < 1 or modulus % fixed_gcd or limit < 1:
        raise ValueError("expected positive M,G,L with G dividing M")
    quotient = modulus // fixed_gcd
    kernel = squarefree_kernel(modulus)
    if gcd(kernel, quotient) != 1:
        return 0
    base = fixed_gcd * kernel
    return base * sum(
        u * u for u in range(1, isqrt(limit // base) + 1)
        if gcd(u, quotient) == 1
    )


_CASES = (
    (72, 24), (75, 15), (84, 21), (90, 10), (98, 14),
    (180, 60), (200, 40), (252, 84), (300, 60), (432, 108),
)


@question_type(
    "math.gcd_lcm_square_olympiad",
    display_name={"th": "ห.ร.ม. คงที่และ ค.ร.น. เป็นกำลังสอง"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="ทฤษฎีจำนวน: ห.ร.ม. และ ค.ร.น.",
)
class GcdLcmSquare(WordProblem):
    def expr(self, rng: Random):
        modulus, fixed_gcd = rng.choice(_CASES)
        base = fixed_gcd * squarefree_kernel(modulus)
        limit = base * rng.randint(5, 30) + rng.randrange(base)
        answer = sum_fixed_gcd_square_lcm(modulus, fixed_gcd, limit)
        quotient = modulus // fixed_gcd
        top = isqrt(limit // base)
        eligible = [u for u in range(1, top + 1) if gcd(u, quotient) == 1]
        return MathDraw(
            rf"1\le n\le {limit},\quad\gcd(n,{modulus})={fixed_gcd},\quad"
            rf"\operatorname{{lcm}}(n,{modulus})=k^2",
            str(answer),
            prompt="หาผลบวกของจำนวนเต็มบวก n ทุกค่าที่สอดคล้องกับเงื่อนไขที่กำหนด โดย k เป็นจำนวนเต็มบวก",
            hint=(rf"n={fixed_gcd}t,\quad\gcd(t,{quotient})=1;\quad "
                  rf"\operatorname{{lcm}}(n,{modulus})={modulus}t"),
            distractors=[
                str(base * sum(u * u for u in range(1, top + 1))),  # ignore coprimality
                str(base * sum(eligible)),  # forget that u is squared
                str(answer + base),  # include the next forbidden u as if it were 1
                str(answer - base),  # omit the first qualifying value
                str(answer + 2 * base),  # count an extra qualifying term
            ],
        )
