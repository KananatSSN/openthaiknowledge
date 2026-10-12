"""ทศนิยม

คณิตศาสตร์ · ป.5 · สสวท. พื้นฐาน
Indicators: ค 1.1 ป.5/*

Sets moved here from: math, math_p5.
"""

from __future__ import annotations

from decimal import Decimal
from fractions import Fraction
from random import Random

from otk.core.content import math as content_math
from otk.core.content import text
from otk.core.distractors import fixed
from otk.core.mistakes import named
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, MathType, WordProblem
from otk.sets._support.math_p4 import fr
from otk.sets._support.math_p5 import LEVEL, dstr

PROVENANCE = Provenance("original")


def _labelled(pairs, fmt, answer, keep=lambda value: True) -> list[str]:
    """Wrong values as choice strings, each formatted once and named where a key is
    given: ``[(value, mistake key or None), ...]``. Duplicates and the answer are
    dropped by value, first kept, exactly as ``dict.fromkeys`` did before."""
    out: list[str] = []
    seen: set = set()
    for value, key in pairs:
        if value == answer or value in seen or not keep(value):
            continue
        seen.add(value)
        shown = fmt(value)
        out.append(named(key, shown) if key else shown)
    return out


_DEC_TOPIC = "ทศนิยม"


def _rand_dec(rng: Random, places: int, lo: int, hi: int) -> Decimal:
    v = Decimal(rng.randint(lo * 10 ** places, hi * 10 ** places)).scaleb(-places)
    if v == v.to_integral_value():
        v += Decimal(1).scaleb(-places)
    return v


@question_type("math.compare_decimals",
               display_name={"th": "เปรียบเทียบทศนิยม"}, level={"th": "ป.5"},
               topic="ทศนิยม")
class CompareDecimals(QuestionType):
    def build(self, rng: Random, **params) -> GeneratedQuestion:
        a = rng.randint(1, 9999)
        b = a if rng.random() < 0.15 else rng.randint(1, 9999)
        fa, fb = f"{a / 1000:.3f}", f"{b / 1000:.3f}"
        sign = "<" if a < b else ">" if a > b else "="
        wrong = [s for s in ("<", ">", "=") if s != sign]
        return GeneratedQuestion(
            stem=[text(f"จงเติมเครื่องหมายที่ถูกต้อง:  {fa} ___ {fb}")],
            correct=[content_math(sign)],
            distractors=fixed(*[[content_math(s)] for s in wrong]),
            topic=self.topic,
        )


@question_type("math.decimal_times_power_of_ten",
               display_name={"th": "คูณ/หารทศนิยมด้วย 10, 100, 1000"},
               level={"th": "ป.5"}, topic="ทศนิยม")
class DecimalTimesPowerOfTen(MathType):
    def expr(self, rng: Random):
        x = rng.randint(1, 9999) / 100              # up to 2 decimal places
        p = rng.choice([10, 100, 1000])
        if rng.random() < 0.5:
            op, val = r"\times", x * p
        else:
            op, val = r"\div", x / p
        fmt = lambda v: f"{v:g}"
        return MathDraw(rf"{fmt(x)} {op} {p}", fmt(val),
                        distractors=[fmt(x), fmt(val * 10), fmt(val / 10)])


@question_type("math.decimal_multiply_p5",
               display_name={"th": "การคูณทศนิยม"},
               level=LEVEL, topic=_DEC_TOPIC)
class DecimalMultiplyP5(MathType):
    def expr(self, rng: Random):
        a = _rand_dec(rng, rng.choice((1, 2)), 0, 30)
        b = (Decimal(rng.randint(2, 19)) if rng.random() < 0.5
             else _rand_dec(rng, 1, 0, 9))
        ans = a * b
        # The point one place off either way, then adding instead.
        wrongs = [named("decimal.point_misplaced", dstr(ans * 10)),
                  named("decimal.point_misplaced", dstr(ans / 10)),
                  named("operation.reversed", dstr(a + b)), dstr(ans + 1)]
        return MathDraw(rf"{dstr(a)} \times {dstr(b)}", dstr(ans), prompt="จงหาผลคูณ",
                        distractors=[w for w in dict.fromkeys(wrongs) if w != dstr(ans)])


@question_type("math.fraction_to_decimal_p5",
               display_name={"th": "เขียนเศษส่วนที่ตัวส่วนเป็นตัวประกอบของ 10, 100, 1,000 เป็นทศนิยม"},
               level=LEVEL, topic=_DEC_TOPIC)
class FractionToDecimalP5(MathType):
    _DENS = (2, 4, 5, 8, 20, 25, 40, 50, 125, 200, 250)

    def expr(self, rng: Random):
        d = rng.choice(self._DENS)
        n = rng.randint(1, d - 1)
        while Fraction(n, d).denominator == 1:
            n = rng.randint(1, d - 1)
        v = Decimal(n) / Decimal(d)
        # Writing n and d side by side, and n/d as n tenths.
        wrongs = [named("fraction.digits_as_decimal", f"{n}.{d}"),
                  named("fraction.numerator_as_tenths", dstr(Decimal(n) / 10)),
                  named("decimal.point_misplaced", dstr(v * 10)),
                  named("fraction.inverted", dstr(Decimal(d) / n))
                  if (Decimal(d) / n) == (Decimal(d) / n).quantize(Decimal("0.001"))
                  else named("fraction.digits_as_decimal", f"0.{n}{d}")]
        return MathDraw(fr(n, d), dstr(v), prompt="เขียนเศษส่วนนี้เป็นทศนิยม",
                        distractors=[w for w in dict.fromkeys(wrongs) if w != dstr(v)])


