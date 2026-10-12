"""เรนจ์ของฟังก์ชันกำลังสอง

คณิตศาสตร์ · ม.4 · สสวท. เพิ่มเติม
Indicators: ค เพิ่มเติม จำนวนและพีชคณิต 2 ม.4/2

Sets moved here from: math, math_algebra.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, MathType, WordProblem, poly_tex
from otk.sets._support.math_algebra import _nonzero

PROVENANCE = Provenance("original")


@question_type("math.quadratic_max_min_word",
               display_name={"th": "ค่าสูงสุด/ต่ำสุดของฟังก์ชันกำลังสอง"},
               level={"th": "ม.4"}, topic="เรนจ์ของฟังก์ชันกำลังสอง")
class QuadraticMaxMinWord(WordProblem):
    def expr(self, rng: Random, lead_hi: int = 3, h_hi: int = 8):
        a = _nonzero(rng, -lead_hi, lead_hi)
        h = rng.randint(-h_hi, h_hi)
        k = rng.randint(-15, 15)
        b, c = -2 * a * h, a * h * h + k
        shown = poly_tex((a, "x^2"), (b, "x"), (c, ""))
        word = "ต่ำสุด" if a > 0 else "สูงสุด"
        return MathDraw(
            shown, str(k),
            prompt=f"ฟังก์ชัน f(x) ต่อไปนี้มีค่า{word}เท่าใด",
            distractors=[str(h), str(c), str(-k)])


@question_type("math.quadratic_range_open_interval",
               display_name={"th": "เรนจ์ของฟังก์ชันกำลังสองบนทุกจำนวนจริง"},
               level={"th": "ม.4"}, topic="เรนจ์ของฟังก์ชันกำลังสอง")
class QuadraticRangeAllReals(MathType):
    def expr(self, rng: Random, lead_hi: int = 3, h_hi: int = 6):
        a = _nonzero(rng, -lead_hi, lead_hi)
        h = rng.randint(-h_hi, h_hi)
        k = rng.randint(-12, 12)
        b, c = -2 * a * h, a * h * h + k
        shown = poly_tex((a, "x^2"), (b, "x"), (c, ""))
        answer = rf"[{k}, \infty)" if a > 0 else rf"(-\infty, {k}]"
        return MathDraw(
            f"f(x) = {shown}", answer,
            prompt="จงหาเรนจ์ของฟังก์ชันนี้ เมื่อโดเมนเป็นจำนวนจริงทั้งหมด",
            distractors=[rf"(-\infty, {k}]" if a > 0 else rf"[{k}, \infty)",
                         rf"[{h}, \infty)", r"(-\infty, \infty)"])


@question_type("math.quadratic_range",
               display_name={"th": "เรนจ์ของฟังก์ชันกำลังสองบนโดเมนปิด"},
               level={"th": "ม.4"}, topic="เรนจ์ของฟังก์ชันกำลังสอง")
class QuadraticRange(MathType):
    def expr(self, rng: Random):
        p, q = rng.randint(-3, 3), rng.randint(-6, 4)
        d1 = p - rng.randint(0, 3)
        d2 = d1 + rng.randint(2, 5)
        f = lambda x: (x - p) ** 2 + q
        v1, v2 = f(d1), f(d2)
        lo = q if d1 <= p <= d2 else min(v1, v2)
        hi = max(v1, v2)
        tex = poly_tex((1, "x^{2}"), (-2 * p, "x"), (p * p + q, ""))
        return MathDraw(rf"y = {tex} \;\; ({d1} \leq x \leq {d2})",
                        rf"{lo} \leq y \leq {hi}",
                        hint=rf"\text{{vertex at }} x = {p}",
                        prompt="จงหาเรนจ์ของฟังก์ชัน")
