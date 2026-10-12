"""ค่าคาดหมาย

คณิตศาสตร์ · ม.5 · สสวท. เพิ่มเติม
Indicators: ค เพิ่มเติม สถิติและความน่าจะเป็น 1 ม.5/2

Sets moved here from: math, math_apply_add, math_data.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, MathType, WordProblem, frac_tex
from otk.sets._support.math_apply_add import M5, _c, _fr

PROVENANCE = Provenance("original")


@question_type("math.expected_value_dice", display_name={"th": "ค่าคาดหมายจากลูกเต๋า"},
               level={"th": "ม.6"}, topic="ค่าคาดหมาย")
class ExpectedValueDice(WordProblem):
    invent_numbers = True  # computed answer: near values on the short side cannot be right
    def expr(self, rng: Random, faces: int = 6, prize_hi: int = 100):
        prize = rng.randrange(10, prize_hi, 10)
        # Win `prize` on one face out of `faces`, nothing otherwise.
        value = Fraction(prize, faces)
        prompt = rng.choice((
            f"ทอดลูกเต๋า {faces} หน้าหนึ่งลูก ถ้าออกแต้ม 6 ได้รางวัล "
            f"{prize} บาท มิฉะนั้นไม่ได้อะไร ค่าคาดหมายของรางวัลเป็นกี่บาท",
            f"วงล้อแบ่งเป็น {faces} ช่องเท่า ๆ กัน มีช่องรางวัล {prize} บาทอยู่ 1 ช่อง "
            f"ช่องอื่นไม่ได้อะไร หมุนวงล้อหนึ่งครั้ง ค่าคาดหมายของรางวัลเป็นกี่บาท",
            f"ในกล่องมีสลาก {faces} ใบ เป็นสลากรางวัล {prize} บาทอยู่ 1 ใบ ที่เหลือไม่ได้อะไร "
            f"สุ่มหยิบหนึ่งใบ ค่าคาดหมายของรางวัลเป็นกี่บาท",
        ))
        return MathDraw(
            "", frac_tex(value), prompt=prompt,
            distractors=[str(prize), frac_tex(Fraction(prize, faces - 1)),
                         frac_tex(Fraction(prize * 5, faces))])


@question_type("math.expected_value",
               display_name={"th": "ค่าคาดหมาย"}, level={"th": "ม.6"},
               topic="ค่าคาดหมาย")
class ExpectedValue(MathType):
    def expr(self, rng: Random):
        kind = rng.choice(["die", "two_dice", "heads", "die_sq"])
        if kind == "die":
            return MathDraw(r"E[X]", frac_tex(Fraction(7, 2)),
                            prompt="ให้ X เป็นแต้มจากการทอดลูกเต๋า 1 ลูก")
        if kind == "two_dice":
            return MathDraw(r"E[X]", "7",
                            prompt="ให้ X เป็นผลรวมแต้มจากลูกเต๋า 2 ลูก")
        if kind == "heads":
            n = rng.choice([3, 5, 7])
            return MathDraw(r"E[X]", frac_tex(Fraction(n, 2)),
                            prompt=f"ให้ X เป็นจำนวนหัวจากการโยนเหรียญ {n} ครั้ง")
        return MathDraw(r"E[X^{2}]", frac_tex(Fraction(91, 6)),
                        prompt="ให้ X เป็นแต้มจากการทอดลูกเต๋า 1 ลูก")


@question_type("math.expected_value_game_m5",
               display_name={"th": "ค่าคาดหมายของเกม ลอตเตอรี่ และประกัน"},
               level=M5, topic="ค่าคาดหมาย")
class ExpectedValueGameM5(WordProblem):
    def expr(self, rng: Random):
        kind = rng.randrange(5)
        if kind == 0:
            big, small = rng.choice((30, 36, 42, 48, 60)), rng.choice((6, 9, 12, 15))
            fee = rng.randint(5, 15)
            ev = Fraction(big + 2 * small, 6) - fee
            return MathDraw("", _fr(ev),
                            prompt=(f"เกมทอดลูกเต๋าหนึ่งลูก ต้องจ่ายค่าเล่นครั้งละ {fee} บาท ถ้าได้ 6 ได้รางวัล {big} บาท "
                                    f"ถ้าได้ 4 หรือ 5 ได้รางวัล {small} บาท นอกนั้นไม่ได้รางวัล "
                                    f"ผู้เล่นคาดว่าจะได้กำไรเฉลี่ยครั้งละกี่บาท (ค่าติดลบหมายถึงขาดทุน)"),
                            distractors=[_fr(ev + fee), _fr(Fraction(big + small, 6) - fee), _fr(-ev)])
        if kind == 1:
            big, small = rng.choice((40, 60, 80, 100)), rng.choice((10, 20, 30))
            fair = Fraction(big, 4) + Fraction(small, 2)
            return MathDraw("", _fr(fair),
                            prompt=(f"เกมโยนเหรียญสองเหรียญ ถ้าออกหัวทั้งสองเหรียญได้รางวัล {big} บาท "
                                    f"ถ้าออกหัวเหรียญเดียวได้รางวัล {small} บาท ถ้าไม่ออกหัวเลยไม่ได้อะไร "
                                    f"ค่าเล่นควรเป็นกี่บาทเกมนี้จึงจะยุติธรรม"),
                            distractors=[_fr(Fraction(big + small, 3)), _fr(Fraction(big + small, 2)),
                                         _fr(Fraction(big, 4) + Fraction(small, 4))])
        if kind == 2:
            n = rng.choice((500, 1000, 2000))
            first, second, n2 = rng.choice((5000, 10000, 20000)), rng.choice((500, 1000)), rng.choice((5, 10, 20))
            price = rng.choice((20, 40, 50, 80))
            ev = Fraction(first + n2 * second, n) - price
            return MathDraw("", _fr(ev),
                            prompt=(f"สลากชุดหนึ่งมี {_c(n)} ใบ ราคาใบละ {price} บาท มีรางวัลที่หนึ่ง 1 รางวัล "
                                    f"รางวัลละ {_c(first)} บาท และรางวัลที่สอง {n2} รางวัล รางวัลละ {_c(second)} บาท "
                                    f"ผู้ซื้อสลากหนึ่งใบคาดว่าจะได้กำไรกี่บาท (ค่าติดลบหมายถึงขาดทุน)"),
                            distractors=[_fr(ev + price), _fr(Fraction(first + second, n) - price), _fr(-ev)])
        if kind == 3:
            premium = rng.choice((1500, 2000, 2500, 3000))
            claim, per = rng.choice((100000, 200000, 300000)), rng.choice((100, 200, 400))
            ev = premium - Fraction(claim, per)
            return MathDraw("", _fr(ev),
                            prompt=(f"บริษัทประกันเก็บเบี้ยประกันปีละ {_c(premium)} บาท ถ้าผู้เอาประกันเจ็บป่วยจะจ่าย "
                                    f"{_c(claim)} บาท โอกาสที่ผู้เอาประกันหนึ่งคนจะเจ็บป่วยในหนึ่งปีคือ 1 ใน {per} "
                                    f"บริษัทคาดว่าจะได้กำไรจากกรมธรรม์หนึ่งฉบับกี่บาทต่อปี"),
                            distractors=[_fr(Fraction(claim, per)), _fr(premium + Fraction(claim, per)),
                                         _fr(premium - Fraction(claim, 2 * per))])
        red, blue = rng.randint(2, 6), rng.randint(3, 8)
        win, lose = rng.choice((20, 30, 40, 50)), rng.choice((10, 15, 20))
        total = red + blue
        ev = Fraction(red * win - blue * lose, total)
        return MathDraw("", _fr(ev),
                        prompt=(f"ถุงใบหนึ่งมีลูกบอลสีแดง {red} ลูก สีน้ำเงิน {blue} ลูก สุ่มหยิบหนึ่งลูก "
                                f"ถ้าได้สีแดงได้เงิน {win} บาท ถ้าได้สีน้ำเงินเสียเงิน {lose} บาท "
                                f"ค่าคาดหมายของเงินที่ได้ต่อการหยิบหนึ่งครั้งคือกี่บาท"),
                        distractors=[_fr(Fraction(win - lose, 2)), _fr(Fraction(red * win + blue * lose, total)),
                                     _fr(-ev)])


@question_type("math.expected_value_table", display_name={"th": "ค่าคาดหมายจากตารางแจกแจง"},
               level={"th": "ม.6"}, topic="ค่าคาดหมาย")
class ExpectedValueTable(MathType):
    def expr(self, rng: Random, den: int = 10, value_hi: int = 20):
        # Weights over a fixed denominator, so the expectation stays exact.
        weights = [rng.randint(1, den - 2) for _ in range(3)]
        total = sum(weights)
        values = [rng.randint(1, value_hi) for _ in range(3)]
        expectation = sum(Fraction(w, total) * v for w, v in zip(weights, values))
        rows = r",\quad ".join(
            rf"P(X = {v}) = {frac_tex(Fraction(w, total))}"
            for v, w in zip(values, weights))
        return MathDraw(
            rows, frac_tex(expectation), prompt="จงหาค่าคาดหมาย E(X)",
            distractors=[frac_tex(Fraction(sum(values), 3)),
                         str(max(values)),
                         frac_tex(expectation + 1)])