@question_type("math.decimal_divide_p5",
               display_name={"th": "การหารทศนิยมด้วยจำนวนนับ"},
               level=LEVEL, topic=_DEC_TOPIC)
class DecimalDivideP5(MathType):
    def expr(self, rng: Random):
        b = rng.randint(2, 12)
        q = _rand_dec(rng, rng.choice((1, 2, 3)), 0, 20)
        a = q * b
        pairs = [(q * 10, "decimal.point_misplaced"), (q / 10, "decimal.point_misplaced"),
                 (q + 1, None),
                 (a - b, "operation.reversed") if a > b else (q + Decimal("0.1"), None)]
        return MathDraw(rf"{dstr(a)} \div {b}", dstr(q), prompt="จงหาผลหาร",
                        distractors=_labelled(pairs, dstr, q, keep=lambda w: w > 0))


@question_type("math.decimal_word_problem_p5",
               display_name={"th": "โจทย์ปัญหาการคูณหารทศนิยม (สองขั้นตอน)"},
               level=LEVEL, topic=_DEC_TOPIC)
class DecimalWordProblemP5(WordProblem):
    def expr(self, rng: Random):
        p = rng.choice(_story.NAMES)
        kind = rng.randrange(6)
        if kind == 3:
            lap = _rand_dec(rng, 1, 0, 2) + Decimal("0.5")
            per_day, days = rng.randint(2, 4), rng.randint(3, 6)
            ans = lap * per_day * days
            return MathDraw("", dstr(ans),
                            prompt=(f"{p}วิ่งรอบสวนสาธารณะรอบละ {dstr(lap)} กิโลเมตร วันละ {per_day} รอบ "
                                    f"เป็นเวลา {days} วัน {p}วิ่งได้ทั้งหมดกี่กิโลเมตร"),
                            distractors=_labelled(
                                [(lap * per_day, "steps.missed_a_step"), (lap * days, "steps.missed_a_step"),
                                 (ans * 10, "decimal.point_misplaced"),
                                 (lap + per_day + days, "operation.reversed")], dstr, ans))
        if kind == 4:
            each = Decimal(rng.randint(5, 40)) + Decimal(rng.choice((25, 50, 75))) / 100
            n, m = rng.randint(3, 8), rng.randint(2, 9)
            total = each * n
            ans = each * m
            return MathDraw("", f"{ans:.2f}",
                            prompt=(f"ขนม {n} ชิ้น ราคารวม {total:.2f} บาท ถ้าซื้อขนมชนิดเดียวกัน {m} ชิ้น "
                                    f"ต้องจ่ายกี่บาท"),
                            distractors=_labelled(
                                [(total * m, "proportion.no_divide"), (total / m, None),
                                 (each, "proportion.unit_rate_only"), (ans + each, None)],
                                lambda w: f"{w:.2f}", ans))
        if kind == 5:
            metres = _rand_dec(rng, 1, 1, 6)
            per = rng.randint(35, 90)
            thread = rng.randint(10, 40)
            ans = metres * per + thread
            return MathDraw("", dstr(ans),
                            prompt=(f"{p}ซื้อผ้า {dstr(metres)} เมตร ราคาเมตรละ {per} บาท และซื้อด้ายอีก "
                                    f"{thread} บาท {p}จ่ายเงินทั้งหมดกี่บาท"),
                            distractors=_labelled(
                                [(metres * per, "steps.missed_a_step"), (metres * (per + thread), None),
                                 (ans * 10, "decimal.point_misplaced"),
                                 (metres + per + thread, "operation.reversed")], dstr, ans))
        if kind == 0:
            price = Decimal(rng.randint(12, 60)) + Decimal(rng.choice((25, 50, 75))) / 100
            n = rng.randint(2, 9)
            note = (int(price * n) // 100 + 1) * 100
            ans = note - price * n
            return MathDraw("", f"{ans:.2f}",
                            prompt=(f"{p}ซื้อน้ำผลไม้ {n} ขวด ขวดละ {price:.2f} บาท จ่ายเงิน {note} บาท "
                                    f"ได้เงินทอนกี่บาท"),
                            distractors=[named("steps.missed_a_step", f"{price * n:.2f}"),
                                         named("steps.missed_a_step", f"{note - price:.2f}"),
                                         f"{ans + 1:.2f}"])
        if kind == 1:
            kg = _rand_dec(rng, 1, 1, 9)
            per = rng.randint(25, 120)
            ans = kg * per
            return MathDraw("", dstr(ans),
                            prompt=f"เนื้อหมูราคากิโลกรัมละ {per} บาท ซื้อ {dstr(kg)} กิโลกรัม ต้องจ่ายกี่บาท",
                            distractors=_labelled(
                                [(ans * 10, "decimal.point_misplaced"), (ans / 10, "decimal.point_misplaced"),
                                 (kg + per, "operation.reversed"), (ans + per, None)], dstr, ans))
        total = _rand_dec(rng, 2, 3, 30)
        n = rng.randint(2, 8)
        total = (total * n).quantize(Decimal("0.01"))
        each = total / n
        return MathDraw("", dstr(each),
                        prompt=(f"ผ้ายาว {dstr(total)} เมตร แบ่งเป็น {n} ผืนยาวเท่า ๆ กัน "
                                f"ผืนหนึ่งยาวกี่เมตร"),
                        distractors=_labelled(
                            [(each * 10, "decimal.point_misplaced"), (each / 10, "decimal.point_misplaced"),
                             (total * n, "operation.reversed"), (each + 1, None)], dstr, each))
