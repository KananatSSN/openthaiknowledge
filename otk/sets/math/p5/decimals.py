"""ทศนิยม

คณิตศาสตร์ · ป.5 · สสวท. พื้นฐาน
Indicators: ค 1.1 ป.5/*

Sets moved here from: math, math_p5.
"""

from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal
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


from otk.core.registry import QuestionType, question_type  # noqa: E402
from otk.kit.math_problems import ChoiceType, MathType, WordProblem  # noqa: E402
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


# ── More decimals (2026-11): rounding to one or two places, the largest or smallest of four, the value of a
# digit, and estimating a product ──


@question_type("math.round_decimal_p5", display_name={"th": "ปัดทศนิยมเป็นทศนิยมหนึ่งหรือสองตำแหน่ง"},
               level=LEVEL, topic="ทศนิยม")
class RoundDecimalP5(WordProblem):
    def expr(self, rng: Random):
        v = rng.randint(1001, 99999)
        while v % 10 == 0:
            v += 1
        places = rng.choice((1, 2))
        step = 10 ** (3 - places)
        right = (v + step // 2) // step
        cut = v // step
        names = {1: "หนึ่งตำแหน่ง", 2: "สองตำแหน่ง"}
        prompt = f"ปัด {_dec(v, 3)} เป็นทศนิยม{names[places]} ได้เท่าใด"

        def fixed(x: int) -> str:
            return f"{x // 10 ** places}.{x % 10 ** places:0{places}d}"

        # Cut off instead of rounding; one step either side.
        return MathDraw("", fixed(right), prompt=prompt,
                        distractors=[fixed(int(x)) for x in _story.keep(cut, cut + 1, right + 1, right - 1,
                                                                   answer=right, lo=1)])


@question_type("math.decimal_order_p5", display_name={"th": "ทศนิยมที่มากที่สุดหรือน้อยที่สุด"},
               level=LEVEL, topic="ทศนิยม")
class DecimalOrderP5(ChoiceType):
    def compose(self, rng: Random):
        whole = rng.randint(0, 9)
        d1, d2, d3 = rng.sample(range(1, 10), 3)
        # Same digits in different places, so place value decides, not length.
        values = [whole * 1000 + d1 * 100 + d2 * 10 + d3, whole * 1000 + d1 * 100 + d3 * 10,
                  whole * 1000 + d2 * 100 + d1, whole * 1000 + d3 * 100 + d2 * 10 + d1]
        most = rng.random() < 0.5
        right = max(values) if most else min(values)
        texts = [_dec(v, 3) for v in values]
        return (f"ทศนิยมใด{'มากที่สุด' if most else 'น้อยที่สุด'}", _dec(right, 3),
                [t for v, t in zip(values, texts) if v != right])


@question_type("math.decimal_digit_value_p5", display_name={"th": "ค่าของเลขโดดในทศนิยม"},
               level=LEVEL, topic="ทศนิยม")
class DecimalDigitValueP5(ChoiceType):
    def compose(self, rng: Random):
        digits = rng.sample(range(1, 10), 4)
        number = f"{digits[0]}.{digits[1]}{digits[2]}{digits[3]}"
        pos = rng.randint(1, 3)
        d = digits[pos]
        values = [f"{d}", f"0.{d}", f"0.0{d}", f"0.00{d}"]
        right = values[pos]
        return f"ในจำนวน {number} เลขโดด {d} มีค่าเท่าใด", right, [v for v in values if v != right]


@question_type("math.estimate_decimal_product_p5", display_name={"th": "ประมาณผลคูณของทศนิยม"},
               level=LEVEL, topic="ทศนิยม")
class EstimateDecimalProductP5(WordProblem):
    def expr(self, rng: Random):
        a = rng.randint(2, 9)
        b = rng.randint(2, 9)
        x = a * 10 + rng.choice((-4, -3, -2, -1, 1, 2, 3, 4))
        y = b * 10 + rng.choice((-4, -3, -2, -1, 1, 2, 3, 4))
        right = a * b
        prompt = f"ประมาณผลคูณของ {_dec(x, 1)} × {_dec(y, 1)} โดยปัดแต่ละจำนวนเป็นจำนวนเต็มก่อน"
        # Cutting off instead of rounding; a place too far; one factor rounded only.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep((x // 10) * (y // 10), right * 10, a * (y // 10) + 1,
                                                right + a, answer=right, lo=1))



def _bank_decimal_choices_p5(answer,values,places):
    quantum=Decimal(1).scaleb(-places)
    right=answer.quantize(quantum,rounding=ROUND_HALF_UP)
    seen={right}
    wrongs=[]
    for value in values:
        value=value.quantize(quantum,rounding=ROUND_HALF_UP)
        if value>=0 and value not in seen:
            seen.add(value)
            wrongs.append(f"{value:.{places}f}")
    return f"{right:.{places}f}",wrongs


@question_type("math.decimal_three_place_addsub_p5", display_name={"th": "บวกลบทศนิยมต่างจำนวนตำแหน่ง"}, level={"th": "ป.5"}, topic="ทศนิยม")
class DecimalThreePlaceAddSubP5(ChoiceType):
    PROVENANCE = Provenance("adapted", sources=("openthaiknowledge-bank/mathematics/level/primary-5/4723-5-2567-2-1.pdf, ข้อ 1–4",))

    def compose(self,rng: Random):
        a=Decimal(rng.randint(300001,899999))/1000
        b=Decimal(rng.randint(10001,29999))/100
        add=rng.choice((False,True))
        answer=a+b if add else a-b
        # Align decimal points, not the final written digits.
        misaligned=a+(b/10 if add else -b/10)
        right,wrongs=_bank_decimal_choices_p5(answer,[misaligned,a-b if add else a+b,
                                                      answer+Decimal('0.1'),answer-Decimal('0.1')],3)
        return f"จงหาค่าของ {a:.3f} {'+' if add else '−'} {b:.2f}",right,wrongs


