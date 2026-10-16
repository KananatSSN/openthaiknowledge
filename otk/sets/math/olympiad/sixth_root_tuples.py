"""Count ordered tuples of three roots subject to a sum constraint."""

from __future__ import annotations

from math import comb, factorial
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("original")


def sixth_root_tuple_count(m: int, n: int) -> int:
    """Count tuples from the roots of z^3-2z^2+2z-1 with sum z^7=n."""
    if n < 1 or not n <= m <= 2 * n:
        raise ValueError("require positive n and n <= m <= 2n")
    nonreal_each = m - n
    real = 2 * n - m
    return factorial(m) // (factorial(nonreal_each) ** 2 * factorial(real))


@question_type(
    "math.sixth_root_tuples_olympiad",
    display_name={"th": "นับชุดลำดับของรากเอกภาพอันดับหก"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="หลักการนับ",
)
class SixthRootTuples(WordProblem):
    def expr(self, rng: Random):
        n = rng.randint(3, 7)
        m = rng.randint(n + 1, 2 * n - 1)
        answer = sixth_root_tuple_count(m, n)
        t = m - n
        return MathDraw(
            rf"n={n},\quad m={m}",
            str(answer),
            prompt=(
                "แต่ละจำนวนเชิงซ้อน z₁,…,zₘ เป็นรากของสมการ z³−2z²+2z−1=0 "
                "ถ้า z₁⁷+⋯+zₘ⁷=n จงหาจำนวนชุดลำดับ (z₁,…,zₘ) ที่เป็นไปได้"
            ),
            hint="แยกรากจริงหนึ่งรากกับรากเชิงซ้อนสังยุค แล้วนับจำนวนของแต่ละชนิด",
            distractors=[
                str(comb(m, 2 * t)),  # merge conjugate types
                str(comb(m, t) ** 2),  # select their positions independently, allowing overlap
                str(factorial(m)),  # treat repeated roots as distinct
                str(answer + m),  # add one extra arrangement per position
            ],
        )
