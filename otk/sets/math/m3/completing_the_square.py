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

from fractions import Fraction  # noqa: E402

from otk.core.content import text as _text_block  # noqa: E402
from otk.core.registry import QuestionType, question_type  # noqa: E402
from otk.kit.math_problems import MathType, WordProblem  # noqa: E402
from otk.kit.math_problems import frac_tex  # noqa: E402
from otk.sets._support.math_m3 import LEVEL  # noqa: E402
from otk.sets._support.math_p2 import _maths as _fixed_maths  # noqa: E402


def _fk3(*values: Fraction, answer: Fraction, lo: Fraction | None = None) -> list[str]:
    """Distinct fraction distractors as TeX, the answer (and values below lo) left out."""
    out: list[str] = []
    for v in values:
        v = Fraction(v)
        if v == answer or (lo is not None and v < lo) or frac_tex(v) in out:
            continue
        out.append(frac_tex(v))
    return out


def _tk3(*values: str, answer: str) -> list[str]:
    """Distinct TeX distractors, the answer left out."""
    return [v for v in dict.fromkeys(values) if v != answer]


def _roots3(a: int, b: int) -> str:
    lo, hi = sorted((a, b))
    return rf"x = {lo}, \; {hi}"


def _g3(n: int) -> str:
    """A whole number in TeX with grouped thousands: 4{,}572."""
    return f"{n:,}".replace(",", "{,}")


def _gk3(*values: int, answer: int, lo: int = 0) -> list[str]:
    """``story.keep`` for grouped numbers."""
    return [_g3(int(v)) for v in _story.keep(*values, answer=answer, lo=lo)]


# ── More completing the square (2026-11): the vertex from the completed form, a least value, solving by
# square roots, the two numbers of a completed square, a greatest value, and which expression is a perfect
# square ──


def _nz3c(rng: Random, lo: int, hi: int) -> int:
    return rng.choice((1, -1)) * rng.randint(lo, hi)


def _sq3(h: int) -> str:
    """(x - h)^2 with the sign folded in."""
    return f"(x {'-' if h > 0 else '+'} {abs(h)})^2"


@question_type("math.vertex_from_completed_m3", display_name={"th": "จุดยอดจากรูปกำลังสองสมบูรณ์"},
               level=LEVEL, topic="กำลังสองสมบูรณ์")
class VertexFromCompletedM3(MathType):
    def expr(self, rng: Random):
        h, k = _nz3c(rng, 1, 9), _nz3c(rng, 1, 9)
        right = f"({h}, {k})"
        # The sign of h kept from the bracket; the numbers swapped; the sign of k flipped.
        wrongs = [f"({-h}, {k})", f"({k}, {h})", f"({h}, {-k})"]
        return MathDraw(f"y = {_sq3(h)} {'+' if k > 0 else '-'} {abs(k)}", right, prompt="พาราโบลานี้มีจุดยอดที่จุดใด",
                        distractors=_tk3(*wrongs, answer=right))


@question_type("math.least_value_m3", display_name={"th": "ค่าต่ำสุดของนิพจน์กำลังสอง"},
               level=LEVEL, topic="กำลังสองสมบูรณ์")
class LeastValueM3(MathType):
    def expr(self, rng: Random):
        h = _nz3c(rng, 1, 9)
        right = rng.randint(-20, 20)
        c = h * h + right
        # The constant itself; h squared; the sign of the square flipped.
        return MathDraw(poly_tex((1, "x^{2}"), (-2 * h, "x"), (c, "")), str(right),
                        prompt="ค่าต่ำสุดของนิพจน์นี้เท่ากับเท่าใด",
                        distractors=_tk3(str(c), str(h * h), str(c + h * h), str(-right) if right else "1",
                                         answer=str(right)))


@question_type("math.solve_by_square_root_m3", display_name={"th": "แก้สมการด้วยการถอดรากที่สอง"},
               level=LEVEL, topic="กำลังสองสมบูรณ์")
class SolveBySquareRootM3(MathType):
    def expr(self, rng: Random):
        a = _nz3c(rng, 1, 9)
        k = rng.randint(1, 10)
        right = _roots3(-a + k, -a - k)
        # Only the positive root; the sign of a kept; k squared.
        wrongs = [rf"x = {-a + k}", _roots3(a + k, a - k), _roots3(-a + k * k, -a - k * k)]
        return MathDraw(f"(x {'+' if a > 0 else '-'} {abs(a)})^{{2}} = {k * k}", right, prompt="จงแก้สมการ",
                        distractors=_tk3(*wrongs, answer=right))


@question_type("math.completed_square_numbers_m3", display_name={"th": "เขียนเป็น (x + p)² + q แล้วหา q"},
               level=LEVEL, topic="กำลังสองสมบูรณ์")
class CompletedSquareNumbersM3(MathType):
    def expr(self, rng: Random):
        p = _nz3c(rng, 1, 9)
        c = rng.randint(-30, 40)
        q = c - p * p
        expr = poly_tex((1, "x^{2}"), (2 * p, "x"), (c, ""))
        # The square added instead of taken away; b itself squared; the constant.
        return MathDraw(f"{expr} = (x + p)^{{2}} + q", str(q), prompt="จงหาค่าของ q",
                        distractors=_tk3(str(c + p * p), str(c - 4 * p * p), str(c), str(q + 1), answer=str(q)))


@question_type("math.greatest_value_m3", display_name={"th": "ค่าสูงสุดของนิพจน์กำลังสอง"},
               level=LEVEL, topic="กำลังสองสมบูรณ์")
class GreatestValueM3(MathType):
    def expr(self, rng: Random):
        h = _nz3c(rng, 1, 8)
        right = rng.randint(-10, 30)
        c = right - h * h
        # The constant; the square taken away; h itself.
        return MathDraw(poly_tex((-1, "x^{2}"), (2 * h, "x"), (c, "")), str(right),
                        prompt="ค่าสูงสุดของนิพจน์นี้เท่ากับเท่าใด",
                        distractors=_tk3(str(c), str(c - h * h), str(h), str(right + 1), answer=str(right)))


@question_type("math.which_perfect_square_m3", display_name={"th": "นิพจน์ใดเป็นกำลังสองสมบูรณ์"},
               level=LEVEL, topic="กำลังสองสมบูรณ์")
class WhichPerfectSquareM3(QuestionType):
    """Fixed choices: an expression from another draw could also be a perfect square."""

    def build(self, rng: Random, **params):
        a = _nz3c(rng, 1, 9)
        right = poly_tex((1, "x^{2}"), (2 * a, "x"), (a * a, ""))
        # The middle term not doubled; the constant doubled; the constant's sign flipped.
        wrongs = [poly_tex((1, "x^{2}"), (a, "x"), (a * a, "")), poly_tex((1, "x^{2}"), (2 * a, "x"), (2 * a * a, "")),
                  poly_tex((1, "x^{2}"), (2 * a, "x"), (-a * a, ""))]
        return _fixed_maths([_text_block("นิพจน์ใดเป็นกำลังสองสมบูรณ์")], right, _tk3(*wrongs, answer=right), self.topic)
