"""ร้อยละ

คณิตศาสตร์ · ป.6 · สสวท. พื้นฐาน
Indicators: ค 1.1 ป.6/*

Sets moved here from: math, math_p6.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, MathType, WordProblem
from otk.sets._support.math_p4 import grouped
from otk.sets._support.math_p6 import LEVEL

PROVENANCE = Provenance("original")


_RATIO_PCT = [
    (1, 2, 50), (1, 4, 25), (3, 4, 75),
    (1, 5, 20), (2, 5, 40), (3, 5, 60), (4, 5, 80),
    (1, 10, 10), (3, 10, 30), (7, 10, 70), (9, 10, 90),
    (1, 20, 5), (3, 20, 15), (7, 20, 35), (9, 20, 45),
    (11, 20, 55), (13, 20, 65), (17, 20, 85), (19, 20, 95),
    (1, 25, 4), (2, 25, 8), (3, 25, 12), (4, 25, 16),
]


_PC_TOPIC = "ร้อยละ"


@question_type("math.ratio_to_percent",
               display_name={"th": "เศษส่วนเป็นร้อยละ"}, level={"th": "ป.6"},
               topic="ร้อยละ")
class RatioToPercent(MathType):
    def expr(self, rng: Random):
        a, b, pct = rng.choice(_RATIO_PCT)
        return MathDraw(rf"\frac{{{a}}}{{{b}}}", rf"{pct}\%",
                        hint=r"\text{multiply by } 100", prompt="จงเขียนเป็นร้อยละ")


@question_type("math.percent_to_ratio",
               display_name={"th": "ร้อยละเป็นเศษส่วน"}, level={"th": "ป.6"},
               topic="ร้อยละ")
class PercentToRatio(MathType):
    def expr(self, rng: Random):
        a, b, pct = rng.choice(_RATIO_PCT)
        return MathDraw(rf"{pct}\%", rf"\frac{{{a}}}{{{b}}}",
                        hint=r"\text{divide by } 100 \text{, simplify}",
                        prompt="จงเขียนเป็นเศษส่วน")


@question_type("math.simple_interest",
               display_name={"th": "ดอกเบี้ยอย่างง่าย"}, level={"th": "ป.6"},
               topic="ร้อยละ")
class SimpleInterest(WordProblem):
    def expr(self, rng: Random):
        p = rng.randint(1, 20) * 1000
        r = rng.choice([1, 2, 3, 4, 5])
        t = rng.randint(1, 4)
        interest = p * r * t // 100
        who = rng.choice(_story.NAMES)
        kind = rng.randrange(3)
        if kind == 0:
            return MathDraw("", str(interest),
                            prompt=(f"{who}ฝากเงิน {p} บาท ได้ดอกเบี้ยร้อยละ {r} ต่อปี "
                                    f"เป็นเวลา {t} ปี ได้ดอกเบี้ยกี่บาท"),
                            # One year's interest, and the whole balance.
                            distractors=_story.keep(p * r // 100, p + interest, interest * 2,
                                                    answer=interest))
        if kind == 1:
            return MathDraw("", str(p + interest),
                            prompt=(f"{who}ฝากเงิน {p} บาท ได้ดอกเบี้ยร้อยละ {r} ต่อปี "
                                    f"ครบ {t} ปี จะมีเงินรวมกี่บาท"),
                            distractors=_story.keep(interest, p + p * r // 100, p * r * t,
                                                    answer=p + interest))
        return MathDraw("", str(interest),
                        prompt=(f"{who}กู้เงิน {p} บาท เสียดอกเบี้ยร้อยละ {r} ต่อปี "
                                f"เป็นเวลา {t} ปี ต้องเสียดอกเบี้ยกี่บาท"),
                        distractors=_story.keep(p * r // 100, p + interest, interest * 2,
                                                answer=interest))


@question_type("math.profit_loss_p6",
               display_name={"th": "กำไร ขาดทุน และร้อยละ"},
               level=LEVEL, topic=_PC_TOPIC)
class ProfitLossP6(WordProblem):
    def expr(self, rng: Random):
        cost = rng.randint(4, 60) * 100          # every percent of it is whole
        pct = rng.choice((5, 10, 15, 20, 25, 30, 40))
        diff = cost * pct // 100
        goods = rng.choice(("จักรยาน", "โทรศัพท์", "โต๊ะ", "พัดลม", "นาฬิกา", "กระเป๋า"))
        kind = rng.randrange(4)
        if kind == 0:
            ans = cost + diff
            return MathDraw("", str(ans),
                            prompt=(f"แม่ค้าซื้อ{goods}มาราคา {grouped(cost)} บาท ต้องการขายให้ได้กำไร "
                                    f"ร้อยละ {pct} ต้องขายราคากี่บาท"),
                            distractors=_story.keep(diff, cost - diff, cost + pct, answer=ans))
        if kind == 1:
            ans = cost - diff
            return MathDraw("", str(ans),
                            prompt=(f"ซื้อ{goods}มาราคา {grouped(cost)} บาท ขายไปขาดทุนร้อยละ {pct} "
                                    f"ขายไปราคากี่บาท"),
                            distractors=_story.keep(cost + diff, diff, cost - pct, answer=ans))
        if kind == 2:
            return MathDraw("", str(pct),
                            prompt=(f"ซื้อ{goods}มาราคา {grouped(cost)} บาท ขายไป {grouped(cost + diff)} บาท "
                                    f"ได้กำไรร้อยละเท่าใด"),
                            # Profit over the selling price, and the profit in baht.
                            distractors=_story.keep(diff * 100 // (cost + diff), diff, pct + 5,
                                                    100 - pct, answer=pct, lo=1))
        return MathDraw("", str(diff),
                        prompt=(f"ซื้อ{goods}มาราคา {grouped(cost)} บาท ขายไป {grouped(cost - diff)} บาท "
                                f"ขาดทุนกี่บาท"),
                        distractors=_story.keep(pct, cost + diff, 2 * cost - diff, answer=diff, lo=1))


@question_type("math.percent_change_p6",
               display_name={"th": "ร้อยละของการเพิ่มขึ้นและลดลง"},
               level=LEVEL, topic=_PC_TOPIC)
class PercentChangeP6(WordProblem):
    def expr(self, rng: Random):
        base = rng.randint(2, 40) * 20
        pct = rng.choice((5, 10, 15, 20, 25, 40, 50))
        change = base * pct // 100
        what = rng.choice((("นักเรียนในโรงเรียน", "คน"), ("ราคาข้าวสาร 1 กระสอบ", "บาท"),
                           ("จำนวนต้นไม้ในสวน", "ต้น")))
        noun, unit = what
        up = rng.random() < 0.5
        if rng.random() < 0.5:
            ans = base + change if up else base - change
            return MathDraw("", str(ans),
                            prompt=(f"ปีที่แล้ว{noun}มี {base} {unit} ปีนี้{'เพิ่มขึ้น' if up else 'ลดลง'}"
                                    f"ร้อยละ {pct} ปีนี้มีกี่{unit}"),
                            distractors=_story.keep(change, base - change if up else base + change,
                                                    base + pct if up else base - pct,
                                                    answer=ans, lo=1))
        after = base + change if up else base - change
        return MathDraw("", str(pct),
                        prompt=(f"ปีที่แล้ว{noun}มี {base} {unit} ปีนี้มี {after} {unit} "
                                f"{'เพิ่มขึ้น' if up else 'ลดลง'}ร้อยละเท่าใด"),
                        distractors=_story.keep(change, change * 100 // after, pct + 10,
                                                answer=pct, lo=1))
