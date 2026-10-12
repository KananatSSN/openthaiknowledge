"""แนวรอยต่อของแผ่นธรณี

ธรณีวิทยา · ม.4 · สสวท. เพิ่มเติม
Indicators: โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 1 ม.4/3

Sets moved here from: science_wave_f75.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f75 import SUBJECT, UPPER_FOUR

PROVENANCE = Provenance("original")


TOPIC_MARGIN = "แนวรอยต่อของแผ่นธรณี"


MARGINS = (
    ("แนวแผ่นธรณีแยกตัว", "สันเขากลางมหาสมุทรแอตแลนติก", "เกิดเปลือกโลกใหม่ สันเขากลางมหาสมุทร และหุบเขาทรุด"),
    ("แนวแผ่นธรณีแยกตัว", "หุบเขาทรุดแอฟริกาตะวันออก", "เกิดเปลือกโลกใหม่ สันเขากลางมหาสมุทร และหุบเขาทรุด"),
    ("แผ่นมหาสมุทรชนกับแผ่นทวีป", "เทือกเขาแอนดีสและร่องลึกเปรู-ชิลี", "แผ่นมหาสมุทรมุดลงเกิดร่องลึกก้นสมุทรและแนวภูเขาไฟบนทวีป"),
    ("แผ่นมหาสมุทรชนกับแผ่นมหาสมุทร", "หมู่เกาะญี่ปุ่นและร่องลึกมาเรียนา", "แผ่นหนึ่งมุดลงเกิดร่องลึกก้นสมุทรและหมู่เกาะภูเขาไฟรูปโค้ง"),
    ("แผ่นทวีปชนกับแผ่นทวีป", "เทือกเขาหิมาลัย", "เปลือกโลกโก่งตัวและยกตัวเป็นเทือกเขาสูง แทบไม่มีภูเขาไฟ"),
    ("แนวแผ่นธรณีเลื่อนผ่านกัน", "รอยเลื่อนซานแอนเดรียส", "แผ่นธรณีเลื่อนผ่านกันในแนวราบ เกิดแผ่นดินไหวบ่อย"),
)


MARGIN_HINT = ("แยกตัว: สันเขากลางมหาสมุทร หุบเขาทรุด มหาสมุทรชนทวีป: ร่องลึกและภูเขาไฟบนทวีป มหาสมุทรชนมหาสมุทร: หมู่เกาะภูเขาไฟ "
               "ทวีปชนทวีป: เทือกเขาสูง เลื่อนผ่านกัน: รอยเลื่อนแนวราบ แผ่นธรณีเคลื่อนที่เพราะการพาความร้อนในเนื้อโลก")


@question_type(
    "geo.plate_margin_foundation",
    display_name={"th": "ชนิดของแนวรอยต่อแผ่นธรณีและตัวอย่าง"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_MARGIN,
)
class PlateMarginFoundation(QuestionType):
    """Name the boundary from a real place, and back."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        kind, place, _ = rng.choice(MARGINS)
        kinds = sorted({m[0] for m in MARGINS} - {kind})
        if rng.random() < 0.55:
            return _labelled(stem=f"{place}เกิดจากแนวรอยต่อของแผ่นธรณีแบบใด", correct=kind, wrongs=tuple(kinds), topic=TOPIC_MARGIN,
                             hint=MARGIN_HINT)
        places = [m[1] for m in MARGINS if m[0] != kind]
        return _labelled(stem=f"ข้อใดเป็นตัวอย่างของ{kind}", correct=place, wrongs=tuple(places), topic=TOPIC_MARGIN, hint=MARGIN_HINT)


@question_type(
    "geo.plate_margin_fluency",
    display_name={"th": "ธรณีสัณฐานที่เกิดจากแนวรอยต่อแผ่นธรณี"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_MARGIN,
)
class PlateMarginFluency(QuestionType):
    """What forms at each boundary, and why plates move."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.3:
            facts = (("แรงสำคัญที่ทำให้แผ่นธรณีเคลื่อนที่คือข้อใด", "การพาความร้อนของเนื้อโลก รวมทั้งแรงดึงของแผ่นที่มุดตัวลง",
                      ("แรงดึงดูดของดวงจันทร์เพียงอย่างเดียว", "ลมที่พัดบนผิวโลก", "กระแสน้ำในมหาสมุทร", "การหมุนรอบดวงอาทิตย์")),
                     ("เหตุใดแผ่นมหาสมุทรจึงมุดลงใต้แผ่นทวีปเมื่อชนกัน", "แผ่นมหาสมุทรมีความหนาแน่นมากกว่า",
                      ("แผ่นมหาสมุทรบางกว่าจึงเบากว่า", "แผ่นทวีปร้อนกว่า", "แผ่นทวีปจมน้ำ", "แผ่นมหาสมุทรเป็นของเหลว")))
            stem, right, wrongs = rng.choice(facts)
            return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_MARGIN, hint=MARGIN_HINT)
        kind, _, result = rng.choice(MARGINS)
        results = sorted({m[2] for m in MARGINS} - {result})
        if rng.random() < 0.5:
            return _labelled(stem=f"บริเวณ{kind}เกิดลักษณะทางธรณีวิทยาใด", correct=result, wrongs=tuple(results), topic=TOPIC_MARGIN,
                             hint=MARGIN_HINT)
        kinds = sorted({m[0] for m in MARGINS} - {kind})
        return _labelled(stem=f"\"{result}\" เกิดที่แนวรอยต่อแบบใด", correct=kind, wrongs=tuple(kinds), topic=TOPIC_MARGIN,
                         hint=MARGIN_HINT)


@question_type(
    "geo.plate_margin_application",
    display_name={"th": "คำนวณระยะที่แผ่นธรณีเคลื่อนที่"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_MARGIN,
)
class PlateMarginApplication(QuestionType):
    """Rate in cm per year times time; convert to km."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        rate = rng.choice((1, 2, Fraction(5, 2), 3, 4, 5, 6, 8, 10))
        if rng.random() < 0.55:
            ma = rng.choice((1, 2, 5, 10, 20, 50))
            km = rate * ma * 10  # cm/yr × 10⁶ yr ÷ 10⁵ cm/km
            return numeric(stem=f"แผ่นธรณีเคลื่อนที่ด้วยอัตรา {show(rate)} cm ต่อปี ใน {ma} ล้านปีจะเคลื่อนที่ได้กี่กิโลเมตร", answer=km,
                           wrongs=[rate * ma, km * 10, km / 10], unit="km", topic=TOPIC_MARGIN,
                           hint="ระยะ (km) = อัตรา (cm/ปี) × เวลา (ล้านปี) × 10 เพราะ 1 km = 100,000 cm")
        km = rng.choice((100, 200, 500, 1000, 1500, 3000))
        years_ma = Fraction(km, rate * 10)
        if (years_ma * 100).denominator != 1:
            rate = 5
            years_ma = Fraction(km, 50)
        return numeric(stem=f"มหาสมุทรกว้าง {km:,} km กำลังปิดตัวเพราะแผ่นธรณีเคลื่อนเข้าหากันด้วยอัตรารวม {show(rate)} cm ต่อปี "
                            f"ต้องใช้เวลากี่ล้านปีมหาสมุทรจึงปิดสนิท", answer=years_ma,
                       wrongs=[Fraction(km, rate), years_ma * 10, years_ma / 10], unit="ล้านปี", topic=TOPIC_MARGIN,
                       hint="เวลา (ล้านปี) = ระยะ (km) ÷ (อัตรา cm/ปี × 10)")
