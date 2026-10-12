"""ลำดับเลขคณิต

คณิตศาสตร์ · ม.6 · สสวท. เพิ่มเติม
Indicators: ค เพิ่มเติม จำนวนและพีชคณิต 2 ม.6/2, ค เพิ่มเติม จำนวนและพีชคณิต 2 ม.6/4

Sets moved here from: math, math_apply_add, math_bank_sequences, math_calculus.
"""

from __future__ import annotations

from fractions import Fraction
from math import isqrt
from random import Random

from otk.core.content import math as content_math
from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, MathType, WordProblem, frac_tex
from otk.sets._support.math_apply_add import M6 as M6_math_apply_add
from otk.sets._support.math_apply_add import _c
from otk.sets._support.math_bank_sequences import M6, _num_q, num
from otk.sets._support.math_calculus import _nonzero

ARITHMETIC = "ลำดับเลขคณิต"


def seq_tex(terms) -> str:
    return ", ".join(num(t) for t in terms) + r", \ldots"


def ap(a1: Fraction, d: Fraction, n: int) -> Fraction:
    return a1 + (n - 1) * d


def alternating_sum(a1: Fraction, d: Fraction, n: int) -> Fraction:
    """a₁ − a₂ + a₃ − ⋯ ± aₙ: pairs give −d each; an odd n leaves a₁ unpaired at the front."""
    if n % 2 == 0:
        return -Fraction(n, 2) * d
    return a1 + Fraction(n - 1, 2) * d


def alternating_square_sum(a1: Fraction, d: Fraction, n: int) -> Fraction:
    """a₁² − a₂² + ⋯ − aₙ² (n even) = −d·Sₙ."""
    return -d * Fraction(n, 2) * (a1 + ap(a1, d, n))


def range_sum(a1: Fraction, d: Fraction, p: int, q: int) -> Fraction:
    """aₚ + ⋯ + a_q."""
    return Fraction(q - p + 1, 2) * (ap(a1, d, p) + ap(a1, d, q))


def exp_sum(rho: int, j: int, n: int) -> Fraction:
    """b₁ + ⋯ + bₙ where bₖ = ρ^(j + k − 1): a geometric series with first term ρʲ."""
    return Fraction(rho) ** j * Fraction(rho ** n - 1, rho - 1)


#: (c, d) with c^d = ρ an integer: bₙ = c^(aₙ) is geometric with ratio ρ.
EXP_BASES = ((8, Fraction(1, 3), 2), (27, Fraction(1, 3), 3), (4, Fraction(1, 2), 2), (9, Fraction(1, 2), 3))


def second_difference_term(a1: int, d1: int, e: int, n: int) -> int:
    """aₙ when the gaps are d₁, d₁ + e, d₁ + 2e, …: a₁ + (n − 1)d₁ + e(n − 1)(n − 2)/2."""
    return a1 + (n - 1) * d1 + e * (n - 1) * (n - 2) // 2


def term_from_partial_sums(p: int, q: int, k: int) -> int:
    """aₖ = Sₖ − Sₖ₋₁ for Sₙ = pn² + qn."""
    return p * (2 * k - 1) + q


def paired_recurrence_sum(s: int, d: int, m: int) -> int:
    """a₁ + ⋯ + a₂ₘ when a₁ + a₂ = s and aₙ₊₂ − aₙ = d: pair k sums to s + 2(k − 1)d."""
    return m * s + d * m * (m - 1)


def previous_partial_sum(sm: int, sm1: int, m: int) -> Fraction:
    """Sₘ₋₁ of an arithmetic series from Sₘ and Sₘ₊₁."""
    am1 = Fraction(sm1 - sm)                                    # aₘ₊₁
    a1 = Fraction(2 * sm1, m + 1) - am1
    d = (am1 - a1) / m
    am = am1 - d
    return sm - am


def triangle_row(k: int) -> tuple[int, int]:
    """(first number, sum) of row k when 1, 2, 3, … fill rows of 1, 2, 3, … numbers."""
    first = 1 + k * (k - 1) // 2
    return first, k * (2 * first + k - 1) // 2


