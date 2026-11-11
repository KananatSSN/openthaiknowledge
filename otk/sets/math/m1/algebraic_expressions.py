"""นิพจน์พีชคณิต

คณิตศาสตร์ · ม.1 · สสวท. พื้นฐาน
Indicators: ค 1.1 ม.1/*

Sets moved here from: math, math_algebra, math_apply_stage.
"""

from __future__ import annotations

import math
from random import Random

from otk.core.content import math as content_math
from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.math_problems import MathDraw, MathType, poly_tex
from otk.sets._support.math_algebra import _nonzero
from otk.sets._support.math_apply_stage import _nums
from otk.sets._support.math_m4 import maths

PROVENANCE = Provenance("original")


@question_type("math.evaluate_expression",
               display_name={"th": "แทนค่าในนิพจน์"}, level={"th": "ม.1"},
               topic="นิพจน์พีชคณิต")
class EvaluateExpression(MathType):
    def expr(self, rng: Random, x_lo: int = -9, x_hi: int = 9):
        while True:
            x = rng.randint(x_lo, x_hi)
            if x:
                break
        if rng.random() < 0.3:
            b = rng.randint(-9, 9)
            tex, val = poly_tex((1, "x^{2}"), (b, "")), x * x + b
        else:
            a = rng.choice([n for n in range(-5, 6) if n not in (-1, 0, 1)])
            b = rng.randint(-9, 9)
            tex, val = poly_tex((a, "x"), (b, "")), a * x + b
        return MathDraw(tex, rf"{val}", prompt=f"จงหาค่าเมื่อ x = {x}")


@question_type("math.evaluate_two_variables", display_name={"th": "แทนค่าสองตัวแปร"},
               level={"th": "ม.1"}, topic="นิพจน์พีชคณิต")
class EvaluateTwoVariables(MathType):
    def expr(self, rng: Random, coef_hi: int = 6, value_hi: int = 8):
        a, b, c = (_nonzero(rng, -coef_hi, coef_hi) for _ in range(3))
        x, y = (_nonzero(rng, -value_hi, value_hi) for _ in range(2))
        value = a * x * x + b * x * y + c * y
        shown = poly_tex((a, "x^2"), (b, "xy"), (c, "y"))
        return MathDraw(
            shown, str(value),
            prompt=f"จงหาค่าของนิพจน์ เมื่อ x = {x} และ y = {y}",
            # Squaring a negative x wrongly, and swapping x with y.
            distractors=[str(-a * x * x + b * x * y + c * y),
                         str(a * y * y + b * x * y + c * x),
                         str(a * x + b * x * y + c * y)])


@question_type("math.simplify_linear",
               display_name={"th": "กระจายวงเล็บและรวมพจน์"}, level={"th": "ม.1"},
               topic="นิพจน์พีชคณิต")
class SimplifyLinear(MathType):
    def expr(self, rng: Random):
        u, v = rng.choice([("a", "b"), ("x", "y")])
        c1 = rng.randint(1, 5)
        k = rng.randint(2, 4)
        s = rng.choice([1, -1])
        su = rng.choice([1, -1])
        p = rng.randint(1, 5)
        q = rng.choice([1, -1]) * rng.randint(1, 5)
        ru = c1 + s * k * su * p
        rv = s * k * q
        inner = poly_tex((su * p, u), (q, v))
        tex = rf"{c1}{u} {'+' if s > 0 else '-'} {k}({inner})"
        return MathDraw(tex, poly_tex((ru, u), (rv, v)),
                        hint=r"\text{distribute, then collect}")


@question_type("math.expression_word_m1", display_name={"th": "นิพจน์พีชคณิตในสถานการณ์"},
               level={"th": "ม.1"}, topic="นิพจน์พีชคณิต")
