"""Algebraic invariants from aggregate data, roots, and signed pairs."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem, poly_tex

PROVENANCE = Provenance("original")
LEVEL = {"th": "โอลิมปิก (สอวน.)"}


def shifted_square_sum(count: int, total: int, squares: int, shift: int) -> int:
    """Expand each (x_i - shift)^2 and aggregate like terms."""
    return squares - 2 * shift * total + count * shift * shift


def cubic_root_sum(root_sum: int, root_product: int) -> int:
    """Compute a^3+b^3 from the elementary symmetric polynomials."""
    return root_sum**3 - 3 * root_sum * root_product


def minimum_signed_pair_sum(count: int) -> int:
    """Minimum pair score when exactly ceil(count/2) indices have a plus sign.

    Twice the pair score is (sum(i*s_i))**2 - sum(i*i).  Sums of
    ceil(count/2) distinct indices from 1..count fill the integer interval
    between their smallest and largest possible sums, so the signed sum can
    attain the smallest magnitude allowed by the parity of 1+...+count.
    """
    total = count * (count + 1) // 2
    squares = count * (count + 1) * (2 * count + 1) // 6
    smallest_signed_sum = total % 2
    return (smallest_signed_sum**2 - squares) // 2


@question_type(
    "math.moment_shift_olympiad",
    display_name={"th": "ผลรวมกำลังสองหลังเลื่อนค่า"},
    level=LEVEL,
    topic="การจัดรูปพีชคณิต",
)
class ShiftedSquareSum(WordProblem):
    def expr(self, rng: Random):
        values = [rng.randint(-4, 9) for _ in range(rng.randint(5, 15))]
        count = len(values)
        total = sum(values)
        squares = sum(value * value for value in values)
        shift = rng.randint(1, 5)
        answer = shifted_square_sum(count, total, squares, shift)
        return MathDraw(
            rf"\sum_{{i=1}}^{{{count}}}x_i={total},\qquad "
            rf"\sum_{{i=1}}^{{{count}}}x_i^2={squares},\qquad "
            rf"\sum_{{i=1}}^{{{count}}}(x_i-{shift})^2=?",
            str(answer),
            prompt="จำนวนจริงชุดหนึ่งมีผลรวมและผลรวมกำลังสองตามที่กำหนด "
            "จงหาผลรวมกำลังสองหลังลบค่าคงตัวออกจากแต่ละจำนวน",
            hint=rf"(x_i-{shift})^2=x_i^2-2({shift})x_i+{shift**2}",
            distractors=[
                str(squares - 2 * shift * total),  # omit the constant term
                str(squares - 2 * shift * total + shift * shift),  # add it once
                str(squares + 2 * shift * total + count * shift * shift),  # sign
                str(squares - shift * total + count * shift * shift),  # factor 2
            ],
        )


@question_type(
    "math.symmetric_cubic_olympiad",
    display_name={"th": "ผลบวกกำลังสามของรากสมการ"},
    level=LEVEL,
    topic="การจัดรูปพีชคณิต",
)
class CubicRootSum(WordProblem):
    def expr(self, rng: Random):
        a = rng.choice((-8, -7, -6, -5, -4, -3, -2, 2, 3, 4, 5, 6, 7, 8))
        b = rng.choice((-8, -7, -6, -5, -4, -3, -2, 2, 3, 4, 5, 6, 7, 8))
        if a == b or a == -b:
            b = a + 1
        root_sum, root_product = a + b, a * b
        answer = cubic_root_sum(root_sum, root_product)
        equation = poly_tex((1, "x^2"), (-root_sum, "x"), (root_product, ""))
        return MathDraw(
            rf"{equation}=0,\qquad a^3+b^3=?",
            str(answer),
            prompt="ให้ a และ b เป็นรากสองรากของสมการกำลังสองที่กำหนด "
            "จงหาผลบวกกำลังสามของราก",
            hint=r"a^3+b^3=(a+b)^3-3ab(a+b)",
            distractors=[
                str(root_sum**3),  # treat powers as distributing over sum
                str(root_sum**3 - root_sum * root_product),  # omit factor 3
                str(root_sum**3 + 3 * root_sum * root_product),  # sign
                str(root_sum**2 - 2 * root_product),  # sum of squares
            ],
        )


@question_type(
    "math.signed_pair_minimum_olympiad",
    display_name={"th": "ผลบวกคู่แบบมีเครื่องหมายต่ำสุด"},
    level=LEVEL,
    topic="การจัดรูปพีชคณิต",
)
class SignedPairMinimum(WordProblem):
    def expr(self, rng: Random):
        count = rng.randint(6, 18)
        total = count * (count + 1) // 2
        squares = count * (count + 1) * (2 * count + 1) // 6
        answer = minimum_signed_pair_sum(count)
        alternating = sum(i if i % 2 else -i for i in range(1, count + 1))
        return MathDraw(
            rf"\sum_{{1\le i<j\le {count}}}ij\,s_i s_j\;=?",
            str(answer),
            prompt=(f"ติดป้าย + ให้ดัชนี {((count + 1) // 2)} ตัวจาก 1 ถึง {count} "
                    "และติดป้าย − ให้ตัวที่เหลือ โดย s_i เป็นเครื่องหมายของดัชนี i "
                    "จงหาค่าต่ำสุดของผลบวกที่กำหนด"),
            hint=(r"2\sum_{i<j}ij s_i s_j="
                  r"\left(\sum_i i s_i\right)^2-\sum_i i^2"),
            distractors=[
                str(-squares),  # forget the factor of two in the identity
                str((total * total - squares) // 2),  # ignore all minus signs
                str((alternating * alternating - squares) // 2),  # fix signs by index parity
                str(((total % 2 + 2) ** 2 - squares) // 2),  # accept a larger imbalance
            ],
        )
