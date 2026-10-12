"""ฟังก์ชัน

คณิตศาสตร์ · ม.4 · สสวท. เพิ่มเติม
Indicators: ค เพิ่มเติม จำนวนและพีชคณิต 2 ม.4/2

Sets moved here from: math_bank_functions, math_chapters.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.content import math as content_math
from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.math_problems import frac_tex
from otk.sets._support.math_bank_functions import (
    M4 as M4_math_bank_functions,
)
from otk.sets._support.math_bank_functions import (
    _frac_q,
    _minus,
    _tex_q,
)
from otk.sets._support.math_chapters import _distinct, _lin
from otk.sets._support.math_m4 import maths as _num_maths
from otk.sets._support.math_p2 import _maths, _texts


def moved(point: tuple[int, int], rule: str, h: int, k: int) -> tuple[int, int]:
    """Where (p, q) on y = f(x) lands on the transformed graph."""
    p, q = point
    return {"shift": (p + h, q + k), "neg_y": (p, -q), "neg_x": (-p, q),
            "both": (-p, -q)}[rule]


def exp_constants(base: int, x_cut: int, a: int) -> tuple[int, Fraction]:
    """(a, c) for y = base^(x + a) + c through (x_cut, 0), plus the y-intercept."""
    c = -base ** (x_cut + a)
    return a, Fraction(base) ** a + c


M4 = {"th": "ม.4"}


_FUNCTION_TOPIC = "ฟังก์ชัน"


def _over(num: str, den: int) -> str:
    """A linear numerator over a whole denominator, sign moved to the front."""
    return rf"\frac{{{num}}}{{{den}}}" if den > 0 else rf"-\frac{{{num}}}{{{-den}}}"


def _inverse_linear(a: int, b: int) -> str:
    return _over(_lin(1, -b), a)


_ONE_TO_ONE = ("y = 2x + 1", "y = x^{3}", "y = 2^{x}", "y = 5 - 3x", r"y = \log_{2} x",
               r"y = \sqrt{x}")


_MANY_TO_ONE = ("y = x^{2}", "y = |x|", "y = x^{2} + 1", "y = (x - 1)^{2}", "y = 4",
                "y = x^{2} - 4x")


# (the parent graph, its shifted form, what the turning point is called)
_PARENTS = (
    ("x^{2}", lambda inner: f"({inner})^{{2}}", "จุดยอด"),
    ("|x|", lambda inner: f"|{inner}|", "จุดยอด"),
    (r"\sqrt{x}", lambda inner: rf"\sqrt{{{inner}}}", "จุดเริ่มต้น"),
)


def _shifted(parent, h: int, k: int) -> str:
    inner = _lin(1, -h)
    tail = f" + {k}" if k > 0 else f" - {-k}"
    return f"y = {parent[1](inner)}{tail}"


def _moves(h: int, k: int) -> str:
    return (f"เลื่อนไปทาง{'ขวา' if h > 0 else 'ซ้าย'} {abs(h)} หน่วย "
            f"และเลื่อน{'ขึ้น' if k > 0 else 'ลง'} {abs(k)} หน่วย")


@question_type("math.inverse_function_value_m4",
               display_name={"th": "ค่าของฟังก์ชันผกผันและฟังก์ชันหนึ่งต่อหนึ่ง"},
               level=M4, topic=_FUNCTION_TOPIC)
class InverseFunctionValueM4(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        kind = rng.randrange(3)
        if kind == 0:
            a = rng.choice((-4, -3, -2, 2, 3, 4, 5))
            b = rng.choice([v for v in range(-9, 10) if v])
            t = rng.randint(-6, 9)
            c = a * t + b
            back = Fraction(c + b, a)
            # f(c) in place of f⁻¹(c), and the constant undone the wrong way.
            wrongs = [str(a * c + b), frac_tex(back) if back != t else str(t + 2), str(-t) if t else "1"]
            return _num_maths([text("กำหนดให้"), content_math(f"f(x) = {_lin(a, b)}"),
                               text("จงหาค่าของ"), content_math(rf"f^{{-1}}({c})")],
                              str(t), wrongs, self.topic)
        if kind == 1:
            xs = rng.sample(range(-3, 10), 4)
            ys = rng.sample(range(-3, 13), 4)
            pairs = r",\ ".join(f"({x}, {y})" for x, y in zip(xs, ys))
            j = rng.randrange(4)
            return _num_maths([content_math(rf"f = \{{{pairs}\}}"),
                               text("จงหาค่าของ"), content_math(rf"f^{{-1}}({ys[j]})")],
                              str(xs[j]), [str(x) for i, x in enumerate(xs) if i != j], self.topic)
        if rng.random() < 0.5:
            right = rng.choice(_ONE_TO_ONE)
            wrongs = rng.sample(_MANY_TO_ONE, 3)
            ask = "ฟังก์ชันใดเป็นฟังก์ชันหนึ่งต่อหนึ่ง (มีฟังก์ชันผกผันที่เป็นฟังก์ชัน)"
        else:
            right = rng.choice(_MANY_TO_ONE)
            wrongs = rng.sample(_ONE_TO_ONE, 3)
            ask = "ฟังก์ชันใดไม่เป็นฟังก์ชันหนึ่งต่อหนึ่ง"
        return _maths([text(ask)], right, wrongs, self.topic)
InverseFunctionValueM4.PROVENANCE = Provenance("original")


@question_type("math.inverse_function_formula_m4", display_name={"th": "หาฟังก์ชันผกผัน"},
               level=M4, topic=_FUNCTION_TOPIC)
class InverseFunctionFormulaM4(QuestionType):
    break_convergence = True  # one-part slips cluster round the answer
    def build(self, rng: Random) -> GeneratedQuestion:
        if rng.random() < 0.55:
            a = rng.choice((-5, -4, -3, -2, 2, 3, 4, 5, 6, 7))
            b = rng.choice([v for v in range(-9, 10) if v])
            f = _lin(a, b)
            right = _inverse_linear(a, b)
            # Subtracting the wrong sign, the reciprocal, dividing before
            # undoing the constant.
            wrongs = [_inverse_linear(-a, -b), _inverse_linear(a, -b), rf"\frac{{1}}{{{f}}}",
                      _over("x", a) + (f" - {b}" if b > 0 else f" + {-b}"), _lin(a, -b)]
        else:
            p, q = rng.sample([v for v in range(-6, 7) if v], 2)
            if p == -q:
                q = -q + (1 if q > 0 else -1) or 2
            f = rf"\frac{{{_lin(1, p)}}}{{{_lin(1, -q)}}}"
            right = rf"\frac{{{_lin(q, p)}}}{{x - 1}}"
            # The reciprocal, p and q swapped, every sign flipped.
            wrongs = [rf"\frac{{{_lin(1, -q)}}}{{{_lin(1, p)}}}", rf"\frac{{{_lin(p, q)}}}{{x - 1}}",
                      rf"\frac{{{_lin(q, -p)}}}{{x + 1}}", rf"\frac{{x - 1}}{{{_lin(q, p)}}}"]
        fmt = [rf"f^{{-1}}(x) = {w}" for w in _distinct(right, *wrongs)]
        return _maths([text("จงหาฟังก์ชันผกผันของ"), content_math(f"f(x) = {f}")],
                      rf"f^{{-1}}(x) = {right}", fmt[:3], self.topic)
InverseFunctionFormulaM4.PROVENANCE = Provenance("original")


@question_type("math.graph_transform_point_m4",
               display_name={"th": "การเลื่อนและการสะท้อนกราฟ"},
               level=M4_math_bank_functions, topic="ฟังก์ชัน")
class GraphTransformPointM4(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        if rng.random() < 0.7:
            # Nonzero coordinates, so that every reflection actually moves the point.
            p, q = rng.choice([v for v in range(-5, 6) if v]), rng.choice([v for v in range(-6, 7) if v])
            rule = rng.choice(("shift", "neg_y", "neg_x", "both"))
            h, k = rng.choice([v for v in range(-4, 5) if v]), rng.choice([v for v in range(-4, 5) if v])
            new = moved((p, q), rule, h, k)
            g = {"shift": rf"y = f(x {'-' if h > 0 else '+'} {abs(h)}) {'+' if k > 0 else '-'} {abs(k)}",
                 "neg_y": r"y = -f(x)", "neg_x": r"y = f(-x)", "both": r"y = -f(-x)"}[rule]
            # Shifting the wrong way; reflecting in the other axis; both.
            named = {"shift": [(p - h, q + k), (p + h, q - k), (p - h, q - k)],
                     "neg_y": [(-p, q), (-p, -q), (p, q)],
                     "neg_x": [(p, -q), (-p, -q), (p, q)],
                     "both": [(p, -q), (-p, q), (p, q)]}[rule]
            fmt = lambda pt: f"({pt[0]}, {pt[1]})"
            stem = [text(f"ถ้าจุด ({p}, {q}) อยู่บนกราฟของ y = f(x) แล้วจุดในข้อใดอยู่บนกราฟของ"),
                    content_math(g)]
            return _tex_q(stem, fmt(new), [fmt(w) for w in named if w != new], self.topic)
        base = rng.choice((2, 3))
        x_cut, a = rng.randint(1, 3), rng.randint(-2, 1)
        if x_cut + a < 1:
            x_cut = 1 - a
        _, y0 = exp_constants(base, x_cut, a)
        c = -base ** (x_cut + a)
        right = a + c
        y_text = _minus(y0.numerator) if y0.denominator == 1 else f"{_minus(y0.numerator)}/{y0.denominator}"
        stem = [text("กำหนดให้ a และ b เป็นจำนวนจริง ถ้ากราฟของ"),
                content_math(rf"y = {base}^{{x + a}} + b"),
                text(f"ตัดแกน X ที่จุด ({x_cut}, 0) และตัดแกน Y ที่จุด (0, {y_text})"
                     f" แล้ว a + b มีค่าเท่ากับเท่าใด")]
        # The sign of a flipped; b alone; the y-intercept as b.
        named = [-a + c, c, a + y0]
        return _frac_q(stem, Fraction(right), named, self.topic)
GraphTransformPointM4.PROVENANCE = Provenance("adapted", sources=('sheet_database/rathcenter/4 ฟังก์ชัน',))


@question_type("math.graph_shift_m4", display_name={"th": "การเลื่อนกราฟของฟังก์ชัน"},
               level=M4, topic=_FUNCTION_TOPIC)
class GraphShiftM4(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        parent = rng.choice(_PARENTS)
        while True:
            h, k = (rng.choice([v for v in range(-6, 7) if v]) for _ in range(2))
            if abs(h) != abs(k):
                break
        eq = _shifted(parent, h, k)
        kind = rng.randrange(3)
        if kind == 0:
            # Reading x − h as a move left, and the two amounts swapped.
            wrongs = [_moves(-h, k), _moves(h, -k), _moves(-h, -k),
                      _moves(k if h * k > 0 else -k, h if h * k > 0 else -h)]
            return _texts([text("กราฟของ"), content_math(eq), text("ได้จากการเลื่อนกราฟของ"),
                           content_math(f"y = {parent[0]}"), text("อย่างไร")],
                          _moves(h, k), _distinct(_moves(h, k), *wrongs)[:3], self.topic)
        if kind == 1:
            right = f"({h}, {k})"
            wrongs = [f"({-h}, {k})", f"({h}, {-k})", f"({k}, {h})", f"({-h}, {-k})"]
            return _maths([text(f"{parent[2]}ของกราฟ"), content_math(eq), text("คือจุดใด")],
                          right, _distinct(right, *wrongs)[:3], self.topic)
        wrongs = [_shifted(parent, -h, k), _shifted(parent, h, -k), _shifted(parent, -h, -k)]
        return _maths([text("เลื่อนกราฟของ"), content_math(f"y = {parent[0]}"),
                       text(_moves(h, k).removeprefix("เลื่อน") + " จะได้กราฟของฟังก์ชันใด")],
                      eq, wrongs, self.topic)
GraphShiftM4.PROVENANCE = Provenance("original")