class ExpressionWordM1(QuestionType):
    def build(self, rng: Random, **params) -> GeneratedQuestion:
        kind = rng.randrange(3)
        if kind == 0:
            a, b, c, d = rng.randint(1, 5), rng.randint(1, 9), rng.randint(1, 5), rng.randint(1, 9)
            w, ell = poly_tex((a, "x"), (b, "")), poly_tex((c, "x"), (d, ""))
            stem = [text("รูปสี่เหลี่ยมผืนผ้ากว้าง"), content_math(w), text("หน่วย ยาว"), content_math(ell),
                    text("หน่วย ความยาวรอบรูปเขียนเป็นนิพจน์ในรูปอย่างง่ายได้อย่างไร")]
            right = poly_tex((2 * (a + c), "x"), (2 * (b + d), ""))
            # Only half the perimeter, the sides multiplied, and the 2 applied to x only.
            wrongs = [poly_tex((a + c, "x"), (b + d, "")), poly_tex((a * c, "x^{2}"), (a * d + b * c, "x"), (b * d, "")),
                      poly_tex((2 * (a + c), "x"), (b + d, "")), poly_tex((4 * (a + c), "x"), (4 * (b + d), ""))]
            return maths(stem, right, wrongs, self.topic)
        if kind == 1:
            a, b = rng.choice((12, 15, 20, 25)), rng.choice((5, 8, 10))
            note = rng.choice((200, 500, 1000))
            stem = [text(f"ซื้อสมุด x เล่ม ราคาเล่มละ {a} บาท และปากกา y ด้าม ราคาด้ามละ {b} บาท "
                         f"จ่ายด้วยธนบัตร {note} บาท นิพจน์ใดแทนเงินทอน")]
            right = rf"{note} - {a}x - {b}y"
            wrongs = [rf"{note} - {a}x + {b}y", rf"{a}x + {b}y - {note}", rf"{note} - {a + b}xy",
                      rf"{note} - {a}y - {b}x"]
            return maths(stem, right, wrongs, self.topic)
        start, per = rng.choice((20, 30, 40)), rng.choice((10, 15, 25))
        h = rng.randint(2, 9)
        stem = [text(f"ร้านให้เช่าจักรยานคิดค่าเช่า {start} + {per}h บาท เมื่อ h คือจำนวนชั่วโมงที่เช่า "
                     f"ถ้าเช่า {h} ชั่วโมง ต้องจ่ายกี่บาท")]
        cost = start + per * h
        return maths(stem, str(cost), _nums(cost, (start + per) * h, start * h + per, per * h, lo=1), self.topic)


# ── More algebraic expressions (2026-11): like terms, words to expressions, coefficients, a pattern's rule, a
# perimeter in x, and substituting into a formula ──

from otk.kit import story as _story  # noqa: E402
from otk.kit.math_problems import WordProblem  # noqa: E402
from otk.sets._support.math_m1 import LEVEL  # noqa: E402
from otk.sets._support.math_p2 import _maths  # noqa: E402

_EXPR_TOPIC = "นิพจน์พีชคณิต"


@question_type("math.like_terms_m1", display_name={"th": "พจน์ที่คล้ายกัน"},
               level=LEVEL, topic=_EXPR_TOPIC)
class LikeTermsM1(QuestionType):
    """Like terms have the same letters to the same powers; the number in front does not matter."""

    _SHAPES = ("x^{2}y", "xy^{2}", "xy", "x^{2}", "y^{2}", "x^{3}")

    def build(self, rng: Random) -> GeneratedQuestion:
        shape = rng.choice(self._SHAPES)
        c1, c2 = rng.choice([v for v in range(-9, 10) if v not in (0, 1, -1)]), rng.choice([v for v in range(2, 10)])
        others = [s for s in self._SHAPES if s != shape]
        rng.shuffle(others)
        right = f"{c2}{shape}"
        # The same number with other letters.
        wrongs = [f"{c1}{s}" for s in others[:3]]
        return _maths([text("พจน์ใดคล้ายกับ"), content_math(f"{c1}{shape}")], right, wrongs, self.topic)


@question_type("math.words_to_expression_m1", display_name={"th": "เขียนนิพจน์จากข้อความ"},
               level=LEVEL, topic=_EXPR_TOPIC)
