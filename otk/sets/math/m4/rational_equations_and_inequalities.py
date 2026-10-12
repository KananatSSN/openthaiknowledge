"""สมการและอสมการเศษส่วน

คณิตศาสตร์ · ม.4 · สสวท. เพิ่มเติม
Indicators: ค เพิ่มเติม จำนวนและพีชคณิต 3 ม.4/2

Sets moved here from: math_bank_textbook_real, math_gaps_secondary.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.content import math as content_math
from otk.core.content import text
from otk.core.distractors import fixed
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, WordProblem, frac_tex
from otk.sets._support.math_bank_textbook_real import M4, _q, ptex
from otk.sets._support.math_gaps_secondary import _lin as _lin_math_gaps_secondary
from otk.sets._support.math_gaps_secondary import _nz

PROVENANCE = Provenance("original")


def cover_up(p: int, q: int, a: int, b: int) -> tuple[Fraction, Fraction]:
    """(A, B) with (px + q)/((x − a)(x − b)) = A/(x − a) + B/(x − b)."""
    return Fraction(p * a + q, a - b), Fraction(p * b + q, b - a)


def _lin(r: int) -> str:
    return "x" if r == 0 else f"x {'-' if r > 0 else '+'} {abs(r)}"


def _ab(A, B) -> str:
    return rf"A = {frac_tex(Fraction(A))},\ B = {frac_tex(Fraction(B))}"


_RATIONAL_TOPIC = "สมการและอสมการเศษส่วน"


@question_type("math.rational_equation_m4", display_name={"th": "แก้สมการเศษส่วนของพหุนาม"},
               level={"th": "ม.4"}, topic=_RATIONAL_TOPIC)
class RationalEquationM4(WordProblem):
    """(x + a)/(x + b) = k with k ≠ 1, so x = (kb − a)/(1 − k) and x ≠ −b."""
    break_convergence = True  # one-part slips cluster round the answer

    def expr(self, rng: Random):
        while True:
            a, b, k = _nz(rng, -9, 9), _nz(rng, -9, 9), rng.choice((-3, -2, 2, 3, 4))
            if (k * b - a) % (1 - k) == 0 and a != b:
                x = (k * b - a) // (1 - k)
                if x != -b:
                    break
        tex = rf"\frac{{{_lin_math_gaps_secondary(1, a)}}}{{{_lin_math_gaps_secondary(1, b)}}} = {k}"
        # Stopping before dividing by 1 − k, a sign slip, and the value the
        # denominator forbids.
        return MathDraw(tex, f"x = {x}", prompt="จงแก้สมการ",
                        distractors=[f"x = {w}" for w in _story.keep(k * b - a, -x, -b, x + 1,
                                                                     answer=x, lo=-999)[:3]])


@question_type("math.rational_equation_extraneous_m4", display_name={"th": "สมการเศษส่วนที่มีคำตอบที่ใช้ไม่ได้"},
               level={"th": "ม.4"}, topic=_RATIONAL_TOPIC)
class RationalEquationExtraneousM4(QuestionType):
    """x²/(x − a) = a²/(x − a): clearing the denominator gives x = ±a, but
    x = a makes the denominator zero, so only x = −a is a solution."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        a = rng.randint(2, 9)
        kind = rng.randrange(3)
        if kind == 0:
            tex = rf"\frac{{x^{{2}}}}{{x - {a}}} = \frac{{{a * a}}}{{x - {a}}}"
            right, wrongs = rf"\{{-{a}\}}", [rf"\{{-{a}, {a}\}}", rf"\{{{a}\}}", r"\varnothing"]
        elif kind == 1:
            # The mirror image: x = −a is the one the denominator forbids.
            tex = rf"\frac{{x^{{2}}}}{{x + {a}}} = \frac{{{a * a}}}{{x + {a}}}"
            right, wrongs = rf"\{{{a}\}}", [rf"\{{-{a}, {a}\}}", rf"\{{-{a}\}}", r"\varnothing"]
        else:
            # The only root clearing gives is forbidden, so there is none.
            tex = rf"\frac{{x}}{{x - {a}}} = \frac{{{a}}}{{x - {a}}}"
            right, wrongs = r"\varnothing", [rf"\{{{a}\}}", rf"\{{-{a}\}}", r"\{0\}"]
        stem = [text("จงหาเซตคำตอบของสมการ"), content_math(tex)]
        return GeneratedQuestion(stem=stem, correct=[content_math(right)],
                                 distractors=fixed(*[[content_math(w)] for w in wrongs]), topic=self.topic)


