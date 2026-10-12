"""ลำดับและอนุกรม

คณิตศาสตร์ · ม.5 · สสวท. พื้นฐาน
Indicators: ค 1.2 ม.5/*

Sets moved here from: math_bank_sequences, math_chapters, math_m5.
"""

from __future__ import annotations

from decimal import Decimal
from fractions import Fraction
from random import Random

from otk.core.content import math as content_math
from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, WordProblem
from otk.sets._support.math_bank_sequences import _tex_q, num
from otk.sets._support.math_m5 import (
    _FACTORS,
    _base,
)
from otk.sets._support.math_m5 import (
    money as money_math_chapters,
)
from otk.sets._support.math_m5 import (
    money as money_math_m5,
)

M5 = {"th": "ม.5"}


FINANCE = "ลำดับและอนุกรม"


def per_period(rate_pct: Fraction, k: int) -> Fraction:
    return rate_pct / 100 / k


def dec(v: Fraction) -> str:
    """A terminating fraction as a plain decimal string: 1.0025."""
    d = Decimal(v.numerator) / Decimal(v.denominator)
    return format(d.normalize(), "f")


#: (annual %, compoundings per year) with a short terminating per-period rate.
RATE_PLANS = ((Fraction(12), 2), (Fraction(6), 2), (Fraction(3), 3), (Fraction(6), 12), (Fraction(12), 12),
              (Fraction(18, 10), 2), (Fraction(3), 12), (Fraction(4), 4), (Fraction(6), 4), (Fraction(24, 10), 12))


PERIOD_TH = {1: "ทุกปี", 2: "ทุก 6 เดือน", 3: "ทุก 4 เดือน", 4: "ทุก 3 เดือน", 12: "ทุกเดือน"}


def money(v: Fraction) -> str:
    """A terminating amount with thousands separators: 3{,}060.4."""
    d = Decimal(v.numerator) / Decimal(v.denominator)
    return format(d.normalize(), ",f").replace(",", "{,}")


def interest_earned(p: int, i: Fraction, n: int) -> Fraction:
    return p * ((1 + i) ** n - 1)


_CENT = Decimal("0.01")


_SEQ_TOPIC = "ลำดับและอนุกรม"


@question_type("math.arithmetic_sequence_word_m5",
               display_name={"th": "โจทย์ปัญหาลำดับและอนุกรมเลขคณิต"},
               level=M5, topic=_SEQ_TOPIC)
