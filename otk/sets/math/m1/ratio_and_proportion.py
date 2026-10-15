"""อัตราส่วนและสัดส่วน

คณิตศาสตร์ · ม.1 · สสวท. พื้นฐาน
Indicators: ค 1.1 ม.1/3

Sets moved here from: math, math_m1, math_number.
"""

from __future__ import annotations

import math
import math as _math
from fractions import Fraction
from random import Random

from otk.core.content import math as content_math
from otk.core.content import text
from otk.core.mistakes import named
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, MathType, WordProblem, frac_tex
from otk.sets._support.math_m1 import LEVEL
from otk.sets._support.math_p2 import _maths
from otk.sets._support.math_p4 import grouped

PROVENANCE = Provenance("original")


_RATIO_TOPIC = "อัตราส่วนและสัดส่วน"


@question_type("math.solve_proportion",
               display_name={"th": "แก้สัดส่วน"}, level={"th": "ม.1"},
               topic="อัตราส่วนและสัดส่วน")
class SolveProportion(WordProblem):
    def expr(self, rng: Random):
        a = rng.randint(2, 9)
        t = rng.randint(2, 6)
        b = a * t
        c = rng.randint(2, 9)
        x = t * c                                   # x = b·c / a
        prompt = rng.choice((
            f"ถ้า {a} : {b} = {c} : x แล้ว x เท่ากับเท่าใด?",
            f"ทำขนม {a} ชิ้นใช้แป้ง {b} ช้อน ถ้าทำขนม {c} ชิ้น ต้องใช้แป้งกี่ช้อน",
            f"ซื้อสมุด {a} เล่มราคา {b} บาท ถ้าซื้อสมุดแบบเดียวกัน {c} เล่ม ต้องจ่ายกี่บาท",
            f"เดิน {a} รอบสนามได้ระยะทาง {b} กิโลเมตร ถ้าเดิน {c} รอบ จะได้ระยะทางกี่กิโลเมตร",
        ))
        return MathDraw("", str(x), prompt=prompt,
                        distractors=[str(a * c), str(b + c - a), str(a * b // c)])


@question_type("math.simplify_ratio", display_name={"th": "อัตราส่วนอย่างต่ำ"},
               level={"th": "ม.1"}, topic="อัตราส่วนและสัดส่วน")
class SimplifyRatio(MathType):
    def expr(self, rng: Random, part_hi: int = 12, scale_hi: int = 9):
        a, b = rng.randint(1, part_hi), rng.randint(1, part_hi)
        g = _math.gcd(a, b)
        a, b = a // g, b // g                     # start from lowest terms
        k = rng.randint(2, scale_hi)
        return MathDraw(f"{a * k} : {b * k}", f"{a} : {b}",
                        prompt="จงเขียนอัตราส่วนนี้ในรูปอย่างต่ำ",
                        distractors=[f"{b} : {a}", f"{a * k} : {b}",
                                     f"{a + 1} : {b + 1}"])


@question_type("math.three_term_ratio_m1",
               display_name={"th": "อัตราส่วนของจำนวนหลายจำนวน"},
               level=LEVEL, topic=_RATIO_TOPIC)
class ThreeTermRatioM1(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        a, b1 = rng.sample(range(1, 10), 2)
        b2, c = rng.sample(range(1, 10), 2)
        length = b1 * b2 // math.gcd(b1, b2)
        A, B, C = a * length // b1, length, c * length // b2
        g = math.gcd(math.gcd(A, B), C)
        A, B, C = A // g, B // g, C // g
        if rng.random() < 0.5:
            right = f"{A} : {B} : {C}"
            # Writing the two ratios side by side without matching b.
            wrongs = [f"{a} : {b1} : {c}", f"{a} : {b1 * b2} : {c}", f"{a * b2} : {b1 * b2} : {c * b1 + 1}",
                      f"{C} : {B} : {A}", f"{A} : {C} : {B}", f"{B} : {A} : {C}", f"{A + 1} : {B} : {C}"]
            return _maths([text("ถ้า"), content_math(rf"a : b = {a} : {b1}"), text("และ"),
                           content_math(rf"b : c = {b2} : {c}"), text("แล้ว a : b : c เท่ากับข้อใด")],
                          right, [w for w in dict.fromkeys(wrongs) if w != right], self.topic)
        unit = rng.randint(2, 30) * 10
        total = (A + B + C) * unit
        p, q, r = _story.names(rng, 3)
        ans = C * unit
        return _maths([text(f"แบ่งเงิน {grouped(total)} บาท ให้{p} {q} และ{r} ในอัตราส่วน {A} : {B} : {C} "
                             f"{r}ได้เงินกี่บาท")], str(ans),
                      _story.keep(A * unit, B * unit, total // C if total % C == 0 else ans + unit,
                                  total - ans, ans + unit, ans - unit, answer=ans, lo=1), self.topic)


@question_type("math.proportion_word_problem_m1",
               display_name={"th": "โจทย์ปัญหาสัดส่วน"},
               level=LEVEL, topic=_RATIO_TOPIC)
class ProportionWordProblemM1(WordProblem):
    def expr(self, rng: Random):
        kind = rng.randrange(3)
        a, b = rng.sample(range(2, 12), 2)
        if kind == 0:
            per = rng.randint(8, 18)
            return MathDraw("", str(b * 5),
                            prompt=(f"รถยนต์ใช้น้ำมัน {a * 5} ลิตร แล่นได้ {a * 5 * per} กิโลเมตร ถ้าแล่นด้วย"
                                    f"อัตราเดิมเป็นระยะทาง {b * 5 * per} กิโลเมตร จะใช้น้ำมันกี่ลิตร"),
                            distractors=_story.keep(a * 5 * b, b * per, a * 5 + b, b * 5 + per,
                                                    answer=b * 5, lo=1))
        if kind == 1:
            scale = rng.choice((10_000, 25_000, 50_000, 100_000))
            cm = rng.randint(2, 30)
            km = cm * scale // 100_000
            m = cm * scale // 100
            if cm * scale % 100_000 == 0:
                return MathDraw("", str(km),
                                prompt=(f"แผนที่มาตราส่วน 1 : {grouped(scale)} ระยะทางบนแผนที่ {cm} เซนติเมตร "
                                        f"คิดเป็นระยะทางจริงกี่กิโลเมตร"),
                                distractors=_story.keep(m, km * 10, cm * scale, answer=km, lo=1))
            return MathDraw("", str(m),
                            prompt=(f"แผนที่มาตราส่วน 1 : {grouped(scale)} ระยะทางบนแผนที่ {cm} เซนติเมตร "
                                    f"คิดเป็นระยะทางจริงกี่เมตร"),
                            distractors=_story.keep(m * 10, m // 10, cm * scale, answer=m, lo=1))
        per = rng.randint(3, 25)
        return MathDraw("", str(per * b),
                        prompt=(f"ช่างทาสีทาผนังได้ {per * a} ตารางเมตร ใน {a} ชั่วโมง ถ้าทาด้วยอัตราเดิม "
                                f"{b} ชั่วโมง จะทาได้กี่ตารางเมตร"),
                        distractors=_story.keep(per * a * b, per * a + b, per, answer=per * b, lo=1))


@question_type("math.percent_word_problem_m1",
               display_name={"th": "โจทย์ปัญหาร้อยละ (ภาษีมูลค่าเพิ่ม ราคาเดิม ร้อยละของการเปลี่ยนแปลง)"},
               level=LEVEL, topic=_RATIO_TOPIC)
class PercentWordProblemM1(WordProblem):
    def expr(self, rng: Random):
        kind = rng.randrange(6)
        if kind == 3:
            principal = rng.randint(2, 50) * 1000
            rate = rng.choice((1, 2, 3, 4, 5))
            ans = principal + principal * rate // 100
            return MathDraw("", str(ans),
                            prompt=(f"ฝากเงิน {grouped(principal)} บาท ได้ดอกเบี้ยร้อยละ {rate} ต่อปี "
                                    f"เมื่อครบ 1 ปี จะมีเงินรวมกี่บาท"),
                            distractors=_story.keep(principal * rate // 100, principal + rate,
                                                    principal + principal * rate // 10, answer=ans, lo=1))
        if kind == 4:
            sales = rng.randint(5, 80) * 1000
            rate = rng.choice((2, 3, 5, 8, 10))
            ans = sales * rate // 100
            return MathDraw("", str(ans),
                            prompt=(f"พนักงานขายได้ค่าคอมมิชชันร้อยละ {rate} ของยอดขาย เดือนนี้ขายได้ "
                                    f"{grouped(sales)} บาท ได้ค่าคอมมิชชันกี่บาท"),
                            distractors=_story.keep(sales - ans, ans * 10, sales // rate, answer=ans, lo=1))
        if kind == 5:
            total = rng.choice((20, 25, 40, 50))
            got = rng.randint(total // 4, total - 1)
            while got * 100 % total:
                got += 1
            pct = got * 100 // total
            return MathDraw("", str(pct),
                            prompt=(f"ข้อสอบมี {total} ข้อ {rng.choice(_story.NAMES)}ตอบถูก {got} ข้อ "
                                    f"คิดเป็นร้อยละเท่าใด"),
                            distractors=_story.keep(got, total - got, 100 - pct, answer=pct, lo=1))
        if kind == 0:
            price = rng.randint(1, 40) * 100
            vat = price * 7 // 100
            return MathDraw("", str(price + vat),
                            prompt=(f"สินค้าราคา {grouped(price)} บาท ยังไม่รวมภาษีมูลค่าเพิ่มร้อยละ 7 "
                                    f"ต้องจ่ายเงินรวมภาษีกี่บาท"),
                            distractors=_story.keep(vat, price - vat, price + 7, answer=price + vat,
                                                    lo=1))
        if kind == 1:
            pct = rng.choice((10, 20, 25, 40, 50))
            original = rng.randint(2, 40) * 100
            paid = original * (100 - pct) // 100
            return MathDraw("", str(original),
                            prompt=(f"ร้านลดราคาร้อยละ {pct} {rng.choice(_story.NAMES)}จ่ายเงิน {grouped(paid)} บาท "
                                    f"ราคาเดิมของสินค้าเป็นกี่บาท"),
                            # Adding pct of the paid price back is the classic slip.
                            distractors=_story.keep(paid + paid * pct // 100, paid + pct,
                                                    paid * (100 + pct) // 100 + 10, answer=original,
                                                    lo=1))
        base = rng.randint(2, 40) * 50
        pct = rng.choice((4, 5, 10, 12, 15, 20, 25, 30))
        if base * pct % 100:
            base *= 2
        new = base + base * pct // 100
        return MathDraw("", str(pct),
                        prompt=(f"ปีที่แล้วโรงงานผลิตสินค้าได้ {grouped(base)} ชิ้น ปีนี้ผลิตได้ {grouped(new)} ชิ้น "
                                f"ผลิตได้เพิ่มขึ้นร้อยละเท่าใด"),
                        distractors=_story.keep(new - base, (new - base) * 100 // new, pct + 5,
                                                answer=pct, lo=1))


@question_type("math.inverse_work_proportion_m1",
               display_name={"th": "จำนวนคนกับเวลาทำงานแบบแปรผกผัน"},
               level=LEVEL, topic=_RATIO_TOPIC)
class InverseWorkProportionM1(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        old_workers, new_workers = rng.sample((3, 4, 5, 6, 8, 10), 2)
        total_worker_days = math.lcm(old_workers, new_workers) * rng.randint(2, 5)
        old_days = total_worker_days // old_workers
        new_days = total_worker_days // new_workers
        wrongs = [
            named("proportion.direct_instead_of_inverse", frac_tex(Fraction(old_days * new_workers,
                                                                        old_workers))),
            named("proportion.kept_time_fixed", str(old_days)),
            named("proportion.multiplied_without_dividing", str(total_worker_days)),
        ]
        return _maths([text(f"ช่าง {old_workers} คน ทำงานชิ้นหนึ่งเสร็จใน {old_days} วัน "
                            f"ถ้าช่างทุกคนทำงานเร็วเท่ากันและมีช่าง {new_workers} คน "
                            "จะทำงานชิ้นเดิมเสร็จในกี่วัน")],
                      str(new_days), wrongs, self.topic)


@question_type("math.map_area_scale_m1",
               display_name={"th": "พื้นที่จริงจากมาตราส่วนแผนที่"},
               level=LEVEL, topic=_RATIO_TOPIC)
class MapAreaScaleM1(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        scale = rng.choice((50_000, 200_000, 300_000))
        length, width = rng.randint(3, 12), rng.randint(2, 9)
        km_per_cm = Fraction(scale, 100_000)
        map_area = length * width
        area = map_area * km_per_cm ** 2
        wrongs = [
            named("proportion.area_scaled_once", frac_tex(map_area * km_per_cm)),
            named("proportion.map_area_unscaled", str(map_area)),
            named("proportion.scale_reversed", frac_tex(map_area / km_per_cm ** 2)),
        ]
        return _maths([text(f"แผนที่มาตราส่วน 1 : {grouped(scale)} แสดงที่ดินรูปสี่เหลี่ยมผืนผ้า "
                            f"ยาว {length} เซนติเมตร กว้าง {width} เซนติเมตร "
                            "ที่ดินจริงมีพื้นที่กี่ตารางกิโลเมตร")],
                      frac_tex(area), wrongs, self.topic)


@question_type("math.ratio_after_adding_m1",
               display_name={"th": "สัดส่วนของส่วนผสมหลังเติมวัตถุดิบ"},
               level=LEVEL, topic=_RATIO_TOPIC)
class RatioAfterAddingM1(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        red_parts, blue_parts = rng.sample(range(2, 9), 2)
        batch = rng.randint(3, 9)
        added = rng.randint(2, 12)
        red, blue = red_parts * batch, blue_parts * batch
        total = red + blue
        answer = Fraction(red + added, total + added)
        wrongs = [
            named("proportion.ignored_added_part", frac_tex(Fraction(red, total))),
            named("proportion.changed_total_only", frac_tex(Fraction(red, total + added))),
            named("proportion.changed_part_only", frac_tex(Fraction(red + added, total))),
        ]
        return _maths([text(f"ผสมน้ำสีแดง {red} ลิตร กับน้ำสีน้ำเงิน {blue} ลิตร "
                            f"แล้วเติมน้ำสีแดงอีก {added} ลิตร "
                            "น้ำสีแดงคิดเป็นส่วนเท่าใดของน้ำสีทั้งหมดหลังเติม")],
                      frac_tex(answer), wrongs, self.topic)
