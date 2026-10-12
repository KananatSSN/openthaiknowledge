"""ธาตุอาหารของพืช

ชีวะ · ม.5 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 3 ม.5/7

Sets moved here from: science_wave_f55.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f55 import SUBJECT, UPPER_FIVE

PROVENANCE = Provenance("original")


TOPIC_NUTR = "ธาตุอาหารของพืช"


MACRO = ("ไนโตรเจน", "ฟอสฟอรัส", "โพแทสเซียม", "แคลเซียม", "แมกนีเซียม", "กำมะถัน")


MICRO = ("เหล็ก", "แมงกานีส", "โบรอน", "สังกะสี", "ทองแดง", "โมลิบดีนัม", "คลอรีน")


DEFICIENCY = (
    ("ไนโตรเจน", "ใบแก่เหลืองซีดทั้งใบก่อน ต้นแคระแกร็น"),
    ("ฟอสฟอรัส", "ใบเขียวเข้มผิดปกติหรือมีสีม่วงแดง รากไม่เจริญ"),
    ("โพแทสเซียม", "ขอบใบแก่เหลืองแล้วไหม้เป็นสีน้ำตาล"),
    ("แมกนีเซียม", "ใบแก่เหลืองระหว่างเส้นใบ แต่เส้นใบยังเขียว"),
    ("เหล็ก", "ใบอ่อนเหลืองซีดระหว่างเส้นใบ ใบแก่ยังเขียว"),
    ("แคลเซียม", "ยอดอ่อนและปลายรากตาย ผลมะเขือเทศเน่าที่ก้นผล"),
    ("โบรอน", "ตายอดตาย ลำต้นและก้านเปราะ"),
)


NUTR_HINT = ("ธาตุอาหารหลักพืชต้องการมาก (N P K) ธาตุอาหารรองและจุลธาตุต้องการน้อยแต่ขาดไม่ได้ ธาตุที่เคลื่อนย้ายได้ (N P K Mg) "
             "แสดงอาการที่ใบแก่ก่อน ธาตุที่เคลื่อนย้ายไม่ได้ (Fe Ca B) แสดงอาการที่ใบอ่อนหรือยอด")


@question_type(
    "biology.plant_nutrient_foundation",
    display_name={"th": "ธาตุอาหารที่พืชต้องการมากและน้อย"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_NUTR,
)
class PlantNutrientFoundation(QuestionType):
    """Macronutrients against micronutrients, and what the big three do."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.6:
            macro = rng.random() < 0.5
            right, wrong = (MACRO, MICRO) if macro else (MICRO, MACRO)
            return _labelled(stem=f"ธาตุใดเป็นธาตุอาหารที่พืชต้องการใน{'ปริมาณมาก (มหธาตุ)' if macro else 'ปริมาณน้อย (จุลธาตุ)'}",
                             correct=rng.choice(right), wrongs=tuple(wrong), topic=TOPIC_NUTR, hint=NUTR_HINT)
        roles = (("ไนโตรเจน", "เป็นองค์ประกอบของโปรตีน กรดนิวคลีอิก และคลอโรฟิลล์"),
                 ("ฟอสฟอรัส", "เป็นองค์ประกอบของ ATP และกรดนิวคลีอิก ช่วยการเจริญของราก"),
                 ("โพแทสเซียม", "ควบคุมการปิดเปิดปากใบและกระตุ้นการทำงานของเอนไซม์"),
                 ("แมกนีเซียม", "เป็นองค์ประกอบของโมเลกุลคลอโรฟิลล์"),
                 ("แคลเซียม", "เป็นองค์ประกอบของผนังเซลล์ส่วนมิดเดิลลาเมลลา"))
        name, role = rng.choice(roles)
        others = rng.sample([r for r in roles if r[0] != name], 3)
        return _labelled(stem=f"ธาตุใด{role}", correct=name, wrongs=tuple(r[0] for r in others), topic=TOPIC_NUTR, hint=NUTR_HINT)


@question_type(
    "biology.plant_nutrient_fluency",
    display_name={"th": "อาการของพืชที่ขาดธาตุอาหาร"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_NUTR,
)
class PlantNutrientFluency(QuestionType):
    """Old leaves first for mobile elements, young leaves and tips for immobile ones."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        name, sign = rng.choice(DEFICIENCY)
        others = rng.sample([d for d in DEFICIENCY if d[0] != name], 3)
        crop = rng.choice(("ข้าวโพด", "มะเขือเทศ", "ผักกาด", "ถั่วเหลือง", "ข้าว"))
        if rng.random() < 0.55:
            return _labelled(stem=f"{crop}มีอาการ \"{sign}\" น่าจะขาดธาตุใด", correct=name, wrongs=tuple(d[0] for d in others),
                             topic=TOPIC_NUTR, hint=NUTR_HINT)
        return _labelled(stem=f"{crop}ที่ขาด{name}จะแสดงอาการใด", correct=sign, wrongs=tuple(d[1] for d in others), topic=TOPIC_NUTR,
                         hint=NUTR_HINT)


@question_type(
    "biology.plant_nutrient_application",
    display_name={"th": "คำนวณธาตุอาหารจากสูตรปุ๋ย"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_NUTR,
)
class PlantNutrientApplication(QuestionType):
    """Grade N-P-K is kilograms of each (as N, P₂O₅, K₂O) per 100 kg of fertiliser."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        grades = ((15, 15, 15), (16, 16, 8), (46, 0, 0), (16, 20, 0), (13, 13, 21), (8, 24, 24), (21, 0, 0), (0, 0, 60), (25, 7, 7))
        n, p, k = rng.choice(grades)
        names = (("ไนโตรเจน (N)", n), ("ฟอสฟอรัส (P₂O₅)", p), ("โพแทสเซียม (K₂O)", k))
        name, share = rng.choice([x for x in names if x[1]])
        bag = rng.choice((25, 50, 100, 20, 10))
        hint = "ปุ๋ยสูตร N-P-K เช่น 15-15-15 หมายถึงปุ๋ย 100 kg มี N 15 kg P₂O₅ 15 kg และ K₂O 15 kg"
        if rng.random() < 0.55:
            return numeric(stem=f"ปุ๋ยสูตร {n}-{p}-{k} หนัก {bag} kg มีธาตุอาหาร{name}กี่กิโลกรัม", answer=Fraction(bag * share, 100),
                           wrongs=[share, bag * share, Fraction(bag * (100 - share), 100)], unit="kg", topic=TOPIC_NUTR, hint=hint)
        need = Fraction(share * rng.randint(1, 10), 10)
        return numeric(stem=f"ต้องการให้ธาตุอาหาร{name} {show(need)} kg แก่แปลงปลูกพืช ต้องใช้ปุ๋ยสูตร {n}-{p}-{k} กี่กิโลกรัม",
                       answer=need * 100 / share, wrongs=[need, need * share, need * 100], unit="kg", topic=TOPIC_NUTR,
                       hint=hint + " ปริมาณปุ๋ย = ธาตุที่ต้องการ × 100 ÷ ตัวเลขในสูตร")
