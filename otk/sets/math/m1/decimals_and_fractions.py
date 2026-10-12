"""ทศนิยมและเศษส่วน

คณิตศาสตร์ · ม.1 · สสวท. พื้นฐาน
Indicators: ค 1.1 ม.1/*

Sets moved here from: math_m1.
"""

from __future__ import annotations

from decimal import Decimal
from fractions import Fraction
from random import Random

from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.math_problems import MathDraw, MathType, frac_tex
from otk.sets._support.math_m1 import LEVEL
from otk.sets._support.math_p2 import _maths
from otk.sets._support.math_p5 import dstr

PROVENANCE = Provenance("original")


def signed(n) -> str:
    """-3 -> (-3) so a negative operand reads unambiguously after a sign."""
    return f"({n})" if str(n).startswith("-") else str(n)


_DF_TOPIC = "ทศนิยมและเศษส่วน"


def _terminates(f: Fraction) -> bool:
    d = f.denominator
    for p in (2, 5):
        while d % p == 0:
            d //= p
    return d == 1


@question_type("math.terminating_or_repeating_m1",
               display_name={"th": "เศษส่วนใดเป็นทศนิยมรู้จบหรือทศนิยมซ้ำ"},
               level=LEVEL, topic=_DF_TOPIC)
class TerminatingOrRepeatingM1(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        want_repeat = rng.random() < 0.5
        good, bad = [], []
        while len(good) < 1 or len(set(bad)) < 3:
            d = rng.choice((3, 4, 6, 7, 8, 9, 11, 12, 15, 16, 20, 24, 25, 30, 40, 50))
            n = rng.randint(1, d - 1)
            f = Fraction(n, d)
            if f.denominator == 1:
                continue
            # Show it unreduced sometimes: 6/15 looks repeating but is 2/5.
            shown = rf"\frac{{{n}}}{{{d}}}"
            (bad if _terminates(f) == want_repeat else good).append(shown)
        return _maths([text("เศษส่วนใดเขียนเป็นทศนิยม" + ("ซ้ำ" if want_repeat else "รู้จบ") + "ได้")],
                      good[0], list(dict.fromkeys(bad))[:3], self.topic)


@question_type("math.signed_decimal_ops_m1",
               display_name={"th": "การบวก ลบ คูณ หารทศนิยมที่เป็นจำนวนลบ"},
               level=LEVEL, topic=_DF_TOPIC)
class SignedDecimalOpsM1(MathType):
    def expr(self, rng: Random):
        a = Decimal(rng.randint(-99, 99) or 7) / 10
        b = Decimal(rng.choice([x for x in range(-40, 41) if x not in (0, 10, -10)])) / 10
        op = rng.choice("+-*/")
        if op == "/":
            a = (a * b).quantize(Decimal("0.01"))
            ans = a / b
            tex = rf"{signed(dstr(a))} \div {signed(dstr(b))}"
        elif op == "*":
            ans = a * b
            tex = rf"{signed(dstr(a))} \times {signed(dstr(b))}"
        elif op == "+":
            ans = a + b
            tex = rf"{signed(dstr(a))} + {signed(dstr(b))}"
        else:
            ans = a - b
            tex = rf"{signed(dstr(a))} - {signed(dstr(b))}"
        wrongs = [-ans, ans * 10, ans / 10, a + b if op != "+" else a - b]
        return MathDraw(tex, dstr(ans), prompt="จงหาผลลัพธ์",
                        distractors=[dstr(w) for w in dict.fromkeys(wrongs) if w != ans])


@question_type("math.repeating_decimal_to_fraction_m1",
               display_name={"th": "เขียนทศนิยมซ้ำเป็นเศษส่วน"},
               level=LEVEL, topic=_DF_TOPIC)
class RepeatingDecimalToFractionM1(MathType):
    def expr(self, rng: Random):
        kind = rng.randrange(3)
        if kind == 0:                        # 0.aaa...
            a = rng.randint(1, 8)
            value = Fraction(a, 9)
            tex = rf"0.\dot{{{a}}}"
            wrongs = [Fraction(a, 10), Fraction(a, 99), Fraction(a, 90)]
        elif kind == 1:                      # 0.abab...
            ab = rng.choice([n for n in range(10, 99) if n % 11])
            value = Fraction(ab, 99)
            tex = rf"0.\dot{{{ab // 10}}}\dot{{{ab % 10}}}"
            wrongs = [Fraction(ab, 100), Fraction(ab, 90), Fraction(ab, 9) if ab < 9 else
                      Fraction(ab, 999)]
        else:                                # 0.abbb...
            a, b = rng.randint(1, 9), rng.randint(1, 8)
            if a == b:
                a = a % 9 + 1
            value = Fraction(10 * a + b - a, 90)
            tex = rf"0.{a}\dot{{{b}}}"
            wrongs = [Fraction(10 * a + b, 99), Fraction(10 * a + b, 90), Fraction(10 * a + b, 100)]
        # Reading the digits as a terminating decimal comes first.
        right = frac_tex(value)
        return MathDraw(tex, right, prompt="เขียนทศนิยมซ้ำนี้เป็นเศษส่วนอย่างต่ำ",
                        distractors=[t for t in dict.fromkeys(frac_tex(w) for w in wrongs)
                                     if t != right])
