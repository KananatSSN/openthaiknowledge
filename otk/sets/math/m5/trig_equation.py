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
        # A bare command such as \pi needs a space before x: \pix is an unknown command, not πx.
        lx = lt + " " if lt.startswith("\\") and lt[1:].isalpha() else lt
        stem = [text("จำนวนคำตอบของสมการ"), content_math(rf"\tan({lx}x) = \tan({lt}\pi)"), text("สำหรับ"),
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


from otk.core.provenance import Provenance  # noqa: E402
from otk.core.registry import QuestionType, question_type  # noqa: E402
from otk.kit.math_problems import MathType  # noqa: E402
from otk.sets._support.math_m5 import M5 as LEVEL  # noqa: E402


def _nz5(rng: Random, lo: int, hi: int) -> int:
    return rng.choice((1, -1)) * rng.randint(lo, hi)


def _tk5(*values: str, answer: str) -> list[str]:
    """Distinct TeX distractors, the answer left out."""
    return [v for v in dict.fromkeys(values) if v != answer]


def _fk5(*values, answer: Fraction) -> list[str]:
    """Distinct fraction distractors as TeX, the answer left out."""
    return _tk5(*(frac_tex(Fraction(v)) for v in values), answer=frac_tex(answer))


def _pt5(x, y) -> str:
    return f"({frac_tex(Fraction(x))}, {frac_tex(Fraction(y))})"


def _nk5(*values: int, answer: int, lo: int | None = None) -> list[str]:
    """Distinct whole-number distractors, the answer (and values below lo) left out."""
    return _tk5(*(str(v) for v in values if lo is None or v >= lo), answer=str(answer))


def _g5(n: int) -> str:
    """A whole number in TeX with grouped thousands."""
    return f"{n:,}".replace(",", "{,}")


def _gk5(*values: int, answer: int, lo: int = 1) -> list[str]:
    return _tk5(*(_g5(int(v)) for v in values if v >= lo), answer=_g5(answer))


def _deg5(*angles: int) -> str:
    return "x = " + ", ".join(f"{a}^{{\\circ}}" for a in angles)

# ── More trigonometric equations (2026-11): sin x = 1/2, cos x = −1/2, tan x = −1, how many solutions of
# sin²x = 1/4, 2cos x + √3 = 0, and the sum of two solutions ──


@question_type("math.sin_equals_value_m5", display_name={"th": "แก้สมการ sin x = ค่าพิเศษ"}, level=LEVEL, topic="สมการตรีโกณมิติ")
class SinEqualsValueM5(MathType):
    _CASES = ((r"\frac{1}{2}", 30), (r"\frac{\sqrt{3}}{2}", 60), (r"\frac{\sqrt{2}}{2}", 45),
              (r"-\frac{1}{2}", -30), (r"-\frac{\sqrt{3}}{2}", -60))

    def expr(self, rng: Random):
        value, a = rng.choice(self._CASES)
        sols = sorted({(a) % 360, (180 - a) % 360})
        right = _deg5(*sols)
        wrongs = [_deg5(*sorted({abs(a), 360 - abs(a)})), _deg5(sols[0]), _deg5(*sorted({(90 - a) % 360, (90 + a) % 360})),
                  _deg5(*sorted({(a + 180) % 360, (360 - a) % 360}))]
        return MathDraw(rf"\sin x = {value} \quad (0^{{\circ}} \le x < 360^{{\circ}})", right, prompt="จงแก้สมการ",
                        distractors=_tk5(*wrongs, answer=right)[:3])


@question_type("math.cos_equals_value_m5", display_name={"th": "แก้สมการ cos x = ค่าพิเศษ"}, level=LEVEL, topic="สมการตรีโกณมิติ")
class CosEqualsValueM5(MathType):
    _CASES = ((r"-\frac{1}{2}", 120), (r"\frac{1}{2}", 60), (r"-\frac{\sqrt{3}}{2}", 150), (r"\frac{\sqrt{2}}{2}", 45),
              (r"-\frac{\sqrt{2}}{2}", 135))

    def expr(self, rng: Random):
        value, a = rng.choice(self._CASES)
        right = _deg5(a, 360 - a)
        wrongs = [_deg5(a, 180 - a) if a != 90 else _deg5(a), _deg5(a), _deg5(180 - a, 180 + a)]
        return MathDraw(rf"\cos x = {value} \quad (0^{{\circ}} \le x < 360^{{\circ}})", right, prompt="จงแก้สมการ",
                        distractors=_tk5(*wrongs, _deg5(360 - a), answer=right)[:3])


@question_type("math.tan_equals_value_m5", display_name={"th": "แก้สมการ tan x = ค่าพิเศษ"}, level=LEVEL, topic="สมการตรีโกณมิติ")
class TanEqualsValueM5(MathType):
    _CASES = (("-1", 135), ("1", 45), (r"\sqrt{3}", 60), (r"-\sqrt{3}", 120), (r"\frac{\sqrt{3}}{3}", 30))

    def expr(self, rng: Random):
        value, a = rng.choice(self._CASES)
        right = _deg5(a, a + 180)
        wrongs = [_deg5(a, 360 - a), _deg5(a), _deg5(a, 180 - a)]
        return MathDraw(rf"\tan x = {value} \quad (0^{{\circ}} \le x < 360^{{\circ}})", right, prompt="จงแก้สมการ",
                        distractors=_tk5(*wrongs, answer=right))


@question_type("math.sin_squared_count_m5", display_name={"th": "นับคำตอบของสมการ sin²x = k"}, level=LEVEL, topic="สมการตรีโกณมิติ")
class SinSquaredCountM5(MathType):
    _CASES = ((r"\frac{1}{4}", 4), (r"\frac{3}{4}", 4), (r"\frac{1}{2}", 4), ("1", 2), ("0", 2))

    def expr(self, rng: Random):
        value, right = rng.choice(self._CASES)
        fn = rng.choice(("sin", "cos"))
        # Only the positive roots; twice too many; one.
        return MathDraw(rf"\{fn}^{{2}} x = {value} \quad (0^{{\circ}} \le x < 360^{{\circ}})", str(right),
                        prompt="สมการนี้มีคำตอบกี่คำตอบ", distractors=_nk5(right // 2, right * 2, 1, 3, answer=right, lo=1))


@question_type("math.two_cos_plus_root3_m5", display_name={"th": "แก้สมการ a cos x + b = 0"}, level=LEVEL, topic="สมการตรีโกณมิติ")
class TwoCosPlusRoot3M5(MathType):
    _CASES = ((r"2\cos x + \sqrt{3} = 0", (150, 210)), (r"2\cos x - 1 = 0", (60, 300)),
              (r"2\sin x - \sqrt{3} = 0", (60, 120)), (r"2\sin x + 1 = 0", (210, 330)), (r"\sqrt{2}\cos x - 1 = 0", (45, 315)))

    def expr(self, rng: Random):
        eq, sols = rng.choice(self._CASES)
        right = _deg5(*sols)
        a, b = sols
        wrongs = [_deg5(180 - a, 180 + a) if 180 - a >= 0 else _deg5(a + 90, b + 90), _deg5(a), _deg5((a + 180) % 360, (b + 180) % 360)]
        return MathDraw(rf"{eq} \quad (0^{{\circ}} \le x < 360^{{\circ}})", right, prompt="จงแก้สมการ",
                        distractors=_tk5(*wrongs, _deg5(a, b + 10), answer=right)[:3])


@question_type("math.sum_of_two_solutions_m5", display_name={"th": "ผลบวกของคำตอบของสมการตรีโกณมิติ"}, level=LEVEL,
               topic="สมการตรีโกณมิติ")
class SumOfTwoSolutionsM5(MathType):
    def expr(self, rng: Random):
        fn = rng.choice(("sin", "cos"))
        k = rng.choice((r"\frac{1}{3}", r"\frac{2}{5}", r"\frac{3}{4}", "0.6"))
        right = 180 if fn == "sin" else 360
        return MathDraw(rf"\{fn} x = {k} \quad (0^{{\circ}} \le x < 360^{{\circ}})", f"{right}^{{\\circ}}",
                        prompt="ผลบวกของคำตอบทั้งหมดของสมการนี้เท่ากับกี่องศา",
                        distractors=_tk5(f"{540 - right}^{{\\circ}}", "90^{\\circ}", "720^{\\circ}", answer=f"{right}^{{\\circ}}"))


SinEqualsValueM5.PROVENANCE = Provenance("original")
CosEqualsValueM5.PROVENANCE = Provenance("original")
TanEqualsValueM5.PROVENANCE = Provenance("original")
SinSquaredCountM5.PROVENANCE = Provenance("original")
TwoCosPlusRoot3M5.PROVENANCE = Provenance("original")
SumOfTwoSolutionsM5.PROVENANCE = Provenance("original")
