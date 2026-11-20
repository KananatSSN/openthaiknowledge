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


from otk.core.content import math as _math_block  # noqa: E402
from otk.core.content import text as _text_block  # noqa: E402
from otk.core.provenance import Provenance  # noqa: E402
from otk.core.registry import QuestionType, question_type  # noqa: E402
from otk.kit.math_problems import MathType, WordProblem  # noqa: E402
from otk.kit.math_problems import poly_tex  # noqa: E402
from otk.sets._support.math_m4 import M4 as LEVEL  # noqa: E402
from otk.sets._support.math_p2 import _maths as _fixed_maths  # noqa: E402


def _nz4(rng: Random, lo: int, hi: int) -> int:
    return rng.choice((1, -1)) * rng.randint(lo, hi)


def _tk4(*values: str, answer: str) -> list[str]:
    """Distinct TeX distractors, the answer left out."""
    return [v for v in dict.fromkeys(values) if v != answer]


def _fk4(*values, answer: Fraction) -> list[str]:
    """Distinct fraction distractors as TeX, the answer left out."""
    return _tk4(*(frac_tex(Fraction(v)) for v in values), answer=frac_tex(answer))


def _pt4(x, y) -> str:
    return f"({frac_tex(Fraction(x))}, {frac_tex(Fraction(y))})"


def _nk4(*values: int, answer: int, lo: int | None = None) -> list[str]:
    """Distinct whole-number distractors, the answer (and values below lo) left out."""
    return _tk4(*(str(v) for v in values if lo is None or v >= lo), answer=str(answer))

# ── More rational equations and inequalities (2026-11): a / (x − b) = c, a cross-multiplied pair, a sum of
# unit fractions, values x cannot take, a quotient greater than zero, and two workers together ──


@question_type("math.rational_simple_m4", display_name={"th": "แก้สมการเศษส่วนอย่างง่าย"}, level=LEVEL,
               topic="สมการและอสมการเศษส่วน")
class RationalSimpleM4(MathType):
    def expr(self, rng: Random):
        c = _nz4(rng, 1, 6)
        b = _nz4(rng, 1, 9)
        q = _nz4(rng, 1, 6)
        a = c * q
        right = b + q
        # b left behind; a over c only; the sign of b flipped.
        return MathDraw(rf"\frac{{{a}}}{{x {'-' if b > 0 else '+'} {abs(b)}}} = {c}", f"x = {right}", prompt="จงแก้สมการ",
                        distractors=_tk4(f"x = {q}", f"x = {-b + q}", f"x = {b - q}", f"x = {right + 1}", answer=f"x = {right}"))


@question_type("math.rational_cross_m4", display_name={"th": "แก้สมการเศษส่วนโดยคูณไขว้"}, level=LEVEL,
               topic="สมการและอสมการเศษส่วน")
class RationalCrossM4(MathType):
    def expr(self, rng: Random):
        while True:
            a, c = rng.sample(range(1, 8), 2)
            b, d = rng.randint(-9, 9), rng.randint(-9, 9)
            # a(x + d) = c(x + b) → (a − c)x = cb − ad
            if (c * b - a * d) % (a - c) == 0:
                x = (c * b - a * d) // (a - c)
                if x + b != 0 and x + d != 0:
                    break
        right = f"x = {x}"
        wrongs = [f"x = {-x}", f"x = {(c * b + a * d) // (a - c) if (c * b + a * d) % (a - c) == 0 else x + 1}", f"x = {x + 2}"]
        left = rf"\frac{{{a}}}{{{poly_tex((1, 'x'), (b, ''))}}} = \frac{{{c}}}{{{poly_tex((1, 'x'), (d, ''))}}}"
        return MathDraw(left, right, prompt="จงแก้สมการ", distractors=_tk4(*wrongs, answer=right))