def recur_linear(a1: Fraction, p: Fraction, q: Fraction, n: int) -> Fraction:
    """aₙ for a₁ given and aₖ = p·aₖ₋₁ + q (k ≥ 2), stepped term by term."""
    a = Fraction(a1)
    for _ in range(n - 1):
        a = p * a + q
    return a


def recur_two(a1: int, a2: int, c: int, n: int) -> int:
    """aₙ for aₖ = aₖ₋₁ + c·aₖ₋₂ (k ≥ 3)."""
    if n == 1:
        return a1
    x, y = a1, a2
    for _ in range(n - 2):
        x, y = y, y + c * x
    return y


#: (TeX of aₙ, aₙ as a function of n); bases of powers stay small so the terms stay readable.
GENERAL_TERMS = (
    (lambda p, q: (rf"(n - {p})(n + {q})", lambda n: Fraction((n - p) * (n + q)))),
    (lambda p, q: (rf"\left(-{p}\right)^{{n}}", lambda n: Fraction(-p) ** n)),
    (lambda p, q: (rf"\frac{{n + {q}}}{{n}}", lambda n: Fraction(n + q, n))),
    (lambda p, q: (rf"\frac{{{q} + (-1)^{{n}}}}{{n}}", lambda n: Fraction(q + (-1) ** n, n))),
    (lambda p, q: (rf"n^{{2}} - {p}n + {q}", lambda n: Fraction(n * n - p * n + q))),
)


def _signed(v: Fraction) -> str:
    return f"+ {num(v)}" if v >= 0 else f"- {num(-v)}"


@question_type("math.sequence_terms_m6",
               display_name={"th": "พจน์ของลำดับจากพจน์ทั่วไปและความสัมพันธ์เวียนเกิด"},
               level=M6, topic=ARITHMETIC)
