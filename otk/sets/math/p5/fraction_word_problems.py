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
