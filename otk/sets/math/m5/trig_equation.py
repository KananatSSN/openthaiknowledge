"""สมการตรีโกณมิติ

คณิตศาสตร์ · ม.5 · สสวท. เพิ่มเติม
Indicators: ค เพิ่มเติม จำนวนและพีชคณิต 3 ม.5/1

Sets moved here from: math, math_bank_trig, math_geometry.
"""

from __future__ import annotations

import math
from fractions import Fraction
from random import Random

from otk.core.content import math as content_math
from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.math_problems import MathDraw, MathType, frac_tex
from otk.sets._support.math_bank_trig import M5, _int_q, pi_tex
from otk.sets._support.math_geometry import _COS, _SIN, _TAN

_TRIG_EQUATIONS = [
    (r"\sin", r"\frac{1}{2}", (30, 150)),
    (r"\sin", r"\frac{\sqrt{2}}{2}", (45, 135)),
    (r"\sin", r"\frac{\sqrt{3}}{2}", (60, 120)),
    (r"\cos", r"\frac{1}{2}", (60, 300)),
    (r"\cos", r"\frac{\sqrt{2}}{2}", (45, 315)),
    (r"\cos", r"\frac{\sqrt{3}}{2}", (30, 330)),
    (r"\tan", "1", (45, 225)),
    (r"\tan", r"\sqrt{3}", (60, 240)),
    (r"\tan", r"\frac{\sqrt{3}}{3}", (30, 210)),
]


EQUATIONS = "สมการตรีโกณมิติ"


def sine_solution_count(k: int, n: int, positive: bool) -> int:
    """#θ ∈ [0, nπ] with sin kθ = c, 0 < |c| < 1: two per 2π of u = kθ, plus the half period."""
    m = k * n
    if m % 2 == 0:
        return m
    return m + 1 if positive else m - 1


def cos_or_tan_solution_count(k: int, n: int) -> int:
    """#θ ∈ [0, nπ] with cos kθ = c (|c| < 1) or tan kθ = c (c ≠ 0): one per π of u = kθ."""
    return k * n


def tan_shift_count(lam: float, m: int) -> int:
    """#x ∈ [0, mπ] with tan(λx) = tan(λπ), λ irrational: x = π + jπ/λ, −λ ≤ j ≤ (m − 1)λ."""
    return math.floor((m - 1) * lam) + math.floor(lam) + 1


#: (TeX, the value stated in the stem, true value) for irrational λ.
LAMBDAS = (("e", "2.71", math.e), (r"\sqrt{2}", "1.41", math.sqrt(2)), (r"\sqrt{3}", "1.73", math.sqrt(3)),
           (r"\sqrt{5}", "2.24", math.sqrt(5)), (r"\pi", "3.14", math.pi))


@question_type("math.trig_equation",
               display_name={"th": "สมการตรีโกณมิติ"}, level={"th": "ม.5"},
               topic="สมการตรีโกณมิติ")
class TrigEquation(MathType):
    def expr(self, rng: Random):
        fn, val, (s1, s2) = rng.choice(_TRIG_EQUATIONS)
        return MathDraw(rf"{fn} x = {val} \;\; (0^{{\circ}} \leq x < 360^{{\circ}})",
                        rf"x = {s1}^{{\circ}}, \; {s2}^{{\circ}}", prompt="จงแก้สมการ")
TrigEquation.PROVENANCE = Provenance("original")


@question_type("math.trig_equation_general",
               display_name={"th": "สมการตรีโกณมิติ: คำตอบทั่วไป"},
               level={"th": "ม.5"}, topic="สมการตรีโกณมิติ")
class TrigEquationGeneral(MathType):
    """sin θ = k has two solutions in [0°, 360°) — remembering the second one is
    the whole lesson."""

    def expr(self, rng: Random):
        angle = rng.choice([30, 45, 60])
        sin = rng.random() < 0.5
        negative = rng.random() < 0.5
        value = (_SIN if sin else _COS)[angle]
        fn = r"\sin" if sin else r"\cos"
        # A negative value sits in the other two quadrants: sin in III and IV,
        # cos in II and III.
        if sin:
            first, second = (180 + angle, 360 - angle) if negative else (angle, 180 - angle)
        else:
            first, second = (180 - angle, 180 + angle) if negative else (angle, 360 - angle)
        # The positive value's pair; only the first solution; the other
        # function's pair; and a period of 180°, which is tan's.
        other = ((angle, 180 - angle) if sin else (angle, 360 - angle)) if negative else (
            (180 + angle, 360 - angle) if sin else (180 - angle, 180 + angle))
        wrongs = [f"{other[0]}^\\circ, {other[1]}^\\circ", f"{first}^\\circ",
                  f"{first}^\\circ, {(360 - first) if sin else (540 - first) % 360}^\\circ",
                  f"{first}^\\circ, {(first + 180) % 360}^\\circ"]
        right = f"{first}^\\circ, {second}^\\circ"
        return MathDraw(
            rf"{fn}\theta = {'-' if negative else ''}{value}, \quad 0^\circ \le \theta < 360^\circ",
            right, prompt="จงหาคำตอบทั้งหมดของสมการ",
            distractors=[w for w in dict.fromkeys(wrongs) if w != right])