class SequenceTermsM6(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        kind = rng.randrange(3)
        if kind == 0:
            make = rng.choice(GENERAL_TERMS)
            tex, f = make(rng.randint(2, 3), rng.randint(1, 5))
            k = rng.randint(3, 7)
            stem = [text("กำหนดลำดับ"), content_math(rf"a_n = {tex}"), text(f"พจน์ที่ {k} ของลำดับนี้คือจำนวนใด")]
            # One place early; one place late; the sign of a power or (−1)ⁿ read at n = k + 1.
            return _num_q(stem, f(k), [f(k - 1), f(k + 1), -f(k)], self.topic)
        if kind == 1:
            a1 = Fraction(rng.randint(1, 6))
            p = Fraction(rng.choice((2, 3, -2)))
            q = Fraction(rng.choice((-3, -2, -1, 1, 2, 3)))
            k = rng.randint(4, 5)
            stem = [text("กำหนดลำดับ"), content_math(rf"a_1 = {num(a1)}"), text("และ"),
                    content_math(rf"a_n = {num(p)}a_{{n-1}} {_signed(q)}"), text("เมื่อ"),
                    content_math(r"n \ge 2"), text(f"พจน์ที่ {k} ของลำดับนี้คือจำนวนใด")]
            # One step short; one step too many; the constant q forgotten (geometric a₁pⁿ⁻¹).
            named = [recur_linear(a1, p, q, k - 1), recur_linear(a1, p, q, k + 1), a1 * p ** (k - 1)]
            return _num_q(stem, recur_linear(a1, p, q, k), named, self.topic)
        a1, a2 = rng.randint(1, 3), rng.randint(0, 4)
        c = rng.choice((2, 3, -1))
        k = rng.randint(5, 6)
        coef = "" if c == 1 else ("-" if c == -1 else str(c))
        rec = rf"a_n = a_{{n-1}} {'-' if c < 0 else '+'} {coef.lstrip('-')}a_{{n-2}}"
        stem = [text("กำหนดลำดับ"), content_math(rf"a_1 = {a1},\ a_2 = {a2}"), text("และ"),
                content_math(rec), text("เมื่อ"), content_math(r"n \ge 3"),
                text(f"พจน์ที่ {k} ของลำดับนี้คือจำนวนใด")]
        # One step short; one step too many; the coefficient c dropped (Fibonacci rule).
        named = [recur_two(a1, a2, c, k - 1), recur_two(a1, a2, c, k + 1), recur_two(a1, a2, 1, k)]
        return _num_q(stem, recur_two(a1, a2, c, k), named, self.topic)
SequenceTermsM6.PROVENANCE = Provenance("adapted", sources=('sheet_database/rathcenter/14 ลำดับและอนุกรม',))


@question_type("math.arithmetic_nth_term", display_name={"th": "พจน์ที่ n ของลำดับเลขคณิต"},
               level={"th": "ม.6"}, topic="ลำดับเลขคณิต")
class ArithmeticNthTerm(MathType):
    def expr(self, rng: Random, first_hi: int = 20, diff_hi: int = 9,
             n_lo: int = 8, n_hi: int = 40):
        a1 = rng.randint(-first_hi, first_hi)
        d = _nonzero(rng, -diff_hi, diff_hi)
        n = rng.randint(n_lo, n_hi)
        value = a1 + (n - 1) * d
        shown = ", ".join(str(a1 + i * d) for i in range(4)) + r", \ldots"
        return MathDraw(
            shown, str(value), prompt=f"จงหาพจน์ที่ {n} ของลำดับนี้",
            hint=r"a_n = a_1 + (n-1)d",
            # Using n instead of n − 1 is the classic off-by-one.
            distractors=[str(a1 + n * d), str(a1 + (n - 2) * d), str(n * d)])
ArithmeticNthTerm.PROVENANCE = Provenance("original")


@question_type("math.arithmetic_sequence",
               display_name={"th": "ลำดับ-อนุกรมเลขคณิต"}, level={"th": "ม.6"}, topic="ลำดับเลขคณิต")
class ArithmeticSequence(MathType):
    def expr(self, rng: Random):
        a1 = rng.randint(-9, 9)
        d = rng.choice([n for n in range(-6, 7) if n])
        terms = ", ".join(str(a1 + i * d) for i in range(4))
        n = rng.randint(10, 25)
        if rng.random() < 0.5:
            return MathDraw(rf"{terms}, \ldots \quad a_{{{n}}}",
                            rf"{a1 + (n - 1) * d}", topic="ลำดับเลขคณิต",
                            hint=r"a_n = a_1 + (n-1)d")
        return MathDraw(rf"{terms}, \ldots \quad S_{{{n}}}",
                        rf"{n * (2 * a1 + (n - 1) * d) // 2}", topic="อนุกรมเลขคณิต",
                        hint=r"S_n = \frac{n}{2}(2a_1 + (n-1)d)")
ArithmeticSequence.PROVENANCE = Provenance("original")


@question_type("math.arithmetic_series_word_m6",
               display_name={"th": "โจทย์ปัญหาอนุกรมเลขคณิต (หาจำนวนพจน์)"},
               level=M6_math_apply_add, topic="ลำดับเลขคณิต")
class ArithmeticSeriesWordM6(WordProblem):
    def expr(self, rng: Random):
        kind = rng.randrange(5)
        if kind == 0:
            a, d, n = rng.randint(12, 25), rng.choice((2, 3, 4)), rng.randint(8, 20)
            s = n * (2 * a + (n - 1) * d) // 2 if n * (2 * a + (n - 1) * d) % 2 == 0 else None
            if s is None:
                n += 1
                s = n * (2 * a + (n - 1) * d) // 2
            return MathDraw("", str(n),
                            prompt=(f"หอประชุมจัดเก้าอี้แถวแรก {a} ตัว แถวถัดไปเพิ่มขึ้นแถวละ {d} ตัว "
                                    f"ถ้ามีเก้าอี้ทั้งหมด {_c(s)} ตัว จัดได้กี่แถว"),
                            distractors=_story.keep(s // a, n - 1, n + 1, s // (a + (n - 1) * d),
                                                    answer=n, lo=1))
        if kind == 1:
            x, d = rng.choice((10, 20, 30)), rng.choice((5, 10))
            n = rng.randint(6, 14)
            b = x + (n - 1) * d // 2 if (n - 1) * d % 2 == 0 else None
            if b is None:
                n += 1
                b = x + (n - 1) * d // 2
            p, q = _story.names(rng, 2)
            return MathDraw("", str(n),
                            prompt=(f"{p}ออมเงินวันแรก {x} บาท และออมเพิ่มขึ้นวันละ {d} บาท ส่วน{q}ออมวันละ {b} บาทเท่ากันทุกวัน "
                                    f"เมื่อครบกี่วัน ทั้งสองคนจะมีเงินออมรวมเท่ากัน"),
                            distractors=_story.keep((b - x) // d + 1, n - 1, n + 1, 2 * n, answer=n, lo=2))
        if kind == 2:
            n = rng.randint(8, 25)
            t = n * (n + 1) // 2
            return MathDraw("", str(n),
                            prompt=(f"เรียงกระป๋องเป็นรูปสามเหลี่ยม แถวบนสุด 1 กระป๋อง แถวถัดลงมาเพิ่มขึ้นแถวละ 1 กระป๋อง "
                                    f"ใช้กระป๋องทั้งหมด {t} กระป๋อง แถวล่างสุดมีกี่กระป๋อง"),
                            distractors=_story.keep(t // 2, n + 1, n - 1, isqrt(t), answer=n, lo=1))
        if kind == 3:
            while True:
                a, d, n = rng.choice((200, 300, 400)), rng.choice((20, 30, 50)), rng.randint(10, 20)
                fixed = rng.choice((500, 600, 700, 800))
                s = n * (2 * a + (n - 1) * d) // 2
                if s != n * fixed:
                    break
            diff = abs(s - n * fixed)
            better = "แบบที่หนึ่ง" if s > n * fixed else "แบบที่สอง"
            return MathDraw("", _c(diff),
                            prompt=(f"งานชั่วคราว {n} วัน เสนอค่าจ้างสองแบบ แบบที่หนึ่งได้วันแรก {a} บาท และเพิ่มขึ้นวันละ {d} บาท "
                                    f"แบบที่สองได้วันละ {fixed} บาทเท่ากันทุกวัน รวมทั้ง {n} วัน {better}ได้เงินมากกว่ากี่บาท"),
                            # the last day's gap only; n·d instead of (n−1)·d; a whole extra step
                            distractors=[_c(abs(a + (n - 1) * d - fixed)), _c(abs(n * (a + n * d) // 1 - n * fixed)),
                                         _c(diff + d)])
        a, d, n = rng.randint(2, 5), rng.choice((1, 2)), rng.randint(6, 14)
        s = n * (2 * a + (n - 1) * d) // 2 if n * (2 * a + (n - 1) * d) % 2 == 0 else None
        if s is None:
            n += 1
            s = n * (2 * a + (n - 1) * d) // 2
        return MathDraw("", str(n),
                        prompt=(f"นักวิ่งซ้อมวิ่งวันแรก {a} กิโลเมตร และวิ่งเพิ่มขึ้นวันละ {d} กิโลเมตร "
                                f"เมื่อสิ้นวันที่เท่าใด ระยะทางที่วิ่งรวมทั้งหมดจะเป็น {s} กิโลเมตรพอดี"),
                        distractors=_story.keep(s // a, n - 1, n + 1, s // (a + (n - 1) * d), answer=n, lo=1))
ArithmeticSeriesWordM6.PROVENANCE = Provenance("original")


@question_type("math.arithmetic_series_tricks_m6",
               display_name={"th": "จับคู่พจน์ในอนุกรมเลขคณิต"},
               level=M6, topic=ARITHMETIC)
class ArithmeticSeriesTricksM6(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        kind = rng.randrange(4)
        given = text("กำหนดให้ a₁, a₂, a₃, … เป็นลำดับเลขคณิต")
        if kind == 0:
            a1 = Fraction(rng.randint(-5, 9))
            d = Fraction(rng.choice((1, 2, 3, -2, -1)), rng.choice((1, 2, 3)))
            n = rng.randint(10, 40)
            signs = "a_{1} - a_{2} + a_{3} - a_{4} + \\cdots " + ("- " if n % 2 == 0 else "+ ") + f"a_{{{n}}}"
            if n % 2 == 0 and rng.random() < 0.5:
                total = alternating_sum(a1, d, n)
                stem = [given, text("ถ้า"), content_math(f"{signs} = {num(total)}"),
                        text("แล้วผลต่างร่วมของลำดับนี้เท่ากับเท่าใด")]
                # The sign lost; dividing by n instead of n/2; −total/n.
                return _num_q(stem, d, [-d, -total / n, total / n * 2], self.topic)
            stem = [given, text(f"ถ้า a₁ = {a1} และผลต่างร่วมเท่ากับ"), content_math(num(d)),
                    text("แล้ว"), content_math(signs), text("เท่ากับเท่าใด")]
            right = alternating_sum(a1, d, n)
            # The pairs' sign flipped; forgetting the unpaired a₁ (odd n) or adding it (even n); n·d/2.
            other = alternating_sum(a1, -d, n) if n % 2 else -right
            named = [other, right - a1 if n % 2 else right + a1, Fraction(n, 2) * d]
            return _num_q(stem, right, named, self.topic)
        if kind == 1:
            a1, d = rng.randint(1, 9), rng.choice((1, 2, 3))
            n = 2 * rng.randint(10, 30)
            an = ap(Fraction(a1), Fraction(d), n)
            right = alternating_square_sum(Fraction(a1), Fraction(d), n)
            stem = [given, text(f"ถ้า a₁ = {a1} และ"), content_math(f"a_{{{n}}} = {num(an)}"), text("แล้ว"),
                    content_math(rf"a_{{1}}^{{2}} - a_{{2}}^{{2}} + a_{{3}}^{{2}} - \cdots - a_{{{n}}}^{{2}}"),
                    text("เท่ากับเท่าใด")]
            s = Fraction(n, 2) * (a1 + an)
            # The sign lost; Sₙ itself; −d·Sₙ/2 (half the pairs).
            return _num_q(stem, right, [-right, -s, right / 2], self.topic)
        if kind == 2:
            a1, d = rng.randint(-5, 20), rng.choice((1, 2, 3, 4, -2))
            s, t = sorted(rng.sample(range(2, 20), 2))
            p = rng.randint(1, s)
            q = rng.randint(max(p + 3, t - 3), t + 4)
            as_, at = ap(Fraction(a1), Fraction(d), s), ap(Fraction(a1), Fraction(d), t)
            right = range_sum(Fraction(a1), Fraction(d), p, q)
            stem = [text(f"ลำดับเลขคณิตลำดับหนึ่งมีพจน์ที่ {s} คือ"), content_math(num(as_)),
                    text(f"และพจน์ที่ {t} คือ"), content_math(num(at)),
                    text(f"ผลบวกของพจน์ที่ {p} ถึงพจน์ที่ {q} ของลำดับนี้เท่ากับเท่าใด")]
            # q − p terms instead of q − p + 1; the sum of the first q terms; one term short at the end.
            named = [Fraction(q - p, 2) * (ap(a1, d, p) + ap(a1, d, q)), range_sum(Fraction(a1), Fraction(d), 1, q),
                     range_sum(Fraction(a1), Fraction(d), p, q - 1)]
            return _num_q(stem, right, named, self.topic)
        c, d, rho = rng.choice(EXP_BASES)
        while True:                                  # j = 1 always gives a positive exponent
            j, n = rng.randint(-3, 1), rng.randint(5, 10)
            exponent = n * j + n * (n - 1) // 2      # b₁⋯bₙ = c^(Sₙ) = ρ^(Sₙ/d)
            if exponent:
                break
        right = exp_sum(rho, j, n)
        stem = [given, text("ซึ่งมีผลต่างร่วมเท่ากับ"), content_math(frac_tex(d)), text("และ"),
                content_math(rf"b_{{n}} = {c}^{{a_{{n}}}}"), text("ถ้า"),
                content_math(rf"b_{{1}} \cdot b_{{2}} \cdots b_{{{n}}} = {rho}^{{{exponent}}}"), text("แล้ว"),
                content_math(rf"b_{{1}} + b_{{2}} + \cdots + b_{{{n}}}"), text("เท่ากับเท่าใด")]
        # a₁ read as j (not j·d); one term fewer; ρⁿ − 1 without the first-term factor.
        named = [Fraction(c) ** j * Fraction(rho ** n - 1, rho - 1), exp_sum(rho, j, n - 1),
                 Fraction(rho ** n - 1, rho - 1)]
        return _num_q(stem, right, named, self.topic)
ArithmeticSeriesTricksM6.PROVENANCE = Provenance("adapted", sources=('sheet_database/rathcenter/14 ลำดับและอนุกรม',))


@question_type("math.sequence_patterns_m6",
               display_name={"th": "ลำดับจากแบบรูป ผลต่างขั้นที่สอง และผลบวกย่อย"},
               level=M6, topic=ARITHMETIC)
class SequencePatternsM6(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        kind = rng.randrange(5)
        if kind == 0:
            a1, d1, e = rng.randint(1, 9), rng.randint(1, 4), rng.randint(1, 3)
            n = rng.randint(20, 50)
            terms = [second_difference_term(a1, d1, e, k) for k in range(1, 7)]
            right = second_difference_term(a1, d1, e, n)
            stem = [text("จากแบบรูปของจำนวน"), content_math(seq_tex(terms)), text(f"พจน์ที่ {n} คือจำนวนใด")]
            # Read as arithmetic with the first gap; the triangular part off by one; one term further.
            named = [a1 + (n - 1) * d1, a1 + (n - 1) * d1 + e * n * (n - 1) // 2,
                     second_difference_term(a1, d1, e, n + 1)]
            return _num_q(stem, right, named, self.topic)
        if kind == 1:
            p, q = rng.randint(1, 3), rng.randint(-5, 5)
            k = rng.randint(10, 100)
            sn = rf"{'' if p == 1 else p}n^{{2}}" + (f" {'+' if q > 0 else '-'} {'' if abs(q) == 1 else abs(q)}n" if q else "")
            right = term_from_partial_sums(p, q, k)
            stem = [text("ถ้าผลบวก n พจน์แรกของอนุกรมหนึ่งเท่ากับ"), content_math(sn),
                    text(f"เมื่อ n เป็นจำนวนเต็มบวก แล้วพจน์ที่ {k} ของอนุกรมนี้เท่ากับเท่าใด")]
            # Sₖ itself; Sₖ₊₁ − Sₖ; Sₖ/k.
            named = [p * k * k + q * k, term_from_partial_sums(p, q, k + 1), Fraction(p * k * k + q * k, k)]
            return _num_q(stem, right, named, self.topic)
        if kind == 2:
            s, d, m = rng.randint(3, 15), rng.randint(1, 5), rng.randint(5, 25)
            right = paired_recurrence_sum(s, d, m)
            stem = [text("กำหนดให้ a₁, a₂, a₃, … เป็นลำดับ ถ้า"), content_math(f"a_{{1}} + a_{{2}} = {s}"),
                    text("และ"), content_math(f"a_{{n+2}} - a_{{n}} = {d}"), text("เมื่อ n = 1, 2, 3, … แล้ว"),
                    content_math(rf"a_{{1}} + a_{{2}} + \cdots + a_{{{2 * m}}}"), text("เท่ากับเท่าใด")]
            # The pairs growing by d, not 2d; one pair too many; 2d per pair squared in; the pairs not growing.
            named = [m * s + d * m * (m - 1) // 2, paired_recurrence_sum(s, d, m + 1), m * s + 2 * d * m * (m - 1),
                     m * s]
            return _num_q(stem, right, named, self.topic)
        if kind == 3:
            a1, d, m = rng.randint(-6, 9), rng.randint(1, 5), rng.randint(6, 14)
            sm = m * (2 * a1 + (m - 1) * d) // 2               # m(2a₁ + (m − 1)d) is always even
            sm1 = (m + 1) * (2 * a1 + m * d) // 2
            right = previous_partial_sum(sm, sm1, m)
            stem = [text("กำหนดให้ Sₙ เป็นผลบวก n พจน์แรกของลำดับเลขคณิตชุดหนึ่ง ถ้า"),
                    content_math(f"S_{{{m}}} = {num(sm)}"), text("และ"), content_math(f"S_{{{m + 1}}} = {num(sm1)}"),
                    text("แล้ว"), content_math(f"S_{{{m - 1}}}"), text("เท่ากับเท่าใด")]
            # Sₘ − aₘ₊₁ (the wrong last term removed); scaling Sₘ or Sₘ₊₁ by the number of terms.
            named = [2 * sm - sm1, Fraction(sm * (m - 1), m), Fraction(sm1 * (m - 1), m + 1)]
            return _num_q(stem, right, named, self.topic)
        k = rng.randint(15, 60)
        first, total = triangle_row(k)
        rows = r" \\ ".join(" \\; ".join(str(v) for v in range(triangle_row(r)[0], triangle_row(r)[0] + r))
                            for r in range(1, 5))
        shape = content_math(rf"\begin{{matrix}} {rows} \\ \vdots \end{{matrix}}")
        if rng.random() < 0.5:
            stem = [text("จัดเรียงจำนวนนับเป็นแถวดังนี้"), shape, text(f"จำนวนแรกของแถวที่ {k} คือจำนวนใด")]
            # k(k − 1)/2 without the +1; the last number of the row before; k(k + 1)/2.
            return _num_q(stem, first, [first - 1, k * (k + 1) // 2, first + k], self.topic)
        stem = [text("จัดเรียงจำนวนนับเป็นแถวดังนี้"), shape, text(f"ผลบวกของจำนวนในแถวที่ {k} เท่ากับเท่าใด")]
        # Starting the row one too late; k·first; the sum of rows 1 to k.
        _, nxt = triangle_row(k + 1)
        return _num_q(stem, total, [total + k, k * first, k * (k + 1) * (k * (k + 1) + 2) // 8, nxt], self.topic)
SequencePatternsM6.PROVENANCE = Provenance("adapted", sources=('sheet_database/rathcenter/14 ลำดับและอนุกรม',))


@question_type("math.arithmetic_series_sum", display_name={"th": "ผลบวกอนุกรมเลขคณิต"},
               level={"th": "ม.6"}, topic="ลำดับเลขคณิต")
class ArithmeticSeriesSum(MathType):
    def expr(self, rng: Random, first_hi: int = 15, diff_hi: int = 8,
             n_lo: int = 5, n_hi: int = 30):
        a1 = rng.randint(-first_hi, first_hi)
        d = _nonzero(rng, -diff_hi, diff_hi)
        n = rng.randint(n_lo, n_hi)
        last = a1 + (n - 1) * d
        total = n * (a1 + last) // 2 if (n * (a1 + last)) % 2 == 0 else None
        if total is None:                          # keep the answer an integer
            n += 1
            last = a1 + (n - 1) * d
            total = n * (a1 + last) // 2
        shown = ", ".join(str(a1 + i * d) for i in range(4)) + r", \ldots"
        return MathDraw(
            shown, str(total), prompt=f"จงหาผลบวก {n} พจน์แรกของอนุกรมนี้",
            hint=r"S_n = \frac{n}{2}(a_1 + a_n)",
            distractors=[str(n * (a1 + last)), str(last), str(n * a1)])
ArithmeticSeriesSum.PROVENANCE = Provenance("original")
