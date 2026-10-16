"""Divisibility in a nonlinear recurrence."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("original")


def divisible_terms_through(index: int, endpoint: int) -> int:
    """Count a_q divisible by a_index for a_1=1, a_(n+1)=a_n^d+1.

    For d>=2, earlier terms are positive and strictly below a_index. Modulo
    a_index the recurrence moves from 0 to 1, then retraces those earlier
    terms. Its first return to 0 is exactly index steps later.
    """
    return endpoint // index


@question_type(
    "math.recurrence_divisibility_olympiad",
    display_name={"th": "จำนวนพจน์ที่หารลงตัวในลำดับเวียนเกิด"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="ลำดับและอนุกรม",
)
class RecurrenceDivisibility(WordProblem):
    def expr(self, rng: Random):
        exponent = rng.randint(2, 4)
        index = rng.randint(3, 8)
        endpoint = rng.randint(3 * index, 6 * index + 5)
        answer = divisible_terms_through(index, endpoint)
        return MathDraw(
            rf"a_1=1,\quad a_{{n+1}}=a_n^{{{exponent}}}+1,\quad "
            rf"1\le q\le {endpoint},\quad a_q\equiv0\pmod{{a_{index}}}",
            str(answer),
            prompt=(f"กำหนดลำดับตามสมการและตรึงพจน์ที่ {index} "
                    "จงนับดัชนี q ในช่วงที่กำหนดซึ่งพจน์ที่ q หารด้วยพจน์ที่ตรึงไว้ลงตัว"),
            hint=(r"a_{p+1}\equiv1\pmod{a_p};\ "
                  r"\text{เศษที่ตามมาซ้ำเศษของพจน์ก่อนหน้า}"),
            distractors=[
                str(endpoint // (index - 1)),  # one-step-short period
                str(endpoint // (index + 1)),  # one-step-long period
                str(answer + 1),  # include index zero
                str(endpoint - answer),  # count nonmultiples instead
            ],
        )
