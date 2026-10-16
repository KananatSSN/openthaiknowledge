"""อนุกรม

คณิตศาสตร์ · ม.6 · สสวท. เพิ่มเติม
Indicators: ค เพิ่มเติม จำนวนและพีชคณิต 2 ม.6/3

Sets moved here from: math, math_apply_stage, math_bank_notes, math_bank_sequences, math_calculus.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.content import math as content_math
from otk.core.content import text
from otk.core.mistakes import named
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.math_problems import (
    ChoiceType,
    MathDraw,
    MathType,
    WordProblem,
    frac_answer_tex,
    frac_tex,
)
from otk.sets._support.math_apply_stage import _nums
from otk.sets._support.math_bank_notes import M6, _q
from otk.sets._support.math_bank_sequences import M6 as M6_math_bank_sequences
from otk.sets._support.math_bank_sequences import _num_q, _tex_q, num
from otk.sets._support.math_m4 import maths
from otk.sets._support.math_p2 import _maths


def s1(n: int) -> int:
    return n * (n + 1) // 2


def s2(n: int) -> int:
    return n * (n + 1) * (2 * n + 1) // 6


def s3(n: int) -> int:
    return s1(n) ** 2


def poly_sum(a: int, b: int, c: int, lo: int, hi: int) -> int:
    """Σ_{k=lo}^{hi} (ak² + bk + c)."""
    total = lambda n: a * s2(n) + b * s1(n) + c * n
    return total(hi) - total(lo - 1)


def _poly_tex(a: int, b: int, c: int) -> str:
    out = ""
    for coef, body in ((a, "k^{2}"), (b, "k"), (c, "")):
        if not coef:
            continue
        mag = str(abs(coef)) if abs(coef) != 1 or not body else ""
        if not out:
            out = ("-" if coef < 0 else "") + mag + body
        else:
            out += f" {'-' if coef < 0 else '+'} {mag}{body}"
    return out


SERIES = "อนุกรม"


def telescoping_infinite(c: int, p: int, k: int) -> Fraction:
    """Σₙ₌₁^∞ c/((n + p)(n + p + k)) = (c/k)(1/(1 + p) + ⋯ + 1/(k + p))."""
    return Fraction(c, k) * sum(Fraction(1, i + p) for i in range(1, k + 1))


def fibonacci_like_sum(a1: int, a2: int) -> Fraction:
    """Σₙ₌₂^∞ aₙ/(aₙ₋₁aₙ₊₁) with aₙ₊₁ = aₙ + aₙ₋₁: terms are 1/aₙ₋₁ − 1/aₙ₊₁, leaving 1/a₁ + 1/a₂."""
    return Fraction(1, a1) + Fraction(1, a2)


def median_of_reciprocals(m: int) -> Fraction:
    """Median of 1/(n(n + 1)), n = 1, …, m (m even)."""
    lo, hi = m // 2, m // 2 + 1
    return (Fraction(1, lo * (lo + 1)) + Fraction(1, hi * (hi + 1))) / 2


def weighted_power_sum_parts(n: int) -> tuple[int, int, int]:
    """Σₖ₌₁ⁿ k·2ᵏ = (n − 1)·2ⁿ⁺¹ + 2, returned as (n − 1, n + 1, 2)."""
    return n - 1, n + 1, 2


@question_type("math.series_converges", display_name={"th": "อนุกรมเรขาคณิตลู่เข้าหรือไม่"},
               level={"th": "ม.6"}, topic="อนุกรม")
class SeriesConverges(ChoiceType):
    def compose(self, rng: Random):
        p, q = rng.randint(1, 9), rng.randint(1, 9)
        converges = rng.random() < 0.5
        if converges and p >= q:
            p, q = q, p + q
        if not converges and p <= q:
            p, q = p + q, q
        r = Fraction(p, q)                        # reduced by Fraction itself
        stem = (f"อนุกรมเรขาคณิตที่มีอัตราส่วนร่วม r = "
                f"{r.numerator}/{r.denominator} มีลักษณะอย่างไร")
        if abs(r) < 1:
            return stem, "ลู่เข้า", ["ลู่ออก", "ลู่เข้าสู่ศูนย์เสมอ",
                                     "ตัดสินไม่ได้"]
        return stem, "ลู่ออก", ["ลู่เข้า", "ลู่เข้าสู่ศูนย์เสมอ",
                                "ตัดสินไม่ได้"]
SeriesConverges.PROVENANCE = Provenance("original")


@question_type("math.infinite_geometric_series",
               display_name={"th": "ผลบวกอนุกรมเรขาคณิตอนันต์"}, level={"th": "ม.6"},
               topic="อนุกรม")
class InfiniteGeometricSeries(WordProblem):
    def expr(self, rng: Random):
        a1 = rng.randint(1, 10)
        r = rng.choice([Fraction(1, 2), Fraction(1, 3), Fraction(2, 3)])
        total = Fraction(a1) / (1 - r)
        first = [frac_tex(a1 * r ** i) for i in range(3)]
        tex, prompt = rng.choice((
            # A plain-text prompt cannot typeset a fraction, so r is written as n/d.
            ("", f"ผลบวกอนุกรมเรขาคณิตอนันต์ a₁ = {a1}, r = {r.numerator}/{r.denominator} เท่ากับเท่าใด?"),
            (" + ".join(first) + r" + \cdots", "จงหาผลบวกของอนุกรมเรขาคณิตอนันต์"),
            (rf"a_1 = {first[0]},\ a_2 = {first[1]}",
             "อนุกรมเรขาคณิตอนันต์มีพจน์แรกและพจน์ที่สองดังนี้ ผลบวกของอนุกรมเท่ากับเท่าใด"),
        ))
        return MathDraw(
            tex, frac_answer_tex(total), prompt=prompt,
            distractors=[frac_answer_tex(Fraction(a1) / (1 + r)),
                         frac_answer_tex(Fraction(a1) * (1 - r)),
                         frac_answer_tex(Fraction(a1) / r)])
InfiniteGeometricSeries.PROVENANCE = Provenance("original")


@question_type("math.infinite_series_word_m6", display_name={"th": "โจทย์ปัญหาอนุกรมเรขาคณิตอนันต์"},
               level={"th": "ม.6"}, topic="อนุกรม")
class InfiniteSeriesWordM6(QuestionType):
    def build(self, rng: Random, **params) -> GeneratedQuestion:
        kind = rng.randrange(3)
        if kind == 0:
            p, q = rng.choice(((1, 2), (1, 3), (2, 3), (3, 4), (1, 4), (2, 5), (3, 5)))
            r = Fraction(p, q)
            h = q * (q - p) * rng.randint(1, 3)
            total = h + 2 * h * r / (1 - r)
            stem = (f"ปล่อยลูกบอลจากความสูง {h} เมตร ทุกครั้งที่ตกกระทบพื้นลูกบอลกระดอนขึ้นไปสูง {p}/{q} "
                    f"ของความสูงก่อนหน้า ถ้ากระดอนไปเรื่อย ๆ ไม่สิ้นสุด ลูกบอลเคลื่อนที่ได้ระยะทางทั้งหมดกี่เมตร")
            wrongs = [h / (1 - r), h + h * r / (1 - r), 2 * h / (1 - r)]
            return maths([text(stem)], frac_tex(total), [frac_tex(w) for w in wrongs if w != total], self.topic)
        if kind == 1:
            s = rng.randint(2, 12)
            stem = (f"รูปสี่เหลี่ยมจัตุรัสรูปแรกยาวด้านละ {s} เซนติเมตร ลากส่วนของเส้นตรงเชื่อมจุดกึ่งกลางของด้าน "
                    f"ได้รูปสี่เหลี่ยมจัตุรัสรูปใหม่ ทำเช่นนี้ไปเรื่อย ๆ ไม่สิ้นสุด ผลรวมพื้นที่ของรูปทั้งหมดเป็นกี่ตารางเซนติเมตร")
            return maths([text(stem)], str(2 * s * s), _nums(2 * s * s, s * s, 4 * s * s, s * s * 3 // 2, lo=1),
                         self.topic)
        d = rng.choice((2, 4, 6, 8, 10, 12))
        stem = (f"เดินไปยังจุดหมายที่อยู่ห่าง {d} กิโลเมตร นาทีแรกเดินได้ครึ่งหนึ่งของระยะทาง "
                f"แต่ละนาทีต่อมาเดินได้ครึ่งหนึ่งของระยะทางที่เหลือ ถ้าเดินไปเรื่อย ๆ ไม่สิ้นสุด "
                f"ผลรวมระยะทางที่เดินได้เข้าใกล้กี่กิโลเมตร")
        return maths([text(stem)], str(d), _nums(d, d // 2, 2 * d, d - 1, lo=1), self.topic)
InfiniteSeriesWordM6.PROVENANCE = Provenance("original")


@question_type("math.sigma_sums_m6",
               display_name={"th": "สัญลักษณ์ซิกมาและสูตรผลบวก"},
               level=M6, topic="อนุกรม")
class SigmaSumsM6(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        kind = rng.randrange(3)
        if kind == 0:
            a, b, c = rng.randint(1, 4), rng.randint(-5, 6), rng.randint(-4, 6)
            n = rng.randint(5, 20)
            right = poly_sum(a, b, c, 1, n)
            stem = [text("ค่าของ"), content_math(rf"\sum_{{k=1}}^{{{n}}} \left({_poly_tex(a, b, c)}\right)"),
                    text("เท่ากับเท่าใด")]
            # c added once, not n times; Σk² taken as (Σk)²; Σk² taken as n².
            named = [a * s2(n) + b * s1(n) + c, a * s1(n) ** 2 + b * s1(n) + c * n, a * n * n + b * s1(n) + c * n]
            return _q(stem, right, named, self.topic)
        if kind == 1:
            lo, hi = rng.randint(3, 10), rng.randint(15, 30)
            square = rng.random() < 0.5
            right = (s2(hi) - s2(lo - 1)) if square else (s1(hi) - s1(lo - 1))
            f = s2 if square else s1
            term = "k^{2}" if square else "k"
            stem = [text("ค่าของ"), content_math(rf"\sum_{{k={lo}}}^{{{hi}}} {term}"), text("เท่ากับเท่าใด")]
            # Subtracting up to lo instead of lo − 1; starting from 1; one term too few.
            return _q(stem, right, [f(hi) - f(lo), f(hi), f(hi - 1) - f(lo - 1)], self.topic)
        n = rng.randint(5, 20)
        form = rng.choice(("k(k+1)", "k^{3}", "(2k-1)"))
        right = {"k(k+1)": s2(n) + s1(n), "k^{3}": s3(n), "(2k-1)": n * n}[form]
        stem = [text("ค่าของ"), content_math(rf"\sum_{{k=1}}^{{{n}}} {form}"), text("เท่ากับเท่าใด")]
        # Σk·Σ(k+1); Σk² for Σk³; 2Σk − 1.
        named = {"k(k+1)": [s1(n) * (s1(n) + n), s2(n), s2(n) + n],
                 "k^{3}": [s2(n), s1(n) * n, s1(n) ** 2 - n],
                 "(2k-1)": [2 * s1(n) - 1, n * n - 1, s1(n)]}[form]
        return _q(stem, right, named, self.topic)
SigmaSumsM6.PROVENANCE = Provenance("original")


@question_type("math.telescoping_series_m6",
               display_name={"th": "อนุกรมที่ตัดกันเป็นทอด ๆ"},
               level=M6_math_bank_sequences, topic=SERIES)
class TelescopingSeriesM6(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        kind = rng.randrange(4)
        if kind == 0:
            c, p, k = rng.choice((1, 2, 3, 4, 6)), rng.randint(0, 3), rng.randint(1, 3)
            den = ("n" if not p else f"(n + {p})") + f"(n + {p + k})"
            stem = [text("ค่าของ"), content_math(rf"\sum_{{n=1}}^{{\infty}} \frac{{{c}}}{{{den}}}"),
                    text("เท่ากับเท่าใด")]
            right = telescoping_infinite(c, p, k)
            # Forgetting to divide by k; only the first leftover term; the sum started one term late.
            named = [right * k, Fraction(c, k * (1 + p)), telescoping_infinite(c, p + 1, k)]
            return _num_q(stem, right, named, self.topic)
        if kind == 1:
            a1, a2 = rng.randint(1, 4), rng.randint(2, 7)
            stem = [text("ให้ aₙ เป็นลำดับซึ่ง"), content_math(f"a_{{1}} = {a1},\\ a_{{2}} = {a2}"), text("และ"),
                    content_math(r"a_{n+1} = a_{n} + a_{n-1}"), text("เมื่อ n = 2, 3, 4, … ค่าของ"),
                    content_math(r"\sum_{n=2}^{\infty} \frac{a_{n}}{a_{n-1} a_{n+1}}"), text("เท่ากับเท่าใด")]
            # Only 1/a₁; 1/a₁ − 1/a₂; 1/(a₁a₂).
            return _num_q(stem, fibonacci_like_sum(a1, a2),
                          [Fraction(1, a1), Fraction(1, a1) - Fraction(1, a2), Fraction(1, a1 * a2)], self.topic)
        if kind == 2:
            m = 2 * rng.randint(4, 15)
            med = median_of_reciprocals(m)
            stem = [text("กำหนดให้ a₁, a₂, …, aₘ เป็นข้อมูล โดยที่"), content_math(r"a_{n} = \frac{1}{n(n+1)}"),
                    text("เมื่อ n = 1, 2, …, m ถ้าข้อมูลชุดนี้มีมัธยฐานเท่ากับ"), content_math(num(med)),
                    text("แล้วค่าเฉลี่ยเลขคณิตของข้อมูลชุดนี้เท่ากับเท่าใด")]
            # 1/m; 1/(m + 2); the median itself.
            return _num_q(stem, Fraction(1, m + 1), [Fraction(1, m), Fraction(1, m + 2), med], self.topic)
        n = rng.choice((20, 50, 99, 100))
        a, e, c = weighted_power_sum_parts(n)
        stem = [text("ค่าของ"), content_math(rf"\sum_{{k=1}}^{{{n}}} k \cdot 2^{{k}}"), text("เท่ากับเท่าใด")]
        right = rf"{a} \cdot 2^{{{e}}} + {c}"
        wrongs = [rf"{n} \cdot 2^{{{e}}} + {c}", rf"{a} \cdot 2^{{{n}}} + {c}", rf"{a} \cdot 2^{{{e}}} - {c}",
                  rf"{n} \cdot 2^{{{n}}}"]
        return _tex_q(stem, right, wrongs, self.topic)
TelescopingSeriesM6.PROVENANCE = Provenance("adapted", sources=('openthaiknowledge-bank/rathcenter/14 ลำดับและอนุกรม',))


@question_type("math.repeating_decimal_to_fraction",
               display_name={"th": "ทศนิยมซ้ำเป็นเศษส่วน"},
               level={"th": "ม.6"}, topic="อนุกรม")
class RepeatingDecimalToFraction(MathType):
    """0.ddd… is a geometric series with r = 1/10 — the reason every repeating
    decimal is rational."""

    def expr(self, rng: Random, digit_lo: int = 1, digit_hi: int = 8):
        kind = rng.randrange(3)
        if kind == 0:
            d = rng.randint(digit_lo, digit_hi)
            value, shown = Fraction(d, 9), rf"0.\overline{{{d}}}"
            wrongs = [Fraction(d, 10), Fraction(d, 99), Fraction(d, 11)]
        elif kind == 1:
            # Two repeating digits: a series with r = 1/100.
            ab = rng.choice([n for n in range(10, 99) if n % 11])
            value, shown = Fraction(ab, 99), rf"0.\overline{{{ab}}}"
            wrongs = [Fraction(ab, 100), Fraction(ab, 90), Fraction(ab, 9)]
        else:
            # One digit before the repeat: a/10 plus a series starting at b/100.
            a, b = rng.randint(1, 8), rng.randint(1, 9)
            while a == b:
                b = rng.randint(1, 9)
            value, shown = Fraction(10 * a + b - a, 90), rf"0.{a}\overline{{{b}}}"
            wrongs = [Fraction(10 * a + b, 99), Fraction(10 * a + b, 90), Fraction(10 * a + b - a, 99)]
        return MathDraw(
            shown, frac_tex(value), prompt="จงเขียนทศนิยมซ้ำนี้ในรูปเศษส่วน",
            distractors=[frac_tex(w) for w in dict.fromkeys(wrongs) if w != value])
RepeatingDecimalToFraction.PROVENANCE = Provenance("original")


@question_type("math.alternating_geometric_sum_m6",
               display_name={"th": "ผลบวกอนุกรมเรขาคณิตสลับเครื่องหมาย"},
               level=M6, topic=SERIES)
class AlternatingGeometricSumM6(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        p = rng.randint(1, 8)
        q = rng.randint(p + 1, p + 8)
        a = rng.randint(2, 18)
        r = Fraction(p, q)
        answer = Fraction(a, 1 + r)
        wrongs = [
            named("series.ignored_alternation", frac_tex(Fraction(a, 1 - r))),
            named("series.used_first_term_only", str(a)),
            named("series.reversed_first_term_sign", frac_tex(-answer)),
        ]
        return _maths([text("จงหาผลบวกของอนุกรมอนันต์"),
                       content_math(rf"\sum_{{n=0}}^{{\infty}} {a}\left(-\frac{{{p}}}{{{q}}}\right)^n")],
                      frac_tex(answer), wrongs, self.topic)
AlternatingGeometricSumM6.PROVENANCE = Provenance("original")


@question_type("math.finite_telescoping_fraction_m6",
               display_name={"th": "ผลบวกอนุกรมตัดกันเป็นทอด ๆ แบบจำกัด"},
               level=M6, topic=SERIES)
class FiniteTelescopingFractionM6(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        c, n = rng.randint(2, 18), rng.randint(5, 40)
        answer = Fraction(c * n, n + 1)
        wrongs = [
            named("series.used_infinite_sum", str(c)),
            named("series.used_tail_only", frac_tex(Fraction(c, n + 1))),
            named("series.reversed_telescoping_fraction", frac_tex(Fraction(c * (n + 1), n))),
        ]
        return _maths([text("จงหาผลบวก"),
                       content_math(rf"\sum_{{k=1}}^{{{n}}}\frac{{{c}}}{{k(k+1)}}")],
                      frac_tex(answer), wrongs, self.topic)
FiniteTelescopingFractionM6.PROVENANCE = Provenance("original")


@question_type("math.weighted_geometric_infinite_m6",
               display_name={"th": "ผลบวกอนุกรมเรขาคณิตถ่วงน้ำหนักด้วยลำดับพจน์"},
               level=M6, topic=SERIES)
class WeightedGeometricInfiniteM6(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        while True:
            p = rng.randint(1, 8)
            q = rng.randint(p + 1, p + 9)
            a = rng.randint(2, 18)
            r = Fraction(p, q)
            answer = Fraction(a, (1 - r) ** 2)
            candidates = (
                frac_tex(Fraction(a, 1 - r)),
                frac_tex(Fraction(a * r, (1 - r) ** 2)),
                frac_tex(Fraction(a, (1 + r) ** 2)),
            )
            if len({frac_tex(answer), *candidates}) == 4:
                break
        wrongs = [named(key, value) for key, value in zip((
            "series.forgot_term_weight", "series.shifted_weight_index",
            "series.used_plus_ratio"), candidates)]
        return _maths([text("จงหาผลบวกของอนุกรมอนันต์"),
                       content_math(rf"\sum_{{n=1}}^{{\infty}} {a}n\left(\frac{{{p}}}{{{q}}}\right)^{{n-1}}")],
                      frac_tex(answer), wrongs, self.topic)
WeightedGeometricInfiniteM6.PROVENANCE = Provenance("original")
