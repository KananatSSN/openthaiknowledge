"""ทศนิยมและเศษส่วน

คณิตศาสตร์ · ม.1 · สสวท. พื้นฐาน
Indicators: ค 1.1 ม.1/*

Sets moved here from: math_m1.
"""

from __future__ import annotations

import math
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


# ── More decimals and fractions (2026-11): converting both ways, comparing, rounding, the repeating bar,
# money with decimals, and ordering fractions with decimals ──

from otk.kit.math_problems import WordProblem  # noqa: E402


def _dec(numerator: int, places: int) -> str:
    """numerator / 10^places as a decimal string, trailing zeros dropped: (375, 3) → 0.375, (-5, 1) → -0.5."""
    sign = "-" if numerator < 0 else ""
    n = abs(numerator)
    whole, frac = divmod(n, 10 ** places)
    digits = str(frac).rjust(places, "0").rstrip("0")
    return f"{sign}{whole}" + (f".{digits}" if digits else "")


# Fractions with terminating decimals: (numerator, denominator), the decimal in thousandths.
_TERMINATING = tuple((n, d) for d in (2, 4, 5, 8, 20, 25) for n in range(1, 2 * d) if math.gcd(n, d) == 1 and n != d)


@question_type("math.fraction_to_decimal_m1", display_name={"th": "เขียนเศษส่วนเป็นทศนิยม"},
               level=LEVEL, topic=_DF_TOPIC)
