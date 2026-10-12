"""เลขยกกำลัง

คณิตศาสตร์ · ม.2 · สสวท. พื้นฐาน
Indicators: ค 1.1 ม.2/*

Sets moved here from: math, math_algebra, math_formats_hi.
"""

from __future__ import annotations

from random import Random

from otk.core.content import math as content_math
from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.math_problems import MathDraw, MathType
from otk.sets._support.math_algebra import _pow
from otk.sets._support.math_diagrams import _math_q

PROVENANCE = Provenance("original")


@question_type("math.negative_exponent",
               display_name={"th": "เลขชี้กำลังติดลบ"}, level={"th": "ม.2"},
               topic="เลขยกกำลัง")
class NegativeExponent(MathType):
    def expr(self, rng: Random, base_lo: int = 2, base_hi: int = 9,
             n_lo: int = 1, n_hi: int = 4):
        base = rng.randint(base_lo, base_hi)
        n = rng.randint(n_lo, n_hi)
        return MathDraw(rf"{base}^{{-{n}}}", rf"\frac{{1}}{{{base ** n}}}",
                        hint=r"a^{-n} = \frac{1}{a^n}")


@question_type("math.power_of_product",
               display_name={"th": "กำลังของผลคูณ"}, level={"th": "ม.2"},
               topic="เลขยกกำลัง")
class PowerOfProduct(MathType):
    def expr(self, rng: Random, base_lo: int = 2, base_hi: int = 6,
             n_lo: int = 2, n_hi: int = 4):
        a, b = rng.randint(base_lo, base_hi), rng.randint(base_lo, base_hi)
        n = rng.randint(n_lo, n_hi)
        return MathDraw(rf"\left({a} \cdot {b}\right)^{{{n}}}",
                        rf"{a ** n} \cdot {b ** n} = {(a * b) ** n}",
                        hint=r"(ab)^n = a^n \cdot b^n")


@question_type("math.power_of_quotient",
               display_name={"th": "กำลังของเศษส่วน"}, level={"th": "ม.2"},
               topic="เลขยกกำลัง")
class PowerOfQuotient(MathType):
    def expr(self, rng: Random):
        a = rng.randint(2, 8)
        b = rng.choice([x for x in range(2, 9) if x != a])
        n = rng.randint(2, 4)
        return MathDraw(rf"\left(\frac{{{a}}}{{{b}}}\right)^{{{n}}}",
                        rf"\frac{{{a ** n}}}{{{b ** n}}}",
                        hint=r"\left(\frac{a}{b}\right)^n = \frac{a^n}{b^n}")


@question_type("math.negative_exponent_evaluate",
               display_name={"th": "หาค่าเลขยกกำลังติดลบ"},
               level={"th": "ม.2"}, topic="เลขยกกำลัง")
class NegativeExponentEvaluate(MathType):
    def expr(self, rng: Random, base_lo: int = 2, base_hi: int = 6,
             exp_hi: int = 4):
        base = rng.randint(base_lo, base_hi)
        e = rng.randint(1, exp_hi)
        return MathDraw(
            rf"{base}^{{-{e}}}", rf"\frac{{1}}{{{base ** e}}}",
            prompt="จงหาค่า",
            # A negative exponent is a reciprocal, not a negative number.
            distractors=[f"-{base ** e}", str(base ** e),
                         rf"-\frac{{1}}{{{base ** e}}}"])


@question_type("math.hard_product_then_power",
               display_name={"th": "โจทย์ผสม: คูณแล้วยกกำลัง"}, level={"th": "ม.2"},
               topic="เลขยกกำลัง")
class HardProductThenPower(MathType):
    def expr(self, rng: Random):
        base = rng.randint(2, 5)
        m, n = rng.randint(1, 4), rng.randint(1, 4)
        p = rng.randint(2, 3)
        return MathDraw(
            rf"\left({base}^{{{m}}} \cdot {base}^{{{n}}}\right)^{{{p}}}",
            rf"{base}^{{{(m + n) * p}}}", hint=r"\text{product rule, then power rule}")


@question_type("math.hard_quotient_then_power",
               display_name={"th": "โจทย์ผสม: หารแล้วยกกำลัง"}, level={"th": "ม.2"},
               topic="เลขยกกำลัง")
class HardQuotientThenPower(MathType):
    def expr(self, rng: Random):
        base = rng.randint(2, 5)
        m = rng.randint(3, 7)
        n = rng.randint(1, m - 1)
        p = rng.randint(2, 3)
        return MathDraw(
            rf"\left(\frac{{{base}^{{{m}}}}}{{{base}^{{{n}}}}}\right)^{{{p}}}",
            rf"{base}^{{{(m - n) * p}}}", hint=r"\text{quotient rule, then power rule}")


@question_type("math.hard_product_with_negative",
               display_name={"th": "โจทย์ผสม: คูณกับเลขชี้กำลังติดลบ"}, level={"th": "ม.2"},
               topic="เลขยกกำลัง")
class HardProductWithNegative(MathType):
    def expr(self, rng: Random):
        base = rng.randint(2, 7)
        n = rng.randint(1, 4)
        m = rng.randint(n + 1, n + 5)
        return MathDraw(rf"{base}^{{{m}}} \cdot {base}^{{-{n}}}", rf"{base}^{{{m - n}}}",
                        hint=r"\text{negative exponent, then product rule}")


@question_type("math.hard_power_then_negative",
               display_name={"th": "โจทย์ผสม: กำลังซ้อนติดลบ"}, level={"th": "ม.2"},
               topic="เลขยกกำลัง")
