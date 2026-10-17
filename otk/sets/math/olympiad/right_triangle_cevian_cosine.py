"""cos∠CAE for E dividing the hypotenuse BE : EC = p : q in a right triangle."""

from __future__ import annotations

from math import gcd
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2551, วันแรก ข้อ 1",))


def cosine_parts(angle_b: int, p: int, q: int) -> tuple[int, int, int]:
    """With A at the origin, AB = 1 on the x-axis and AC = tan B on the y-axis,
    E = (q, p·tan B)/(p + q), so cos∠CAE = p tan B/√(q² + p² tan² B).
    Returned as (k, s, D): cos = k√s/√D with s ∈ {1, 3}."""
    if angle_b == 60:
        return p, 3, q * q + 3 * p * p
    if angle_b == 45:
        return p, 1, p * p + q * q
    if angle_b == 30:
        return p, 1, 3 * q * q + p * p
    raise ValueError(angle_b)


def cosine_tex(k: int, s: int, d: int) -> str:
    """k√s/√d rationalised as k√(sd)/d, reduced."""
    radicand, outside = s * d, 1
    f = 2
    while f * f <= radicand:
        while radicand % (f * f) == 0:
            radicand //= f * f
            outside *= f
        f += 1
    num, den = k * outside, d
    g = gcd(num, den)
    num, den = num // g, den // g
    root = "" if radicand == 1 else rf"\sqrt{{{radicand}}}"
    top = (str(num) if num != 1 or not root else "") + root
    return top if den == 1 else rf"\frac{{{top}}}{{{den}}}"


@question_type(
    "math.right_triangle_cevian_cosine_olympiad",
    display_name={"th": "โคไซน์ของมุมที่เส้นจากมุมฉากแบ่งด้านตรงข้าม"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="เรขาคณิต: สามเหลี่ยมมุมฉาก",
)
class RightTriangleCevianCosine(WordProblem):
    def expr(self, rng: Random):
        angle_b = rng.choice((30, 45, 60))
        p, q = rng.randint(1, 6), rng.randint(1, 6)
        while p == q:
            q = rng.randint(1, 6)
        answer = cosine_tex(*cosine_parts(angle_b, p, q))
        wrong = [t for t in dict.fromkeys([
            cosine_tex(*cosine_parts(angle_b, q, p)),  # swap BE and EC
            cosine_tex(*cosine_parts(90 - angle_b if angle_b != 45 else 60, p, q)),
            cosine_tex(p, 1, p * p + q * q),
            cosine_tex(q, 1, p * p + q * q),
            cosine_tex(1, 1, 2),
        ]) if t != answer]
        return MathDraw(
            rf"\angle BAC=90^\circ,\ \angle ABC={angle_b}^\circ,\quad BE:EC={p}:{q}",
            answer,
            prompt="E อยู่บน BC ตามอัตราส่วนต่อไปนี้ จงหา cos∠CAE",
            hint="วาง A ที่จุดกำเนิด AB บนแกน x และ AC บนแกน y แล้วหาพิกัดของ E จากอัตราส่วน",
            distractors=wrong,
        )
