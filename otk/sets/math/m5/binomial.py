"""ทฤษฎีบททวินาม

คณิตศาสตร์ · ม.5 · สสวท. เพิ่มเติม
Indicators: ค เพิ่มเติม สถิติและความน่าจะเป็น 1 ม.5/1

Sets moved here from: math, math_apply_stage, math_data.
"""

from __future__ import annotations

import math
import math as _math
from decimal import Decimal
from random import Random

from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.math_problems import MathDraw, MathType, WordProblem
from otk.sets._support.math_apply_stage import _nums
from otk.sets._support.math_m4 import maths

PROVENANCE = Provenance("original")


@question_type("math.binomial_coefficient",
               display_name={"th": "สัมประสิทธิ์ทวินาม"}, level={"th": "ม.5"},
               topic="ทฤษฎีบททวินาม")
class BinomialCoefficient(WordProblem):
    def expr(self, rng: Random):
        n = rng.randint(3, 7)
        k = rng.randint(1, n - 1)
        return MathDraw(
            "", str(math.comb(n, k)),
            prompt=f"สัมประสิทธิ์ของพจน์ที่มี x^{k} ในการกระจาย (x+1)^{n} "
                   f"เท่ากับเท่าใด?",
            distractors=[str(math.comb(n, k + 1)), str(n * k),
                         str(math.comb(n - 1, k))])


@question_type("math.binomial_term", display_name={"th": "พจน์ที่ต้องการในการกระจายทวินาม"},
               level={"th": "ม.5"}, topic="ทฤษฎีบททวินาม")
class BinomialTerm(MathType):
    def expr(self, rng: Random, n_lo: int = 4, n_hi: int = 8):
        n = rng.randint(n_lo, n_hi)
        k = rng.randint(1, n - 1)
        a = rng.randint(1, 3)
        # Coefficient of x^(n−k) in (x + a)^n is C(n, k)·a^k.
        coef = _math.comb(n, k) * a ** k
        return MathDraw(
            rf"(x + {a})^{{{n}}}", str(coef),
            prompt=f"จงหาสัมประสิทธิ์ของ x^{n - k} ในการกระจาย",
            distractors=[str(_math.comb(n, k)), str(_math.comb(n, k) * a),
                         str(_math.comb(n, k + 1) * a ** (k + 1))])


@question_type("math.binomial_apply_m5", display_name={"th": "นำทฤษฎีบททวินามไปใช้ (นับ ประมาณค่า เศษจากการหาร)"},
               level={"th": "ม.5"}, topic="ทฤษฎีบททวินาม")
class BinomialApplyM5(QuestionType):
    def build(self, rng: Random, **params) -> GeneratedQuestion:
        kind = rng.randrange(3)
        if kind == 0:
            n = rng.randint(4, 10)
            stem = (f"ร้านมีท็อปปิง {n} ชนิด ลูกค้าเลือกใส่กี่ชนิดก็ได้ (ไม่ใส่เลยก็ได้) จะได้ไอศกรีมต่างกันกี่แบบ "
                    f"(ใช้ C(n,0) + C(n,1) + … + C(n,n))")
            return maths([text(stem)], str(2 ** n), _nums(2 ** n, 2 ** n - 1, n * n, math.factorial(n) if n < 7
                                                          else 2 * n, lo=1), self.topic)
        if kind == 1:
            n = rng.randint(3, 19)
            last = (1 + 10 * n) % 100
            stem = f"เลขสองหลักสุดท้ายของ 11^{n} คือจำนวนใด (เขียน 11^{n} = (10 + 1)^{n})"
            return maths([text(stem)], f"{last:02d}", [f"{(11 * n) % 100:02d}", f"{(10 * n) % 100:02d}",
                                                       f"{(1 + n) % 100:02d}", "01"], self.topic)
        n = rng.randint(3, 8)
        approx = Decimal(1) + Decimal(n) / 100 + Decimal(math.comb(n, 2)) / 10_000
        stem = (f"ใช้สามพจน์แรกของการกระจาย (1 + 0.01)^{n} ประมาณค่า (1.01)^{n} ได้เท่าใด")
        wrongs = [Decimal(1) + Decimal(n) / 100, Decimal(1) + Decimal(n) / 100 + Decimal(n) / 10_000,
                  Decimal(1) + Decimal(n) / 10 + Decimal(math.comb(n, 2)) / 100]
        return maths([text(stem)], f"{approx:.4f}", [f"{w:.4f}" for w in wrongs], self.topic)


@question_type("math.binomial_middle_coefficient",
               display_name={"th": "ผลบวกสัมประสิทธิ์ทวินาม"},
               level={"th": "ม.5"}, topic="ทฤษฎีบททวินาม")
class BinomialSumCoefficients(MathType):
    """Setting x = 1 turns the whole expansion into 2ⁿ — a substitution trick."""

    def expr(self, rng: Random, n_lo: int = 3, n_hi: int = 12):
        n = rng.randint(n_lo, n_hi)
        return MathDraw(
            rf"(x + 1)^{{{n}}}", str(2 ** n),
            prompt="ผลบวกของสัมประสิทธิ์ทุกพจน์ในการกระจายนี้เท่ากับเท่าใด",
            distractors=[str(2 ** n - 1), str(n ** 2), str(2 * n)])

from fractions import Fraction  # noqa: E402
from math import comb  # noqa: E402

