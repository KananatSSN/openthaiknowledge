"""Products of real roots after composing a cubic with a quadratic."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem, poly_tex

PROVENANCE = Provenance("original")


def real_root_product(
    shift: int, depth: int, outer_roots: tuple[int | Fraction, ...]
) -> int | Fraction:
    """Product of distinct real x satisfying F((x+shift)^2-depth)=0.

    For each distinct root r of F, solve (x+shift)^2=depth+r.
    A negative right side gives no real root, zero gives one root -shift,
    and a positive right side gives a pair whose product is
    shift²-(depth+r). Different r values give disjoint root sets.
    """
    if len(set(outer_roots)) != len(outer_roots):
        raise ValueError("outer roots must be distinct")
    product: int | Fraction = 1
    for root in outer_roots:
        offset = depth + root
        if offset < 0:
            continue
        if offset == 0:
            product *= -shift
        else:
            product *= shift * shift - offset
    return product


@question_type(
    "math.composed_polynomial_real_roots_olympiad",
    display_name={"th": "ผลคูณรากจริงของพหุนามประกอบ"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="พหุนามและเศษเหลือ",
)
class ComposedPolynomialRoots(WordProblem):
    def expr(self, rng: Random):
        shift = rng.randint(2, 6)
        depth = rng.randint(1, 4)
        offsets = (-rng.randint(1, 4), rng.randint(1, 3), rng.randint(5, 7))
        roots = tuple(offset - depth for offset in offsets)
        answer = real_root_product(shift, depth, roots)
        root_sum = sum(roots)
        pair_sum = roots[0] * roots[1] + roots[0] * roots[2] + roots[1] * roots[2]
        root_product = roots[0] * roots[1] * roots[2]
        inner = poly_tex((1, "x^2"), (2 * shift, "x"), (shift * shift - depth, ""))
        outer = poly_tex((1, "y^3"), (-root_sum, "y^2"),
                         (pair_sum, "y"), (-root_product, ""))
        return MathDraw(
            rf"P(x)={inner},\quad F(y)={outer},\quad F(P(x))=0",
            str(answer),
            prompt="กำหนดพหุนามตามสมการ จงหาผลคูณของรากจริงที่แตกต่างกันทั้งหมดของสมการประกอบ",
            hint=(rf"P(x)=(x+{shift})^2-{depth};\quad "
                  rf"P(x)=r\Rightarrow(x+{shift})^2={depth}+r"),
            distractors=[
                str(answer * (shift * shift - offsets[0])),  # include impossible outer root
                str(-answer),  # lose the sign of the root-pair product
                str(-4 * shift),  # sum the four real roots instead
                str(answer + 1),  # off-by-one in a pair product
                str(answer - 1),  # off-by-one in a pair product
            ],
        )
