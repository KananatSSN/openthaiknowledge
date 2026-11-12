"""ลำดับเรขาคณิต

คณิตศาสตร์ · ม.6 · สสวท. เพิ่มเติม
Indicators: ค เพิ่มเติม จำนวนและพีชคณิต 2 ม.6/2, ค เพิ่มเติม จำนวนและพีชคณิต 2 ม.6/4

Sets moved here from: math, math_apply_add, math_bank_sequences, math_calculus.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.content import math as content_math
from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.math_problems import MathDraw, MathType, WordProblem
from otk.sets._support.math_apply_add import M6, _c, _fr
from otk.sets._support.math_bank_sequences import M6 as M6_math_bank_sequences
from otk.sets._support.math_bank_sequences import _num_q, num

GEOMETRIC = "ลำดับเรขาคณิต"


def ratio_from_two_conditions(x: Fraction, y: Fraction) -> Fraction:
    """r when aₚ₊₂ − aₚ = x and aₚ₊₁ + aₚ = y: aₚ(r − 1)(r + 1) / aₚ(r + 1) = r − 1."""
    return 1 + x / y


def ratio_from_alternating(total: Fraction, alt: Fraction) -> Fraction:
    """r when a₁ + ⋯ + aₙ = total and a₁ − a₂ + ⋯ − aₙ = alt (n even): total/alt = (1 + r)/(1 − r)."""
    return (total - alt) / (total + alt)


def squares_from_sums(s: Fraction, t: Fraction) -> Fraction:
    """Σaₙ² from Σaₙ = a/(1 − r) = s and Σ(−1)ⁿaₙ = −a/(1 + r) = t: a²/(1 − r²) = −st."""
    return -s * t


def infinite_from_blocks(x: Fraction, t: Fraction) -> Fraction:
    """S∞ when S₅ = x and a₆ + ⋯ + a₁₅ = x·t(1 + t) with t = r⁵: x/(1 − t)."""
    return x / (1 - t)


@question_type("math.geometric_sequence",
               display_name={"th": "ลำดับเรขาคณิต"}, level={"th": "ม.6"},
               topic="ลำดับเรขาคณิต")
class GeometricSequence(MathType):
    def expr(self, rng: Random):
        a1 = rng.choice([1, -1]) * rng.randint(1, 5)
        r = rng.choice([2, 3, -2])
        n = rng.randint(5, 8 if abs(r) == 2 else 6)
        terms = ", ".join(str(a1 * r ** i) for i in range(4))
        return MathDraw(rf"{terms}, \ldots \quad a_{{{n}}}", rf"{a1 * r ** (n - 1)}",
                        hint=r"a_n = a_1 r^{n-1}")
GeometricSequence.PROVENANCE = Provenance("original")


@question_type("math.geometric_nth_term", display_name={"th": "พจน์ที่ n ของลำดับเรขาคณิต"},
               level={"th": "ม.6"}, topic="ลำดับเรขาคณิต")
class GeometricNthTerm(MathType):
    def expr(self, rng: Random, first_hi: int = 6, n_lo: int = 4, n_hi: int = 9):
        a1 = rng.randint(1, first_hi)
        r = rng.choice([-3, -2, 2, 3])
        n = rng.randint(n_lo, n_hi)
        value = a1 * r ** (n - 1)
        shown = ", ".join(str(a1 * r ** i) for i in range(4)) + r", \ldots"
        return MathDraw(
            shown, str(value), prompt=f"จงหาพจน์ที่ {n} ของลำดับนี้",
            hint=r"a_n = a_1 r^{n-1}",
            distractors=[str(a1 * r ** n), str(a1 * r ** (n - 2)),
                         str(a1 * (n - 1) * r)])
GeometricNthTerm.PROVENANCE = Provenance("original")


@question_type("math.geometric_series_word_m6",
               display_name={"th": "โจทย์ปัญหาอนุกรมเรขาคณิต (ลูกบอลกระดอน การส่งต่อ การออม)"},
               level=M6, topic="ลำดับเรขาคณิต")
class GeometricSeriesWordM6(WordProblem):
    def expr(self, rng: Random):
        kind = rng.randrange(5)
        if kind == 0:
            n = rng.randint(3, 5)
            H = 2 ** n * rng.choice((2, 3, 4, 5))
            ups = sum(Fraction(H, 2 ** i) for i in range(1, n))
            total = H + 2 * ups
            return MathDraw("", _fr(total),
                            prompt=(f"ปล่อยลูกบอลจากความสูง {H} เมตร ทุกครั้งที่ตกกระทบพื้นจะกระดอนขึ้นไปสูงครึ่งหนึ่ง"
                                    f"ของความสูงเดิม เมื่อลูกบอลตกกระทบพื้นครั้งที่ {n} ลูกบอลเคลื่อนที่ได้ทั้งหมดกี่เมตร"),
                            distractors=[_fr(H + ups), _fr(2 * H), _fr(H + 2 * ups + Fraction(H, 2 ** n) * 2)])
        if kind == 1:
            r, n = rng.choice((2, 3)), rng.randint(4, 6)
            total = r * (r ** n - 1) // (r - 1)
            return MathDraw("", _c(total),
                            prompt=(f"ข้อความหนึ่งถูกส่งต่อ รอบแรกส่งไปยังคน {r} คน แต่ละคนที่ได้รับส่งต่อให้คนใหม่อีก "
                                    f"{r} คนในรอบถัดไป เมื่อครบ {n} รอบ มีคนได้รับข้อความทั้งหมดกี่คน"),
                            distractors=[_c(r ** n), _c(r * n), _c(r ** (n + 1))])
        if kind == 2:
            a, n = rng.choice((10, 20, 50, 100)), rng.randint(5, 8)
            total = a * (2 ** n - 1)
            return MathDraw("", _c(total),
                            prompt=(f"ออมเงินเดือนแรก {a} บาท เดือนต่อ ๆ ไปออมเป็นสองเท่าของเดือนก่อน "
                                    f"เมื่อครบ {n} เดือน มีเงินออมทั้งหมดกี่บาท"),
                            distractors=[_c(a * 2 ** (n - 1)), _c(a * 2 ** n), _c(a * n * 2)])
        if kind == 3:
            num, den = rng.choice(((1, 2), (2, 3), (3, 4)))
            H = den * rng.randint(2, 8)
            total = H + 2 * Fraction(H * num, den) / (1 - Fraction(num, den))
            return MathDraw("", _fr(total),
                            prompt=(f"ทิ้งลูกบอลยางจากความสูง {H} เมตร ทุกครั้งที่กระทบพื้นจะกระดอนขึ้นไป "
                                    f"{num}/{den} ของความสูงเดิม ถ้าลูกบอลกระดอนไปเรื่อย ๆ จนหยุด "
                                    f"ลูกบอลเคลื่อนที่ได้ทั้งหมดกี่เมตร"),
                            distractors=[_fr(H / (1 - Fraction(num, den))), _fr(total - H),
                                         _fr(2 * H / (1 - Fraction(num, den)))])
        L = rng.choice((20, 30, 40, 50))
        num, den = rng.choice(((4, 5), (3, 4), (9, 10)))
        total = L / (1 - Fraction(num, den))
        return MathDraw("", _fr(total),
                        prompt=(f"ลูกตุ้มแกว่งครั้งแรกได้ระยะทาง {L} เซนติเมตร แต่ละครั้งต่อไปแกว่งได้ "
                                f"{num}/{den} ของระยะครั้งก่อน ถ้าแกว่งไปเรื่อย ๆ จนหยุด "
                                f"ลูกตุ้มแกว่งได้ระยะทางรวมกี่เซนติเมตร"),
                        distractors=[_fr(L * Fraction(num, den) / (1 - Fraction(num, den))),
                                     _fr(L * den), _fr(2 * total)])
GeometricSeriesWordM6.PROVENANCE = Provenance("original")


@question_type("math.geometric_series_tricks_m6",
               display_name={"th": "หาอัตราส่วนร่วมจากความสัมพันธ์ของพจน์และผลบวก"},
               level=M6_math_bank_sequences, topic=GEOMETRIC)
class GeometricSeriesTricksM6(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        kind = rng.randrange(5)
        given = text("กำหนดให้ a₁, a₂, a₃, … เป็นลำดับเรขาคณิต")
        if kind == 0:
            r = rng.choice((2, 3, 4, -2, -3))
            ap_ = Fraction(rng.randint(1, 9), rng.choice((1, 2, 4)))
            p = rng.randint(2, 8)
            x, y = ap_ * (r * r - 1), ap_ * (r + 1)
            stem = [given, text("ถ้า"), content_math(f"a_{{{p + 2}}} - a_{{{p}}} = {num(x)}"), text("และ"),
                    content_math(f"a_{{{p + 1}}} + a_{{{p}}} = {num(y)}"),
                    text("แล้วอัตราส่วนร่วมของลำดับนี้เท่ากับเท่าใด")]
            # x/y itself (r − 1); x/y − 1; −r.
            return _num_q(stem, ratio_from_two_conditions(x, y), [x / y, x / y - 1, -Fraction(r)], self.topic)
        if kind == 1:
            k = rng.randint(4, 9)
            j = rng.randint(1, k - 1)
            ak = rng.choice((-8, -6, -5, -4, 3, 5, 6, 7, 9))
            stem = [given, text("ถ้า"), content_math(f"a_{{{k}}} = {ak}"), text("แล้ว"),
                    content_math(rf"a_{{{k - j}}} \cdot a_{{{k + j}}}"), text("เท่ากับเท่าใด")]
            # The sign kept; 2aₖ; aₖ itself.
            return _num_q(stem, ak * ak, [-(ak * ak), 2 * ak, ak], self.topic)
        if kind == 2:
            q, n, scale = rng.choice((2, 3)), 2 * rng.randint(3, 6), rng.randint(1, 3)
            sn = scale * (q ** (n // 2) - 1)
            right = scale * (q ** (n // 2 - 1) - 1)
            stem = [given, text("ซึ่งมีอัตราส่วนร่วมเท่ากับ"), content_math(rf"\sqrt{{{q}}}"), text("และ"),
                    content_math(rf"a_{{1}} + a_{{2}} + \cdots + a_{{{n}}} = {num(sn)}"), text("แล้ว"),
                    content_math(rf"a_{{1}} + a_{{2}} + \cdots + a_{{{n - 2}}}"), text("เท่ากับเท่าใด")]
            # Dividing by q; scaling by the number of terms; subtracting q.
            return _num_q(stem, right, [Fraction(sn, q), Fraction(sn * (n - 2), n), sn - q], self.topic)
        if kind == 3:
            p, qd = rng.choice(((1, 3), (2, 5), (1, 4), (-1, 3), (-2, 15), (-1, 5), (2, 7)))
            k = rng.randint(1, 3)
            total, alt = Fraction(k * (qd + p)), Fraction(k * (qd - p))
            n = 2 * rng.randint(5, 12)
            stem = [given, text("ถ้า"), content_math(rf"a_{{1}} + a_{{2}} + \cdots + a_{{{n}}} = {num(total)}"),
                    text("และ"), content_math(rf"a_{{1}} - a_{{2}} + \cdots - a_{{{n}}} = {num(alt)}"),
                    text("แล้วอัตราส่วนร่วมของลำดับนี้เท่ากับเท่าใด")]
            right = ratio_from_alternating(total, alt)
            # Inverted; the sign flipped; total/alt.
            return _num_q(stem, right, [(total + alt) / (total - alt), -right, total / alt], self.topic)
        if rng.random() < 0.5:
            a = Fraction(rng.randint(1, 6), rng.choice((1, 2, 3)))
            r = rng.choice((Fraction(1, 3), Fraction(-1, 3), Fraction(1, 2), Fraction(-1, 2), Fraction(2, 3),
                            Fraction(-2, 3), Fraction(1, 4), Fraction(3, 4), Fraction(2, 5)))
            s, t = a / (1 - r), -a / (1 + r)
            stem = [given, text("ถ้า"), content_math(rf"\sum_{{n=1}}^{{\infty}} a_{{n}} = {num(s)}"), text("และ"),
                    content_math(rf"\sum_{{n=1}}^{{\infty}} (-1)^{{n}} a_{{n}} = {num(t)}"), text("แล้ว"),
                    content_math(r"\sum_{n=1}^{\infty} a_{n}^{2}"), text("เท่ากับเท่าใด")]
            # s·t with its sign; s²; s² − t².
            return _num_q(stem, squares_from_sums(s, t), [s * t, s * s, s * s - t * t], self.topic)
        t = rng.choice((Fraction(1, 2), Fraction(1, 3), Fraction(1, 4), Fraction(2, 3), Fraction(-1, 2)))
        x = rng.randint(1, 6) * t.denominator ** 2
        y = x * t * (1 + t)
        stem = [given, text("ซึ่งมีอัตราส่วนร่วม r โดยที่ |r| < 1 ถ้า"),
                content_math(f"a_{{1}} + a_{{2}} + \\cdots + a_{{5}} = {num(x)}"), text("และ"),
                content_math(f"a_{{6}} + a_{{7}} + \\cdots + a_{{15}} = {num(y)}"), text("แล้ว"),
                content_math(r"\sum_{n=1}^{\infty} a_{n}"), text("เท่ากับเท่าใด")]
        # x + y (the first 15 terms); x/(1 − t²); x/(1 + t).
        return _num_q(stem, infinite_from_blocks(Fraction(x), t), [x + y, x / (1 - t * t), x / (1 + t)], self.topic)
GeometricSeriesTricksM6.PROVENANCE = Provenance("adapted", sources=('openthaiknowledge-bank/rathcenter/14 ลำดับและอนุกรม',))


@question_type("math.geometric_series_finite", display_name={"th": "ผลบวกอนุกรมเรขาคณิตจำกัด"},
               level={"th": "ม.6"}, topic="ลำดับเรขาคณิต")
class GeometricSeriesFinite(MathType):
    def expr(self, rng: Random, first_hi: int = 5, n_lo: int = 3, n_hi: int = 8):
        a1 = rng.randint(1, first_hi)
        r = rng.choice([2, 3])
        n = rng.randint(n_lo, n_hi)
        total = a1 * (r ** n - 1) // (r - 1)
        shown = ", ".join(str(a1 * r ** i) for i in range(3)) + r", \ldots"
        return MathDraw(
            shown, str(total), prompt=f"จงหาผลบวก {n} พจน์แรกของอนุกรมนี้",
            hint=r"S_n = \frac{a_1(r^n - 1)}{r - 1}",
            distractors=[str(a1 * r ** n), str(a1 * (r ** n - 1)),
                         str(a1 * r ** (n - 1))])
GeometricSeriesFinite.PROVENANCE = Provenance("original")


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

# ── More geometric sequences (2026-11): the ratio from two terms, a term from two others, a sum with ratio 3,
# a geometric mean, and which term has a value ──


@question_type("math.ratio_from_terms_m6", display_name={"th": "หาอัตราส่วนร่วมจากสองพจน์"}, level=LEVEL, topic="ลำดับเรขาคณิต")
class RatioFromTermsM6(WordProblem):
    def expr(self, rng: Random):
        a, r = rng.randint(1, 5), rng.choice((2, 3, -2, -3))
        a2, a5 = a * r, a * r ** 4
        prompt = f"ลำดับเรขาคณิตมี a_2 = {a2} และ a_5 = {a5} อัตราส่วนร่วมเท่ากับเท่าใด"
        # The ratio of the terms; the gap over three; the sign lost.
        return MathDraw("", str(r), prompt=prompt, distractors=_nk6(a5 // a2, (a5 - a2) // 3, -r, r * r, answer=r))


@question_type("math.geo_term_from_two_m6", display_name={"th": "หาพจน์ของลำดับเรขาคณิตจากสองพจน์"}, level=LEVEL, topic="ลำดับเรขาคณิต")
class GeoTermFromTwoM6(WordProblem):
    def expr(self, rng: Random):
        a, r = rng.randint(1, 6), rng.choice((2, 3))
        a1, a3, right = a, a * r * r, a * r ** 4
        prompt = f"ลำดับเรขาคณิตที่ทุกพจน์เป็นบวก มี a_1 = {a1} และ a_3 = {a3} พจน์ที่ 5 เท่ากับเท่าใด"
        # Arithmetic instead; one ratio short; the ratio squared once.
        return MathDraw("", str(right), prompt=prompt, distractors=_nk6(2 * a3 - a1, a * r ** 3, a3 * r, a3 + a1, answer=right, lo=1))


@question_type("math.geo_sum_ratio_three_m6", display_name={"th": "ผลบวก n พจน์แรกของอนุกรมเรขาคณิต"}, level=LEVEL, topic="ลำดับเรขาคณิต")
class GeoSumRatioThreeM6(MathType):
    def expr(self, rng: Random):
        a, r, n = rng.randint(1, 5), rng.choice((2, 3)), rng.randint(4, 7)
        right = a * (r ** n - 1) // (r - 1)
        # The last term; one term short; r to the n.
        return MathDraw(f"{a} + {a * r} + {a * r * r} + \\cdots", f"{right:,}".replace(",", "{,}"), prompt=f"จงหาผลบวก {n} พจน์แรก",
                        distractors=[f"{v:,}".replace(",", "{,}") for v in dict.fromkeys(
                            (a * r ** (n - 1), a * (r ** (n - 1) - 1) // (r - 1), a * r ** n, right + a)) if v != right])


@question_type("math.geometric_mean_m6", display_name={"th": "ค่าเฉลี่ยเรขาคณิตของสองจำนวน"}, level=LEVEL, topic="ลำดับเรขาคณิต")
class GeometricMeanM6(WordProblem):
    def expr(self, rng: Random):
        m, r = rng.randint(1, 8), rng.randint(2, 6)
        a, b = m, m * r * r
        right = m * r
        prompt = f"ค่าเฉลี่ยเรขาคณิตของ {a} และ {b} (ค่าบวก) เท่ากับเท่าใด"
        # The arithmetic mean; the product; half the larger.
        return MathDraw("", str(right), prompt=prompt, distractors=_tk6(_num6(Fraction(a + b, 2)), str(a * b), _num6(Fraction(b, 2)), str(right + 1),
                                                                         answer=str(right)))


@question_type("math.geo_which_term_m6", display_name={"th": "จำนวนนี้เป็นพจน์ที่เท่าใดของลำดับเรขาคณิต"}, level=LEVEL,
               topic="ลำดับเรขาคณิต")
class GeoWhichTermM6(WordProblem):
    def expr(self, rng: Random):
        a, r, n = rng.randint(1, 5), rng.choice((2, 3)), rng.randint(4, 9)
        value = a * r ** (n - 1)
        prompt = f"ลำดับ {a}, {a * r}, {a * r * r}, ... จำนวน {value:,} เป็นพจน์ที่เท่าใด"
        # The power of r; one more; the value over the ratio.
        return MathDraw("", str(n), prompt=prompt, distractors=_nk6(n - 1, n + 1, 2 * n, value // r if value // r < 40 else n + 2, answer=n, lo=1))


RatioFromTermsM6.PROVENANCE = Provenance("original")
GeoTermFromTwoM6.PROVENANCE = Provenance("original")
GeoSumRatioThreeM6.PROVENANCE = Provenance("original")
GeometricMeanM6.PROVENANCE = Provenance("original")
GeoWhichTermM6.PROVENANCE = Provenance("original")