@question_type("math.unit_fraction_sum_m4", display_name={"th": "สมการผลบวกของเศษส่วนที่มีตัวแปรเป็นตัวส่วน"},
               level=LEVEL, topic="สมการและอสมการเศษส่วน")
class UnitFractionSumM4(MathType):
    def expr(self, rng: Random):
        k = rng.randint(2, 6)
        x = rng.randint(2, 12)
        rhs = Fraction(k + 1, k * x)
        right = f"x = {x}"
        # Only the first fraction; the right side flipped; the k left in.
        wrongs = [f"x = {frac_tex(1 / rhs)}", f"x = {k * x}", f"x = {x + k}", f"x = {frac_tex(Fraction(k + 1, k))}"]
        return MathDraw(rf"\frac{{1}}{{x}} + \frac{{1}}{{{k}x}} = {frac_tex(rhs)}", right, prompt="จงแก้สมการ",
                        distractors=_tk4(*wrongs, answer=right))


@question_type("math.rational_excluded_value_m4", display_name={"th": "ค่าของ x ที่ทำให้เศษส่วนไม่มีความหมาย"},
               level=LEVEL, topic="สมการและอสมการเศษส่วน")
class RationalExcludedValueM4(QuestionType):
    """Fixed choices: a number from another draw could also make the denominator zero."""

    def build(self, rng: Random, **params):
        a, b = _nz4(rng, 1, 9), _nz4(rng, 1, 9)
        while a == b or a == -b:
            b = _nz4(rng, 1, 9)
        expr = rf"\frac{{x {'+' if b > 0 else '-'} {abs(b)}}}{{x {'-' if a > 0 else '+'} {abs(a)}}}"
        right = str(a)
        # The numerator's zero; the sign flipped; zero itself.
        wrongs = [str(-b), str(-a), "0" if a and b else str(a + 1)]
        return _fixed_maths([_text_block("ค่า x ใดทำให้นิพจน์นี้ไม่มีความหมาย"), _math_block(expr)], right,
                            _tk4(*wrongs, answer=right), self.topic)


@question_type("math.quotient_positive_m4", display_name={"th": "อสมการเศษส่วนที่มากกว่าศูนย์"}, level=LEVEL,
               topic="สมการและอสมการเศษส่วน")
class QuotientPositiveM4(MathType):
    def expr(self, rng: Random):
        a, b = sorted(rng.sample(range(-9, 10), 2))
        right = rf"x < {a} \lor x > {b}"
        # Between the roots; one end closed wrongly; the signs flipped.
        wrongs = [rf"{a} < x < {b}", rf"x \le {a} \lor x > {b}", rf"x < {-b} \lor x > {-a}"]
        expr = rf"\frac{{{poly_tex((1, 'x'), (-a, ''))}}}{{{poly_tex((1, 'x'), (-b, ''))}}} > 0"
        return MathDraw(expr, right, prompt="จงหาคำตอบของอสมการ", distractors=_tk4(*wrongs, answer=right))


@question_type("math.work_together_m4", display_name={"th": "ทำงานร่วมกันเสร็จในกี่ชั่วโมง"}, level=LEVEL,
               topic="สมการและอสมการเศษส่วน")
class WorkTogetherM4(WordProblem):
    _PAIRS = ((3, 6), (4, 12), (6, 12), (10, 15), (12, 24), (20, 30), (6, 3), (12, 4), (5, 20), (8, 24), (9, 18), (15, 10))

    def expr(self, rng: Random):
        a, b = rng.choice(self._PAIRS)
        right = a * b // (a + b)
        p, q = _story.names(rng)
        prompt = f"{p}ทาสีห้องคนเดียวเสร็จใน {a} ชั่วโมง {q}ทำคนเดียวเสร็จใน {b} ชั่วโมง ถ้าทำพร้อมกันจะเสร็จในกี่ชั่วโมง"
        # The average; the sum; the difference.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_nk4((a + b) // 2, a + b, abs(a - b), min(a, b), answer=right, lo=1))
