"""ลิมิต

คณิตศาสตร์ · ม.6 · สสวท. เพิ่มเติม
Indicators: ค เพิ่มเติม แคลคูลัส 1 ม.6/1

Sets moved here from: math, math_m6, math_pictures_add, math_thin_topics.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.content import image, text
from otk.core.content import math as content_math
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.math_problems import MathDraw, MathType, frac_tex, poly_tex
from otk.sets._support.math_chapters import _distinct
from otk.sets._support.math_diagrams import _text_q
from otk.sets._support.math_m4 import maths as _maths
from otk.sets._support.math_m4 import maths as _num_maths
from otk.sets._support.math_m6 import M6
from otk.sets._support.math_p2 import _texts
from otk.sets._support.math_pictures_add import LIMIT_GRAPHS

PROVENANCE = Provenance("original")


LIMIT_ALT = ("กราฟของฟังก์ชัน y = f(x) บนระนาบพิกัดฉาก จุดโปร่งแทนจุดที่ไม่อยู่บนกราฟ "
             "จุดทึบแทนจุดที่อยู่บนกราฟ")


NO_LIMIT = "หาค่าไม่ได้"


@question_type("math.limit",
               display_name={"th": "ลิมิตของฟังก์ชัน"}, level={"th": "ม.6"},
               topic="ลิมิต")
class Limit(MathType):
    def expr(self, rng: Random):
        if rng.random() < 0.5:
            a = rng.choice([n for n in range(-4, 5) if n])
            sign = "-" if a >= 0 else "+"
            return MathDraw(
                rf"\lim_{{x \to {a}}} \frac{{x^{{2}} - {a * a}}}{{x {sign} {abs(a)}}}",
                rf"{2 * a}", hint=r"\text{factorise, then cancel}")
        a, d = rng.randint(1, 6), rng.randint(1, 6)
        b, e = rng.randint(-5, 5), rng.randint(-5, 5)
        num = poly_tex((a, "x^{2}"), (b, "x"))
        den = poly_tex((d, "x^{2}"), (e, "x"))
        return MathDraw(rf"\lim_{{x \to \infty}} \frac{{{num}}}{{{den}}}",
                        frac_tex(Fraction(a, d)),
                        hint=r"\text{compare leading terms}")


@question_type("math.limit_graph_picture_m6",
               display_name={"th": "ลิมิตซ้าย ลิมิตขวา และค่าฟังก์ชันจากกราฟ"},
               level={"th": "ม.6"}, topic="ลิมิต")
class LimitGraphPictureM6(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        s = rng.choice(LIMIT_GRAPHS)
        img = image(s.asset_id, alt=LIMIT_ALT)
        ask = rng.randrange(4)
        both = str(s.left) if s.left == s.right else NO_LIMIT
        exprs = (rf"\lim_{{x \to {s.c}^{{-}}}} f(x)", rf"\lim_{{x \to {s.c}^{{+}}}} f(x)",
                 rf"\lim_{{x \to {s.c}}} f(x)", f"f({s.c})")
        correct = (str(s.left), str(s.right), both, str(s.at))[ask]
        pool = [str(s.left), str(s.right), str(s.at), both, NO_LIMIT, str(s.c)]
        pool += [str(s.left + d) for d in (1, -1, 2)]
        stem = [text("จากกราฟของ y = f(x) ในภาพ จงหาค่าของ"), content_math(exprs[ask]), img]
        return _text_q(stem, correct, [p for p in dict.fromkeys(pool) if p != correct][:3], self.topic)


@question_type("math.sequence_limit_m6", display_name={"th": "ลิมิตของลำดับอนันต์"},
               level=M6, topic="ลิมิต")
class SequenceLimitM6(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        kind = rng.randrange(3)
        if kind == 0:
            a, b, c, d = rng.randint(1, 9), rng.randint(-9, 9), rng.randint(1, 9), rng.randint(1, 9)
            expr = rf"\lim_{{n \to \infty}} \frac{{{a}n {'+' if b >= 0 else '-'} {abs(b)}}}{{{c}n + {d}}}"
            v = Fraction(a, c)
            return _maths([text("จงหาค่าของลิมิต"), content_math(expr)], frac_tex(v),
                          [frac_tex(Fraction(b, d)) if Fraction(b, d) != v else "0", "0",
                           frac_tex(Fraction(a + b, c + d)) if Fraction(a + b, c + d) != v else "1",
                           r"\infty"], self.topic)
        if kind == 1:
            a, c = rng.randint(1, 9), rng.randint(1, 9)
            expr = rf"\lim_{{n \to \infty}} \frac{{{a}n^{{2}} + 1}}{{{c}n^{{3}} + n}}"
            return _maths([text("จงหาค่าของลิมิต"), content_math(expr)], "0",
                          [frac_tex(Fraction(a, c)), r"\infty", "1"], self.topic)
        r = rng.choice((Fraction(1, 2), Fraction(2, 3), Fraction(3, 4), Fraction(-1, 2), Fraction(1, 3)))
        big = rng.choice((2, 3))
        if rng.random() < 0.5:
            return _texts([text("ลำดับต่อไปนี้ลู่เข้าหรือลู่ออก"), content_math(rf"a_n = \left({frac_tex(r)}\right)^{{n}}")],
                          "ลู่เข้าสู่ 0", ["ลู่ออก", f"ลู่เข้าสู่ {r}", "ลู่เข้าสู่ 1"], self.topic)
        return _texts([text("ลำดับต่อไปนี้ลู่เข้าหรือลู่ออก"), content_math(rf"a_n = {big}^{{n}}")],
                      "ลู่ออก", ["ลู่เข้าสู่ 0", f"ลู่เข้าสู่ {big}", "ลู่เข้าสู่ 1"], self.topic)


@question_type("math.piecewise_limit_m6", display_name={"th": "ลิมิตและความต่อเนื่องของฟังก์ชันเป็นช่วง"},
               level=M6, topic="ลิมิต")
class PiecewiseLimitM6(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        c = rng.choice((1, 2, 3, -1, -2))
        k = rng.choice([v for v in range(-4, 6) if v])
        q = rng.randint(-5, 5)
        p = k * c + q - c * c              # continuous at c by construction
        left = poly_tex((1, "x^{2}"), (p, ""))
        kind = rng.randrange(3)
        if kind == 0:
            kx = "kx" + (f" {'+' if q > 0 else '-'} {abs(q)}" if q else "")
            f = rf"f(x) = \begin{{cases}} {left} & x < {c} \\ {kx} & x \geq {c} \end{{cases}}"
            return _num_maths([text("ฟังก์ชันต่อไปนี้ต่อเนื่องที่ x = " + str(c) + " จงหาค่า k"), content_math(f)],
                              str(k), [str(-k), str(k + 1), str(c * c + p)], self.topic)
        jump = rng.choice((0, rng.choice((-3, -2, 2, 3))))
        right = poly_tex((k, "x"), (q + jump, ""))
        f = rf"f(x) = \begin{{cases}} {left} & x < {c} \\ {right} & x \geq {c} \end{{cases}}"
        L, R = c * c + p, k * c + q + jump
        if kind == 1:
            return _num_maths([text("จงหาค่าของ"), content_math(rf"\lim_{{x \to {c}^{{-}}}} f(x)"),
                               text("เมื่อ"), content_math(f)], str(L), [str(R) if R != L else str(L + 1),
                                                                         str(c * c), str(p)], self.topic)
        right_ans = f"ลิมิตมีค่าเท่ากับ {L}" if L == R else "ไม่มีลิมิต เพราะลิมิตซ้ายไม่เท่ากับลิมิตขวา"
        wrongs = ([f"ลิมิตมีค่าเท่ากับ {L}", f"ลิมิตมีค่าเท่ากับ {R}"] if L != R
                  else ["ไม่มีลิมิต เพราะลิมิตซ้ายไม่เท่ากับลิมิตขวา", f"ลิมิตมีค่าเท่ากับ {c * c}"])
        wrongs += ["ไม่มีลิมิต เพราะ f ไม่นิยามที่จุดนี้", f"ลิมิตมีค่าเท่ากับ {L + R}"]
        return _texts([text(f"ข้อใดถูกต้องเกี่ยวกับลิมิตของ f(x) เมื่อ x เข้าใกล้ {c}"), content_math(f)],
                      right_ans, _distinct(right_ans, *wrongs)[:3], self.topic)