class FractionToDecimalM1(WordProblem):
    def expr(self, rng: Random):
        n, d = rng.choice(_TERMINATING)
        sign = rng.choice((1, 1, -1))
        thousandths = sign * n * 1000 // d
        right = _dec(thousandths, 3)
        # The digits of the fraction side by side; one place out; the denominator over the numerator.
        wrongs = [f"{'-' if sign < 0 else ''}{n}.{d}", _dec(thousandths * 10, 3), _dec(sign * d * 1000 // n, 3)]
        return MathDraw(frac_tex(Fraction(sign * n, d)), right, prompt="เขียนเป็นทศนิยมได้เท่าใด",
                        distractors=[w for w in dict.fromkeys(wrongs) if w != right])


@question_type("math.decimal_to_fraction_m1", display_name={"th": "เขียนทศนิยมเป็นเศษส่วนอย่างต่ำ"},
               level=LEVEL, topic=_DF_TOPIC)
class DecimalToFractionM1(WordProblem):
    def expr(self, rng: Random):
        n, d = rng.choice([t for t in _TERMINATING if t[0] < t[1]])
        thousandths = n * 1000 // d
        decimal = _dec(thousandths, 3)
        places = len(decimal.split(".")[1])
        right = Fraction(n, d)
        # Not reduced; the digits over 100; the digits over the wrong power of ten.
        digits = int(decimal.split(".")[1])
        wrongs = [rf"\frac{{{digits}}}{{{10 ** places}}}", rf"\frac{{{digits}}}{{{10 ** (places + 1)}}}",
                  frac_tex(Fraction(digits, 10 ** max(1, places - 1))) if places > 1 else rf"\frac{{{digits}}}{{100}}"]
        right_tex = frac_tex(right)
        return MathDraw(decimal, right_tex, prompt="เขียนเป็นเศษส่วนอย่างต่ำได้เท่าใด",
                        distractors=[w for w in dict.fromkeys(wrongs) if w != right_tex])


@question_type("math.compare_decimals_m1", display_name={"th": "เปรียบเทียบทศนิยม"},
               level=LEVEL, topic=_DF_TOPIC)
class CompareDecimalsM1(QuestionType):
    """0.5 > 0.45 > 0.405 > 0.054: compare place by place, not by how many digits. The four numbers are the
    four choices, so no other draw's number can slip in."""

    def build(self, rng: Random) -> GeneratedQuestion:
        a, b = rng.randint(1, 9), rng.randint(1, 9)
        while a == b:
            b = rng.randint(1, 9)
        values = [a * 100, a * 10 + b, a * 100 + b, b * 10 + a]   # in thousandths: 0.a, 0.0ab, 0.a0b, 0.0ba
        values = list(dict.fromkeys(values))
        rng.shuffle(values)
        largest = rng.random() < 0.5
        right = max(values) if largest else min(values)
        return _maths([text(f"จำนวนในข้อใด{'มากที่สุด' if largest else 'น้อยที่สุด'}")], _dec(right, 3),
                      [_dec(v, 3) for v in values if v != right], self.topic)


@question_type("math.round_decimal_m1", display_name={"th": "ปัดเศษทศนิยม"},
               level=LEVEL, topic=_DF_TOPIC)
class RoundDecimalM1(WordProblem):
    def expr(self, rng: Random):
        value = rng.randint(1000, 99999)       # in thousandths
        places = rng.choice((1, 2))
        step = 10 ** (3 - places)
        down = value // step * step
        up = down + step
        right = up if value - down >= step // 2 else down

        def fixed(thousandths: int) -> str:
            """Exactly `places` decimals, as the answer to a rounding question is written: 13.0, 4.50."""
            whole, frac = divmod(thousandths, 1000)
            return f"{whole}." + str(frac).rjust(3, "0")[:places]

        prompt = f"ปัดเศษ {_dec(value, 3)} ให้เป็นทศนิยม {places} ตำแหน่ง"
        # Rounded the other way; one place more than asked; one step further.
        other = down if right == up else up
        wrongs = [fixed(other), _dec(value // 10 * 10, 3) if places == 1 else fixed(right + step), fixed(right + step)
                  if places == 1 else fixed(right - step)]
        return MathDraw("", fixed(right), prompt=prompt,
                        distractors=[w for w in dict.fromkeys(wrongs) if w != fixed(right)])


@question_type("math.repeating_bar_m1", display_name={"th": "เขียนทศนิยมซ้ำด้วยจุดหรือขีด"},
               level=LEVEL, topic=_DF_TOPIC)
class RepeatingBarM1(WordProblem):
    """0.272727… repeats 27, so the bar goes over 27; 0.1666… repeats only the 6."""

    def expr(self, rng: Random):
        if rng.random() < 0.5:
            a, b = rng.sample(range(1, 10), 2)
            shown = f"0.{a}{b}{a}{b}{a}{b}…"
            right = rf"0.\overline{{{a}{b}}}"
            wrongs = [rf"0.{a}\overline{{{b}}}", rf"0.\overline{{{a}}}{b}", rf"0.\overline{{{a}{b}{a}}}"]
        else:
            a, b = rng.sample(range(1, 10), 2)
            shown = f"0.{a}{b}{b}{b}{b}…"
            right = rf"0.{a}\overline{{{b}}}"
            wrongs = [rf"0.\overline{{{a}{b}}}", rf"0.\overline{{{a}}}", rf"0.{a}{b}\overline{{{b}{b}}}"]
        return MathDraw("", right, prompt=f"{shown} เขียนในรูปทศนิยมซ้ำได้อย่างไร", distractors=wrongs)


@question_type("math.decimal_money_m1", display_name={"th": "โจทย์ปัญหาทศนิยมเกี่ยวกับเงิน"},
               level=LEVEL, topic=_DF_TOPIC)
class DecimalMoneyM1(WordProblem):
    def expr(self, rng: Random):
        price = rng.randint(105, 2995) // 5 * 5        # in satang
        count = rng.randint(2, 6)
        cost = price * count
        paid = (cost // 10000 + 1) * 10000 if cost % 10000 else cost + 10000
        paid = max(paid, 5000) if cost <= 5000 else paid
        change = paid - cost
        prompt = (f"ซื้อของ {count} ชิ้น ราคาชิ้นละ {_dec(price, 2)} บาท จ่ายธนบัตร {paid // 100} บาท "
                  f"ได้เงินทอนกี่บาท")
        # One item only; the cost itself; the decimal point dropped one place.
        wrongs = [paid - price, cost, change * 10 if change * 10 < paid else change + 100]
        return MathDraw("", _dec(change, 2), prompt=prompt,
                        distractors=[_dec(w, 2) for w in dict.fromkeys(wrongs) if w != change and w > 0])


@question_type("math.order_fractions_decimals_m1", display_name={"th": "เรียงลำดับเศษส่วนและทศนิยม"},
               level=LEVEL, topic=_DF_TOPIC)
class OrderFractionsDecimalsM1(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        while True:
            picks = rng.sample(_TERMINATING, 4)
            values = [Fraction(n, d) for n, d in picks]
            if len(set(values)) == 4 and all(v < 2 for v in values):
                break
        shown = [frac_tex(v) if i % 2 == 0 else _dec(v.numerator * 1000 // v.denominator, 3)
                 for i, v in enumerate(values)]
        largest = rng.random() < 0.5
        i = values.index(max(values) if largest else min(values))
        return _maths([text(f"จำนวนในข้อใด{'มากที่สุด' if largest else 'น้อยที่สุด'}")], shown[i],
                      [s for n, s in enumerate(shown) if n != i], self.topic)
