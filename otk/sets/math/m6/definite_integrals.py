"""อินทิกรัลจำกัดเขต

คณิตศาสตร์ · ม.6 · สสวท. เพิ่มเติม
Indicators: ค เพิ่มเติม แคลคูลัส 1 ม.6/3

Sets moved here from: math, math_apply_add, math_thin_topics.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.content import math as content_math
from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, MathType, WordProblem, poly_tex
from otk.sets._support.math_apply_add import M6, _c, _fr
from otk.sets._support.math_m4 import maths as _num_maths
from otk.sets._support.math_thin_topics import M5

PROVENANCE = Provenance("original")


@question_type("math.integral_properties_m5", display_name={"th": "สมบัติของอินทิกรัลจำกัดเขต"},
               level=M5, topic="อินทิกรัลจำกัดเขต")
class IntegralPropertiesM5(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        a = rng.randint(-2, 2)
        b = a + rng.randint(1, 3)
        c = b + rng.randint(1, 3)
        P, Q = rng.choice([v for v in range(-9, 13) if v]), rng.choice([v for v in range(-9, 13) if v])
        given = [text("กำหนดให้"), content_math(rf"\int_{{{a}}}^{{{b}}} f(x)\,dx = {P},\quad "
                                                   rf"\int_{{{b}}}^{{{c}}} f(x)\,dx = {Q}")]
        kind = rng.randrange(3)
        if kind == 0:
            ask, ans, wrongs = rf"\int_{{{a}}}^{{{c}}} f(x)\,dx", P + Q, [P - Q, Q - P, P * Q]
        elif kind == 1:
            ask, ans, wrongs = rf"\int_{{{b}}}^{{{a}}} f(x)\,dx", -P, [P, Q, -Q]
        else:
            k, m = rng.randint(2, 4), rng.randint(1, 5)
            ask = rf"\int_{{{a}}}^{{{b}}} \left({k}f(x) + {m}\right)dx"
            # The constant integrated as m instead of m(b − a).
            ans, wrongs = k * P + m * (b - a), [k * P + m, k * (P + m), P + m * (b - a)]
        return _num_maths(given + [text("จงหาค่าของ"), content_math(ask)], str(ans),
                          [str(w) for w in wrongs], self.topic)


@question_type("math.definite_integral",
               display_name={"th": "อินทิกรัลจำกัดเขต"}, level={"th": "ม.5"},
               topic="อินทิกรัลจำกัดเขต")
class DefiniteIntegral(MathType):
    def expr(self, rng: Random):
        k = rng.randint(1, 3)
        m = rng.randint(-3, 3)
        c = rng.randint(-4, 4)
        a = rng.randint(-2, 1)
        b = a + rng.randint(1, 3)
        F = lambda x: k * x ** 3 + m * x * x + c * x
        integrand = poly_tex((3 * k, "x^{2}"), (2 * m, "x"), (c, ""))
        return MathDraw(rf"\int_{{{a}}}^{{{b}}} ({integrand}) \, dx",
                        rf"{F(b) - F(a)}", prompt="จงหาค่า")


@question_type("math.integral_accumulation_m6",
               display_name={"th": "โจทย์ปัญหาปริพันธ์: ระยะทางรวม ปริมาณสะสม"},
               level=M6, topic="อินทิกรัลจำกัดเขต")
class IntegralAccumulationM6(WordProblem):
    def expr(self, rng: Random):
        kind = rng.randrange(5)
        if kind in (0, 1):
            p, q = rng.choice(((1, 2), (1, 3), (2, 3), (1, 4), (2, 4)))
            T = q + rng.choice((1, 2))

            def pos(t):                                # ∫ 6(t - p)(t - q) dt
                return 2 * t ** 3 - 3 * (p + q) * t ** 2 + 6 * p * q * t

            disp = pos(T) - pos(0)
            dist = abs(pos(p) - pos(0)) + abs(pos(q) - pos(p)) + abs(pos(T) - pos(q))
            v = f"6t² - {6 * (p + q)}t + {6 * p * q}"
            if kind == 0:
                return MathDraw("", str(dist),
                                prompt=(f"อนุภาคเคลื่อนที่ในแนวเส้นตรงด้วยความเร็ว v(t) = {v} เมตรต่อวินาที "
                                        f"ตั้งแต่ t = 0 ถึง t = {T} วินาที อนุภาคเคลื่อนที่ได้ระยะทางทั้งหมดกี่เมตร"),
                                distractors=_story.keep(abs(disp), dist - abs(pos(q) - pos(p)),
                                                        dist + abs(pos(q) - pos(p)), answer=dist, lo=1))
            return MathDraw("", str(disp),
                            prompt=(f"อนุภาคเคลื่อนที่ในแนวเส้นตรงด้วยความเร็ว v(t) = {v} เมตรต่อวินาที "
                                    f"การกระจัดของอนุภาคตั้งแต่ t = 0 ถึง t = {T} วินาที เป็นกี่เมตร"),
                            distractors=_story.keep(dist, -disp, disp + 2 * abs(pos(q) - pos(p)),
                                                    answer=disp, lo=-10 ** 6))
        if kind == 2:
            a, b, T, V0 = 2 * rng.randint(1, 5), rng.randint(3, 20), rng.randint(5, 20), rng.choice((0, 50, 100, 200))
            vol = V0 + a * T * T // 2 + b * T
            start = f"ถังมีน้ำอยู่ {V0} ลิตร เปิดน้ำเข้าถัง" if V0 else "เปิดน้ำเข้าถังเปล่า"
            return MathDraw("", _c(vol),
                            prompt=(f"{start}ในอัตรา r(t) = {a}t + {b} ลิตรต่อนาที "
                                    f"เมื่อเวลาผ่านไป {T} นาที ถังมีน้ำกี่ลิตร"),
                            # the rate at T taken as the amount; forgetting the ½; forgetting V0
                            distractors=[_c(V0 + a * T + b), _c(V0 + a * T * T + b * T),
                                         _c(vol - V0 if V0 else vol + b)])
        if kind == 3:
            d = rng.choice((2, 4, 5))
            c = d * rng.randint(3, 10)
            total = Fraction(c * c, 2 * d)
            return MathDraw("", _fr(total),
                            prompt=(f"น้ำมันรั่วจากถังในอัตรา r(t) = {c} - {d}t ลิตรต่อชั่วโมง จนกระทั่งหยุดรั่ว "
                                    f"มีน้ำมันรั่วออกทั้งหมดกี่ลิตร"),
                            distractors=[_fr(Fraction(c * c, d)), _fr(Fraction(c, d)), _fr(Fraction(c * c, 4 * d))])
        v0, a = rng.choice(((20, 4), (30, 5), (24, 6), (40, 8), (36, 4), (30, 6)))
        return MathDraw("", _fr(Fraction(v0 * v0, 2 * a)),
                        prompt=(f"รถเบรกเมื่อ t = 0 ความเร็วขณะเบรกคือ v(t) = {v0} - {a}t เมตรต่อวินาที "
                                f"จนรถหยุด รถเคลื่อนที่ได้ระยะทางกี่เมตรตั้งแต่เริ่มเบรก"),
                        distractors=[_fr(Fraction(v0 * v0, a)), _fr(Fraction(v0, a)), _fr(Fraction(v0 * v0, 4 * a))])


@question_type("math.integral_distance_m5", display_name={"th": "ระยะทางจากความเร็ว (อินทิกรัลจำกัดเขต)"},
               level=M5, topic="อินทิกรัลจำกัดเขต")
class IntegralDistanceM5(WordProblem):
    def expr(self, rng: Random):
        T = rng.randint(2, 10)
        if rng.random() < 0.5:
            a, b = 2 * rng.randint(1, 5), rng.randint(1, 20)
            dist = a * T * T // 2 + b * T
            v = poly_tex((a, "t"), (b, ""))
            wrongs = [a * T + b, a * T * T + b * T, a * T // 2 + b]
        else:
            k, b = 3 * rng.randint(1, 3), rng.randint(0, 10)
            dist = k * T ** 3 // 3 + b * T
            v = poly_tex((k, "t^{2}"), (b, ""))
            wrongs = [k * T * T + b, k * T ** 3 + b * T, 2 * k * T]
        return MathDraw(rf"v(t) = {v}", str(dist),
                        prompt=(f"วัตถุเคลื่อนที่ในแนวตรงไปทางเดียว ในช่วงเวลา t = 0 ถึง t = {T} วินาที "
                                f"วัตถุเคลื่อนที่ได้ระยะทางกี่เมตร ถ้าความเร็ว v(t) เมตรต่อวินาที เป็นดังนี้"),
                        # The speed at T, the half forgotten, and a guess from v.
                        distractors=_story.keep(*wrongs, answer=dist, lo=1))


from otk.core.provenance import Provenance  # noqa: E402
from otk.core.registry import QuestionType, question_type  # noqa: E402
from otk.kit.math_problems import MathType, WordProblem  # noqa: E402
from otk.kit.math_problems import frac_tex  # noqa: E402
from otk.sets._support.math_m6 import M6 as LEVEL  # noqa: E402


def _nz6(rng: Random, lo: int, hi: int) -> int:
    return rng.choice((1, -1)) * rng.randint(lo, hi)


def _tk6(*values: str, answer: str) -> list[str]:
    """Distinct TeX distractors, the answer left out."""
    return [v for v in dict.fromkeys(values) if v != answer]


def _fk6(*values, answer: Fraction) -> list[str]:
    """Distinct fraction distractors as TeX, the answer left out."""
    return _tk6(*(frac_tex(Fraction(v)) for v in values), answer=frac_tex(answer))


def _pt6(x, y) -> str:
    return f"({frac_tex(Fraction(x))}, {frac_tex(Fraction(y))})"


def _nk6(*values: int, answer: int, lo: int | None = None) -> list[str]:
    """Distinct whole-number distractors, the answer (and values below lo) left out."""
    return _tk6(*(str(v) for v in values if lo is None or v >= lo), answer=str(answer))


def _num6(v) -> str:
    """A terminating decimal without trailing zeros: Fraction(25, 2) -> 12.5."""
    v = Fraction(v)
    sign = "-" if v < 0 else ""
    v = abs(v)
    whole, rem = divmod(v.numerator, v.denominator)
    if not rem:
        return f"{sign}{whole}"
    digits = ""
    for _ in range(6):
        rem *= 10
        d, rem = divmod(rem, v.denominator)
        digits += str(d)
        if not rem:
            break
    return f"{sign}{whole}.{digits.rstrip('0')}"


def _dk6(*values, answer) -> list[str]:
    """Distinct decimal distractors, the answer left out."""
    return _tk6(*(_num6(v) for v in values), answer=_num6(answer))

# ── More definite integrals (2026-11): a power from zero, a straight line, linearity, splitting the interval,
# an odd part over a symmetric interval, and the upper limit from the value ──


@question_type("math.integral_of_power_m6", display_name={"th": "อินทิกรัลจำกัดเขตของ xⁿ"}, level=LEVEL, topic="อินทิกรัลจำกัดเขต")
class IntegralOfPowerM6(MathType):
    def expr(self, rng: Random):
        n, a = rng.randint(1, 4), rng.randint(1, 4)
        right = Fraction(a ** (n + 1), n + 1)
        return MathDraw(rf"\int_{{0}}^{{{a}}} x^{{{n}}} \, dx", frac_tex(right), prompt="จงหาค่า",
                        distractors=_fk6(a ** (n + 1), Fraction(a ** n, n), n * a ** (n - 1), Fraction(a ** (n + 1), n), answer=right))


@question_type("math.integral_of_line_m6", display_name={"th": "อินทิกรัลจำกัดเขตของฟังก์ชันเชิงเส้น"}, level=LEVEL,
               topic="อินทิกรัลจำกัดเขต")
class IntegralOfLineM6(MathType):
    def expr(self, rng: Random):
        m, c = _nz6(rng, 1, 6), rng.randint(-9, 9)
        a, b = sorted(rng.sample(range(-3, 6), 2))
        right = Fraction(m, 2) * (b * b - a * a) + c * (b - a)
        return MathDraw(rf"\int_{{{a}}}^{{{b}}} ({poly_tex((m, 'x'), (c, ''))}) \, dx", frac_tex(right), prompt="จงหาค่า",
                        distractors=_fk6(m * (b * b - a * a) + c * (b - a), Fraction(m, 2) * (b * b - a * a), m * (b - a),
                                         right + (b - a), answer=right))


@question_type("math.integral_linearity_m6", display_name={"th": "สมบัติเชิงเส้นของอินทิกรัล"}, level=LEVEL, topic="อินทิกรัลจำกัดเขต")
class IntegralLinearityM6(MathType):
    def expr(self, rng: Random):
        a, b = sorted(rng.sample(range(0, 8), 2))
        k, p, q = rng.randint(-9, 9), rng.randint(2, 5), rng.randint(1, 6)
        right = p * k + q * (b - a)
        return MathDraw(rf"\int_{{{a}}}^{{{b}}} f(x) \, dx = {k}", str(right), prompt=f"จงหาค่าของ ∫ จาก {a} ถึง {b} ของ ({p}f(x) + {q}) dx",
                        distractors=_nk6(p * k + q, p * (k + q), k + q * (b - a), p * k, answer=right))


@question_type("math.integral_split_m6", display_name={"th": "แบ่งช่วงของอินทิกรัล"}, level=LEVEL, topic="อินทิกรัลจำกัดเขต")
class IntegralSplitM6(MathType):
    def expr(self, rng: Random):
        a, b, c = sorted(rng.sample(range(-5, 10), 3))
        p, q = rng.randint(-15, 15), rng.randint(-15, 15)
        right = q - p
        return MathDraw(rf"\int_{{{a}}}^{{{b}}} f(x) \, dx = {p}, \quad \int_{{{a}}}^{{{c}}} f(x) \, dx = {q}", str(right),
                        prompt=f"จงหาค่าของ ∫ จาก {b} ถึง {c} ของ f(x) dx", distractors=_nk6(p + q, p - q, q, right + 1, answer=right))


@question_type("math.symmetric_odd_integral_m6", display_name={"th": "อินทิกรัลบนช่วงสมมาตรที่มีส่วนเป็นฟังก์ชันคี่"}, level=LEVEL,
               topic="อินทิกรัลจำกัดเขต")
class SymmetricOddIntegralM6(MathType):
    def expr(self, rng: Random):
        a, b, c = rng.randint(1, 5), _nz6(rng, 1, 6), rng.randint(1, 9)
        right = 2 * a * c
        return MathDraw(rf"\int_{{-{a}}}^{{{a}}} ({poly_tex((b, 'x^{3}'), (c, ''))}) \, dx", str(right), prompt="จงหาค่า",
                        distractors=_nk6(0, a * c, 2 * a * c + b * a ** 4 // 2, 4 * a * c, answer=right))


@question_type("math.upper_limit_from_value_m6", display_name={"th": "หาขอบบนของอินทิกรัลจากค่าที่กำหนด"}, level=LEVEL,
               topic="อินทิกรัลจำกัดเขต")
class UpperLimitFromValueM6(MathType):
    def expr(self, rng: Random):
        k = rng.randint(2, 12)
        return MathDraw(rf"\int_{{0}}^{{k}} 2x \, dx = {k * k}, \quad k > 0", str(k), prompt="จงหาค่า k",
                        distractors=_nk6(k * k, 2 * k, k * k // 2, k + 1, answer=k, lo=1))
