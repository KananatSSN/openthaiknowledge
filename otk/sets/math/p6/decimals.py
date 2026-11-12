"""ทศนิยม

คณิตศาสตร์ · ป.6 · สสวท. พื้นฐาน
Indicators: ค 1.1 ป.6/*

Sets moved here from: math, math_formats, math_gaps_indicators.
"""

from __future__ import annotations

import math
from decimal import Decimal
from random import Random

from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, MathType, WordProblem
from otk.sets._support.math_diagrams import _math_q
from otk.sets._support.math_gaps_indicators import _cents, _dec

PROVENANCE = Provenance("original")


_TERMINATING_DENS = [2, 4, 5, 8, 10, 20, 25, 40, 50]


@question_type("math.fraction_to_decimal",
               display_name={"th": "เศษส่วนเป็นทศนิยม"}, level={"th": "ป.6"},
               topic="ทศนิยม")
class FractionToDecimal(MathType):
    def expr(self, rng: Random):
        q = rng.choice(_TERMINATING_DENS)
        p = rng.choice([n for n in range(1, q) if math.gcd(n, q) == 1])
        return MathDraw(rf"\frac{{{p}}}{{{q}}}", rf"{p / q:g}",
                        prompt="จงเขียนเป็นรูปทศนิยม")


@question_type("math.decimal_to_fraction",
               display_name={"th": "ทศนิยมเป็นเศษส่วน"}, level={"th": "ป.6"},
               topic="ทศนิยม")
class DecimalToFraction(MathType):
    def expr(self, rng: Random):
        q = rng.choice(_TERMINATING_DENS)
        p = rng.choice([n for n in range(1, q) if math.gcd(n, q) == 1])
        return MathDraw(rf"{p / q:g}", rf"\frac{{{p}}}{{{q}}}",
                        prompt="จงเขียนเป็นรูปเศษส่วน")


@question_type("math.divide_decimal_by_decimal_p6", display_name={"th": "หารทศนิยมด้วยทศนิยม"},
               level={"th": "ป.6"}, topic="ทศนิยม")
class DivideDecimalByDecimalP6(WordProblem):
    """a ÷ b with b a one-place decimal and a quotient of at most two places,
    so the dividend has at most three."""

    def expr(self, rng: Random):
        b = Decimal(rng.choice((2, 3, 4, 5, 6, 8, 12, 15, 25))) / 10
        q = Decimal(rng.randint(12, 480)) / rng.choice((1, 10, 100))
        a = q * b
        shown = format(a.normalize(), "f")
        answer = format(q.normalize(), "f")
        # The decimal point moved one place the wrong way, either way.
        wrongs = [format((q * 10).normalize(), "f"), format((q / 10).normalize(), "f"),
                  format((q * 100).normalize(), "f")]
        return MathDraw(rf"{shown} \div {format(b.normalize(), 'f')}", answer, prompt="จงหาผลหาร",
                        distractors=[w for w in dict.fromkeys(wrongs) if w != answer])


@question_type("math.decimal_ops",
               display_name={"th": "ทศนิยม: สี่การดำเนินการ"}, level={"th": "ป.6"},
               topic="ทศนิยม")
class DecimalOps(MathType):
    def expr(self, rng: Random, dp: int = 1):
        dp = max(1, min(int(dp), 2))
        s = 10 ** dp
        fmt = lambda scaled, scale=s: f"{scaled / scale:g}"
        op = rng.choice("+-*/")
        if op == "+":
            ai, bi = rng.randint(s, 99 * s), rng.randint(s, 99 * s)
            return rf"{fmt(ai)} + {fmt(bi)}", fmt(ai + bi)
        if op == "-":
            ai, bi = rng.randint(s, 99 * s), rng.randint(s, 99 * s)
            if ai < bi:
                ai, bi = bi, ai
            return rf"{fmt(ai)} - {fmt(bi)}", fmt(ai - bi)
        if op == "*":
            ai, b = rng.randint(2, 9 * s), rng.randint(2, 9)
            return rf"{fmt(ai)} \times {b}", fmt(ai * b)
        bi, q = rng.randint(s + 1, 9 * s), rng.randint(2, 9)
        return rf"{fmt(bi * q)} \div {fmt(bi)}", str(q)


@question_type("math.decimal_word_problem_p6", display_name={"th": "โจทย์ปัญหาการหารทศนิยม"},
               level={"th": "ป.6"}, topic="ทศนิยม")
