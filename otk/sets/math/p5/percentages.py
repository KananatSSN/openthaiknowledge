"""ร้อยละ

คณิตศาสตร์ · ป.5 · สสวท. พื้นฐาน
Indicators: ค 1.1 ป.5/*

Sets moved here from: math, math_p5, math_pictures_extra.
"""

from __future__ import annotations

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
from otk.sets._support.math_p5 import LEVEL
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
