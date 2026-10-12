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
