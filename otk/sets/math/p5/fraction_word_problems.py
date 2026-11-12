"""โจทย์ปัญหาเศษส่วน

คณิตศาสตร์ · ป.5 · สสวท. พื้นฐาน
Indicators: ค 1.1 ป.5/*

Sets moved here from: math_p5.
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
from otk.kit import story as _story
from otk.sets._support.math_p2 import _maths
from otk.sets._support.math_p4 import _not_equal, as_mixed, fr
from otk.sets._support.math_p5 import LEVEL

PROVENANCE = Provenance("original")


_FW_TOPIC = "โจทย์ปัญหาเศษส่วน"


@question_type("math.fraction_of_amount_p5",
               display_name={"th": "เศษส่วนของจำนวน"},
               level=LEVEL, topic=_FW_TOPIC)
class FractionOfAmountP5(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        p = rng.choice(_story.NAMES)
        d = rng.randint(3, 9)
        n = rng.randint(1, d - 1)
        unit = rng.randint(4, 40)
        whole = d * unit
        part = n * unit
        f = content_math(fr(n, d))
        kind = rng.randrange(3)
        if kind == 0:
            stem = [text(f"{p}มีเงิน {whole} บาท ใช้ไป"), f,
                    text(f"ของเงินทั้งหมด {p}ใช้เงินไปกี่บาท")]
            ans, wrongs = part, [named("part.complement", whole - part),
                                 named("fraction.unit_share_only", unit), whole + part]
        elif kind == 1:
            stem = [text(f"ห้องเรียนมีนักเรียน {whole} คน"), f,
                    text("ของนักเรียนทั้งหมดเป็นนักเรียนหญิง มีนักเรียนชายกี่คน")]
            ans, wrongs = whole - part, [named("part.complement", part), unit, whole - n]
        else:
            # Working back from the part: dividing by n, then multiplying by d.
            stem = [text(f"{p}อ่านหนังสือไปแล้ว {part} หน้า ซึ่งเป็น"), f,
                    text("ของหนังสือทั้งเล่ม หนังสือเล่มนี้มีกี่หน้า")]
            ans, wrongs = whole, [named("fraction.not_worked_back", part * n // d)
                                  if part * n % d == 0 else part + d,
                                  whole - part, part + n]
        return _maths(stem, str(ans), _story.keep(*wrongs, ans + unit, 2 * ans, ans + 1,
                                                  answer=ans, lo=1),
                      self.topic)


@question_type("math.fraction_word_addsub_p5",
               display_name={"th": "โจทย์ปัญหาการบวกลบเศษส่วน (ตัวส่วนไม่เท่ากัน)"},
               level=LEVEL, topic=_FW_TOPIC)
class FractionWordAddSubP5(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        p = rng.choice(_story.NAMES)
        d1, d2 = rng.sample((2, 3, 4, 5, 6, 8), 2)
        x = Fraction(rng.randint(1, d1 - 1), d1) + rng.randint(0, 2)
        y = Fraction(rng.randint(1, d2 - 1), d2) + rng.randint(0, 1)
        if x < y:
            x, y = y, x
        kind = rng.randrange(3)
        tx, ty = as_mixed(x), as_mixed(y)
        if kind == 0:
            stem = [text(f"{p}ซื้อส้ม"), content_math(tx), text("กิโลกรัม และมังคุด"),
                    content_math(ty), text("กิโลกรัม ซื้อผลไม้รวมกี่กิโลกรัม")]
            value = x + y
        elif kind == 1:
            stem = [text("ถังมีน้ำ"), content_math(tx), text("ลิตร ใช้ไป"), content_math(ty),
                    text("ลิตร เหลือน้ำกี่ลิตร")]
            value = x - y
        else:
            z = Fraction(rng.randint(1, 3), rng.choice((2, 4)))
            stem = [text(f"{p}มีริบบิ้นยาว"), content_math(tx), text("เมตร ได้มาเพิ่มอีก"),
                    content_math(ty), text("เมตร แล้วใช้ไป"), content_math(as_mixed(z)),
                    text("เมตร เหลือริบบิ้นยาวกี่เมตร")]
            value = x + y - z
            if value <= 0:
                value, stem = x + y, stem[:4] + [text("เมตร มีริบบิ้นรวมกี่เมตร")]
        answer = as_mixed(value)
        # Adding numerators and denominators is the mistake to name. It is only
        # that mistake in a plain sum; in the other stories the same value mixes
        # two errors, so it is offered but left unnamed.
        naive = as_mixed(Fraction(x.numerator + y.numerator, x.denominator + y.denominator))
        # The opposite operation, which is a clean reversal for the one-step stories.
        swapped = as_mixed(x - y if value != x - y else x + y)
        wrongs = [named("fraction.add_across", naive) if kind == 0 else naive,
                  named("operation.reversed", swapped) if kind in (0, 1) else swapped,
                  as_mixed(value + Fraction(1, max(d1, d2))), as_mixed(value + 1),
                  as_mixed(value + Fraction(1, 2))]
        return _maths(stem, answer, _not_equal(value, wrongs, answer), self.topic)


@question_type("math.fraction_word_muldiv_p5",
               display_name={"th": "โจทย์ปัญหาการคูณหารเศษส่วน"},
               level=LEVEL, topic=_FW_TOPIC)
class FractionWordMulDivP5(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        p = rng.choice(_story.NAMES)
        kind = rng.randrange(6)
        if kind == 3:
            n = rng.randint(2, 6)
            total = Fraction(rng.randint(n + 1, 4 * n), rng.choice((2, 3, 4)))
            stem = [text("น้ำผลไม้"), content_math(as_mixed(total)),
                    text(f"ลิตร แบ่งใส่แก้ว {n} ใบเท่า ๆ กัน แต่ละใบมีน้ำผลไม้กี่ลิตร")]
            value = total / n
            # Multiplying by n; dividing only the numerator's whole part.
            wrongs = [named("operation.reversed", as_mixed(total * n)),
                      as_mixed(total - n) if total > n else as_mixed(total + n),
                      as_mixed(value + Fraction(1, 2)), as_mixed(value * 2)]
        elif kind == 4:
            left = Fraction(rng.randint(1, 3), 4)
            share = Fraction(1, rng.choice((2, 3)))
            stem = [text("เค้กเหลืออยู่"), content_math(as_mixed(left)),
                    text(f"ก้อน {p}กิน"), content_math(as_mixed(share)),
                    text(f"ของเค้กที่เหลือ {p}กินเค้กไปกี่ก้อน")]
            value = left * share
            wrongs = [named("operation.reversed",
                            as_mixed(left - share) if left > share else as_mixed(left + share)),
                      named("operation.reversed", as_mixed(left / share)),
                      named("operation.reversed", as_mixed(left + share)), as_mixed(share),
                      as_mixed(value * 2), as_mixed(value + Fraction(1, 4)),
                      as_mixed(1 - value), as_mixed(value + Fraction(1, 8))]
        elif kind == 5:
            speed = rng.choice((40, 48, 60, 72, 80))
            hours = Fraction(rng.randint(1, 3)) + Fraction(rng.choice((1, 3)), 4)
            stem = [text(f"รถยนต์แล่นด้วยอัตราเร็วชั่วโมงละ {speed} กิโลเมตร เป็นเวลา"),
                    content_math(as_mixed(hours)), text("ชั่วโมง แล่นได้ระยะทางกี่กิโลเมตร")]
            value = speed * hours
            wrongs = [named("operation.reversed", as_mixed(speed / hours)),
                      named("operation.reversed", as_mixed(speed + hours)),
                      named("mixed.whole_part_only", as_mixed(speed * int(hours))),
                      as_mixed(value + 10)]
        elif kind == 0:
            n, each = rng.randint(3, 12), Fraction(rng.randint(1, 3), 4)
            stem = [text(f"{p}ดื่มนมวันละ"), content_math(as_mixed(each)),
                    text(f"ลิตร {n} วัน {p}ดื่มนมทั้งหมดกี่ลิตร")]
            value = n * each
            wrongs = [named("operation.reversed", as_mixed(each + n)),
                      named("fraction.scaled_both_terms",
                            as_mixed(Fraction(each.numerator * n, each.denominator * n))),
                      as_mixed(value + 1), as_mixed(value + Fraction(1, 4))]
        elif kind == 1:
            piece = Fraction(1, rng.choice((4, 6, 8, 10)))
            total = piece * rng.randint(3, 20)
            while total.denominator == 1 and rng.random() < 0.3:
                total += piece
            stem = [text("ริบบิ้นยาว"), content_math(as_mixed(total)), text("เมตร ตัดเป็นเส้นละ"),
                    content_math(as_mixed(piece)), text("เมตร ได้ริบบิ้นกี่เส้น")]
            value = total / piece
            # Multiplying instead of dividing.
            wrongs = [named("operation.reversed", as_mixed(total * piece)), as_mixed(value + 1),
                      as_mixed(value - 1), named("operation.reversed", as_mixed(total + piece))]
        else:
            whole = rng.randint(2, 5)
            part = Fraction(rng.randint(1, 4), 5)
            stem = [text(f"{p}มีแป้ง {whole} กิโลกรัม ใช้ทำขนมไป"), content_math(as_mixed(part)),
                    text("ของแป้งทั้งหมด ใช้แป้งไปกี่กิโลกรัม")]
            value = whole * part
            wrongs = [named("operation.reversed", as_mixed(whole - part)),
                      named("part.complement", as_mixed(whole - value)), as_mixed(part),
                      as_mixed(value + Fraction(1, 5)), as_mixed(value + 1),
                      as_mixed(value + Fraction(2, 5))]
        answer = as_mixed(value)
        return _maths(stem, answer, _not_equal(value, wrongs, answer), self.topic)


from otk.core.registry import QuestionType, question_type  # noqa: E402
from otk.kit.math_problems import MathDraw, WordProblem  # noqa: E402
from otk.sets._support.math_p5 import LEVEL  # noqa: E402


def _g(n: int) -> str:
    """A whole number in TeX with grouped thousands: 4{,}572{,}318."""
    return f"{n:,}".replace(",", "{,}")


def _gk(*values: int, answer: int, lo: int = 0, hi: int | None = None) -> list[str]:
    """``story.keep`` for grouped numbers."""
    return [_g(int(v)) for v in _story.keep(*values, answer=answer, lo=lo, hi=hi)]


def _dec(value: int, places: int) -> str:
    """An integer count of 10**-places as a decimal, trailing zeros dropped: (2350, 3) -> 2.35."""
    sign = "-" if value < 0 else ""
    whole, frac = divmod(abs(value), 10 ** places)
    digits = str(frac).rjust(places, "0").rstrip("0") if places else ""
    return f"{sign}{whole}.{digits}" if digits else f"{sign}{whole}"


def _dk(*values: int, answer: int, places: int, lo: int = 0) -> list[str]:
    """``story.keep`` for decimals held as integer counts of 10**-places."""
    return [_dec(int(v), places) for v in _story.keep(*values, answer=answer, lo=lo)]


# ── More fraction word problems (2026-11): the whole from a part, pieces cut from a length, sharing among
# people, an increase by a fraction, two shares compared, part of an hour, and who ran further ──


def _plain(value: Fraction) -> str:
    """A fraction for Thai prompt text, outside TeX: 2 1/3, 3/4, or 5."""
    whole, rem = divmod(value.numerator, value.denominator)
    if not rem:
        return str(whole)
    return f"{whole} {rem}/{value.denominator}" if whole else f"{rem}/{value.denominator}"


def _fk(*values: Fraction, answer: Fraction) -> list[str]:
    """Distinct fraction distractors as TeX, the answer and non-positive values left out."""
    out: list[str] = []
    for v in values:
        if v > 0 and v != answer and as_mixed(v) not in out:
            out.append(as_mixed(v))
    return out


@question_type("math.whole_from_part_p5", display_name={"th": "หาจำนวนทั้งหมดจากส่วนที่เป็นเศษส่วน"},
               level=LEVEL, topic="โจทย์ปัญหาเศษส่วน")
class WholeFromPartP5(WordProblem):
    def expr(self, rng: Random):
        d = rng.choice((3, 4, 5, 6, 8))
        k = rng.randint(1, d - 1)
        unit = rng.randint(5, 60)
        part = k * unit
        right = d * unit
        p = rng.choice(_story.NAMES)
        prompt = f"{p}ใช้เงินไป {k}/{d} ของเงินที่มี คิดเป็นเงิน {part} บาท เดิม{p}มีเงินกี่บาท"
        # The part itself; the part times the bottom; one part; the money left instead.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(part, part * d, unit, right - part, answer=right, lo=1))


@question_type("math.pieces_from_length_p5", display_name={"th": "ตัดเป็นท่อนยาวเท่ากันได้กี่ท่อน"},
               level=LEVEL, topic="โจทย์ปัญหาเศษส่วน")
class PiecesFromLengthP5(WordProblem):
    def expr(self, rng: Random):
        d = rng.choice((2, 3, 4, 5))
        k = rng.randint(1, d - 1)
        times = rng.randint(2, 12)
        total = k * times
        right = d * times
        thing = rng.choice(("เชือก", "ริบบิ้น", "ผ้า"))
        prompt = f"{thing}ยาว {total} เมตร ตัดเป็นท่อนละ {k}/{d} เมตร ได้กี่ท่อน"
        # Divided by the bottom only; the length times the top; the length; one piece more.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(total * d, total * k, total, right + d, right - 1,
                                                answer=right, lo=1))


@question_type("math.share_among_people_p5", display_name={"th": "แบ่งของให้หลายคนเท่า ๆ กันได้คนละเท่าใด"},
               level=LEVEL, topic="โจทย์ปัญหาเศษส่วน")
class ShareAmongPeopleP5(WordProblem):
    def expr(self, rng: Random):
        people = rng.randint(3, 9)
        items = rng.randint(1, 2 * people)
        while items % people == 0:
            items += 1
        right = Fraction(items, people)
        what = rng.choice(("พิซซ่า", "เค้ก", "ขนมปัง"))
        prompt = f"แบ่ง{what} {items} ถาดให้เด็ก {people} คนเท่า ๆ กัน ได้คนละกี่ถาด"
        # The fraction upside down; one tray fewer or more; one child more.
        return MathDraw("", as_mixed(right), prompt=prompt,
                        distractors=_fk(Fraction(people, items), Fraction(items - 1, people),
                                        Fraction(items + 1, people), Fraction(items, people + 1), answer=right))


@question_type("math.increase_by_fraction_p5", display_name={"th": "เพิ่มขึ้นเป็นเศษส่วนของจำนวนเดิม"},
               level=LEVEL, topic="โจทย์ปัญหาเศษส่วน")
class IncreaseByFractionP5(WordProblem):
    def expr(self, rng: Random):
        d = rng.choice((2, 3, 4, 5, 10))
        k = rng.randint(1, d - 1)
        unit = rng.randint(4, 60)
        old = d * unit
        right = old + k * unit
        what, cl = rng.choice((("ราคาสินค้า", "บาท"), ("จำนวนนักเรียน", "คน"), ("ค่าเช่าห้อง", "บาท")))
        prompt = f"{what}เดิม {old} {cl} ต่อมาเพิ่มขึ้น {k}/{d} ของ{what}เดิม {what}ใหม่เป็นกี่{cl}"
        # Only the increase; a decrease instead; the fraction's top added; one part added.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(k * unit, old - k * unit, old + k, old + unit, answer=right, lo=1))


@question_type("math.two_shares_compare_p5", display_name={"th": "เปรียบเทียบส่วนแบ่งที่เป็นเศษส่วนของจำนวนเดียวกัน"},
               level=LEVEL, topic="โจทย์ปัญหาเศษส่วน")
class TwoSharesCompareP5(WordProblem):
    def expr(self, rng: Random):
        while True:
            d1, d2 = rng.sample((2, 3, 4, 5, 6), 2)
            k1, k2 = rng.randint(1, d1 - 1), rng.randint(1, d2 - 1)
            if Fraction(k1, d1) + Fraction(k2, d2) <= 1 and Fraction(k1, d1) != Fraction(k2, d2):
                break
        if Fraction(k1, d1) < Fraction(k2, d2):
            k1, d1, k2, d2 = k2, d2, k1, d1
        total = d1 * d2 * rng.randint(2, 20)
        a, b = total * k1 // d1, total * k2 // d2
        right = a - b
        p, q = _story.names(rng)
        prompt = (f"แบ่งเงิน {total} บาท {p}ได้ {k1}/{d1} ของเงินทั้งหมด {q}ได้ {k2}/{d2} ของเงินทั้งหมด "
                  f"{p}ได้มากกว่า{q}กี่บาท")
        # The two shares added; either share alone; what is left of the money.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(a + b, a, b, total - a - b, right + 10, answer=right, lo=1))


@question_type("math.part_of_hour_p5", display_name={"th": "เศษส่วนของชั่วโมงเป็นนาที"},
               level=LEVEL, topic="โจทย์ปัญหาเศษส่วน")
class PartOfHourP5(WordProblem):
    def expr(self, rng: Random):
        d = rng.choice((2, 3, 4, 5, 6, 10, 12))
        k = rng.randint(1, d - 1)
        right = 60 * k // d
        p = rng.choice(_story.NAMES)
        prompt = f"{p}อ่านหนังสือ {k}/{d} ชั่วโมง คิดเป็นกี่นาที"
        # An hour taken as 100 minutes; one part only; the minutes left in the hour.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(100 * k // d, 60 // d, 60 - right, right + 5, answer=right, lo=1))


@question_type("math.who_further_p5", display_name={"th": "วิ่งได้ไกลกว่ากันกี่กิโลเมตร"},
               level=LEVEL, topic="โจทย์ปัญหาเศษส่วน")
class WhoFurtherP5(WordProblem):
    def expr(self, rng: Random):
        while True:
            d1, d2 = rng.sample((2, 3, 4, 5, 6, 8), 2)
            a = Fraction(rng.randint(1, 3 * d1 - 1), d1)
            b = Fraction(rng.randint(1, 3 * d2 - 1), d2)
            if a != b and a.denominator > 1 and b.denominator > 1:
                break
        if a < b:
            a, b = b, a
        right = a - b
        p, q = _story.names(rng)
        prompt = f"{p}วิ่งได้ {_plain(a)} กิโลเมตร {q}วิ่งได้ {_plain(b)} กิโลเมตร {p}วิ่งได้ไกลกว่า{q}กี่กิโลเมตร"
        # Added instead; tops subtracted over the larger bottom; the further distance; one step off.
        wrong_tops = Fraction(abs(a.numerator - b.numerator) or 1, max(a.denominator, b.denominator))
        return MathDraw("", as_mixed(right), prompt=prompt,
                        distractors=_fk(a + b, wrong_tops, a, right + Fraction(1, max(d1, d2)), answer=right))