class DecimalWordProblemP6(QuestionType):
    invent_numbers = True  # computed answer: near values on the short side cannot be right
    def build(self, rng: Random) -> GeneratedQuestion:
        kind = rng.randrange(4)
        if kind == 0:
            k = rng.randint(3, 8)
            each = rng.randint(105, 480) / 100
            total = round(each * k, 2)
            stem = f"ริบบิ้นยาว {total:g} เมตร ตัดเป็น {k} ท่อนยาวเท่า ๆ กัน แต่ละท่อนยาวกี่เมตร"
            ans = each
        elif kind == 1:
            k = rng.randint(3, 6)
            each = rng.randint(4550, 12975) / 100
            each = round(each / 0.25) * 0.25
            total = round(each * k, 2)
            stem = f"เพื่อน {k} คนหารค่าอาหาร {total:,.2f} บาท เท่า ๆ กัน จ่ายคนละกี่บาท"
            ans = each
        elif kind == 2:
            price = rng.randint(24, 65)
            kg = rng.choice((0.5, 1.5, 2.5, 0.25, 1.25, 3.5))
            stem = f"ซื้อส้มกิโลกรัมละ {price} บาท จ่ายไป {price * kg:g} บาท ได้ส้มกี่กิโลกรัม"
            ans = kg
        else:
            glasses = rng.randint(4, 9)
            each = rng.choice((0.15, 0.2, 0.25, 0.3, 0.35))
            litres = round(each * glasses, 2)
            stem = f"น้ำผลไม้ {litres:g} ลิตร เทใส่แก้ว {glasses} ใบเท่า ๆ กัน แต่ละใบมีน้ำผลไม้กี่ลิตร"
            ans = each

        def fmt(x: float) -> str:
            return f"{x:,.2f}" if kind == 1 else f"{x:g}"

        # The decimal point one place off either way; multiplying instead.
        return _math_q([text(stem)], fmt(ans), [fmt(ans * 10), fmt(ans / 10), fmt(ans + 1),
                                                fmt(round(ans * 2, 2))], self.topic)


@question_type("math.decimal_three_step_word_p6", display_name={"th": "โจทย์ปัญหาทศนิยม 3 ขั้นตอน"},
               level={"th": "ป.6"}, topic="ทศนิยม")
class DecimalThreeStepWordP6(WordProblem):
    def expr(self, rng: Random):
        name = rng.choice(_story.NAMES)
        kind = rng.randrange(3)
        if kind == 0:
            n, m = rng.randint(2, 5), rng.randint(2, 4)
            p, r = _cents(rng, 8, 35), _cents(rng, 5, 20)
            spent = n * p + m * r
            paid = 500 if spent > 200 else 200 if spent > 100 else 100
            value = Decimal(paid) - spent
            prompt = (f"{name}ซื้อสมุด {n} เล่ม ราคาเล่มละ {_dec(p, 2)} บาท และปากกา {m} ด้าม "
                      f"ราคาด้ามละ {_dec(r, 2)} บาท จ่ายด้วยธนบัตรใบละ {paid} บาท จะได้เงินทอนกี่บาท")
            wrongs = [spent, Decimal(paid) - n * p, Decimal(paid) - p - r]
        elif kind == 1:
            # Cloth cut into pieces, the rest shared equally: (L − n·a) ÷ k.
            k, n = rng.randint(2, 5), rng.randint(2, 4)
            share = Decimal(rng.randint(15, 120)) / 100
            a = Decimal(rng.randint(40, 150)) / 100
            total = n * a + k * share
            value = share
            prompt = (f"ผ้ายาว {_dec(total, 2)} เมตร ตัดเป็นผ้าเช็ดหน้าผืนละ {_dec(a, 2)} เมตร {n} ผืน "
                      f"แล้วแบ่งผ้าที่เหลือเป็น {k} ส่วนเท่า ๆ กัน แต่ละส่วนยาวกี่เมตร")
            wrongs = [total - n * a, (total - a) / k, total / k - n * a]
        else:
            # A shared bill after a discount: (n·p − d) ÷ k.
            while True:
                n, p = rng.randint(2, 4), _cents(rng, 150, 400)
                d = Decimal(rng.choice((20, 30, 50)))
                ks = [k for k in (2, 3, 4, 5) if (n * p - d) * 100 % k == 0]
                if ks:
                    break
            k = rng.choice(ks)
            value = (n * p - d) / k
            prompt = (f"เพื่อน {k} คนสั่งพิซซ่า {n} ถาด ราคาถาดละ {_dec(p, 2)} บาท ได้ส่วนลด {d} บาท "
                      f"แล้วหารค่าอาหารเท่า ๆ กัน จ่ายคนละกี่บาท")
            wrongs = [n * p / k, (n * p + d) / k, n * p - d]
        value = value.quantize(Decimal("0.01"))
        return MathDraw("", _dec(value, 2), prompt=prompt,
                        distractors=[_dec(w.quantize(Decimal("0.01")), 2) for w in dict.fromkeys(wrongs)
                                     if w.quantize(Decimal("0.01")) != value and w > 0])

from fractions import Fraction  # noqa: E402

from otk.core.registry import QuestionType, question_type  # noqa: E402
from otk.kit.math_problems import MathType, WordProblem  # noqa: E402
from otk.sets._support.math_p4 import as_mixed  # noqa: E402
from otk.sets._support.math_p6 import LEVEL  # noqa: E402


def _g6(n: int) -> str:
    """A whole number in TeX with grouped thousands: 4{,}572{,}318."""
    return f"{n:,}".replace(",", "{,}")


