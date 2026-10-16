"""สมการเลขชี้กำลัง

คณิตศาสตร์ · ม.4 · สสวท. เพิ่มเติม
Indicators: ค เพิ่มเติม จำนวนและพีชคณิต 3 ม.4/4

Sets moved here from: math, math_algebra, math_bank_powers.
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
from otk.kit.math_problems import MathDraw, MathType, WordProblem, frac_tex, poly_tex
from otk.sets._support.math_algebra import _pow
from otk.sets._support.math_bank_powers import M4, _tex_q
from otk.sets._support.math_m4 import maths as _num_maths


def solve_factored(a: int, total: int) -> int:
    """x with a^(x+1) + a^x + a^(x−1) = total: a^(x−1)·(a² + a + 1) = total."""
    q, r = divmod(total, a * a + a + 1)
    assert r == 0
    k = round(math.log(q, a))
    assert a ** k == q
    return k + 1


def substitution_solutions(a: int, m: int, n: int) -> list[int]:
    """Real x with a^(2x) − (a^m + a^n)·a^x + a^(m+n) = 0: u = a^x is a^m or a^n."""
    return sorted({m, n})


def solve_exp_inequality(a: Fraction, p: int, q: int, r: int, s: int) -> tuple[Fraction, bool]:
    """a^(px + q) > a^(rx + s), p ≠ r: the solution is x > t (True) or x < t (False).

    Compare exponents, flipping when 0 < a < 1, then divide by p − r,
    flipping again when it is negative.
    """
    t = Fraction(s - q, p - r)
    return t, (p - r > 0) == (a > 1)


@question_type("math.exponential_equation",
               display_name={"th": "สมการเลขชี้กำลัง"}, level={"th": "ม.4"},
               topic="สมการเลขชี้กำลัง")
class ExponentialEquation(MathType):
    def expr(self, rng: Random):
        if rng.random() < 0.3:
            p, i, j = rng.choice([(2, 2, 3), (2, 3, 2), (2, 2, 5),
                                  (3, 2, 3), (2, 3, 4), (3, 3, 2)])
            x = Fraction(j, i)
            return MathDraw(rf"{p ** i}^{{x}} = {p ** j}", rf"x = {frac_tex(x)}",
                            hint=rf"\text{{write both sides as powers of }} {p}",
                            prompt="จงแก้สมการ")
        b = rng.choice([2, 3, 5])
        k = rng.randint(2, 5 if b == 2 else 3)
        s = rng.randint(-2, 2)
        lhs = "x" if s == 0 else f"x {'+' if s > 0 else '-'} {abs(s)}"
        return MathDraw(rf"{b}^{{{lhs}}} = {b ** k}", rf"x = {k - s}",
                        hint=rf"{b ** k} = {b}^{{{k}}}", prompt="จงแก้สมการ")
ExponentialEquation.PROVENANCE = Provenance("original")


@question_type("math.exponential_equation_same_base",
               display_name={"th": "สมการเลขชี้กำลัง (ทำฐานให้เท่ากัน)"},
               level={"th": "ม.4"}, topic="สมการเลขชี้กำลัง")
class ExponentialSameBase(MathType):
    def expr(self, rng: Random, base_lo: int = 2, base_hi: int = 5):
        b = rng.randint(base_lo, base_hi)
        k = rng.randint(2, 3)                     # the right side is b^(k·m)
        m = rng.randint(2, 4)                     # not 1: b^k^1 hides the step
        c = rng.randint(-6, 6)
        # b^(x + c) = (b^k)^m  ⟹  x + c = k·m
        x = k * m - c
        return MathDraw(
            rf"{b}^{{{poly_tex((1, 'x'), (c, ''))}}} = {_pow(str(b ** k), m)}",
            f"x = {x}", prompt="จงแก้สมการ",
            distractors=[f"x = {k * m + c}", f"x = {b ** k * m - c}",
                         f"x = {m - c}"])
ExponentialSameBase.PROVENANCE = Provenance("original")


@question_type("math.exponential_growth_word",
               display_name={"th": "โจทย์ปัญหาการเติบโตแบบเลขชี้กำลัง"},
               level={"th": "ม.4"}, topic="สมการเลขชี้กำลัง")
class ExponentialGrowthWord(WordProblem):
    def expr(self, rng: Random, start_lo: int = 10, start_hi: int = 500,
             periods_hi: int = 6):
        start = rng.randrange(start_lo, start_hi, 10)
        factor = rng.choice([2, 3])
        periods = rng.randint(2, periods_hi)
        hours = rng.choice([1, 2, 3])
        final = start * factor ** periods
        kind = rng.randrange(4)
        # Linear growth in place of repeated multiplication, and one period short.
        wrongs = [str(start * factor * periods), str(start * factor ** (periods - 1)),
                  str(start + factor * periods)]
        if kind == 0:
            prompt = (f"แบคทีเรียเริ่มต้น {start} ตัว และเพิ่มเป็น {factor} เท่า "
                      f"ทุก {hours} ชั่วโมง เมื่อผ่านไป {hours * periods} ชั่วโมง "
                      "จะมีแบคทีเรียกี่ตัว")
        elif kind == 1:
            prompt = (f"ข่าวลือแพร่ต่อกันไป ทุก {hours} วัน จำนวนคนที่รู้ข่าวเพิ่มเป็น {factor} เท่า "
                      f"วันแรกมีคนรู้ {start} คน อีก {hours * periods} วันจะมีคนรู้ข่าวกี่คน")
        elif kind == 2:
            return MathDraw("", str(periods * hours),
                            prompt=(f"แบคทีเรียเริ่มต้น {start} ตัว เพิ่มเป็น {factor} เท่าทุก {hours} ชั่วโมง "
                                    f"ต้องใช้เวลากี่ชั่วโมงจึงจะมีแบคทีเรีย {final} ตัว"),
                            # Counting periods instead of hours, and one period too many.
                            distractors=[str(periods), str((periods + 1) * hours),
                                         str(final // start)])
        else:
            half = start * factor ** periods
            return MathDraw("", str(start),
                            prompt=(f"สารกัมมันตรังสีมวล {half} กรัม สลายเหลือ 1/{factor} ของมวลเดิมทุก "
                                    f"{hours} ปี เมื่อผ่านไป {hours * periods} ปี จะเหลือสารกี่กรัม"),
                            distractors=[str(half // (factor * periods)) if half % (factor * periods) == 0
                                         else str(start * factor), str(start * factor),
                                         str(half - start)])
        return MathDraw("", str(final), prompt=prompt, distractors=wrongs)
ExponentialGrowthWord.PROVENANCE = Provenance("original")


@question_type("math.exponential_equation_advanced_m4",
               display_name={"th": "สมการและอสมการเลขชี้กำลังรูปแบบซับซ้อน"},
               level=M4, topic="สมการเลขชี้กำลัง")
class ExponentialEquationAdvancedM4(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        kind = rng.randrange(4)
        if kind == 0:
            a, x = rng.choice((2, 3, 5)), rng.randint(2, 5)
            total = a ** (x + 1) + a ** x + a ** (x - 1)
            right = solve_factored(a, total)
            stem = [text("จำนวนจริง x ที่สอดคล้องกับสมการ"),
                    content_math(rf"{a}^{{x + 1}} + {a}^{{x}} + {a}^{{x - 1}} = {total}"),
                    text("เท่ากับเท่าใด")]
            # Stopping at x − 1 (the factored exponent); one too many; the factor's power.
            return _num_maths(stem, str(right), [str(right - 1), str(right + 1), str(right - 2)],
                              self.topic)
        if kind == 1:
            a = rng.choice((2, 3))
            m, n = sorted(rng.sample(range(0, 5), 2))
            p, q = a ** m, a ** n
            right = sum(substitution_solutions(a, m, n))
            stem = [text("ผลบวกของคำตอบทั้งหมดของสมการ"),
                    content_math(rf"{a}^{{2x}} - {p + q} \cdot {a}^{{x}} + {p * q} = 0"),
                    text("เท่ากับเท่าใด")]
            # The roots of the quadratic in u, summed; their product; one solution only.
            return _num_maths(stem, str(right), [str(p + q), str(m * n), str(n)], self.topic)
        if kind == 2:
            # a^(x²) = (a^b)^(cx − d), so x² − bcx + bd = 0 with integer roots.
            a, b = rng.choice((2, 3)), rng.choice((2, 3))
            while True:
                r1, r2 = rng.randint(-3, 8), rng.randint(-3, 8)
                if r1 != r2 and (r1 + r2) % b == 0 and (r1 * r2) % b == 0 and r1 + r2 != 0:
                    break
            c, d = (r1 + r2) // b, (r1 * r2) // b
            right = r1 + r2
            coef = "" if c == 1 else ("-" if c == -1 else str(c))
            inner = f"{coef}x {'-' if d > 0 else '+'} {abs(d)}" if d else f"{coef}x"
            stem = [text("ผลบวกของคำตอบของสมการ"),
                    content_math(rf"{a}^{{x^{{2}}}} = {a ** b}^{{{inner}}}"), text("เท่ากับเท่าใด")]
            # Forgetting to rewrite the base (c alone); the product of roots; b·d.
            return _num_maths(stem, str(right), [str(c), str(r1 * r2), str(b * d)], self.topic)
        # a^(px + q) > a^(rx + s): flip the inequality when 0 < a < 1.
        a = rng.choice((Fraction(1, 2), Fraction(1, 3), Fraction(2), Fraction(3)))
        while True:
            p, q, r, s = rng.randint(1, 4), rng.randint(-5, 5), rng.randint(-3, 3), rng.randint(-5, 5)
            if p != r and (s - q) % (p - r) == 0:
                break
        t, greater = solve_exp_inequality(a, p, q, r, s)
        right = rf"({frac_tex(t)}, \infty)" if greater else rf"(-\infty, {frac_tex(t)})"
        other = rf"(-\infty, {frac_tex(t)})" if greater else rf"({frac_tex(t)}, \infty)"
        base_tex = frac_tex(a) if a.denominator == 1 else rf"\left({frac_tex(a)}\right)"
        def lin(k: int, c: int) -> str:
            head = f"{'' if k == 1 else ('-' if k == -1 else k)}x"
            return head if c == 0 else f"{head} {'+' if c > 0 else '-'} {abs(c)}"
        rhs = f"{base_tex}^{{{lin(r, s)}}}" if r else f"{base_tex}^{{{s}}}"
        stem = [text("เซตคำตอบของอสมการ"),
                content_math(rf"{base_tex}^{{{lin(p, q)}}} > {rhs}"), text("คือเซตในข้อใด")]
        # Forgetting to flip for a base below 1 (or flipping for one above); a sign slip on t.
        wrongs = [other, rf"({frac_tex(-t)}, \infty)", rf"(-\infty, {frac_tex(-t)})"]
        if t == 0:
            wrongs = [other, r"(1, \infty)", r"(-\infty, -1)"]
        return _tex_q(stem, right, wrongs, self.topic)
ExponentialEquationAdvancedM4.PROVENANCE = Provenance("adapted", sources=('openthaiknowledge-bank/rathcenter/5 เลขยกกำลัง',))