from otk.core.provenance import Provenance  # noqa: E402
from otk.core.registry import QuestionType, question_type  # noqa: E402
from otk.kit.math_problems import MathType, WordProblem  # noqa: E402
from otk.kit.math_problems import frac_tex, poly_tex  # noqa: E402
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

# ── More binomial theorem (2026-11): the constant term of (x + 1/x)^2n, how many terms, a coefficient in
# (ax + 1)^n, the sum of all coefficients, the (r + 1)th term, and the middle of a row of Pascal's triangle ──


@question_type("math.binomial_constant_term_m5", display_name={"th": "พจน์ที่ไม่มี x ในการกระจาย (x + 1/x)ⁿ"}, level=LEVEL,
               topic="ทฤษฎีบททวินาม")
class BinomialConstantTermM5(MathType):
    def expr(self, rng: Random):
        k = rng.randint(2, 6)
        right = comb(2 * k, k)
        # The neighbouring coefficient; the power itself; two to the power.
        return MathDraw(rf"\left(x + \frac{{1}}{{x}}\right)^{{{2 * k}}}", str(right), prompt="พจน์ที่ไม่มี x ในการกระจายนี้เท่ากับเท่าใด",
                        distractors=_nk5(comb(2 * k, k - 1), 2 * k, 2 ** (2 * k), comb(2 * k, 2), answer=right, lo=1))


@question_type("math.binomial_term_count_m5", display_name={"th": "จำนวนพจน์ในการกระจายทวินาม"}, level=LEVEL, topic="ทฤษฎีบททวินาม")
class BinomialTermCountM5(MathType):
    def expr(self, rng: Random):
        n = rng.randint(4, 20)
        right = n + 1
        return MathDraw(f"(2x - 3y)^{{{n}}}", str(right), prompt="เมื่อกระจายแล้วจะได้กี่พจน์",
                        distractors=_nk5(n, n + 2, 2 * n, 2 ** n if n < 8 else n - 1, answer=right, lo=1))


@question_type("math.coefficient_in_ax_plus_one_m5", display_name={"th": "สัมประสิทธิ์ในการกระจาย (ax + 1)ⁿ"}, level=LEVEL,
               topic="ทฤษฎีบททวินาม")
class CoefficientInAxPlusOneM5(MathType):
    def expr(self, rng: Random):
        a, n = rng.choice((2, 3)), rng.randint(3, 6)
        k = rng.randint(1, n - 1)
        right = comb(n, k) * a ** k
        # a not raised; the binomial coefficient alone; a raised but no coefficient.
        return MathDraw(f"({a}x + 1)^{{{n}}}", _g5(right), prompt=f"สัมประสิทธิ์ของ x ยกกำลัง {k} เท่ากับเท่าใด",
                        distractors=_gk5(comb(n, k) * a, comb(n, k), a ** k, comb(n, k) * a ** (n - k), answer=right))


@question_type("math.sum_of_coefficients_m5", display_name={"th": "ผลบวกของสัมประสิทธิ์ทุกพจน์"}, level=LEVEL, topic="ทฤษฎีบททวินาม")
class SumOfCoefficientsM5(MathType):
    def expr(self, rng: Random):
        a, b, n = rng.randint(1, 3), rng.randint(1, 3), rng.randint(3, 7)
        right = (a + b) ** n
        # Two to the power; the coefficients' sum not raised; n + 1 terms counted.
        return MathDraw(f"({poly_tex((a, 'x'), (b, ''))})^{{{n}}}", _g5(right), prompt="ผลบวกของสัมประสิทธิ์ทุกพจน์เท่ากับเท่าใด",
                        distractors=_gk5(2 ** n, (a + b) * n, n + 1, (a + b) ** (n - 1), answer=right))


@question_type("math.rth_term_coefficient_m5", display_name={"th": "สัมประสิทธิ์ของพจน์ที่ r + 1"}, level=LEVEL, topic="ทฤษฎีบททวินาม")
class RthTermCoefficientM5(MathType):
    def expr(self, rng: Random):
        c, n = rng.randint(1, 3), rng.randint(4, 7)
        r = rng.randint(1, n - 1)
        right = comb(n, r) * c ** r
        # The rth term taken; c not raised; the coefficient alone.
        return MathDraw(f"(x + {c})^{{{n}}}", _g5(right), prompt=f"สัมประสิทธิ์ของพจน์ที่ {r + 1} (นับจากพจน์ที่มี x ยกกำลังสูงสุด) เท่ากับเท่าใด",
                        distractors=_gk5(comb(n, r - 1) * c ** (r - 1), comb(n, r) * c, comb(n, r), comb(n, r + 1) * c ** (r + 1), answer=right))


@question_type("math.pascal_middle_m5", display_name={"th": "จำนวนตรงกลางของแถวในสามเหลี่ยมปาสคาล"}, level=LEVEL,
               topic="ทฤษฎีบททวินาม")
class PascalMiddleM5(WordProblem):
    def expr(self, rng: Random):
        k = rng.randint(2, 6)
        right = comb(2 * k, k)
        prompt = f"สามเหลี่ยมปาสคาลแถวที่ {2 * k} (แถวที่มีสัมประสิทธิ์ของ (a + b) ยกกำลัง {2 * k}) จำนวนที่อยู่ตรงกลางเท่ากับเท่าใด"
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_nk5(comb(2 * k, k - 1), 2 ** (2 * k), comb(2 * k - 1, k), 2 * k, answer=right, lo=1))