@question_type("math.partial_fractions_m4",
               display_name={"th": "แยกเศษส่วนย่อย"},
               level=M4, topic="สมการและอสมการเศษส่วน")
class PartialFractionsM4(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        if rng.random() < 0.6:
            while True:
                a, b = rng.sample([v for v in range(-5, 6)], 2)
                A, B = (rng.choice([v for v in range(-6, 7) if v]) for _ in range(2))
                p, q = A + B, -(A * b + B * a)
                if p == 0 or A == B or abs(a - b) == 1:
                    continue
                if cover_up(p, q, a, b) != (A, B):          # pragma: no cover
                    raise AssertionError("cover-up disagrees with the construction")
                break
            den = rf"({_lin(a)})({_lin(b)})"
            stem = [text("ถ้า"), content_math(rf"\frac{{{ptex([p, q])}}}{{{den}}} = \frac{{A}}{{{_lin(a)}}} + \frac{{B}}{{{_lin(b)}}}"),
                    text("แล้ว A และ B คือข้อใด")]
            # Swapped; both signs flipped; the cover-up without dividing by a − b.
            wrongs = [_ab(B, A), _ab(-A, -B), _ab(p * a + q, p * b + q)]
            return _q(stem, _ab(A, B), wrongs, self.topic)
        while True:
            k = rng.choice((1, 2, 3, 4, 5))
            A, B, C = (rng.choice([v for v in range(-5, 6) if v]) for _ in range(3))
            num = [A + B, C, A * k]                # A(x² + k) + (Bx + C)x
            if num[0] != 0 and k != 1:
                break
        right = A + B + C
        stem = [text("ถ้า"), content_math(rf"\frac{{{ptex(num)}}}{{x(x^{{2}} + {k})}} = \frac{{A}}{{x}} + \frac{{Bx + C}}{{x^{{2}} + {k}}}"),
                text("เมื่อ A, B, C เป็นค่าคงตัว แล้ว A + B + C เท่ากับเท่าใด")]
        # A left as the constant term A·k (not divided by k); C's sign flipped;
        # B read as the whole x² coefficient A + B.
        named = [A * k + B + C, A + B - C, A + num[0] + C, right + 1, right - 1]
        return _q(stem, str(right), [str(w) for w in named], self.topic)


@question_type("math.rational_inequality_m4", display_name={"th": "แก้อสมการเศษส่วนของพหุนาม"},
               level={"th": "ม.4"}, topic=_RATIONAL_TOPIC)
class RationalInequalityM4(QuestionType):
    """(x − p)/(x − q) ≥ 0 or ≤ 0 with p ≠ q. q is never in the set."""
    break_convergence = True  # one-part slips cluster round the answer

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        p, q = rng.sample(range(-6, 7), 2)
        lo, hi = min(p, q), max(p, q)
        ge = rng.random() < 0.5
        lo_b = "[" if lo == p else "("
        hi_b = "]" if hi == p else ")"
        inside = rf"{lo_b}{lo}, {hi}{hi_b}"
        # Outside the roots: the numerator's root is kept, the pole is not.
        left_b = "]" if lo == p else ")"
        right_b = "[" if hi == p else "("
        outside = rf"(-\infty, {lo}{left_b} \cup {right_b}{hi}, \infty)"
        right = outside if ge else inside
        wrong_same = inside if ge else outside
        closed_all = (rf"(-\infty, {lo}] \cup [{hi}, \infty)" if ge else rf"[{lo}, {hi}]")
        open_all = (rf"(-\infty, {lo}) \cup ({hi}, \infty)" if ge else rf"({lo}, {hi})")
        sign = r"\geq" if ge else r"\leq"   # a backslash inside an f-string needs Python 3.12
        stem = [text("จงหาเซตคำตอบของอสมการ"),
                content_math(rf"\frac{{{_lin_math_gaps_secondary(1, -p)}}}{{{_lin_math_gaps_secondary(1, -q)}}} {sign} 0")]
        # The other region with the wrong brackets too: two slips at once.
        other_closed = (rf"[{lo}, {hi}]" if ge else rf"(-\infty, {lo}] \cup [{hi}, \infty)")
        other_open = (rf"({lo}, {hi})" if ge else rf"(-\infty, {lo}) \cup ({hi}, \infty)")
        wrongs = [w for w in dict.fromkeys([closed_all, open_all, wrong_same, other_closed, other_open])
                  if w != right]
        return GeneratedQuestion(stem=stem, correct=[content_math(right)],
                                 distractors=fixed(*[[content_math(w)] for w in wrongs]), topic=self.topic)
