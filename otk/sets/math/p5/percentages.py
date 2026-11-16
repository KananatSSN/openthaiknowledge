"""ร้อยละ

คณิตศาสตร์ · ป.5 · สสวท. พื้นฐาน
Indicators: ค 1.1 ป.5/*

Sets moved here from: math, math_p5, math_pictures_extra.
"""

from __future__ import annotations

from decimal import Decimal
from random import Random

from otk.core.content import image, text
from otk.core.mistakes import named
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, WordProblem
from otk.sets._support.math_diagrams import _math_q
from otk.sets._support.math_p4 import grouped
from otk.sets._support.math_p5 import LEVEL, dstr
from otk.sets._support.math_pictures import _near
from otk.sets._support.math_pictures_extra import GRID_ALT, GRIDS

PROVENANCE = Provenance("original")


_PC_TOPIC = "ร้อยละ"


_SINGLE_GRIDS = tuple(g for g in GRIDS if g.wholes == 0)


@question_type("math.percent_of_number",
               display_name={"th": "หาร้อยละของจำนวน"}, level={"th": "ป.5"},
               topic="ร้อยละ")
class PercentOfNumber(WordProblem):
    def expr(self, rng: Random):
        p = rng.choice([10, 20, 25, 50, 75])
        n = rng.randint(1, 25) * 20                 # divisible → integer answer
        ans = p * n // 100
        who = rng.choice(_story.NAMES)
        prompt = rng.choice((
            f"{p}% ของ {n} เท่ากับเท่าใด?",
            f"โรงเรียนมีนักเรียน {n} คน ร้อยละ {p} ขี่จักรยานมาโรงเรียน "
            f"มีนักเรียนขี่จักรยานมาโรงเรียนกี่คน",
            f"{who}มีเงิน {n} บาท ใช้ไปร้อยละ {p} ของเงินที่มี {who}ใช้เงินไปกี่บาท",
            f"สวนแห่งหนึ่งมีต้นไม้ {n} ต้น เป็นต้นมะม่วงร้อยละ {p} มีต้นมะม่วงกี่ต้น",
        ))
        return MathDraw("", str(ans), prompt=prompt,
                        distractors=[str(p * n // 10), str(n - p), str(n // 4)])


@question_type("math.percent_grid_p5", display_name={"th": "ร้อยละจากภาพตารางร้อยช่อง"},
               level={"th": "ป.5"}, topic="ร้อยละ")
class PercentGridP5(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        g = rng.choice(_SINGLE_GRIDS)
        h = g.hundredths
        shaded = rng.random() < 0.6
        pct = h if shaded else 100 - h
        which = "แรเงา" if shaded else "ไม่ได้แรเงา"
        return _math_q([text(f"ตารางแบ่งเป็น 100 ช่องเท่า ๆ กัน ส่วนที่{which}คิดเป็นร้อยละเท่าใด"),
                        image(g.asset_id, alt=GRID_ALT)],
                       str(pct), _near(pct, 100 - pct, pct * 10 if pct < 10 else pct // 10 or 1,
                                       pct + 10 if pct <= 90 else pct - 20, lo=1), self.topic)


@question_type("math.percent_of_quantity_p5",
               display_name={"th": "โจทย์ปัญหาร้อยละของจำนวน"},
               level=LEVEL, topic=_PC_TOPIC)
class PercentOfQuantityP5(WordProblem):
    def expr(self, rng: Random):
        pct = rng.choice((5, 10, 15, 20, 25, 30, 40, 45, 60, 75, 80))
        whole = rng.randint(2, 30) * 20
        part = whole * pct // 100
        kind = rng.randrange(6)
        if kind == 3:
            return MathDraw("", str(part),
                            prompt=(f"{rng.choice(_story.NAMES)}มีเงิน {whole} บาท ใช้ซื้อหนังสือร้อยละ {pct} "
                                    f"ของเงินที่มี ใช้เงินซื้อหนังสือกี่บาท"),
                            distractors=_story.keep(named("part.complement", whole - part), named("percent.answered_the_percent", pct),
                                                    part + pct, answer=part, lo=1))
        if kind == 4:
            return MathDraw("", str(whole - part),
                            prompt=(f"ร้านค้ามีลูกโป่ง {whole} ลูก แตกไปร้อยละ {pct} เหลือลูกโป่งที่ไม่แตกกี่ลูก"),
                            distractors=_story.keep(named("part.complement", part), named("percent.subtracted_the_number", whole - pct),
                                                    named("percent.answered_the_percent", 100 - pct), answer=whole - part, lo=1))
        if kind == 5:
            return MathDraw("", str(part),
                            prompt=(f"ห้องสมุดมีหนังสือ {whole} เล่ม เป็นหนังสือนิทานร้อยละ {pct} "
                                    f"มีหนังสือนิทานกี่เล่ม"),
                            distractors=_story.keep(named("part.complement", whole - part), named("percent.answered_the_percent", pct),
                                                    whole // pct if pct else 1, part * 2, answer=part, lo=1))
        if kind == 0:
            return MathDraw("", str(part),
                            prompt=f"โรงเรียนมีนักเรียน {whole} คน ร้อยละ {pct} ขี่จักรยานมาโรงเรียน มีนักเรียนขี่จักรยานมากี่คน",
                            distractors=_story.keep(named("part.complement", whole - part), named("percent.answered_the_percent", pct),
                                                    whole * pct // 10, part + pct, answer=part, lo=1))
        if kind == 1:
            return MathDraw("", str(whole - part),
                            prompt=(f"สวนมีต้นไม้ {whole} ต้น ร้อยละ {pct} เป็นต้นมะม่วง "
                                    f"ที่เหลือเป็นต้นอื่น มีต้นไม้อื่นกี่ต้น"),
                            distractors=_story.keep(named("part.complement", part), named("percent.subtracted_the_number", whole - pct),
                                                    named("percent.answered_the_percent", 100 - pct), answer=whole - part, lo=1))
        return MathDraw("", str(part),
                        prompt=f"นักเรียนสอบได้คะแนนร้อยละ {pct} ของคะแนนเต็ม {whole} คะแนน ได้กี่คะแนน",
                        distractors=_story.keep(named("percent.answered_the_percent", pct), named("part.complement", whole - part), part * 2,
                                                answer=part, lo=1))


@question_type("math.find_percent_p5",
               display_name={"th": "คิดเป็นร้อยละเท่าใด"},
               level=LEVEL, topic=_PC_TOPIC)
class FindPercentP5(WordProblem):
    def expr(self, rng: Random):
        pct = rng.choice((5, 10, 20, 25, 30, 40, 50, 60, 75, 80, 90))
        whole = rng.choice((20, 40, 50, 80, 120, 200, 400, 500))
        part = whole * pct // 100
        if part * 100 != whole * pct:
            whole, part = 200, 2 * pct
        what = rng.choice((("นักเรียน", "คน", "สอบผ่าน"), ("ต้นกล้า", "ต้น", "งอก"),
                           ("ลูกบอลที่โยน", "ลูก", "ลงห่วง")))
        noun, cl, verb = what
        return MathDraw("", str(pct),
                        prompt=f"{noun} {whole} {cl} {verb} {part} {cl} คิดเป็นร้อยละเท่าใด",
                        # Part out of 100 instead of out of the whole.
                        distractors=_story.keep(named("percent.part_as_percent", part),
                                                named("part.complement", 100 - pct), whole - part,
                                                pct + 10, answer=pct, lo=1))


@question_type("math.discount",
               display_name={"th": "โจทย์ปัญหาส่วนลด"}, level={"th": "ป.5"},
               topic="ร้อยละ")
class Discount(WordProblem):
    _GOODS = ("เสื้อ", "รองเท้า", "กระเป๋า", "หนังสือ", "พัดลม", "นาฬิกา", "ของเล่น")

    def expr(self, rng: Random):
        price = rng.randint(5, 100) * 20
        disc = rng.choice([5, 10, 15, 20, 25, 30, 40, 50])
        cut = price * disc // 100
        pay = price - cut
        goods = rng.choice(self._GOODS)
        p = rng.choice(_story.NAMES)
        if rng.random() < 0.6:
            prompt = rng.choice((
                f"{goods}ราคา {price} บาท ร้านลดราคาร้อยละ {disc} ต้องจ่ายเงินกี่บาท",
                f"{p}ซื้อ{goods}ที่ติดป้ายราคา {price} บาท ได้ส่วนลด {disc}% {p}จ่ายเงินกี่บาท",
                f"ห้างลดราคาสินค้าทุกชิ้นร้อยละ {disc} {goods}ติดราคา {price} บาท ราคาหลังลดเป็นกี่บาท",
            ))
            return MathDraw("", str(pay), prompt=prompt,
                            # The discount alone, and adding it on.
                            distractors=_story.keep(cut, price + cut, price - disc, answer=pay,
                                                    lo=1))
        return MathDraw("", str(cut),
                        prompt=f"{goods}ราคา {price} บาท ลดราคาร้อยละ {disc} ได้ส่วนลดกี่บาท",
                        distractors=_story.keep(pay, disc, price * disc // 10, answer=cut, lo=1))


@question_type("math.percent_two_step_p5",
               display_name={"th": "โจทย์ปัญหาร้อยละสองขั้นตอน"},
               level=LEVEL, topic=_PC_TOPIC)
class PercentTwoStepP5(WordProblem):
    def expr(self, rng: Random):
        price = rng.randint(4, 50) * 100
        pct = rng.choice((10, 20, 25, 30, 40))
        coupon = rng.choice((50, 100, 150, 200))
        after = price - price * pct // 100
        if rng.random() < 0.5:
            ans = after - coupon
            item = rng.choice(("กระเป๋า", "รองเท้าคู่หนึ่ง", "นาฬิกาเรือนหนึ่ง", "พัดลมเครื่องหนึ่ง"))
            return MathDraw("", str(ans),
                            prompt=(f"{item}ราคา {grouped(price)} บาท ลดราคาร้อยละ {pct} "
                                    f"แล้วใช้คูปองลดอีก {coupon} บาท ต้องจ่ายกี่บาท"),
                            # Taking the coupon off first changes the percentage.
                            distractors=_story.keep(named("steps.missed_a_step", after),
                                                    named("steps.wrong_order",
                                                          (price - coupon) * (100 - pct) // 100),
                                                    named("percent.subtracted_the_number",
                                                          price - pct - coupon),
                                                    ans + coupon, answer=ans, lo=1))
        n = rng.randint(2, 6)
        ans = after * n
        item, cl = rng.choice((("เสื้อ", "ตัว"), ("หนังสือ", "เล่ม"), ("หมวก", "ใบ"), ("กางเกง", "ตัว")))
        return MathDraw("", str(ans),
                        prompt=(f"{item}{cl}ละ {grouped(price)} บาท ลดราคาร้อยละ {pct} "
                                f"ซื้อ {n} {cl} ต้องจ่ายกี่บาท"),
                        distractors=_story.keep(named("steps.missed_a_step", price * n),
                                                named("part.complement", price * n * pct // 100),
                                                named("operation.reversed", after + n),
                                                ans + after, answer=ans, lo=1))


from otk.core.registry import QuestionType, question_type  # noqa: E402
from otk.kit.math_problems import ChoiceType, WordProblem  # noqa: E402
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


# ── More percentages (2026-11): a percent as a fraction, a percent as a decimal, a price raised by a percent,
# and the part left over ──


@question_type("math.percent_to_fraction_p5", display_name={"th": "เขียนร้อยละเป็นเศษส่วนอย่างต่ำ"},
               level=LEVEL, topic="ร้อยละ")
class PercentToFractionP5(ChoiceType):
    _PAIRS = ((50, 1, 2), (25, 1, 4), (75, 3, 4), (20, 1, 5), (40, 2, 5), (60, 3, 5), (80, 4, 5),
              (10, 1, 10), (30, 3, 10), (70, 7, 10), (90, 9, 10), (5, 1, 20), (35, 7, 20), (45, 9, 20))

    def compose(self, rng: Random):
        pct, a, b = rng.choice(self._PAIRS)
        right = f"{a}/{b}"
        wrongs = [f"{pct}/10", f"1/{pct}", f"{b}/{a}" if a != 1 else f"{pct}/1000", f"{a}/{b + 1}"]
        wrongs = [w for w in dict.fromkeys(wrongs) if w != right]
        return f"ร้อยละ {pct} เขียนเป็นเศษส่วนอย่างต่ำได้อย่างไร", right, wrongs[:3]


@question_type("math.percent_to_decimal_p5", display_name={"th": "เขียนร้อยละเป็นทศนิยม"},
               level=LEVEL, topic="ร้อยละ")
class PercentToDecimalP5(WordProblem):
    def expr(self, rng: Random):
        pct = rng.choice([p for p in range(1, 100) if p % 10] + [10, 30, 50, 70, 90])
        right = _dec(pct, 2)
        prompt = f"{pct}% เขียนในรูปทศนิยมได้เท่าใด"
        # A place too far either way; the percent itself.
        wrongs = list(dict.fromkeys([_dec(pct, 1), _dec(pct, 3), str(pct)]))
        return MathDraw("", right, prompt=prompt, distractors=[w for w in wrongs if w != right])


@question_type("math.percent_increase_price_p5", display_name={"th": "ราคาเพิ่มขึ้นเป็นร้อยละ"},
               level=LEVEL, topic="ร้อยละ")
class PercentIncreasePriceP5(WordProblem):
    def expr(self, rng: Random):
        r = rng.choice((5, 10, 15, 20, 25, 30, 40, 50))
        old = rng.randint(2, 60) * 20
        rise = old * r // 100
        right = old + rise
        what = rng.choice(("ค่าเช่าบ้าน", "ราคาจักรยาน", "ค่าเรียนพิเศษ"))
        prompt = f"{what}เดิม {old:,} บาท ปีนี้เพิ่มขึ้นร้อยละ {r} ปีนี้{what}เป็นกี่บาท"
        # Only the rise; the rate added as baht; a decrease instead.
        return MathDraw("", _g(right), prompt=prompt,
                        distractors=_gk(rise, old + r, old - rise, right + 10 * r, answer=right, lo=1))


@question_type("math.percent_left_over_p5", display_name={"th": "ส่วนที่เหลือคิดเป็นจำนวนเท่าใด"},
               level=LEVEL, topic="ร้อยละ")
class PercentLeftOverP5(WordProblem):
    def expr(self, rng: Random):
        r = rng.choice((80, 85, 90, 95, 75, 60))
        total = rng.choice((20, 40, 60, 80, 100, 120, 200))
        while total * r % 100:
            total += 20
        came = total * r // 100
        right = total - came
        prompt = f"นักเรียนชั้นหนึ่งมี {total} คน มาเรียนร้อยละ {r} ขาดเรียนกี่คน"
        # Those who came; the percent left as a count; the percent itself.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(came, 100 - r, r, right + 2, answer=right, lo=1))


@question_type("math.percent_pass_table_p5", display_name={"th": "เลือกผู้ผ่านเกณฑ์ร้อยละจากตารางคะแนน"},
               level=LEVEL, topic="ร้อยละ")
class PercentPassTableP5(ChoiceType):
    PROVENANCE = Provenance("adapted", sources=(
        "openthaiknowledge-bank/mathematics/level/primary-5/4721-5-2567-2-3.pdf, ข้อ 3",))

    def compose(self, rng: Random):
        while True:
            full, percent = rng.choice((20, 40, 50, 80, 100)), rng.choice((50, 60, 75, 80, 90))
            if full * percent % 100 == 0:
                break
        threshold = full * percent // 100
        names = ("ก", "ข", "ค", "ง", "จ")
        scores = [threshold - 1, threshold, threshold + 1, rng.randint(0, full), rng.randint(0, full)]
        rng.shuffle(scores)
        passed = [i for i, score in enumerate(scores) if 100 * score >= full * percent]
        strict = [i for i, score in enumerate(scores) if 100 * score > full * percent]
        failed = [i for i in range(5) if i not in passed]
        say = lambda indices: " และ ".join(names[i] for i in sorted(indices))
        table = "\n".join(f"{name}: {score} คะแนน" for name, score in zip(names, scores))
        return (f"คะแนนเต็ม {full} คะแนน ผ่านเมื่อได้คะแนนไม่ต่ำกว่าร้อยละ {percent}\n{table}\nใครบ้างสอบผ่าน",
                say(passed),
                # Exclude equality; reverse the cutoff; admit one failing student.
                [say(strict), say(failed), say(passed + [failed[0]])])


@question_type("math.monthly_savings_bonus_p5", display_name={"th": "ออมรายเดือนแล้วรับเงินเพิ่มตามร้อยละของยอดรวม"},
               level=LEVEL, topic="ร้อยละ")
class MonthlySavingsBonusP5(WordProblem):
    PROVENANCE = Provenance("adapted", sources=(
        "openthaiknowledge-bank/mathematics/level/primary-5/4721-5-2567-2-3.pdf, ข้อ 4",))

    def expr(self, rng: Random):
        monthly = 10 * rng.randint(5, 50)
        tenths_percent = rng.choice((25, 45, 50, 75, 100))
        total = monthly * 12
        # Hold money in satang; all selected rates terminate exactly.
        answer = total * (1000 + tenths_percent) // 10
        show = lambda cents: dstr(Decimal(int(cents)) / 100)
        percent = dstr(Decimal(tenths_percent) / 10)
        wrongs = [total * 100, total * tenths_percent // 10,
                  monthly * (1000 + tenths_percent) // 10, total * 100 + tenths_percent * 10]
        return MathDraw("", show(answer),
                        prompt=(f"ออมเงินเดือนละ {monthly} บาท ครบ 12 เดือน "
                                f"เมื่อสิ้นปีได้รับเงินรางวัลเพิ่มร้อยละ {percent} ของยอดที่ออมตลอดปี "
                                "รวมเงินออมและรางวัลเป็นกี่บาท"),
                        distractors=[show(v) for v in _story.keep(*wrongs, answer=answer, lo=1)])


@question_type("math.percent_share_difference_p5", display_name={"th": "ส่วนแบ่งสองส่วนตามร้อยละต่างกันเท่าไร"},
               level=LEVEL, topic="ร้อยละ")
class PercentShareDifferenceP5(WordProblem):
    PROVENANCE = Provenance("adapted", sources=(
        "openthaiknowledge-bank/mathematics/level/primary-5/4721-5-2567-2-3.pdf, ข้อ 6 และตอนที่ 2 ข้อ 1",))

    def expr(self, rng: Random):
        total = 20 * rng.randint(3, 50)
        first = rng.randrange(20, 75, 5)
        second = rng.choice(list(range(5, min(first - 5, 100 - first) + 1, 5)))
        a, b = total * first // 100, total * second // 100
        answer = a - b
        return MathDraw("", str(answer),
                        prompt=(f"มีหนังสือ {total} เล่ม เป็นนิยายร้อยละ {first} "
                                f"เป็นสารคดีร้อยละ {second} นิยายมีมากกว่าสารคดีกี่เล่ม"),
                        distractors=_story.keep(named("operation.reversed", a + b),
                                                named("steps.missed_a_step", a),
                                                named("percent.answered_the_percent", first - second),
                                                answer + 1, answer=answer, lo=1))


@question_type("math.percent_remainder_share_p5", display_name={"th": "กันไว้ตามร้อยละแล้วแบ่งส่วนที่เหลือเท่า ๆ กัน"},
               level=LEVEL, topic="ร้อยละ")
class PercentRemainderShareP5(WordProblem):
    PROVENANCE = Provenance("adapted", sources=(
        "openthaiknowledge-bank/mathematics/level/primary-5/4721-5-2567-2-3.pdf, ข้อ 7",))

    def expr(self, rng: Random):
        groups, unit = rng.randint(2, 25), rng.randint(10, 200)
        total, percent = 100 * groups * unit, rng.randrange(10, 85, 5)
        remaining = total * (100 - percent) // 100
        answer = remaining // groups
        return MathDraw("", str(answer),
                        prompt=(f"มีเงินกิจกรรม {total} บาท กันไว้ร้อยละ {percent} "
                                f"ที่เหลือแบ่งให้ห้องเรียน {groups} ห้องเท่า ๆ กัน แต่ละห้องได้เงินกี่บาท"),
                        distractors=_story.keep(named("part.complement", total * percent // 100 // groups),
                                                named("steps.missed_a_step", remaining),
                                                named("percent.subtracted_the_number", (total - percent) // groups),
                                                remaining - groups, answer + 1, answer=answer, lo=1))


@question_type("math.fraction_decimal_to_percent_p5", display_name={"th": "เปลี่ยนเศษส่วนหรือทศนิยมเป็นร้อยละ"}, level={"th": "ป.5"}, topic="ร้อยละ")
class FractionDecimalToPercentP5(ChoiceType):
    PROVENANCE = Provenance("adapted", sources=("openthaiknowledge-bank/mathematics/level/primary-5/4722-5-2567-2-2.pdf, ข้อ 5–6",))

    def compose(self, rng: Random):
        if rng.choice((False,True)):
            denominator = rng.choice((4,5,10,20,25,50,100))
            numerator = rng.randint(1,denominator-1)
            percent = 100*numerator//denominator
            prompt = f"เศษส่วน {numerator}/{denominator} เขียนเป็นร้อยละได้เท่าใด"
        else:
            percent = rng.randint(1,99)
            prompt = f"ทศนิยม 0.{percent:02d} เขียนเป็นร้อยละได้เท่าใด"
        def label(value):
            return f"{value:.2f}%"
        p = Decimal(percent)
        return prompt,label(p),[label(p/10),label(p*10),label(p/100)]


@question_type("math.percent_expression_comparison_p5", display_name={"th": "เปรียบเทียบค่าร้อยละที่มีฐานต่างกัน"}, level={"th": "ป.5"}, topic="ร้อยละ")
class PercentExpressionComparisonP5(ChoiceType):
    PROVENANCE = Provenance("adapted", sources=("openthaiknowledge-bank/mathematics/level/primary-5/4722-5-2567-2-2.pdf, ข้อ 8",))

    def compose(self, rng: Random):
        pairs=[]
        while len(pairs)<4:
            p,n = rng.randrange(5,100,5),20*rng.randint(5,100)
            if all(p*n != a*b for a,b in pairs):
                pairs.append((p,n))
        most = rng.choice((False,True))
        chosen = (max if most else min)(pairs,key=lambda pair:pair[0]*pair[1])
        labels = [f"{p}% ของ {n}" for p,n in pairs]
        right = f"{chosen[0]}% ของ {chosen[1]}"
        return f"ผลลัพธ์ข้อใดมีค่า{'มาก' if most else 'น้อย'}ที่สุด",right,[x for x in labels if x != right]


@question_type("math.percent_part_sentence_p5", display_name={"th": "เลือกวิธีหาร้อยละของจำนวนหรือส่วนลด"}, level={"th": "ป.5"}, topic="ร้อยละ")
class PercentPartSentenceP5(ChoiceType):
    PROVENANCE = Provenance("adapted", sources=("openthaiknowledge-bank/mathematics/level/primary-5/4722-5-2567-2-2.pdf, ข้อ 7, 10",))

    def compose(self, rng: Random):
        p,total = rng.randrange(5,50,5),rng.randint(2,90)*100
        if rng.choice((False,True)):
            prompt = f"ร้อยละ {p} ของ {total} คำนวณด้วยวิธีใด"
        else:
            prompt = f"สินค้าเดิมราคา {total} บาท ลดราคา {p}% ส่วนลดกี่บาท คำนวณด้วยวิธีใด"
        return (prompt,f"({p} ÷ 100) × {total}",
                [f"(100 ÷ {p}) × {total}",f"({p} ÷ 10) × {total}",f"((100 − {p}) ÷ 100) × {total}"])


@question_type("math.percent_remainder_sentence_p5", display_name={"th": "เลือกวิธีคำนวณส่วนที่เหลือเป็นจำนวนหรือร้อยละ"}, level={"th": "ป.5"}, topic="ร้อยละ")
class PercentRemainderSentenceP5(ChoiceType):
    PROVENANCE = Provenance("adapted", sources=("openthaiknowledge-bank/mathematics/level/primary-5/4722-5-2567-2-2.pdf, ข้อ 11, 14",))

    def compose(self, rng: Random):
        if rng.choice((False,True)):
            whole = rng.randint(20,150)
            part = rng.choice([n for n in range(1,whole) if 2*n != whole])
            prompt = (f"ผลไม้ทั้งหมด {whole} ลูก เป็นแอปเปิล {part} ลูก ที่เหลือเป็นส้ม "
                      "ส้มคิดเป็นกี่เปอร์เซ็นต์ของผลไม้ทั้งหมด เลือกวิธีคำนวณ")
            right = f"(({whole} − {part}) ÷ {whole}) × 100"
            wrongs = [f"({part} ÷ {whole}) × 100",f"({whole} ÷ ({whole} − {part})) × 100",f"({whole} ÷ {part}) × 100"]
        else:
            whole,p = 100*rng.randint(2,90),rng.randrange(5,50,5)
            prompt = (f"ที่ดินทั้งหมด {whole} ไร่ ปลูกมะม่วง {p}% ที่เหลือปลูกข้าว "
                      "ปลูกข้าวกี่ไร่ เลือกวิธีคำนวณ")
            right = f"((100 − {p}) ÷ 100) × {whole}"
            # Increase instead of decrease, invert the base conversion, or subtract
            # the rate from the quantity before dividing by a hundred.
            wrongs = [f"((100 + {p}) ÷ 100) × {whole}",f"((100 − {p}) ÷ {whole}) × 100",
                      f"(({whole} − {p}) ÷ 100) × {whole}"]
        return prompt,right,wrongs


@question_type("math.profit_sale_sentence_p5", display_name={"th": "เลือกวิธีหาราคาขายเมื่อกำไรเป็นร้อยละของทุน"}, level={"th": "ป.5"}, topic="ร้อยละ")
class ProfitSaleSentenceP5(ChoiceType):
    PROVENANCE = Provenance("adapted", sources=("openthaiknowledge-bank/mathematics/level/primary-5/4722-5-2567-2-2.pdf, ข้อ 12",))

    def compose(self, rng: Random):
        cost,p = 100*rng.randint(2,90),rng.randrange(5,50,5)
        prompt = (f"ซื้อสินค้ามาราคา {cost} บาท ต้องการขายให้ได้กำไร {p}% ของราคาทุน "
                  "ราคาขายกี่บาท เลือกวิธีคำนวณ")
        return (prompt,f"{cost} + (({p} ÷ 100) × {cost})",
                [f"{cost} − (({p} ÷ 100) × {cost})",f"({p} ÷ 100) × {cost}",f"{cost} + {p}"])


@question_type("math.profit_rate_sentence_p5", display_name={"th": "เลือกฐานคำนวณร้อยละกำไร"}, level={"th": "ป.5"}, topic="ร้อยละ")
class ProfitRateSentenceP5(ChoiceType):
    PROVENANCE = Provenance("adapted", sources=("openthaiknowledge-bank/mathematics/level/primary-5/4722-5-2567-2-2.pdf, ข้อ 13",))

    def compose(self, rng: Random):
        cost = 100*rng.randint(2,90)
        sale = cost+rng.randint(1,cost//2)
        return (f"ลงทุนทำขนม {cost} บาท ขายหมดได้เงิน {sale} บาท กำไรคิดเป็นกี่เปอร์เซ็นต์ของราคาทุน เลือกวิธีคำนวณ",
                f"(({sale} − {cost}) ÷ {cost}) × 100",
                [f"(({sale} − {cost}) ÷ {sale}) × 100",f"({sale} ÷ {cost}) × 100",f"({cost} ÷ {sale}) × 100"])


@question_type("math.original_from_discount_sentence_p5", display_name={"th": "ย้อนหาราคาเดิมจากจำนวนเงินส่วนลด"}, level={"th": "ป.5"}, topic="ร้อยละ")
class OriginalFromDiscountSentenceP5(ChoiceType):
    PROVENANCE = Provenance("adapted", sources=("openthaiknowledge-bank/mathematics/level/primary-5/4722-5-2567-2-2.pdf, ข้อ 15",))

    def compose(self, rng: Random):
        p = rng.randrange(5,50,5)
        discount = p*rng.randint(2,100)
        return (f"ลดราคาสินค้า {discount} บาท คิดเป็น {p}% ของราคาเดิม ราคาเดิมกี่บาท เลือกวิธีคำนวณ",
                f"(100 ÷ {p}) × {discount}",
                [f"({p} ÷ 100) × {discount}",f"({100-p} ÷ 100) × {discount}",f"(100 ÷ {100-p}) × {discount}"])


@question_type("math.cost_from_loss_sentence_p5", display_name={"th": "ย้อนหาราคาทุนจากราคาขายและร้อยละขาดทุน"}, level={"th": "ป.5"}, topic="ร้อยละ")
class CostFromLossSentenceP5(ChoiceType):
    PROVENANCE = Provenance("adapted", sources=("openthaiknowledge-bank/mathematics/level/primary-5/4722-5-2567-2-2.pdf, ข้อ 16",))

    def compose(self, rng: Random):
        p = rng.randrange(5,50,5)
        sale = (100-p)*rng.randint(2,100)
        return (f"ขายสินค้าราคา {sale} บาท ขาดทุน {p}% ของราคาทุน ราคาทุนกี่บาท เลือกวิธีคำนวณ",
                f"(100 ÷ (100 − {p})) × {sale}",
                [f"((100 − {p}) ÷ 100) × {sale}",f"((100 + {p}) ÷ 100) × {sale}",f"(100 ÷ (100 + {p})) × {sale}"])
