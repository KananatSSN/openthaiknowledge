"""A divisibility recurrence with a unique positive-integer sequence."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2564, ข้อ 2",)
)


def unique_term(constant: int, shift: int, index: int) -> int:
    """Term of the only positive-integer solution to the parameterized recurrence."""
    if constant < 1 or shift < 0 or index < 1:
        raise ValueError("expected a positive constant, nonnegative shift and index")
    return index + shift


@question_type(
    "math.integer_recurrence_rigidity_olympiad",
    display_name={"th": "ลำดับจำนวนเต็มจากสมการเวียนเกิดที่บังคับคำตอบ"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="ลำดับและอนุกรม",
)
class IntegerRecurrenceRigidity(WordProblem):
    def expr(self, rng: Random):
        constant = rng.choice((1, 2, 3, 5, 7))
        shift = rng.randint(0, 5)
        index = rng.randint(4, 12)
        rhs = rf"n^3+{shift + 1}n^2"
        if constant > 1:
            rhs += rf"+{constant - 1}n"
        rhs += rf"+{constant + shift * (constant - 1)}"
        answer = unique_term(constant, shift, index)
        return MathDraw(
            rf"(n^2+{constant})a_{{n+1}}-a_n={rhs},\quad n\ge1,\quad k={index}",
            str(answer),
            prompt=(
                "ลำดับอนันต์ a₁,a₂,… มีทุกพจน์เป็นจำนวนเต็มบวก "
                "และเป็นไปตามสมการที่กำหนดสำหรับทุก n จงหา aₖ"
            ),
            hint=(
                "พิจารณาสมการโมดูลัส n²+c เพื่อเขียน aₙ=n+t+(n²+c)bₙ "
                "แล้วดูความสัมพันธ์ของจำนวนเต็มไม่ลบ bₙ"
            ),
            distractors=[
                str(index),  # overlook the additive shift
                str(answer + 1),  # advance the index one step too far
                str(answer - 1),  # stop one step too early
                str(answer + constant),  # add the denominator constant to the term
                str(constant + shift),  # return the initial offset instead of a_k
                str(1 + shift),  # return a_1 instead of a_k
            ],
        )
