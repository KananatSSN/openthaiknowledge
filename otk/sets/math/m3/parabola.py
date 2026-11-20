"""กราฟของฟังก์ชันกำลังสอง

คณิตศาสตร์ · ม.3 · สสวท. พื้นฐาน
Indicators: ค 1.2 ม.3/2

Sets moved here from: math, math_algebra, math_diagrams.
"""

from __future__ import annotations

from random import Random

from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.math_problems import MathDraw, MathType, coef_term, poly_tex
from otk.sets._support.math_algebra import _nonzero
from otk.sets._support.math_diagrams import PARABOLAS, _img, _math_q

PROVENANCE = Provenance("original")


PARABOLA_ALT = "กราฟพาราโบลาบนระนาบพิกัดฉากที่มีเส้นตาราง แกน X และแกน Y กำกับทุก 1 หน่วย"


@question_type("math.parabola_graph_m3", display_name={"th": "อ่านจุดยอด แกนสมมาตร และค่าสูงสุด/ต่ำสุดจากกราฟพาราโบลา"},
               level={"th": "ม.3"}, topic="กราฟของฟังก์ชันกำลังสอง")
class ParabolaGraphM3(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        p = rng.choice(PARABOLAS)
        img = _img(p.asset_id, PARABOLA_ALT)
        kind = rng.randrange(3)
        if kind == 0:
            return _math_q([text("จุดยอดของพาราโบลาในกราฟคือจุดใด"), img], f"({p.h}, {p.k})",
                           [f"({p.k}, {p.h})", f"({-p.h}, {p.k})", f"({p.h}, {-p.k})" if p.k else f"({p.h}, 1)",
                            f"({p.h + 1}, {p.k})", f"({p.h}, {p.k + 1})"], self.topic)
        if kind == 1:
            return _math_q([text("แกนสมมาตรของพาราโบลาในกราฟคือเส้นตรงใด"), img], f"x = {p.h}",
                           [f"y = {p.k}", f"x = {-p.h}" if p.h else "x = 1", f"x = {p.k}" if p.k != p.h
                            else f"x = {p.h + 2}", f"y = {p.h}", f"x = {p.h + 1}"], self.topic)
        word = "ค่าต่ำสุด" if p.a > 0 else "ค่าสูงสุด"
        return _math_q([text(f"ฟังก์ชันในกราฟมี{word}เท่าใด"), img], str(p.k),
                       [str(p.h), str(-p.k) if p.k else "1", str(p.k + 1), str(p.k - 1)], self.topic)


@question_type("math.parabola_vertex",
               display_name={"th": "จุดยอดของพาราโบลา"}, level={"th": "ม.3"},
               topic="กราฟของฟังก์ชันกำลังสอง")
class ParabolaVertex(MathType):
    break_convergence = True  # one-part slips cluster round the answer
    def expr(self, rng: Random):
        a = rng.choice([1, -1, 2])
        h, k = rng.randint(-5, 5), rng.randint(-5, 5)
        lead = "" if a == 1 else ("-" if a == -1 else str(a))
        tex = rf"y = {lead}(x {'-' if h >= 0 else '+'} {abs(h)})^{{2}}" \
              rf"{coef_term(k, '')}"
        return MathDraw(tex, rf"({h}, {k})", prompt="พาราโบลานี้มีจุดยอดที่ใด",
                        distractors=[rf"({-h}, {k})", rf"({h}, {-k})",
                                     rf"({k}, {h})"])


@question_type("math.parabola_axis_intercept",
               display_name={"th": "แกนสมมาตรและจุดตัดแกน y ของพาราโบลา"},
               level={"th": "ม.3"}, topic="กราฟของฟังก์ชันกำลังสอง")
class ParabolaAxisIntercept(MathType):
    break_convergence = True  # one-part slips cluster round the answer
    def expr(self, rng: Random, lead_hi: int = 3, h_hi: int = 8):
        a = _nonzero(rng, -lead_hi, lead_hi)
        h = _nonzero(rng, -h_hi, h_hi)
        k = rng.randint(-12, 12)
        # a(x − h)² + k expanded
        b, c = -2 * a * h, a * h * h + k
        shown = poly_tex((a, "x^2"), (b, "x"), (c, ""))
        if rng.random() < 0.5:
            return MathDraw(f"y = {shown}", f"x = {h}",
                            prompt="จงหาสมการแกนสมมาตรของพาราโบลา",
                            distractors=[f"x = {-h}", f"y = {h}", f"x = {c}"])
        return MathDraw(f"y = {shown}", f"(0, {c})",
                        prompt="พาราโบลานี้ตัดแกน y ที่จุดใด",
                        distractors=[f"(0, {k})", f"({c}, 0)", f"(0, {-c})"])

from fractions import Fraction  # noqa: E402

from otk.core.content import math as _math_block  # noqa: E402
from otk.core.content import text as _text_block  # noqa: E402
from otk.core.registry import QuestionType, question_type  # noqa: E402
from otk.kit import story as _story  # noqa: E402
from otk.kit.math_problems import MathType, WordProblem  # noqa: E402
from otk.kit.math_problems import binomial_tex, frac_tex  # noqa: E402
from otk.sets._support.math_m3 import LEVEL  # noqa: E402
from otk.sets._support.math_p2 import _maths as _fixed_maths  # noqa: E402
from otk.sets._support.math_p2 import _texts as _fixed_texts  # noqa: E402


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


# ── More parabolas (2026-11): which way it opens, the y-intercept, the x-intercepts, the vertex of
# x² + bx + c, the least or greatest value, a point on the graph, and a shifted graph ──


def _nz3p(rng: Random, lo: int, hi: int) -> int:
    return rng.choice((1, -1)) * rng.randint(lo, hi)


def _vertex_form3(a: int, h: int, k: int) -> str:
    lead = "" if a == 1 else "-" if a == -1 else str(a)
    tail = f" {'+' if k > 0 else '-'} {abs(k)}" if k else ""
    return f"y = {lead}(x {'-' if h > 0 else '+'} {abs(h)})^{{2}}{tail}"


@question_type("math.parabola_opens_m3", display_name={"th": "พาราโบลาหงายหรือคว่ำ"},
               level=LEVEL, topic="กราฟของฟังก์ชันกำลังสอง")
class ParabolaOpensM3(QuestionType):
    def build(self, rng: Random, **params):
        a = _nz3p(rng, 1, 5)
        b, c = rng.randint(-9, 9), rng.randint(-9, 9)
        up = a > 0
        right = "หงาย และมีค่าต่ำสุด" if up else "คว่ำ และมีค่าสูงสุด"
        options = ["หงาย และมีค่าต่ำสุด", "คว่ำ และมีค่าสูงสุด", "หงาย และมีค่าสูงสุด", "คว่ำ และมีค่าต่ำสุด"]
        stem = [_text_block("กราฟของฟังก์ชันนี้เป็นพาราโบลาแบบใด"), _math_block(f"y = {poly_tex((a, 'x^{2}'), (b, 'x'), (c, ''))}")]
        return _fixed_texts(stem, right, [o for o in options if o != right], self.topic)


@question_type("math.parabola_y_intercept_m3", display_name={"th": "จุดที่พาราโบลาตัดแกน y"},
               level=LEVEL, topic="กราฟของฟังก์ชันกำลังสอง")
class ParabolaYInterceptM3(MathType):
    def expr(self, rng: Random):
        p, q = _nz3p(rng, 1, 9), _nz3p(rng, 1, 9)
        right = f"(0, {p * q})"
        # The roots read as the intercept; the sum of the roots; the x-axis instead.
        wrongs = [f"(0, {p})", f"(0, {-(p + q)})", f"({p * q}, 0)"]
        return MathDraw(f"y = {binomial_tex(-p)}{binomial_tex(-q)}", right, prompt="พาราโบลานี้ตัดแกน y ที่จุดใด",
                        distractors=_tk3(*wrongs, answer=right))


@question_type("math.parabola_x_intercepts_m3", display_name={"th": "จุดที่พาราโบลาตัดแกน x"},
               level=LEVEL, topic="กราฟของฟังก์ชันกำลังสอง")
class ParabolaXInterceptsM3(MathType):
    def expr(self, rng: Random):
        while True:
            p, q = _nz3p(rng, 1, 9), _nz3p(rng, 1, 9)
            if p != q and p != -q:
                break
        lo, hi = sorted((p, q))
        a, b = sorted((-p, -q))
        right = rf"({lo}, 0), \; ({hi}, 0)"
        # The signs as written in the brackets; the y-axis; one root's sign lost.
        wrongs = [rf"({a}, 0), \; ({b}, 0)", rf"(0, {lo}), \; (0, {hi})", rf"({lo}, 0), \; ({-hi}, 0)"]
        return MathDraw(f"y = {binomial_tex(-p)}{binomial_tex(-q)}", right, prompt="พาราโบลานี้ตัดแกน x ที่จุดใด",
                        distractors=_tk3(*wrongs, answer=right))


@question_type("math.parabola_vertex_standard_m3", display_name={"th": "จุดยอดของ y = x² + bx + c"},
               level=LEVEL, topic="กราฟของฟังก์ชันกำลังสอง")
class ParabolaVertexStandardM3(MathType):
    def expr(self, rng: Random):
        h = _nz3p(rng, 1, 8)
        k = rng.randint(-15, 15)
        b, c = -2 * h, h * h + k
        right = f"({h}, {k})"
        # The sign of h lost; the constant as the height; b and c read off.
        wrongs = [f"({-h}, {k})", f"({h}, {c})", f"({b}, {c})"]
        return MathDraw(f"y = {poly_tex((1, 'x^{2}'), (b, 'x'), (c, ''))}", right, prompt="พาราโบลานี้มีจุดยอดที่จุดใด",
                        distractors=_tk3(*wrongs, answer=right))


@question_type("math.parabola_extreme_value_m3", display_name={"th": "ค่าสูงสุดหรือต่ำสุดของฟังก์ชันกำลังสอง"},
               level=LEVEL, topic="กราฟของฟังก์ชันกำลังสอง")
class ParabolaExtremeValueM3(MathType):
    def expr(self, rng: Random):
        a = rng.choice((1, -1, 2, -2))
        h, k = _nz3p(rng, 1, 9), _nz3p(rng, 1, 15)
        kind = "ต่ำสุด" if a > 0 else "สูงสุด"
        # h read as the value; the sign of k flipped; h and k added.
        return MathDraw(_vertex_form3(a, h, k), str(k), prompt=f"ฟังก์ชันนี้มีค่า{kind}เท่ากับเท่าใด",
                        distractors=_tk3(str(h), str(-k), str(h + k), str(k + a), answer=str(k)))


@question_type("math.point_on_parabola_m3", display_name={"th": "จุดใดอยู่บนกราฟพาราโบลา"},
               level=LEVEL, topic="กราฟของฟังก์ชันกำลังสอง")
class PointOnParabolaM3(QuestionType):
    """Fixed choices: a point from another draw could also lie on this graph."""

    def build(self, rng: Random, **params):
        c = rng.randint(-9, 9)
        x = _nz3p(rng, 1, 5)
        y = x * x + c
        right = f"({x}, {y})"
        # x not squared; the sign of y flipped; the coordinates swapped.
        wrongs = [f"({x}, {2 * x + c})" if 2 * x + c != y else f"({x}, {y + 1})", f"({x}, {-y})" if y else f"({x}, 1)",
                  f"({y}, {x})" if y != x and y * y + c != x else f"({x}, {y + 2})"]
        stem = [_text_block("จุดใดอยู่บนกราฟของ"), _math_block(f"y = {poly_tex((1, 'x^{2}'), (c, ''))}")]
        return _fixed_maths(stem, right, _tk3(*wrongs, f"({x}, {y + 3})", answer=right)[:3], self.topic)


@question_type("math.parabola_shift_m3", display_name={"th": "เลื่อนกราฟ y = x² แล้วได้สมการใด"},
               level=LEVEL, topic="กราฟของฟังก์ชันกำลังสอง")
class ParabolaShiftM3(WordProblem):
    def expr(self, rng: Random):
        h, k = _nz3p(rng, 1, 6), _nz3p(rng, 1, 9)
        horiz = f"ไปทาง{'ขวา' if h > 0 else 'ซ้าย'} {abs(h)} หน่วย"
        vert = f"ขึ้น {k} หน่วย" if k > 0 else f"ลง {-k} หน่วย"
        right = _vertex_form3(1, h, k)
        # The horizontal shift's sign the wrong way; the vertical; both.
        wrongs = [_vertex_form3(1, -h, k), _vertex_form3(1, h, -k), _vertex_form3(1, -h, -k)]
        return MathDraw("", right, prompt=f"เลื่อนกราฟ y = x² {horiz} และ{vert} จะได้กราฟของสมการใด",
                        distractors=_tk3(*wrongs, answer=right))