class HardPowerThenNegative(MathType):
    def expr(self, rng: Random):
        base = rng.randint(2, 4)
        m, n = rng.randint(2, 3), rng.randint(1, 2)
        return MathDraw(rf"\left({base}^{{{m}}}\right)^{{-{n}}}",
                        rf"\frac{{1}}{{{base ** (m * n)}}}",
                        hint=r"\text{power rule, then negative exponent}")


@question_type("math.negative_exponent_simplify",
               display_name={"th": "จัดรูปนิพจน์ที่มีเลขชี้กำลังติดลบ"},
               level={"th": "ม.2"}, topic="เลขยกกำลัง")
class NegativeExponentSimplify(MathType):
    def expr(self, rng: Random, exp_hi: int = 7):
        m, n = rng.randint(1, exp_hi), rng.randint(1, exp_hi)
        # x^m · x^(−n) = x^(m−n)
        e = m - n
        answer = ("1" if e == 0 else _pow("x", e) if e > 0
                  else rf"\frac{{1}}{{{_pow('x', -e)}}}")
        return MathDraw(
            rf"{_pow('x', m)} \cdot x^{{-{n}}}", answer, prompt="จงจัดรูป",
            distractors=[_pow("x", m + n), f"x^{{{n - m}}}", f"x^{{{-m - n}}}"])


@question_type("math.missing_exponent_m2", display_name={"th": "หาเลขชี้กำลังที่หายไป"},
               level={"th": "ม.2"}, topic="เลขยกกำลัง")
class MissingExponentM2(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        a = rng.choice((2, 3, 5, 7, 10, "a", "x"))
        m = rng.randint(2, 6)
        form = rng.randrange(4)
        if form == 0:                      # a^□ · a^m = a^n
            k = rng.randint(-4, 7)
            n = k + m
            tex = rf"{a}^{{\square}} \cdot {a}^{{{m}}} = {a}^{{{n}}}"
            wrongs = [n + m, n * m, -k]
        elif form == 1:                    # (a^□)^m = a^n
            k = rng.choice([v for v in range(-4, 6) if v not in (0, 1)])
            n = k * m
            tex = rf"\left({a}^{{\square}}\right)^{{{m}}} = {a}^{{{n}}}"
            wrongs = [n - m, n + m, n * m]
        elif form == 2:                    # a^n / a^□ = a^m
            k = rng.randint(-3, 8)
            n = m + k
            tex = rf"\frac{{{a}^{{{n}}}}}{{{a}^{{\square}}}} = {a}^{{{m}}}"
            wrongs = [n + m, m - n, n * m]
        else:                              # a^□ = 1 / a^m
            k = -m
            tex = rf"{a}^{{\square}} = \frac{{1}}{{{a}^{{{m}}}}}"
            wrongs = [m, 1 - m, m + 1]
        wrongs = [str(w) for w in dict.fromkeys(wrongs + [k + 1, k - 1, k + 2]) if w != k]
        return _math_q([text("จงหาจำนวนที่แทน □"), content_math(tex)], str(k), wrongs, self.topic)


@question_type("math.fractional_exponent",
               display_name={"th": "เลขชี้กำลังเศษส่วน (ราก)"}, level={"th": "ม.2"},
               topic="เลขยกกำลัง")
class FractionalExponent(MathType):
    _CANDIDATES = [
        (4, 2, 2), (8, 3, 2), (9, 2, 3), (16, 2, 4), (16, 4, 2),
        (25, 2, 5), (27, 3, 3), (32, 5, 2), (36, 2, 6), (64, 2, 8),
        (64, 3, 4), (64, 6, 2), (81, 2, 9), (81, 4, 3), (100, 2, 10),
        (125, 3, 5), (128, 7, 2), (243, 5, 3),
    ]

    def expr(self, rng: Random):
        base, root, result = rng.choice(self._CANDIDATES)
        return MathDraw(rf"{base}^{{\frac{{1}}{{{root}}}}}", rf"{result}",
                        hint=r"a^{\frac{1}{n}} = \sqrt[n]{a}")


@question_type("math.fractional_exponent_evaluate",
               display_name={"th": "หาค่าเลขชี้กำลังเศษส่วน"},
               level={"th": "ม.2"}, topic="เลขยกกำลัง")
class FractionalExponentEvaluate(MathType):
    def expr(self, rng: Random, base_lo: int = 2, base_hi: int = 5):
        root = rng.choice([2, 3])
        base = rng.randint(base_lo, base_hi)
        power = rng.randint(1, 3)
        n = base ** root                          # so the root is exact
        return MathDraw(
            rf"{n}^{{\frac{{{power}}}{{{root}}}}}", str(base ** power),
            prompt="จงหาค่า",
            distractors=[str(n * power // root if n * power % root == 0
                             else n ** power), str(base * power),
                         str(base ** root)])


@question_type("math.radical_to_exponent", display_name={"th": "เขียนกรณฑ์เป็นเลขชี้กำลัง"},
               level={"th": "ม.2"}, topic="เลขยกกำลัง")
class RadicalToExponent(MathType):
    def expr(self, rng: Random, root_hi: int = 5, power_hi: int = 7):
        root = rng.randint(2, root_hi)
        power = rng.choice([p for p in range(1, power_hi + 1) if p != root])
        radical = (rf"\sqrt{{x^{{{power}}}}}" if root == 2
                   else rf"\sqrt[{root}]{{x^{{{power}}}}}")
        return MathDraw(
            radical, rf"x^{{\frac{{{power}}}{{{root}}}}}",
            prompt="จงเขียนในรูปเลขชี้กำลัง",
            distractors=[rf"x^{{\frac{{{root}}}{{{power}}}}}",
                         f"x^{{{power * root}}}", f"x^{{{power}}}"])