TrigEquationGeneral.PROVENANCE = Provenance("original")


@question_type("math.trig_equation_count_m5",
               display_name={"th": "จำนวนคำตอบของสมการตรีโกณมิติในช่วงที่กำหนด"},
               level=M5, topic=EQUATIONS)
class TrigEquationCountM5(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        kind = rng.randrange(3)
        n = rng.randint(1, 3)
        interval = rf"\theta \in \left[0, {pi_tex(Fraction(n))}\right]"
        if kind == 0:
            k = rng.randint(2, 6)
            a, b = rng.choice(((4, 3), (3, 2), (5, 2), (4, -3), (3, -1), (5, -4), (7, 3), (3, 1)))
            right = sine_solution_count(k, n, b > 0)
            stem = [text("เซตคำตอบของสมการ"), content_math(rf"{a}\sin {k}\theta = {b}"), text("เมื่อ"),
                    content_math(interval), text("มีสมาชิกทั้งหมดกี่ตัว")]
            # Ignoring the half period; ignoring k; the sign of c ignored; four per period.
            return _int_q(stem, right, [k * n, sine_solution_count(1, n, b > 0), sine_solution_count(k, n, b < 0),
                                        2 * k * n],
                          self.topic)
        if kind == 1:
            k = rng.randint(2, 6)
            fn = rng.choice(("cos", "tan"))
            c = rng.choice((2, 3, 5)) if fn == "cos" else rng.choice((1, 2, 3))
            d = rng.choice((1, 2, 3, 4, 7)) if fn == "tan" else c + rng.randint(1, 3)
            value = frac_tex(Fraction(rng.choice((1, -1)) * c, d))
            right = cos_or_tan_solution_count(k, n)
            stem = [text("เซตคำตอบของสมการ"), content_math(rf"\{fn} {k}\theta = {value}"), text("เมื่อ"),
                    content_math(interval), text("มีสมาชิกทั้งหมดกี่ตัว")]
            # Two per period as for sine; counting an endpoint; one per period 2π.
            return _int_q(stem, right, [2 * k * n, k * n + 1, max(1, k * n // 2), k * n - 1], self.topic)
        lt, approx, lam = rng.choice(LAMBDAS)
        m = rng.randint(1, 3)
        right = tan_shift_count(lam, m)
        stem = [text("จำนวนคำตอบของสมการ"), content_math(rf"\tan({lt}x) = \tan({lt}\pi)"), text("สำหรับ"),
                content_math(rf"x \in \left[0, {pi_tex(Fraction(m))}\right]"), text("เมื่อ"), content_math(lt),
                text("มีค่าประมาณ"), content_math(approx), text("มีทั้งหมดกี่คำตอบ")]
        # Only the solutions after π; only the one obvious solution plus one each side; one more.
        return _int_q(stem, right, [math.floor((m - 1) * lam) + 1, right - 1, math.floor(m * lam), right + 1],
                      self.topic)
TrigEquationCountM5.PROVENANCE = Provenance("adapted", sources=('openthaiknowledge-bank/rathcenter/8 ตรีโกณมิติ',))


@question_type("math.trig_equation_tangent",
               display_name={"th": "สมการตรีโกณมิติของ tan"},
               level={"th": "ม.5"}, topic="สมการตรีโกณมิติ")
class TrigEquationTangent(MathType):
    def expr(self, rng: Random):
        angle = rng.choice([0, 30, 45, 60])
        negative = bool(angle) and rng.random() < 0.5
        # A negative tan puts the first solution in quadrant II.
        first = 180 - angle if negative else angle
        right = f"{first}^\\circ, {first + 180}^\\circ"
        # tan has period 180°, not 360° — the second solution is θ + 180°,
        # not 360° − θ, which is where sin/cos habits mislead.
        wrongs = [f"{first}^\\circ", f"{first}^\\circ, {360 - first}^\\circ",
                  f"{angle}^\\circ, {angle + 180}^\\circ", f"{first}^\\circ, {first + 90}^\\circ"]
        return MathDraw(
            rf"\tan\theta = {'-' if negative else ''}{_TAN[angle]}, \quad 0^\circ \le \theta < 360^\circ",
            right, prompt="จงหาคำตอบทั้งหมดของสมการ",
            distractors=[w for w in dict.fromkeys(wrongs) if w != right][:3])
TrigEquationTangent.PROVENANCE = Provenance("original")