class ArithmeticSequenceWordM5(WordProblem):
    def expr(self, rng: Random):
        a, d, n = rng.randint(10, 40), rng.randint(2, 6), rng.randint(8, 25)
        last = a + (n - 1) * d
        total = n * (a + last) // 2 if n * (a + last) % 2 == 0 else None
        if total is None:
            n += 1
            last = a + (n - 1) * d
            total = n * (a + last) // 2
        p = rng.choice(_story.NAMES)
        kind = rng.randrange(6)
        if kind == 3:
            bottom, rows = rng.randint(15, 30), rng.randint(5, 12)
            top = bottom - (rows - 1)
            logs = rows * (bottom + top) // 2
            return MathDraw("", str(logs),
                            prompt=(f"กองท่อนไม้แถวล่างสุดมี {bottom} ท่อน แต่ละแถวที่อยู่สูงขึ้นไปมีน้อยกว่า"
                                    f"แถวที่อยู่ข้างล่าง 1 ท่อน กองไว้ {rows} แถว มีท่อนไม้ทั้งหมดกี่ท่อน"),
                            distractors=_story.keep(rows * bottom, rows * top, logs + bottom,
                                                    answer=logs, lo=1))
        if kind == 4:
            start, rise = rng.randint(15, 30) * 1000, rng.choice((500, 600, 800, 1000, 1200))
            year = rng.randint(4, 12)
            pay = start + (year - 1) * rise
            return MathDraw("", f"{pay:,}".replace(",", "{,}"),
                            prompt=(f"{p}ได้เงินเดือนปีแรกเดือนละ {start:,} บาท และได้ขึ้นเงินเดือนปีละ {rise} บาท "
                                    f"ในปีที่ {year} {p}ได้เงินเดือนเดือนละกี่บาท"),
                            distractors=[f"{v:,}".replace(",", "{,}") for v in
                                         (start + year * rise, start * year, pay - rise)])
        if kind == 5:
            first, step = rng.randint(10, 20), rng.choice((2, 3, 5))
            day = rng.randint(6, 15)
            goal = first + (day - 1) * step
            return MathDraw("", str(day),
                            prompt=(f"{p}ฝึกวิ่งวันแรก {first} นาที และวิ่งนานขึ้นวันละ {step} นาที "
                                    f"วันที่เท่าใด{p}จะวิ่งได้ {goal} นาที"),
                            distractors=_story.keep(day - 1, day + 1, (goal - first) // step + 2,
                                                    goal // step, answer=day, lo=1))
        if kind == 0:
            return MathDraw("", str(last),
                            prompt=(f"หอประชุมจัดเก้าอี้แถวแรก {a} ตัว แถวถัดไปเพิ่มขึ้นแถวละ {d} ตัว "
                                    f"แถวที่ {n} มีเก้าอี้กี่ตัว"),
                            # n steps instead of n − 1.
                            distractors=_story.keep(a + n * d, a * n, last - d, answer=last, lo=1))
        if kind == 1:
            return MathDraw("", f"{total:,}".replace(",", "{,}"),
                            prompt=(f"หอประชุมจัดเก้าอี้แถวแรก {a} ตัว แถวถัดไปเพิ่มขึ้นแถวละ {d} ตัว "
                                    f"มีทั้งหมด {n} แถว มีเก้าอี้ทั้งหมดกี่ตัว"),
                            distractors=[f"{n * last:,}".replace(",", "{,}"), f"{n * a:,}".replace(",", "{,}"),
                                         f"{total + last:,}".replace(",", "{,}")])
        save = a * 10
        step = d * 10
        months = rng.randint(6, 12)
        s = months * (2 * save + (months - 1) * step) // 2
        return MathDraw("", f"{s:,}".replace(",", "{,}"),
                        prompt=(f"{p}ออมเงินเดือนแรก {save} บาท และออมเพิ่มขึ้นทุกเดือน เดือนละ {step} บาท "
                                f"{months} เดือนแรก{p}ออมเงินได้ทั้งหมดกี่บาท"),
                        distractors=[f"{months * save:,}".replace(",", "{,}"),
                                     f"{save + (months - 1) * step:,}".replace(",", "{,}"),
                                     f"{s + step * months:,}".replace(",", "{,}")])
ArithmeticSequenceWordM5.PROVENANCE = Provenance("original")


@question_type("math.geometric_sequence_word_m5",
               display_name={"th": "โจทย์ปัญหาลำดับและอนุกรมเรขาคณิต"},
               level=M5, topic=_SEQ_TOPIC)
class GeometricSequenceWordM5(WordProblem):
    def expr(self, rng: Random):
        kind = rng.randrange(3)
        if kind == 0:
            h = rng.choice((243, 256, 512, 729, 1024, 625))
            r = {243: 3, 729: 3, 256: 2, 512: 2, 1024: 2, 625: 5}[h]
            k = rng.randint(2, 4)
            frac = Fraction(r - 1, r) if r != 2 else Fraction(1, 2)
            after = int(h * frac ** k)
            said = {Fraction(1, 2): "ครึ่งหนึ่ง", Fraction(2, 3): "สองในสาม",
                    Fraction(4, 5): "สี่ในห้า"}[frac]
            return MathDraw("", str(after),
                            prompt=(f"ปล่อยลูกบอลจากความสูง {h} เซนติเมตร ทุกครั้งที่กระทบพื้นลูกบอลกระดอนขึ้น"
                                    f"ได้สูง{said}ของความสูงก่อนหน้า "
                                    f"หลังกระทบพื้นครั้งที่ {k} ลูกบอลกระดอนขึ้นสูงกี่เซนติเมตร"),
                            distractors=_story.keep(int(h * frac ** (k - 1)), int(h * frac ** (k + 1)),
                                                    h - k * int(h * (1 - frac)) if h - k * int(h * (1 - frac)) > 0
                                                    else after + 1, answer=after, lo=1))
        if kind == 1:
            a, r, n = rng.randint(2, 9), rng.choice((2, 3)), rng.randint(4, 7)
            s = a * (r ** n - 1) // (r - 1)
            return MathDraw("", f"{s:,}".replace(",", "{,}"),
                            prompt=(f"ส่งข้อความต่อกันเป็นทอด ๆ วันแรกมีคนได้รับ {a} คน แต่ละวันจำนวนคนที่ได้รับ"
                                    f"ใหม่เพิ่มเป็น {r} เท่าของวันก่อน {n} วันแรกมีคนได้รับข้อความรวมกี่คน"),
                            distractors=[f"{a * r ** (n - 1):,}".replace(",", "{,}"),
                                         f"{a * r ** n:,}".replace(",", "{,}"),
                                         f"{a * n * r:,}".replace(",", "{,}")])
        price = rng.choice((200_000, 400_000, 500_000, 800_000))
        years = rng.randint(2, 4)
        value = int(price * Fraction(4, 5) ** years)
        return MathDraw("", f"{value:,}".replace(",", "{,}"),
                        prompt=(f"รถยนต์ราคา {price:,} บาท มูลค่าลดลงร้อยละ 20 ของมูลค่าต้นปีทุกปี "
                                f"เมื่อผ่านไป {years} ปี รถมีมูลค่ากี่บาท"),
                        # Taking 20% of the original price every year.
                        distractors=[f"{price - price // 5 * years:,}".replace(",", "{,}"),
                                     f"{int(price * Fraction(4, 5) ** (years - 1)):,}".replace(",", "{,}"),
                                     f"{int(price * Fraction(1, 5) ** years):,}".replace(",", "{,}")])
GeometricSequenceWordM5.PROVENANCE = Provenance("original")


@question_type("math.compound_interest_m5",
               display_name={"th": "ดอกเบี้ยทบต้น"},
               level=M5, topic=_SEQ_TOPIC)
class CompoundInterestM5(WordProblem):
    def expr(self, rng: Random):
        r, n, factor = rng.choice(_FACTORS)
        p = Decimal(rng.randint(1, 20) * 5000)
        f = Decimal(factor)
        total = (p * f).quantize(Decimal("0.01"))
        simple = p * (1 + Decimal(r * n) / 100)
        who = rng.choice(_story.NAMES)
        given = rf"({_base(r)})^{{{n}}} = {factor}"
        if rng.random() < 0.6:
            # The same growth as a deposit, a loan to repay, and land that gains value.
            prompt = rng.choice((
                f"{who}ฝากเงิน {p:,.0f} บาท ได้รับดอกเบี้ยทบต้นร้อยละ {r} ต่อปี เมื่อครบ {n} ปี "
                f"จะมีเงินรวมกี่บาท (กำหนดค่าดังนี้)",
                f"{who}กู้เงิน {p:,.0f} บาท เสียดอกเบี้ยทบต้นร้อยละ {r} ต่อปี และคืนเงินครั้งเดียวเมื่อครบ "
                f"{n} ปี ต้องคืนเงินทั้งหมดกี่บาท (กำหนดค่าดังนี้)",
                f"ที่ดินแปลงหนึ่งราคา {p:,.0f} บาท ราคาเพิ่มขึ้นร้อยละ {r} ของราคาปีก่อนทุกปี เมื่อผ่านไป "
                f"{n} ปี ที่ดินจะมีราคากี่บาท (กำหนดค่าดังนี้)",
            ))
            return MathDraw(
                given, money_math_m5(total), prompt=prompt,
                # Simple interest in place of compound, and the interest alone.
                distractors=[money_math_m5(simple), money_math_m5(total - p), money_math_m5(p * (1 + Decimal(r) / 100))])
        return MathDraw(
            given, money_math_m5(total - p),
            prompt=(f"{who}ฝากเงิน {p:,.0f} บาท ได้รับดอกเบี้ยทบต้นร้อยละ {r} ต่อปี เมื่อครบ {n} ปี "
                    f"จะได้ดอกเบี้ยทั้งหมดกี่บาท (กำหนดค่าดังนี้)"),
            distractors=[money_math_m5(simple - p), money_math_m5(total), money_math_m5(p * Decimal(r) / 100)])
CompoundInterestM5.PROVENANCE = Provenance("original")


@question_type("math.compounding_periods_m5",
               display_name={"th": "ดอกเบี้ยทบต้นหลายครั้งต่อปี"},
               level=M5, topic=FINANCE)
class CompoundingPeriodsM5(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        kind = rng.randrange(4)
        rate, k = rng.choice(RATE_PLANS)
        i = per_period(rate, k)
        years = rng.randint(2, 5)
        n = k * years
        base = dec(1 + i)
        plain = dec(1 + rate / 100)
        rate_th = f"{dec(rate)}% ต่อปี คิดดอกเบี้ยแบบทบต้น{PERIOD_TH[k]}"
        if kind == 0:
            p = rng.choice((10_000, 20_000, 25_000, 50_000, 100_000))
            stem = [text(f"ฝากเงิน {p:,} บาท อัตราดอกเบี้ย {rate_th} เมื่อครบ {years} ปีจะมีเงินรวมกี่บาท")]
            pt = num(p)
            right = rf"{pt}({base})^{{{n}}}"
            # The annual rate each period; the per-period rate for only t periods; the annual rate for kt periods.
            wrongs = [rf"{pt}({plain})^{{{years}}}", rf"{pt}({base})^{{{years}}}", rf"{pt}({plain})^{{{n}}}"]
            return _tex_q(stem, right, wrongs, self.topic)
        if kind == 1:
            amount = rng.choice(("283{,}704", "11{,}940.52", "37{,}600", "150{,}000"))
            stem = [text(f"กู้เงินจำนวนหนึ่ง อัตราดอกเบี้ย {rate_th} เมื่อครบ {years} ปี มียอดเงินกู้พร้อมดอกเบี้ย"),
                    content_math(amount), text("บาท โดยไม่มีการชำระเงินระหว่างนั้น เงินต้นที่กู้เท่ากับกี่บาท")]
            right = rf"{amount}({base})^{{-{n}}}"
            wrongs = [rf"{amount}({base})^{{{n}}}", rf"{amount}({plain})^{{-{n}}}", rf"{amount}({base})^{{-{years}}}"]
            return _tex_q(stem, right, wrongs, self.topic)
        if kind == 2:
            amount = rng.choice(("37{,}600", "52{,}000", "80{,}000"))
            stem = [text(f"เมื่อ {years} ปีที่แล้วฝากเงินไว้ อัตราดอกเบี้ย {rate_th} ตอนนี้มีเงินในบัญชี"),
                    content_math(amount), text("บาท โดยไม่ได้ฝากเพิ่มหรือถอนออก ได้รับดอกเบี้ยทั้งหมดกี่บาท")]
            right = rf"{amount}\left(1 - ({base})^{{-{n}}}\right)"
            wrongs = [rf"{amount}\left(({base})^{{{n}}} - 1\right)", rf"{amount}\left(1 - ({base})^{{{n}}}\right)",
                      rf"{amount}\left(1 - ({base})^{{-{years}}}\right)"]
            return _tex_q(stem, right, wrongs, self.topic)
        rate, k = rng.choice(((Fraction(3), 3), (Fraction(6), 3), (Fraction(4), 2), (Fraction(2), 2), (Fraction(12), 12),
                              (Fraction(6), 12)))
        i = per_period(rate, k)
        periods = rng.choice((2, 3)) if i >= Fraction(1, 100) else 2
        months = periods * 12 // k
        p = rng.choice((10_000, 20_000, 30_000, 50_000))
        right = interest_earned(p, i, periods)
        stem = [text(f"ฝากเงิน {p:,} บาท อัตราดอกเบี้ย {dec(rate)}% ต่อปี จ่ายดอกเบี้ยทบต้น{PERIOD_TH[k]} "
                     f"ฝากไว้ {months} เดือน จะได้ดอกเบี้ยกี่บาท")]
        # Simple interest; the annual rate per period; one period fewer.
        simple = p * i * periods
        named = [simple, interest_earned(p, rate / 100, periods), interest_earned(p, i, periods - 1)]
        fmt = lambda v: money(Fraction(v))
        return _tex_q(stem, fmt(right), [fmt(w) for w in named] + [fmt(right + 1), fmt(right * 2)], self.topic)
CompoundingPeriodsM5.PROVENANCE = Provenance("adapted", sources=('sheet_database/rathcenter/14 ลำดับและอนุกรม',))


@question_type("math.present_value_m5", display_name={"th": "มูลค่าปัจจุบันของเงิน"},
               level=M5, topic="ลำดับและอนุกรม")
class PresentValueM5(WordProblem):
    def expr(self, rng: Random):
        r, n, factor = rng.choice(_FACTORS)
        g = Decimal(factor)
        now = Decimal(rng.randint(2, 50) * 10_000)
        later = (now * g).quantize(_CENT)
        rate = Decimal(r) / 100
        return MathDraw(
            rf"({_base(r)})^{{{n}}} = {factor}", money_math_chapters(now),
            prompt=rng.choice((
                f"ต้องการมีเงิน {money_math_chapters(later).replace('{,}', ',')} บาท เมื่อสิ้นปีที่ {n} "
                f"โดยฝากเงินครั้งเดียววันนี้ ได้ดอกเบี้ยทบต้นร้อยละ {r} ต่อปี "
                f"ต้องฝากเงินวันนี้กี่บาท (กำหนดค่าดังนี้)",
                f"พ่อต้องการมีเงิน {money_math_chapters(later).replace('{,}', ',')} บาท เป็นค่าเล่าเรียนของลูก"
                f"เมื่อสิ้นปีที่ {n} ถ้าฝากเงินครั้งเดียววันนี้ ได้ดอกเบี้ยทบต้นร้อยละ {r} ต่อปี "
                f"ต้องฝากเงินวันนี้กี่บาท (กำหนดค่าดังนี้)",
                f"มีผู้เสนอจะจ่ายเงิน {money_math_chapters(later).replace('{,}', ',')} บาท เมื่อสิ้นปีที่ {n} "
                f"ถ้าอัตราดอกเบี้ยทบต้นร้อยละ {r} ต่อปี เงินจำนวนนี้มีมูลค่าปัจจุบันกี่บาท "
                f"(กำหนดค่าดังนี้)",
            )),
            # Compounding forward, simple interest taken off, and the
            # simple-interest present value.
            distractors=[money_math_chapters((later * g).quantize(_CENT)), money_math_chapters((later * (1 - rate * n)).quantize(_CENT)),
                         money_math_chapters((later / (1 + rate * n)).quantize(_CENT))])
PresentValueM5.PROVENANCE = Provenance("original")


@question_type("math.loan_instalment_m5", display_name={"th": "ค่างวดผ่อนชำระเงินกู้"},
               level=M5, topic="ลำดับและอนุกรม")
class LoanInstalmentM5(WordProblem):
    def expr(self, rng: Random):
        r, n, factor = rng.choice(_FACTORS)
        g = Decimal(factor)
        rate = Decimal(r) / 100
        loan = Decimal(rng.randint(5, 60) * 10_000)
        # L = R(1 − (1+r)^−n)/r, so R = L·r·(1+r)^n / ((1+r)^n − 1).
        pay = (loan * rate * g / (g - 1)).quantize(_CENT)
        return MathDraw(
            rf"({_base(r)})^{{{n}}} = {factor}", money_math_chapters(pay),
            prompt=rng.choice((
                f"กู้เงิน {loan:,.0f} บาท ผ่อนชำระทุกสิ้นปี ปีละเท่า ๆ กัน เป็นเวลา {n} ปี "
                f"อัตราดอกเบี้ยร้อยละ {r} ต่อปี คิดแบบทบต้น ต้องผ่อนชำระปีละกี่บาท (กำหนดค่าดังนี้)",
                f"ซื้อรถยนต์โดยกู้เงิน {loan:,.0f} บาท ผ่อนชำระทุกสิ้นปี ปีละเท่า ๆ กัน {n} งวด "
                f"อัตราดอกเบี้ยทบต้นร้อยละ {r} ต่อปี ค่างวดปีละกี่บาท (กำหนดค่าดังนี้)",
                f"ร้านค้ากู้เงิน {loan:,.0f} บาท มาขยายกิจการ ตกลงผ่อนชำระทุกสิ้นปี ปีละเท่า ๆ กัน "
                f"เป็นเวลา {n} ปี อัตราดอกเบี้ยทบต้นร้อยละ {r} ต่อปี ต้องผ่อนปีละกี่บาท (กำหนดค่าดังนี้)",
            )),
            # No interest, the whole loan compounded then split, and the
            # saving-towards-a-sum formula.
            distractors=[money_math_chapters((loan / n).quantize(_CENT)), money_math_chapters((loan * g / n).quantize(_CENT)),
                         money_math_chapters((loan * rate / (g - 1)).quantize(_CENT))])
LoanInstalmentM5.PROVENANCE = Provenance("original")


@question_type("math.regular_saving_m5",
               display_name={"th": "มูลค่าของเงินฝากรายงวด (อนุกรมเรขาคณิต)"},
               level=M5, topic=_SEQ_TOPIC)
class RegularSavingM5(WordProblem):
    def expr(self, rng: Random):
        r, n, factor = rng.choice([f for f in _FACTORS if f[1] == 3])
        dep = Decimal(rng.randint(1, 20) * 1000)
        g = Decimal(factor)
        rate = Decimal(r) / 100
        # Deposits at the end of each year for n years: dep · ((1+r)^n − 1) / r.
        total = (dep * (g - 1) / rate).quantize(Decimal("0.01"))
        p = rng.choice(_story.NAMES)
        terms = f"ได้ดอกเบี้ยทบต้นร้อยละ {r} ต่อปี"
        prompt = rng.choice((
            f"ฝากเงินทุกสิ้นปี ปีละ {dep:,.0f} บาท เป็นเวลา {n} ปี {terms} "
            f"เมื่อฝากครบ {n} งวด จะมีเงินรวมกี่บาท (กำหนดค่าดังนี้)",
            f"{p}ออมเงินเพื่อการศึกษาโดยฝากธนาคารทุกสิ้นปี ปีละ {dep:,.0f} บาท {terms} "
            f"เมื่อฝากครบ {n} ปี {p}จะมีเงินรวมกี่บาท (กำหนดค่าดังนี้)",
            f"ร้านค้าแห่งหนึ่งกันเงินไว้ซื้อเครื่องมือใหม่ทุกสิ้นปี ปีละ {dep:,.0f} บาท {terms} "
            f"ครบ {n} ปีจะมีเงินรวมกี่บาท (กำหนดค่าดังนี้)",
        ))
        return MathDraw(
            rf"({_base(r)})^{{{n}}} = {factor}", money_math_m5(total), prompt=prompt,
            # The deposits alone, and the whole sum compounded as one lump.
            distractors=[money_math_m5(dep * n), money_math_m5(dep * n * g), money_math_m5(dep * g)])
RegularSavingM5.PROVENANCE = Provenance("original")