def _gk6(*values: int, answer: int, lo: int = 0, hi: int | None = None) -> list[str]:
    """``story.keep`` for grouped numbers."""
    return [_g6(int(v)) for v in _story.keep(*values, answer=answer, lo=lo, hi=hi)]


def _d6(value: int, places: int) -> str:
    """An integer count of 10**-places as a decimal, trailing zeros dropped: (2350, 3) -> 2.35."""
    sign = "-" if value < 0 else ""
    whole, frac = divmod(abs(value), 10 ** places)
    digits = str(frac).rjust(places, "0").rstrip("0") if places else ""
    return f"{sign}{whole}.{digits}" if digits else f"{sign}{whole}"


def _dk6(*values: int, answer: int, places: int, lo: int = 0) -> list[str]:
    """``story.keep`` for decimals held as integer counts of 10**-places."""
    return [_d6(int(v), places) for v in _story.keep(*values, answer=answer, lo=lo)]


def _fk6(*values: Fraction, answer: Fraction) -> list[str]:
    """Distinct fraction distractors as TeX, the answer and non-positive values left out."""
    out: list[str] = []
    for v in values:
        if v > 0 and v != answer and as_mixed(v) not in out:
            out.append(as_mixed(v))
    return out


# ── More decimals (2026-11): a missing factor, rounding a quotient, a price per kilogram, and a
# rectangle's area ──


@question_type("math.decimal_missing_factor_p6", display_name={"th": "หาตัวคูณที่หายไป (ทศนิยม)"},
               level=LEVEL, topic="ทศนิยม")
class DecimalMissingFactorP6(MathType):
    def expr(self, rng: Random):
        b = rng.randint(2, 9)
        right = rng.randint(2, 25)
        product = right * b
        # The product read as tenths; times instead of divided; one off.
        return MathDraw(f"\\square \\times {_d6(b, 1)} = {_d6(product, 1)}", str(right),
                        prompt="จำนวนใดเติมใน □ แล้วทำให้ประโยคเป็นจริง",
                        distractors=_story.keep(product, right * 10, right + 1, b, answer=right, lo=1))


@question_type("math.round_quotient_p6", display_name={"th": "ปัดผลหารเป็นทศนิยมสองตำแหน่ง"},
               level=LEVEL, topic="ทศนิยม")
class RoundQuotientP6(WordProblem):
    def expr(self, rng: Random):
        b = rng.choice((3, 6, 7, 9, 11))
        a = rng.randint(1, 60)
        while a % b == 0:
            a += 1
        thousandths = a * 1000 // b
        right = (thousandths + 5) // 10
        cut = thousandths // 10

        def fixed(x: int) -> str:
            return f"{x // 100}.{x % 100:02d}"

        prompt = f"{a} ÷ {b} ปัดผลหารเป็นทศนิยมสองตำแหน่ง ได้เท่าใด"
        # Cut instead of rounded; one hundredth either way.
        return MathDraw("", fixed(right), prompt=prompt,
                        distractors=[fixed(int(x)) for x in _story.keep(cut, right + 1, right - 1, cut - 1,
                                                                        answer=right, lo=1)])


@question_type("math.price_per_kilo_p6", display_name={"th": "ราคาต่อกิโลกรัมจากน้ำหนักทศนิยม"},
               level=LEVEL, topic="ทศนิยม")
class PricePerKiloP6(WordProblem):
    def expr(self, rng: Random):
        kg = rng.choice((5, 15, 25, 35, 45, 12, 18, 24))
        right = rng.randint(12, 90)
        total = kg * right
        thing = rng.choice(("กุ้ง", "เนื้อหมู", "มะม่วง", "ปลาทู"))
        prompt = f"ซื้อ{thing} {_d6(kg, 1)} กิโลกรัม จ่ายเงิน {total // 10}.{total % 10}0 บาท {thing}ราคากิโลกรัมละกี่บาท"
        # Ten times off either way; the weight read as whole kilograms.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(right * 10, right // 10 if right >= 20 else right + 10,
                                                total // kg + 1, right + 2, answer=right, lo=1))


@question_type("math.decimal_rectangle_area_p6", display_name={"th": "พื้นที่รูปสี่เหลี่ยมผืนผ้า (ทศนิยม)"},
               level=LEVEL, topic="ทศนิยม")
class DecimalRectangleAreaP6(WordProblem):
    def expr(self, rng: Random):
        w = rng.randint(11, 49)
        length = rng.randint(11, 89)
        right = w * length
        prompt = f"แผ่นป้ายรูปสี่เหลี่ยมผืนผ้ากว้าง {_d6(w, 1)} เมตร ยาว {_d6(length, 1)} เมตร มีพื้นที่กี่ตารางเมตร"
        # The point put one place off; the perimeter; the sides added.
        return MathDraw("", _d6(right, 2), prompt=prompt,
                        distractors=_dk6(right * 10, right + w,
                                         20 * (w + length), 10 * (w + length), answer=right, places=2, lo=1))
