"""จัดรูปกรณฑ์

คณิตศาสตร์ · ม.4 · สสวท. เพิ่มเติม
Indicators: ค เพิ่มเติม จำนวนและพีชคณิต 1 ม.4/3

Sets moved here from: math, math_algebra, math_apply_stage, math_bank_notes, math_bank_powers, math_formats_hi.
"""

from __future__ import annotations

import math
from math import isqrt
from random import Random

from otk.core.content import math as content_math
from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.math_problems import MathDraw, MathType
from otk.sets._support.math_algebra import _surd
from otk.sets._support.math_apply_stage import (
    _nums,
    _split_square,
)
from otk.sets._support.math_apply_stage import (
    _surd as _surd_math_apply_stage,
)
from otk.sets._support.math_bank_notes import M4, _q
from otk.sets._support.math_bank_powers import M4 as M4_math_bank_powers
from otk.sets._support.math_bank_powers import _tex_q
from otk.sets._support.math_diagrams import _math_q
from otk.sets._support.math_m4 import maths


def radical_roots(a: int, b: int, c: int) -> tuple[list[int], list[int]]:
    """Integer roots of √(ax + b) = x + c, as (valid, extraneous) after squaring:
    x² + (2c − a)x + (c² − b) = 0; a root is valid when x + c ≥ 0 (then ax + b = (x + c)² ≥ 0)."""
    p, q = 2 * c - a, c * c - b
    disc = p * p - 4 * q
    if disc < 0 or isqrt(disc) ** 2 != disc or (p + isqrt(disc)) % 2:
        return [], []
    r = isqrt(disc)
    roots = sorted({(-p + r) // 2, (-p - r) // 2})
    return [x for x in roots if x + c >= 0], [x for x in roots if x + c < 0]


def nested_value(m: int) -> int:
    """√(a + √(a + ⋯)) with a = m(m − 1): x² = a + x has the non-negative root m."""
    return m


def _lin(k: int, c: int) -> str:
    head = {1: "", -1: "-"}.get(k, str(k)) + "x"
    return head if not c else f"{head} {'+' if c > 0 else '-'} {abs(c)}"


def _root_tex(k: int) -> str:
    r = math.isqrt(k)
    return str(r) if r * r == k else rf"\sqrt{{{k}}}"


def denest(m: int, n: int, plus: bool) -> str:
    """√(m + n ± 2√(mn)) = √m ± √n (m > n)."""
    return f"{_root_tex(m)} {'+' if plus else '-'} {_root_tex(n)}"


def _true_radical(rng: Random) -> str:
    k = rng.randint(2, 7)
    s = rng.choice((2, 3, 5, 6, 7))
    form = rng.randrange(4)
    if form == 0:
        return rf"\sqrt{{{k * k * s}}} = {k}\sqrt{{{s}}}"
    if form == 1:
        a, b = rng.randint(1, 6), rng.randint(1, 6)
        return rf"{a}\sqrt{{{s}}} + {b}\sqrt{{{s}}} = {a + b}\sqrt{{{s}}}"
    if form == 2:
        return rf"\sqrt{{{s}}} \cdot \sqrt{{{k * k * s}}} = {k * s}"
    return rf"\frac{{\sqrt{{{k * k * s}}}}}{{\sqrt{{{s}}}}} = {k}"


def _false_radical(rng: Random, form: int) -> str:
    a, b = rng.sample((2, 3, 5, 6, 7), 2)
    k = rng.randint(2, 6)
    return (
        rf"\sqrt{{{a}}} + \sqrt{{{b}}} = \sqrt{{{a + b}}}",
        rf"\sqrt{{{k * k * a}}} = {k * k}\sqrt{{{a}}}",
        rf"{k}\sqrt{{{a}}} = \sqrt{{{k * a}}}",
        rf"\sqrt{{{a}}} \cdot \sqrt{{{a}}} = {a * a}",
        rf"\sqrt{{{k * k + a * a}}} = {k + a}",
        rf"\sqrt{{{a}}} + \sqrt{{{a}}} = \sqrt{{{2 * a}}}",
    )[form]


@question_type("math.radical_arithmetic", display_name={"th": "บวกลบคูณกรณฑ์"},
               level={"th": "ม.4"}, topic="จัดรูปกรณฑ์")
class RadicalArithmetic(MathType):
    break_convergence = True  # one-part slips cluster round the answer
    def expr(self, rng: Random, coef_hi: int = 6, radicand_hi: int = 20):
        # Square-free radicands only: √18 + √18 = 2√18 is not in simplest
        # form (6√2), and simplifying is not what this set practises.
        n = rng.choice([m for m in range(2, radicand_hi)
                        if all(m % (k * k) for k in range(2, 5))])
        a, b = rng.randint(1, coef_hi), rng.randint(1, coef_hi)
        total = a + b
        return MathDraw(
            f"{_surd(a, n)} + {_surd(b, n)}", _surd(total, n),
            prompt="จงจัดรูป",
            # Adding the radicands is the standard wrong move.
            distractors=[_surd(a * b, n), _surd(total, 2 * n),
                         _surd(1, total * n)])
RadicalArithmetic.PROVENANCE = Provenance("original")


@question_type("math.rationalize",
               display_name={"th": "จัดรูปส่วนไม่ติดราก"}, level={"th": "ม.4"},
               topic="จัดรูปกรณฑ์")
class Rationalize(MathType):
    def expr(self, rng: Random):
        d, n = rng.choice([(2, 1), (3, 1), (5, 1), (5, 2), (6, 1), (6, 2),
                           (7, 1), (7, 2), (10, 3)])
        minus = rng.random() < 0.5
        op = "-" if minus else "+"
        conj_op = "+" if minus else "-"
        den = d - n * n
        num = rf"\sqrt{{{d}}} {conj_op} {n}"
        answer = num if den == 1 else rf"\frac{{{num}}}{{{den}}}"
        return MathDraw(rf"\frac{{1}}{{\sqrt{{{d}}} {op} {n}}}", answer,
                        hint=r"\text{multiply by the conjugate}",
                        prompt="จงทำส่วนให้ไม่ติดกรณฑ์")
Rationalize.PROVENANCE = Provenance("original")


@question_type("math.radical_true_statement_m4", display_name={"th": "ข้อความใดเกี่ยวกับกรณฑ์ถูกต้อง"},
               level={"th": "ม.4"}, topic="จัดรูปกรณฑ์")
class RadicalTrueStatementM4(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        forms = rng.sample(range(6), 3)
        return _math_q([text("ข้อใดถูกต้อง")], _true_radical(rng),
                       [_false_radical(rng, f) for f in forms], self.topic)
RadicalTrueStatementM4.PROVENANCE = Provenance("original")


@question_type("math.rationalize_binomial",
               display_name={"th": "จัดรูปส่วนด้วยสังยุค"},
               level={"th": "ม.4"}, topic="จัดรูปกรณฑ์")
class RationalizeBinomial(MathType):
    break_convergence = True  # one-part slips cluster round the answer
    def expr(self, rng: Random, radicand_hi: int = 15, term_hi: int = 6):
        squares = {k * k for k in range(1, 8)}
        n = rng.choice([m for m in range(2, radicand_hi) if m not in squares])
        a = rng.randint(1, term_hi)
        denom = a * a - n                         # (a + √n)(a − √n)
        if denom == 0:
            a += 1
            denom = a * a - n
        return MathDraw(
            rf"\frac{{1}}{{{a} + \sqrt{{{n}}}}}",
            rf"\frac{{{a} - \sqrt{{{n}}}}}{{{denom}}}",
            prompt="จงจัดรูปให้ส่วนไม่ติดราก",
            distractors=[rf"\frac{{{a} + \sqrt{{{n}}}}}{{{denom}}}",
                         rf"\frac{{{a} - \sqrt{{{n}}}}}{{{a * a + n}}}",
                         rf"\frac{{1}}{{{a} - \sqrt{{{n}}}}}",
                         # Two slips at once.
                         rf"\frac{{{a} + \sqrt{{{n}}}}}{{{a * a + n}}}",
                         rf"\frac{{{a} + \sqrt{{{n}}}}}{{{-denom}}}"])
RationalizeBinomial.PROVENANCE = Provenance("original")


@question_type("math.radical_geometry_m4", display_name={"th": "กรณฑ์ในการวัดความยาวและพื้นที่"},
               level={"th": "ม.4"}, topic="จัดรูปกรณฑ์")
class RadicalGeometryM4(QuestionType):
    def build(self, rng: Random, **params) -> GeneratedQuestion:
        kind = rng.randrange(3)
        if kind == 0:
            while True:
                a, b = rng.sample(range(1, 10), 2)
                k, m = _split_square(a * a + b * b)
                if k > 1 and m > 1:
                    break
            stem = f"รูปสี่เหลี่ยมผืนผ้ากว้าง {a} หน่วย ยาว {b} หน่วย เส้นทแยงมุมยาวกี่หน่วย"
            right = _surd_math_apply_stage(k, m)
            # Adding the sides under one root, adding them outright, k and m swapped.
            wrongs = [rf"\sqrt{{{a + b}}}", str(a + b), _surd_math_apply_stage(m, k) if m != k else _surd_math_apply_stage(k, m + 1),
                      _surd_math_apply_stage(k + 1, m)]
            return maths([text(stem)], right, wrongs, self.topic)
        if kind == 1:
            m = rng.choice((2, 3, 5))
            ks = rng.sample(range(1, 6), 3)
            sides = [k * k * m for k in ks]
            stem = ("รูปสามเหลี่ยมมีด้านยาว " + ", ".join(rf"√{s}" for s in sides[:2]) +
                    f" และ √{sides[2]} หน่วย ความยาวรอบรูปเท่ากับกี่หน่วย")
            right = _surd_math_apply_stage(sum(ks), m)
            wrongs = [_surd_math_apply_stage(1, sum(sides)), _surd_math_apply_stage(sum(ks), 3 * m), _surd_math_apply_stage(sum(ks) + 1, m), str(sum(ks) * m)]
            return maths([text(stem)], right, wrongs, self.topic)
        a = rng.randint(3, 9)
        b = rng.choice([n for n in range(2, a * a) if _split_square(n)[0] == 1])
        area = a * a - b
        stem = f"รูปสี่เหลี่ยมผืนผ้ากว้าง {a} − √{b} หน่วย ยาว {a} + √{b} หน่วย มีพื้นที่กี่ตารางหน่วย"
        return maths([text(stem)], str(area), _nums(area, a * a + b, a * a - b * b, 2 * a, lo=-999), self.topic)
RadicalGeometryM4.PROVENANCE = Provenance("original")


@question_type("math.radical_equation_m4",
               display_name={"th": "สมการติดรูทและรูทไม่รู้จบ"},
               level=M4, topic="จัดรูปกรณฑ์")
class RadicalEquationM4(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        if rng.random() < 0.65:
            while True:
                r1, r2 = rng.randint(-3, 9), rng.randint(-8, 6)
                if r2 >= r1:
                    continue
                c = rng.randint(-r1, -r2 - 1)                  # r1 + c ≥ 0 > r2 + c
                a, b = 2 * c + r1 + r2, c * c - r1 * r2
                if a and radical_roots(a, b, c) == ([r1], [r2]):
                    break
            lhs = rf"\sqrt{{{_lin(a, b)}}}"
            stem = [text("ผลบวกของคำตอบทั้งหมดของสมการ"), content_math(f"{lhs} = {_lin(1, c)}"),
                    text("เท่ากับเท่าใด")]
            # Keeping the extraneous root; the extraneous root alone; the sum's sign flipped.
            return _q(stem, r1, [r1 + r2, r2, -(r1 + r2)], self.topic)
        m = rng.randint(2, 9)
        a = m * (m - 1)
        stem = [text("ค่าของ"), content_math(rf"\sqrt{{{a} + \sqrt{{{a} + \sqrt{{{a} + \cdots}}}}}}"),
                text("เท่ากับเท่าใด")]
        # The negative root of x² − x − a = 0; √a rounded down; m − 1.
        return _q(stem, nested_value(m), [1 - m, isqrt(a), m - 1], self.topic)
RadicalEquationM4.PROVENANCE = Provenance("original")


@question_type("math.radical_denest_m4",
               display_name={"th": "ถอดรากซ้อน"},
               level=M4_math_bank_powers, topic="จัดรูปกรณฑ์")
class RadicalDenestM4(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        while True:
            m, n = sorted(rng.sample(range(1, 13), 2), reverse=True)
            mn = m * n
            if math.isqrt(mn) ** 2 != mn:
                break
        plus = rng.random() < 0.5
        a = m + n
        right = denest(m, n, plus)
        inner = rf"{a} {'+' if plus else '-'} 2\sqrt{{{mn}}}"
        if rng.random() < 0.4:
            inner = rf"{a} {'+' if plus else '-'} \sqrt{{{4 * mn}}}"
        stem = [text("ค่าของ"), content_math(rf"\sqrt{{{inner}}}"), text("เท่ากับข้อใด")]
        # The other sign; √a ± √(mn); the terms swapped (negative for a minus).
        wrongs = [denest(m, n, not plus), f"{_root_tex(a)} {'+' if plus else '-'} {_root_tex(mn)}",
                  f"{_root_tex(n)} {'+' if plus else '-'} {_root_tex(m)}" if not plus
                  else f"{_root_tex(2 * m)} + {_root_tex(n)}"]
        return _tex_q(stem, right, wrongs, self.topic)
RadicalDenestM4.PROVENANCE = Provenance("adapted", sources=('openthaiknowledge-bank/rathcenter/5 เลขยกกำลัง',))