@question_type("math.decimal_bracket_calculation_p5", display_name={"th": "คำนวณทศนิยมสองขั้นตอนตามวงเล็บ"}, level={"th": "ป.5"}, topic="ทศนิยม")
class DecimalBracketCalculationP5(ChoiceType):
    PROVENANCE = Provenance("adapted", sources=("openthaiknowledge-bank/mathematics/level/primary-5/4723-5-2567-2-1.pdf, ข้อ 11–18",))

    def compose(self,rng: Random):
        a,b,c=(Decimal(rng.randint(1001,9999))/100 for _ in range(3))
        d=rng.randint(2,59)
        mode=rng.randrange(8)
        if mode in (0,1):
            a=a+b+c
            shown=f"{a} − ({b} + {c})" if mode==0 else f"({a} − {b}) − {c}"
            answer=a-b-c
            slips=[a-b+c,a+b-c,a+b+c,a-b,a-c]
        elif mode==2:
            c=Decimal(rng.randint(21,99))/10
            shown=f"{a} + ({b} × {c})"
            answer=a+b*c
            slips=[(a+b)*c,a+b+c,b*c,a*b+c]
        elif mode==3:
            a=a+b
            c=Decimal(rng.randint(21,99))/10
            shown=f"({a} − {b}) × {c}"
            answer=(a-b)*c
            slips=[a-b*c,a-b+c,a*c,b*c]
        elif mode==4:
            a=Decimal(rng.randint(101,9999))/1000*d
            shown=f"({a} ÷ {d}) + {c}"
            answer=a/d+c
            slips=[a/(d+c),a/d,a*d+c,a+c]
        elif mode==5:
            b=Decimal(rng.randint(11,99))/10
            answer=Decimal(rng.randint(1,19))/10
            a=answer*b*d
            shown=f"{a} ÷ ({b} × {d})"
            slips=[a/b*d,a/b,a*b*d,a/(b+d)]
        elif mode==6:
            answer=Decimal(rng.randint(101,9999))/100
            total=answer*d
            a=total*Decimal(rng.randint(2,8))/10
            b=total-a
            shown=f"({a} + {b}) ÷ {d}"
            slips=[a+b/d,a+b,(a+b)*d,a/d]
        else:
            b=Decimal(rng.randint(1001,9999))/1000
            a=b*d+a
            shown=f"{a} − ({b} × {d})"
            answer=a-b*d
            slips=[(a-b)*d,a-b-d,a+b*d,b*d]
        # The fallback choices are decimal-point shifts, not neighbouring padding.
        right,wrongs=_bank_decimal_choices_p5(answer,slips+[answer*10,answer/10,answer*100],3)
        return f"จงหาค่าของ {shown} ตอบเป็นทศนิยม 3 ตำแหน่ง",right,wrongs



def _bank_round_fraction_p5(value,places):
    scale=10**places
    units=(2*value.numerator*scale+value.denominator)//(2*value.denominator)
    return Decimal(units).scaleb(-places)


@question_type("math.decimal_round_expression_p5", display_name={"th": "คำนวณนิพจน์ทศนิยมแล้วปัดเฉพาะผลสุดท้าย"}, level={"th": "ป.5"}, topic="ทศนิยม")
class DecimalRoundExpressionP5(ChoiceType):
    PROVENANCE = Provenance("adapted", sources=("openthaiknowledge-bank/mathematics/level/primary-5/4723-5-2567-2-1.pdf, ข้อ 19–20",))

    def compose(self,rng: Random):
        places=rng.choice((1,2))
        if places==2:
            a=Decimal(rng.randint(1001,9999))/100
            divisor=rng.randint(2,59)
            c=Decimal(rng.randint(11,99))/10
            shown=f"({a} ÷ {divisor}) × {c}"
            exact=Fraction(a)/divisor*Fraction(c)
            early=(a/divisor).quantize(Decimal('.01'),rounding=ROUND_HALF_UP)*c
            values=[early,a/divisor,a*divisor*c,a/divisor+c]
        else:
            a=Decimal(rng.randint(101,1999))
            divisor=rng.choice((8,16,20,25,40))
            b=Decimal(rng.randint(1001,9999))/100
            c=Decimal(rng.randint(101,999))/100
            shown=f"({a} ÷ {divisor}) + ({b} × {c})"
            exact=Fraction(a)/divisor+Fraction(b)*Fraction(c)
            early=(a/divisor).quantize(Decimal('.1'),rounding=ROUND_HALF_UP)+(b*c).quantize(Decimal('.1'),rounding=ROUND_HALF_UP)
            values=[early,a/divisor,b*c,(a/divisor+b)*c,a*divisor+b*c]
        answer=_bank_round_fraction_p5(exact,places)
        truncated=Decimal((exact.numerator*10**places)//exact.denominator).scaleb(-places)
        right,wrongs=_bank_decimal_choices_p5(answer,[truncated]+values+[answer*10,answer/10,answer*100],places)
        return (f"จงหาค่าของ {shown} แล้วปัดผลสุดท้ายเป็นทศนิยม {places} ตำแหน่ง "
                "ปัดแบบดูหลักถัดไป ถ้าเป็น 5 ขึ้นไปให้ปัดขึ้น โดยไม่ปัดค่าระหว่างคำนวณ",right,wrongs)