class WordsToExpressionM1(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        a, b = rng.randint(2, 9), rng.randint(2, 15)
        kind = rng.randrange(4)
        if kind == 0:
            words, right, wrongs = (f"{b} น้อยกว่า {a} เท่าของ x", f"{a}x - {b}",
                                    [f"{b} - {a}x", f"{a}(x - {b})", f"{a} - {b}x"])
        elif kind == 1:
            words, right, wrongs = (f"{a} เท่าของผลบวกของ x กับ {b}", f"{a}(x + {b})",
                                    [f"{a}x + {b}", f"x + {a * b}x", f"{a} + {b}x"])
        elif kind == 2:
            words, right, wrongs = (f"ผลต่างของ x กับ {b} หารด้วย {a}", rf"\frac{{x - {b}}}{{{a}}}",
                                    [rf"x - \frac{{{b}}}{{{a}}}", rf"\frac{{{a}}}{{x - {b}}}", rf"\frac{{x}}{{{a}}} - {b * a}"])
        else:
            words, right, wrongs = (f"กำลังสองของ x ลบด้วย {b}", rf"x^{{2}} - {b}",
                                    [rf"(x - {b})^{{2}}", rf"{b} - x^{{2}}", rf"2x - {b}"])
        # Two slips can print the same when the numbers coincide; a sign slip fills in.
        backup = [rf"{a}x + {b}", rf"x - {a * b}", rf"{a + b}x"]
        wrongs = [w for w in dict.fromkeys(wrongs + backup) if w != right][:3]
        return _maths([text(f"“{words}” เขียนเป็นนิพจน์ได้อย่างไร")], right, wrongs, self.topic)


@question_type("math.coefficient_m1", display_name={"th": "สัมประสิทธิ์และพจน์ที่เป็นค่าคงตัว"},
               level=LEVEL, topic=_EXPR_TOPIC)
class CoefficientM1(WordProblem):
    def expr(self, rng: Random):
        a = _nonzero(rng, -9, 9)
        b = rng.choice([v for v in range(-9, 10) if v not in (0, 1, -1)])
        c = _nonzero(rng, -12, 12)
        tex = poly_tex((a, "x^{2}"), (b, "y"), (c, ""))
        kind = rng.randrange(2)
        if kind == 0:
            # The size without its sign; the other coefficient; the constant.
            return MathDraw(tex, str(b), prompt="สัมประสิทธิ์ของ y ในนิพจน์นี้คือข้อใด",
                            distractors=[str(w) for w in dict.fromkeys((-b, a, c, 1)) if w != b])
        return MathDraw(tex, str(c), prompt="พจน์ที่เป็นค่าคงตัวของนิพจน์นี้คือข้อใด",
                        distractors=[str(w) for w in dict.fromkeys((-c, a, b, 0)) if w != c])


@question_type("math.pattern_rule_m1", display_name={"th": "นิพจน์แทนจำนวนในรูปที่ n ของแบบรูป"},
               level=LEVEL, topic=_EXPR_TOPIC)
class PatternRuleM1(QuestionType):
    """Terms going up by d from a: the nth is dn + (a − d)."""

    def build(self, rng: Random) -> GeneratedQuestion:
        d, first = rng.randint(2, 7), rng.randint(1, 12)
        while first == d:
            first = rng.randint(1, 12)
        terms = [first + d * i for i in range(4)]
        c = first - d
        right = poly_tex((d, "n"), (c, ""))
        # The first term as the constant; n times the first; the step added to n.
        wrongs = [poly_tex((d, "n"), (first, "")), poly_tex((first, "n"), (d - first, "")) if d != first else "n",
                  poly_tex((1, "n"), (d, ""))]
        wrongs = [w for w in dict.fromkeys(wrongs) if w != right]
        return _maths([text(f"แบบรูป {', '.join(str(t) for t in terms)}, … จำนวนในรูปที่ n เขียนเป็นนิพจน์ได้อย่างไร")],
                      right, wrongs, self.topic)


@question_type("math.perimeter_expression_m1", display_name={"th": "นิพจน์แทนความยาวรอบรูป"},
               level=LEVEL, topic=_EXPR_TOPIC)
class PerimeterExpressionM1(WordProblem):
    def expr(self, rng: Random):
        a, b = rng.randint(1, 4), rng.randint(1, 9)
        c, e = rng.randint(1, 4), rng.randint(-5, 9)
        per_x, per_c = 2 * (a + c), 2 * (b + e)
        right = poly_tex((per_x, "x"), (per_c, ""))
        prompt = (f"รูปสี่เหลี่ยมผืนผ้ากว้าง {poly_tex((a, 'x'), (b, '')).replace('-', '−')} หน่วย "
                  f"ยาว {poly_tex((c, 'x'), (e, '')).replace('-', '−')} หน่วย มีความยาวรอบรูปเท่าใด")
        # Each side once; only the x-terms doubled.
        wrongs = [poly_tex((a + c, "x"), (b + e, "")), poly_tex((per_x, "x"), (b + e, "")),
                  poly_tex((a * c, "x^{2}"), (per_c, ""))]
        return MathDraw("", right, prompt=prompt, distractors=[w for w in dict.fromkeys(wrongs) if w != right])


@question_type("math.formula_substitution_m1", display_name={"th": "แทนค่าในสูตร"},
               level=LEVEL, topic=_EXPR_TOPIC)
class FormulaSubstitutionM1(WordProblem):
    def expr(self, rng: Random):
        kind = rng.randrange(3)
        if kind == 0:
            c = 5 * rng.randint(-4, 20)
            f = 9 * c // 5 + 32
            return MathDraw("", str(f), prompt=f"ใช้สูตร F = (9/5)C + 32 เปลี่ยน {c} องศาเซลเซียสเป็นองศาฟาเรนไฮต์",
                            distractors=_story.keep(9 * c // 5, c + 32, 5 * c // 9 + 32 if c % 9 == 0 else f + 10,
                                                    answer=f, lo=-100))
        if kind == 1:
            a, b, h = rng.randint(2, 15), rng.randint(2, 15), 2 * rng.randint(1, 8)
            area = (a + b) * h // 2
            return MathDraw("", str(area), prompt=f"ใช้สูตร A = ½(a + b)h เมื่อ a = {a}, b = {b} และ h = {h} จงหาค่า A",
                            distractors=_story.keep((a + b) * h, a + b * h // 2, (a * b) * h // 2, answer=area, lo=1))
        u, a, t = rng.randint(0, 10), rng.randint(1, 5), rng.randint(1, 8)
        v = u + a * t
        return MathDraw("", str(v), prompt=f"ใช้สูตร v = u + at เมื่อ u = {u}, a = {a} และ t = {t} จงหาค่า v",
                        distractors=_story.keep((u + a) * t, u * a + t, a * t, answer=v, lo=0))


# ── To fifteen (2026-11): taking out a common number, a square with a negative, which expression is equal,
# like terms in two letters, and subtracting a bracket ──


@question_type("math.factor_out_number_m1", display_name={"th": "ดึงตัวร่วมที่เป็นจำนวนออกนอกวงเล็บ"},
               level=LEVEL, topic=_EXPR_TOPIC)
class FactorOutNumberM1(QuestionType):
    """6x + 9 = 3(2x + 3): the distributive property read backwards."""

    def build(self, rng: Random) -> GeneratedQuestion:
        while True:
            g, a, b = rng.randint(2, 9), rng.randint(1, 7), rng.choice([v for v in range(-9, 10) if v])
            if math.gcd(a, abs(b)) == 1 and (a, abs(b)) != (1, 1):
                break
        expanded = poly_tex((g * a, "x"), (g * b, ""))
        right = f"{g}({poly_tex((a, 'x'), (b, ''))})"
        # Only the first term divided; the sign of the constant lost; a smaller common number.
        wrongs = [f"{g}({poly_tex((a, 'x'), (g * b, ''))})", f"{g}({poly_tex((a, 'x'), (-b, ''))})",
                  f"{g * a}({poly_tex((1, 'x'), (b, ''))})" if a > 1 else f"x({poly_tex((g, ''), (g * b, 'x'))})"]
        return _maths([text("จงเขียนในรูปผลคูณโดยดึงตัวร่วมออก"), content_math(expanded)], right,
                      [w for w in dict.fromkeys(wrongs) if w != right], self.topic)


@question_type("math.evaluate_square_m1", display_name={"th": "แทนค่าจำนวนลบในนิพจน์ที่มีกำลังสอง"},
               level=LEVEL, topic=_EXPR_TOPIC)
class EvaluateSquareM1(WordProblem):
    def expr(self, rng: Random):
        a, b, c = rng.randint(1, 4), rng.choice([v for v in range(-6, 7) if v]), rng.randint(-9, 9)
        x0 = -rng.randint(1, 6)
        tex = poly_tex((a, "x^{2}"), (b, "x"), (c, ""))
        right = a * x0 * x0 + b * x0 + c
        # x² read as −x²; x² read as 2x; the sign of bx lost.
        wrongs = (-a * x0 * x0 + b * x0 + c, 2 * a * x0 + b * x0 + c, a * x0 * x0 - b * x0 + c)
        return MathDraw(tex, str(right), prompt=f"เมื่อ x = {x0} นิพจน์นี้มีค่าเท่าใด".replace("-", "−"),
                        distractors=[str(w) for w in dict.fromkeys(wrongs) if w != right])


@question_type("math.equal_expressions_m1", display_name={"th": "นิพจน์ใดเท่ากับนิพจน์ที่กำหนด"},
               level=LEVEL, topic=_EXPR_TOPIC)
class EqualExpressionsM1(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        a, b, c = rng.randint(2, 6), rng.randint(1, 9), rng.randint(1, 5)
        tex = rf"{a}(x - {b}) + {c}x"
        right = poly_tex((a + c, "x"), (-a * b, ""))
        # Only the first term multiplied; the sign of b lost; c added to the number.
        wrongs = [poly_tex((a + c, "x"), (-b, "")), poly_tex((a + c, "x"), (a * b, "")),
                  poly_tex((a, "x"), (-a * b + c, "")) if c != a * b else poly_tex((a * c, "x"), (-a * b, ""))]
        return _maths([text("นิพจน์ในข้อใดเท่ากับ"), content_math(tex)], right,
                      [w for w in dict.fromkeys(wrongs) if w != right], self.topic)


@question_type("math.like_terms_two_letters_m1", display_name={"th": "รวมพจน์ที่คล้ายกันที่มีตัวแปรสองตัว"},
               level=LEVEL, topic=_EXPR_TOPIC)
class LikeTermsTwoLettersM1(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        while True:
            a, b, c, d = (rng.choice([v for v in range(-9, 10) if v]) for _ in range(4))
            if a + c and b + d:
                break
        tex = poly_tex((a, "x"), (b, "y"), (c, "x"), (d, "y"))
        right = poly_tex((a + c, "x"), (b + d, "y"))
        # x and y combined into one; the second x's sign lost; everything added into xy.
        wrongs = [poly_tex((a + b + c + d, "xy")) if a + b + c + d else poly_tex((a + c, "x"), (b - d, "y")),
                  poly_tex((a - c, "x"), (b + d, "y")) if a - c else poly_tex((-(a + c), "x"), (b + d, "y")),
                  poly_tex((a + c, "x"), (b - d, "y")) if b - d else poly_tex((a + c + 1, "x"), (b + d, "y"))]
        return _maths([text("จงรวมพจน์ที่คล้ายกัน"), content_math(tex)], right,
                      [w for w in dict.fromkeys(wrongs) if w != right], self.topic)


@question_type("math.subtract_bracket_m1", display_name={"th": "ลบนิพจน์ที่อยู่ในวงเล็บ"},
               level=LEVEL, topic=_EXPR_TOPIC)
class SubtractBracketM1(QuestionType):
    """(5x + 3) − (2x − 4): the minus changes every sign in the second bracket."""

    def build(self, rng: Random) -> GeneratedQuestion:
        a, b = rng.randint(3, 9), rng.randint(1, 9)
        c, d = rng.randint(1, a - 1), rng.choice([v for v in range(-9, 10) if v])
        tex = rf"({poly_tex((a, 'x'), (b, ''))}) - ({poly_tex((c, 'x'), (d, ''))})"
        right = poly_tex((a - c, "x"), (b - d, ""))
        # Only the first term's sign changed; no signs changed; the x-terms added.
        wrongs = [poly_tex((a - c, "x"), (b + d, "")), poly_tex((a + c, "x"), (b - d, "")),
                  poly_tex((a + c, "x"), (b + d, ""))]
        return _maths([text("จงทำให้อยู่ในรูปอย่างง่าย"), content_math(tex)], right,
                      [w for w in dict.fromkeys(wrongs) if w != right], self.topic)
