"""ดอกเบี้ยและมูลค่าของเงิน

คณิตศาสตร์ · ม.5 · สสวท. พื้นฐาน
Indicators: ค 1.3 ม.5/1

Sets moved here from: math_apply_stage, math_gaps_secondary.
"""

from __future__ import annotations

from random import Random

from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, WordProblem
from otk.sets._support.math_apply_stage import _n, _nums
from otk.sets._support.math_gaps_secondary import _choices, _num
from otk.sets._support.math_m4 import maths

PROVENANCE = Provenance("original")


_MONEY_TOPIC = "ดอกเบี้ยและมูลค่าของเงิน"


def _baht(x: float) -> str:
    return f"{x:,.2f}".replace(",", "{,}")


@question_type("math.simple_interest_years_m5", display_name={"th": "ดอกเบี้ยคงต้นหลายปี"},
               level={"th": "ม.5"}, topic=_MONEY_TOPIC)
class SimpleInterestYearsM5(WordProblem):
    def expr(self, rng: Random):
        p, r, n = rng.choice((10_000, 20_000, 50_000)), rng.choice((2, 3, 4, 5)), rng.randint(2, 5)
        interest = p * r * n // 100
        if rng.random() < 0.5:
            return MathDraw("", _num(interest), prompt=(
                f"ฝากเงิน {p:,} บาท ได้ดอกเบี้ยคงต้น (ดอกเบี้ยอย่างง่าย) ร้อยละ {r} ต่อปี "
                f"เมื่อครบ {n} ปี ได้ดอกเบี้ยรวมกี่บาท"),
                distractors=[_num(int(v)) for v in
                             _story.keep(p * r // 100, p * r * n // 10, p + interest, answer=interest, lo=1)])
        total = p + interest
        return MathDraw("", _num(total), prompt=rng.choice((
            f"ฝากเงิน {p:,} บาท ได้ดอกเบี้ยคงต้นร้อยละ {r} ต่อปี เมื่อครบ {n} ปี จะมีเงินรวมกี่บาท",
            f"กู้เงิน {p:,} บาท เสียดอกเบี้ยคงต้นร้อยละ {r} ต่อปี และคืนเงินครั้งเดียวเมื่อครบ {n} ปี "
            f"ต้องคืนเงินทั้งหมดกี่บาท",
        )),
            distractors=[_num(int(v)) for v in
                         _story.keep(interest, p + p * r // 100, p * (100 + r) ** n // 100 ** n,
                                     answer=total, lo=1)])


@question_type("math.future_present_value_m5", display_name={"th": "มูลค่าในอนาคตและมูลค่าปัจจุบันของเงิน"},
               level={"th": "ม.5"}, topic=_MONEY_TOPIC)
class FuturePresentValueM5(WordProblem):
    def expr(self, rng: Random):
        r, n = rng.choice((2, 3, 4, 5)), rng.randint(2, 4)
        factor = round((1 + r / 100) ** n, 4)
        if rng.random() < 0.5:
            p = rng.choice((10_000, 20_000, 40_000, 50_000))
            fv = p * factor
            return MathDraw("", _baht(fv), prompt=(
                f"ฝากเงิน {p:,} บาท ได้ดอกเบี้ยทบต้นร้อยละ {r} ต่อปี เมื่อครบ {n} ปี มีเงินรวมกี่บาท "
                f"(กำหนด (1 + {r / 100:g})^{n} ≈ {factor})"),
                distractors=[_baht(v) for v in (p * (1 + r * n / 100), p * factor / (1 + r / 100), p * (factor - 1))])
        fv = rng.choice((20_000, 50_000, 100_000))
        pv = fv / factor
        return MathDraw("", _baht(pv), prompt=(
            f"ต้องการมีเงิน {fv:,} บาทในอีก {n} ปีข้างหน้า ถ้าได้ดอกเบี้ยทบต้นร้อยละ {r} ต่อปี "
            f"ต้องฝากเงินตอนนี้กี่บาท (กำหนด (1 + {r / 100:g})^{n} ≈ {factor})"),
            distractors=[_baht(v) for v in (fv * factor, fv * (1 - r * n / 100), fv - fv * r / 100)])


@question_type("math.interest_plan_m5", display_name={"th": "วางแผนการออมและการซื้อด้วยดอกเบี้ย"},
               level={"th": "ม.5"}, topic="ดอกเบี้ยและมูลค่าของเงิน")
class InterestPlanM5(QuestionType):
    def build(self, rng: Random, **params) -> GeneratedQuestion:
        kind = rng.randrange(3)
        who = rng.choice(_story.NAMES)
        if kind == 0:
            p, r = rng.choice((10_000, 20_000, 50_000)), rng.choice((2, 4, 5))
            years = rng.randint(2, 8)
            target = p + p * r * years // 100
            stem = (f"{who}ฝากเงิน {p:,} บาท ได้ดอกเบี้ยคงต้นร้อยละ {r} ต่อปี ต้องฝากกี่ปีจึงจะมีเงินรวม "
                    f"{target:,} บาท")
            return maths([text(stem)], str(years), _nums(years, target // p, years + 1, 100 // r, lo=1), self.topic)
        if kind == 1:
            p, years = rng.choice((10_000, 20_000, 40_000, 50_000)), rng.randint(2, 5)
            r = rng.choice((2, 3, 4, 5, 6))
            target = p + p * r * years // 100
            stem = (f"{who}ฝากเงิน {p:,} บาท เป็นเวลา {years} ปี แบบดอกเบี้ยคงต้น แล้วได้เงินรวม {target:,} บาท "
                    f"ได้ดอกเบี้ยร้อยละเท่าใดต่อปี")
            return maths([text(stem)], str(r), _nums(r, r * years, (target - p) * 100 // p, r + 1, lo=1), self.topic)
        price = rng.choice((12_000, 15_000, 18_000, 24_000))
        disc = rng.choice((5, 10))
        k = rng.choice((6, 10, 12))
        each = price * (100 + rng.choice((5, 8, 10))) // 100 // k
        cash = price * (100 - disc) // 100
        extra = k * each - cash
        stem = (f"โทรศัพท์ราคา {price:,} บาท ถ้าจ่ายเงินสดได้ส่วนลดร้อยละ {disc} ถ้าผ่อน {k} งวด ต้องจ่ายงวดละ "
                f"{each:,} บาท การผ่อนต้องจ่ายมากกว่าการจ่ายเงินสดกี่บาท")
        return maths([text(stem)], _n(extra), _nums(extra, k * each - price, price - cash, k * each, lo=1),
                     self.topic)


@question_type("math.compare_offers_m5", display_name={"th": "เปรียบเทียบทางเลือกการออมและการกู้"},
               level={"th": "ม.5"}, topic=_MONEY_TOPIC)
class CompareOffersM5(QuestionType):
    def build(self, rng: Random, **params) -> GeneratedQuestion:
        p, n = rng.choice((10_000, 50_000, 100_000)), rng.randint(2, 4)
        r_simple = rng.choice((4, 5, 6))
        r_comp = r_simple - 1 if rng.random() < 0.5 else r_simple
        a = p * (1 + r_simple * n / 100)
        factor = round((1 + r_comp / 100) ** n, 4)
        b = p * factor
        if abs(a - b) < 1:
            r_comp += 1
            factor = round((1 + r_comp / 100) ** n, 4)
            b = p * factor
        best = "ธนาคาร ก" if a > b else "ธนาคาร ข"
        other = "ธนาคาร ข" if best == "ธนาคาร ก" else "ธนาคาร ก"
        stem = [text(f"ฝากเงิน {p:,} บาท เป็นเวลา {n} ปี ธนาคาร ก ให้ดอกเบี้ยคงต้นร้อยละ {r_simple} ต่อปี "
                     f"ธนาคาร ข ให้ดอกเบี้ยทบต้นร้อยละ {r_comp} ต่อปี "
                     f"(กำหนด (1 + {r_comp / 100:g})^{n} ≈ {factor:.4f}) "
                     f"ฝากธนาคารใดได้เงินรวมมากกว่า")]
        return _choices(stem, f"{best} ได้มากกว่าประมาณ {abs(a - b):,.2f} บาท",
                        [f"{other} ได้มากกว่าประมาณ {abs(a - b):,.2f} บาท",
                         "ได้เงินเท่ากันทั้งสองธนาคาร",
                         f"{best} ได้มากกว่าประมาณ {abs(a - b) * n:,.2f} บาท",
                         # The wrong bank and the wrong amount.
                         f"{other} ได้มากกว่าประมาณ {abs(a - b) * n:,.2f} บาท"], self.topic)
