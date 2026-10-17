"""f = 1 + x + … + x^(n−1) divides xⁿ − 1, so f(x^m) reduces exponent by exponent modulo n."""

from __future__ import annotations

from math import gcd
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2547, วันแรก ข้อ 6",))


def remainder_tex(n: int, m: int) -> str:
    """x^(mk) ≡ x^(mk mod n); with g = gcd(m, n) each multiple of g below n
    appears g times, giving g(1 + x^g + … + x^(n−g)); for g = 1 that is g·f ≡ 0
    (source: n = 7, m = 7 → 7)."""
    g = gcd(m, n)
    if g == 1:
        return "0"
    if g == n:
        return str(n)
    terms = ["1"] + [("x" if j * g == 1 else f"x^{{{j * g}}}") for j in range(1, n // g)]
    return f"{g}(" + "+".join(terms) + ")"


@question_type(
    "math.cyclotomic_power_remainder_olympiad",
    display_name={"th": "เศษจากการหาร f(x^m) ด้วย f(x)"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="การหารพหุนาม",
)
class CyclotomicPowerRemainder(WordProblem):
    def expr(self, rng: Random):
        n = rng.randint(4, 10)
        m = rng.choice([n * rng.randint(1, 3), rng.randint(2, 30)])
        answer = remainder_tex(n, m)
        others = [remainder_tex(n, n), "0", "1", remainder_tex(n, 2) if n % 2 == 0 else str(m % n), str(m)]
        wrong = [t for t in dict.fromkeys(others) if t != answer]
        f_tex = "+".join([f"x^{{{j}}}" for j in range(n - 1, 1, -1)] + ["x", "1"])
        return MathDraw(
            rf"f(x)={f_tex}",
            answer,
            prompt=f"จงหาเศษเหลือจากการหาร f(x^{m}) ด้วย f(x)",
            hint="f(x) หาร xⁿ − 1 ลงตัว จึง xⁿ ≡ 1 (mod f(x)) ลดเลขชี้กำลังแต่ละพจน์มอดุโล n",
            distractors=wrong,
        )
