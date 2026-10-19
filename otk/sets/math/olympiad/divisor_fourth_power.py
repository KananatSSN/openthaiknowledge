"""n = d(n)⁴: the solutions are 1, 5⁴, 3⁸ and 3⁸·5⁴."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2554, ข้อ 5",)
)

SOLUTIONS = (1, 625, 6561, 4100625)


def divisor_count(n: int) -> int:
    count, d = 1, 2
    while d * d <= n:
        e = 0
        while n % d == 0:
            n //= d
            e += 1
        count *= e + 1
        d += 1
    return count * (2 if n > 1 else 1)


def is_solution(n: int) -> bool:
    """n is a fourth power, so n = Π p^{4a} and d(n) = Π(4a + 1) is odd: n is
    odd. Then (4a + 1) ≤ p^a with equality only for p = 5, a = 1 or p = 3,
    a = 2, which leaves the four solutions above."""
    return divisor_count(n) ** 4 == n


NON_SOLUTIONS = tuple(m**4 for m in range(2, 60) if not is_solution(m**4))


@question_type(
    "math.divisor_fourth_power_olympiad",
    display_name={"th": "จำนวนที่เท่ากับกำลังสี่ของจำนวนตัวหาร"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="ตัวประกอบของจำนวนเต็ม",
)
class DivisorFourthPower(WordProblem):
    def expr(self, rng: Random):
        variant = rng.choice(("pick", "sum", "largest"))
        if variant == "pick":
            answer = rng.choice(SOLUTIONS[1:])
            wrong = rng.sample([v for v in NON_SOLUTIONS if v != answer], 5)
            return MathDraw(
                r"n=\big(d(n)\big)^4",
                str(answer),
                prompt="d(n) คือจำนวนตัวหารบวกของ n จำนวนใดต่อไปนี้สอดคล้องสมการ",
                hint="n ต้องเป็นกำลังสี่และเป็นจำนวนคี่ ลองคำนวณ d(n) ของแต่ละตัวเลือกโดยแยกตัวประกอบ",
                distractors=[str(v) for v in wrong],
                variant=variant,
            )
        if variant == "sum":
            answer = sum(SOLUTIONS)
            wrong = [sum(SOLUTIONS[1:]), 625 + 6561 + 1, 4100625, sum(SOLUTIONS) + 81, 6561 * 625 + 625]
            prompt = "จงหาผลบวกของจำนวนเต็มบวก n ทั้งหมดที่สอดคล้องสมการ เมื่อ d(n) คือจำนวนตัวหารบวกของ n"
        else:
            answer = max(SOLUTIONS)
            wrong = [6561, 625, 3**8 * 7**4, 5**8, 3**4 * 5**4]
            prompt = "จงหาจำนวนเต็มบวก n ที่มากที่สุดที่สอดคล้องสมการ เมื่อ d(n) คือจำนวนตัวหารบวกของ n"
        return MathDraw(
            r"n=\big(d(n)\big)^4",
            str(answer),
            prompt=prompt,
            hint="n = Π p^{4a} มี d(n) = Π(4a + 1) เป็นจำนวนคี่ เทียบ 4a + 1 กับ p^a",
            distractors=[str(v) for v in dict.fromkeys(wrong) if v != answer],
            variant=variant,
        )
