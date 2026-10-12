"""กำลังสองสมบูรณ์

คณิตศาสตร์ · ม.3 · สสวท. พื้นฐาน
Indicators: ค 1.2 ม.3/*

Sets moved here from: math, math_algebra, math_apply_basic.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit import story as _story
from otk.kit.math_problems import (
    MathDraw,
    MathType,
    WordProblem,
    binomial_tex,
    coef_term,
    poly_tex,
)
from otk.sets._support.math_algebra import _nonzero, _signed
from otk.sets._support.math_apply_add import _c

PROVENANCE = Provenance("original")


@question_type("math.complete_square_constant",
               display_name={"th": "เติมพจน์ให้เป็นกำลังสองสมบูรณ์"},
               level={"th": "ม.3"}, topic="กำลังสองสมบูรณ์")
class CompleteSquareConstant(MathType):
    def expr(self, rng: Random, half_hi: int = 10):
        h = _nonzero(rng, -half_hi, half_hi)
        shown = poly_tex((1, "x^2"), (2 * h, "x"), (0, "")) + r" + \; ?"
        return MathDraw(
            shown, str(h * h),
            prompt="ต้องเติมจำนวนใดเพื่อให้เป็นกำลังสองสมบูรณ์",
            # Halving without squaring, and squaring without halving.
            distractors=[str(abs(h)), str(4 * h * h), str(abs(2 * h))])


@question_type("math.quadratic_vertex",
               display_name={"th": "จัดรูปกำลังสองสมบูรณ์"}, level={"th": "ม.3"},
               topic="กำลังสองสมบูรณ์")
class QuadraticVertex(MathType):
    def expr(self, rng: Random):
        p = rng.choice([1, -1]) * rng.randint(1, 5)
        q = rng.randint(-9, 9)
        tex = poly_tex((1, "x^{2}"), (-2 * p, "x"), (p * p + q, ""))
        vertex = rf"{binomial_tex(-p)}^{{2}}{coef_term(q, '')}"
        return MathDraw(rf"y = {tex}", rf"y = {vertex}",
                        hint=r"\text{complete the square}",
                        prompt="จงเขียนในรูปกำลังสองสมบูรณ์")


@question_type("math.vertex_form_convert", display_name={"th": "เขียนในรูปกำลังสองสมบูรณ์"},
               level={"th": "ม.3"}, topic="กำลังสองสมบูรณ์")
class VertexFormConvert(MathType):
    break_convergence = True  # one-part slips cluster round the answer
    def expr(self, rng: Random, h_hi: int = 8, k_hi: int = 15):
        h = _nonzero(rng, -h_hi, h_hi)
        k = rng.randint(-k_hi, k_hi)
        # (x − h)² + k = x² − 2hx + h² + k
        shown = poly_tex((1, "x^2"), (-2 * h, "x"), (h * h + k, ""))
        inner = poly_tex((1, "x"), (-h, ""))
        return MathDraw(
            shown, rf"({inner})^2{_signed(k)}",
            prompt="จงเขียนนิพจน์นี้ในรูปกำลังสองสมบูรณ์",
            distractors=[rf"({poly_tex((1, 'x'), (h, ''))})^2{_signed(k)}",
                         rf"({inner})^2{_signed(-k)}",
                         rf"({inner})^2{_signed(h * h + k)}"])


@question_type("math.vertex_context_m3",
               display_name={"th": "ค่ามากสุดและน้อยสุดด้วยกำลังสองสมบูรณ์"},
               level={"th": "ม.3"}, topic="กำลังสองสมบูรณ์")
class VertexContextM3(WordProblem):
    def expr(self, rng: Random):
        kind = rng.randrange(5)
        if kind == 0:
            t0 = rng.randint(1, 4)
            c = rng.randint(1, 40)                  # launch height, above the ground
            b, H = 10 * t0, c + 5 * t0 * t0
            ask_time = rng.random() < 0.4
            prompt = (f"ลูกบอลถูกโยนขึ้น ความสูงเมื่อเวลา t วินาที คือ h = -5t² + {b}t + {c} เมตร "
                      + ("ลูกบอลขึ้นสูงสุดเมื่อเวลากี่วินาที" if ask_time else "ลูกบอลขึ้นไปได้สูงสุดกี่เมตร"))
            if ask_time:
                return MathDraw("", str(t0), prompt=prompt,
                                distractors=_story.keep(b // 5, 2 * t0, t0 + 1, answer=t0, lo=1))
            return MathDraw("", str(H), prompt=prompt,
                            distractors=_story.keep(c, H + 5 * t0 * t0, b + c, answer=H, lo=1))
        if kind == 1:
            m, c = rng.randint(10, 40), rng.randint(20, 150)
            best = m * m - c
            return MathDraw("", _c(best),
                            prompt=(f"ร้านค้าขายสินค้า x ชิ้นต่อวัน ได้กำไร P = -x² + {2 * m}x - {c} บาท "
                                    f"กำไรมากที่สุดต่อวันเป็นกี่บาท"),
                            distractors=[_c(m * m + c), _c(4 * m * m - c), _c(m)])
        if kind == 2:
            s = 2 * rng.randint(6, 30)
            return MathDraw("", _c(s * s // 4),
                            prompt=(f"ลวดยาว {2 * s} เซนติเมตร ดัดเป็นรูปสี่เหลี่ยมผืนผ้า พื้นที่มากที่สุดเป็นกี่ตารางเซนติเมตร"),
                            distractors=[_c(s * s // 2), _c(s * s), _c(s * s // 4 - 1)])
        if kind == 3:
            m, c = rng.randint(5, 30), rng.randint(1000, 3000)
            low = c - m * m
            return MathDraw("", _c(low),
                            prompt=(f"ต้นทุนการผลิตสินค้า x ชิ้นคือ C = x² - {2 * m}x + {c} บาท "
                                    f"ต้นทุนต่ำที่สุดเป็นกี่บาท"),
                            distractors=[_c(c + m * m), _c(c - 2 * m), _c(c - 4 * m * m) if c > 4 * m * m else _c(c)])
        h, k = rng.randint(1, 5), rng.randint(3, 12)
        b, c = 2 * h, k - h * h
        const = f" + {c}" if c > 0 else (f" - {-c}" if c < 0 else "")
        return MathDraw("", str(k),
                        prompt=(f"สายน้ำพุพุ่งเป็นเส้นโค้ง y = -x² + {b}x{const} เมื่อ x เป็นระยะทางแนวราบ (เมตร) "
                                f"และ y เป็นความสูง (เมตร) สายน้ำพุ่งสูงสุดกี่เมตร"),
                        distractors=_story.keep(h, c if c > 0 else k + h, k + h * h, answer=k, lo=1))
