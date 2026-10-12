"""ผลและการชะลอการเปลี่ยนแปลงภูมิอากาศ

ธรณีวิทยา · ม.5 · สสวท. เพิ่มเติม
Indicators: โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 2 ม.5/11

Sets moved here from: science_wave_f80.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f80 import SUBJECT, UPPER_FIVE

PROVENANCE = Provenance("original")


TOPIC_ACTION = "ผลและการชะลอการเปลี่ยนแปลงภูมิอากาศ"


EVENTS = (
    ("ระดับน้ำทะเลสูงขึ้น", "น้ำทะเลขยายตัวเมื่ออุ่นขึ้นและน้ำจากธารน้ำแข็งบนแผ่นดินไหลลงทะเล",
     ("น้ำแข็งที่ลอยในทะเลละลายเพียงอย่างเดียว จึงทำให้ระดับน้ำสูงขึ้น", "ฝนตกลงทะเลมากขึ้นทุกวันเพราะอากาศร้อนขึ้น", "แผ่นดินไหวยกพื้นทะเลให้สูงขึ้นทั่วโลก", "น้ำทะเลระเหยน้อยลงเพราะอากาศเย็น")),
    ("ปะการังฟอกขาวในวงกว้าง", "น้ำทะเลอุ่นขึ้นผิดปกติเป็นเวลานาน",
     ("น้ำทะเลเย็นลงผิดปกติ", "ปลาการ์ตูนเพิ่มจำนวน", "แสงอาทิตย์ส่องถึงพื้นทะเลน้อยลง", "น้ำทะเลจืดลงทั่วโลก")),
    ("น้ำทะเลเป็นกรดมากขึ้น", "มหาสมุทรดูดซับ CO₂ จากบรรยากาศมากขึ้น",
     ("ฝนกรดตกลงทะเลจากภูเขาไฟเพียงอย่างเดียว", "น้ำแข็งขั้วโลกขยายตัว", "ปลากินแพลงก์ตอนมากขึ้น", "คลื่นใหญ่ขึ้น")),
    ("ชายฝั่งบางขุนเทียนถูกกัดเซาะรุนแรงขึ้น", "ระดับน้ำทะเลสูงขึ้นร่วมกับแผ่นดินทรุดและป่าชายเลนลดลง",
     ("ป่าชายเลนเพิ่มขึ้นจนดันดินออกไป", "ระดับน้ำทะเลลดลง", "มีตะกอนจากแม่น้ำมาทับถมมากขึ้น", "น้ำทะเลเย็นลง")),
    ("คลื่นความร้อนและภัยแล้งเกิดบ่อยและรุนแรงขึ้น", "อุณหภูมิเฉลี่ยสูงขึ้นทำให้สภาพอากาศสุดขั้วเกิดบ่อยขึ้น",
     ("อุณหภูมิเฉลี่ยของโลกลดลงทำให้อากาศหนาวจัดบ่อยขึ้น", "ชั้นโอโซนหนาขึ้นจนกรองแสงแดดได้มากขึ้น", "ดวงอาทิตย์อยู่ใกล้โลกมากขึ้นทุกปี ความร้อนจึงเพิ่มขึ้น", "โลกหมุนรอบตัวเองช้าลง")),
    ("ธารน้ำแข็งบนเทือกเขาหิมาลัยหดตัว", "อุณหภูมิสูงขึ้นทำให้น้ำแข็งละลายเร็วกว่าหิมะที่สะสมใหม่",
     ("หิมะตกมากขึ้นจนธารน้ำแข็งหนักเกินไปและไหลลงมา", "เทือกเขาทรุดตัวลงทุกปี", "อุณหภูมิบนภูเขาลดลง ธารน้ำแข็งจึงแข็งตัวมากขึ้น", "แผ่นดินไหวทำให้น้ำแข็งแตกและไหลลงทะเลจนหมด")),
    ("ฤดูกาลเปลี่ยนไป เช่น ดอกไม้บางชนิดบานเร็วขึ้นและนกอพยพเร็วขึ้น", "อุณหภูมิที่สูงขึ้นทำให้ฤดูใบไม้ผลิมาถึงเร็วขึ้น",
     ("อุณหภูมิที่ลดลงทำให้ฤดูหนาวยาวขึ้น", "โลกโคจรรอบดวงอาทิตย์เร็วขึ้น ฤดูกาลจึงเลื่อน", "กลางวันยาวขึ้นทุกปี ฤดูใบไม้ผลิจึงมาเร็ว", "ดวงจันทร์อยู่ใกล้โลกมากขึ้น ฤดูกาลจึงเปลี่ยน")),
)


MITIGATE = ("เปลี่ยนหลอดไฟเป็นหลอด LED", "ใช้ขนส่งสาธารณะหรือปั่นจักรยานแทนรถยนต์ส่วนตัว", "ติดตั้งแผงเซลล์สุริยะผลิตไฟฟ้า",
            "ปลูกต้นไม้เพิ่มพื้นที่ป่า", "ลดขยะอาหารและคัดแยกขยะ", "ปรับเครื่องปรับอากาศเป็น 26 °C", "ไถกลบตอซังแทนการเผา")


NOT_MITIGATE = ("เผาตอซังข้าวหลังเก็บเกี่ยว", "เปิดเครื่องปรับอากาศทิ้งไว้เมื่อไม่มีคนอยู่", "ขับรถยนต์ส่วนตัวคนเดียวทุกวันแม้มีขนส่งสาธารณะ",
                "ใช้ถุงพลาสติกครั้งเดียวแล้วทิ้ง", "ตัดป่าชายเลนเพื่อทำนากุ้ง", "ผลิตไฟฟ้าจากถ่านหินเพิ่มขึ้น", "ทิ้งอาหารเหลือลงหลุมฝังกลบ")


ADAPT = ("สร้างเขื่อนกันคลื่นป้องกันชายฝั่ง", "เลือกปลูกพืชพันธุ์ทนแล้ง", "ยกพื้นบ้านให้สูงพ้นระดับน้ำท่วม", "ทำระบบเตือนภัยคลื่นความร้อน")


ACTION_HINT = ("การชะลอการเปลี่ยนแปลงภูมิอากาศคือการลดการปล่อยแก๊สเรือนกระจกหรือเพิ่มการดูดซับ เช่น ประหยัดพลังงาน ใช้พลังงานหมุนเวียน "
               "ปลูกป่า ส่วนการปรับตัวคือการรับมือกับผลที่เกิดขึ้นแล้ว เช่น สร้างเขื่อนกันคลื่น ปลูกพืชทนแล้ง")


@question_type(
    "geo.climate_mitigation_foundation",
    display_name={"th": "เหตุการณ์ที่เป็นผลจากการเปลี่ยนแปลงภูมิอากาศ"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_ACTION,
)
class ClimateActionFoundation(QuestionType):
    """Sea-level rise, bleaching, acidification, erosion, heatwaves."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        # One cause can drive several events, so the question only runs event → cause.
        event, cause, wrongs = rng.choice(EVENTS)
        return _labelled(stem=f"เหตุการณ์ \"{event}\" เป็นผลจากการเปลี่ยนแปลงภูมิอากาศอย่างไร", correct=cause, wrongs=tuple(wrongs),
                         topic=TOPIC_ACTION, hint=ACTION_HINT)


@question_type(
    "geo.climate_mitigation_fluency",
    display_name={"th": "แนวปฏิบัติที่ช่วยชะลอการเปลี่ยนแปลงภูมิอากาศ"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_ACTION,
)
class ClimateActionFluency(QuestionType):
    """Mitigation, adaptation, and what makes things worse."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.45:
            return _labelled(stem="ข้อใดเป็นแนวปฏิบัติที่ช่วยชะลอการเปลี่ยนแปลงภูมิอากาศ", correct=rng.choice(MITIGATE),
                             wrongs=tuple(NOT_MITIGATE), topic=TOPIC_ACTION, hint=ACTION_HINT)
        if roll < 0.7:
            return _labelled(stem="ข้อใดทำให้การเปลี่ยนแปลงภูมิอากาศรุนแรงขึ้น", correct=rng.choice(NOT_MITIGATE),
                             wrongs=tuple(MITIGATE), topic=TOPIC_ACTION, hint=ACTION_HINT)
        action = rng.choice(MITIGATE + ADAPT)
        right = "ลดสาเหตุ (ชะลอการเปลี่ยนแปลง)" if action in MITIGATE else "ปรับตัวรับมือกับผลที่เกิดขึ้น"
        return _labelled(stem=f"\"{action}\" เป็นการรับมือกับการเปลี่ยนแปลงภูมิอากาศแบบใด", correct=right,
                         wrongs=tuple(o for o in ("ลดสาเหตุ (ชะลอการเปลี่ยนแปลง)", "ปรับตัวรับมือกับผลที่เกิดขึ้น", "เพิ่มการปล่อยแก๊สเรือนกระจก",
                                                  "ไม่เกี่ยวข้องกับภูมิอากาศ") if o != right),
                         topic=TOPIC_ACTION, hint=ACTION_HINT)


@question_type(
    "geo.climate_mitigation_application",
    display_name={"th": "คำนวณการปล่อยและการลด CO₂ จากกิจกรรมประจำวัน"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_ACTION,
)
class ClimateActionApplication(QuestionType):
    """kWh × factor, litres × factor, savings from a swap, trees to offset."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        grid = "(ไฟฟ้า 1 kWh ปล่อย CO₂ 0.5 kg)"
        if roll < 0.3:
            kwh = rng.randrange(50, 601, 10)
            return numeric(stem=f"บ้านหลังหนึ่งใช้ไฟฟ้าเดือนละ {kwh} kWh {grid} บ้านนี้ปล่อย CO₂ จากการใช้ไฟฟ้าเดือนละกี่ kg",
                           answer=Fraction(kwh, 2), wrongs=[kwh * 2, kwh, Fraction(kwh, 2) * 12], unit="kg", topic=TOPIC_ACTION,
                           hint="CO₂ = พลังงานไฟฟ้า (kWh) × ค่าการปล่อยต่อหน่วย")
        if roll < 0.55:
            old, new = rng.choice(((36, 18), (40, 10), (60, 9), (18, 8), (100, 15), (20, 10)))
            count = rng.randint(2, 20)
            hours = rng.choice((4, 5, 6, 8, 10, 12))
            days = 30
            saved_kwh = Fraction((old - new) * count * hours * days, 1000)
            co2 = saved_kwh / 2
            if (co2 * 100).denominator != 1:
                count = 10
                saved_kwh = Fraction((old - new) * count * hours * days, 1000)
                co2 = saved_kwh / 2
            return numeric(stem=f"โรงเรียนเปลี่ยนหลอดไฟ {old} W เป็นหลอด LED {new} W จำนวน {count} หลอด เปิดวันละ {hours} ชั่วโมง เป็นเวลา {days} วัน "
                                f"{grid} ลด CO₂ ได้กี่ kg",
                           answer=co2, wrongs=[saved_kwh, Fraction(new * count * hours * days, 2000), co2 * 2], unit="kg", topic=TOPIC_ACTION,
                           hint="พลังงานที่ลด (kWh) = (กำลังเดิม − กำลังใหม่) × จำนวน × ชั่วโมง × วัน ÷ 1000 แล้วคูณค่าการปล่อย")
        if roll < 0.8:
            litres = rng.randrange(10, 201, 5)
            factor = Fraction(23, 10)
            return numeric(stem=f"รถยนต์ใช้น้ำมันเบนซินเดือนละ {litres} ลิตร (น้ำมันเบนซิน 1 ลิตรปล่อย CO₂ 2.3 kg) รถคันนี้ปล่อย CO₂ เดือนละกี่ kg",
                           answer=litres * factor, wrongs=[litres * 2, litres + factor, litres * factor * 10], unit="kg", topic=TOPIC_ACTION,
                           hint="CO₂ = ปริมาณน้ำมัน × ค่าการปล่อยต่อลิตร")
        per_tree = rng.choice((10, 15, 20, 25))
        trees = rng.randint(4, 60)
        return numeric(stem=f"ครอบครัวหนึ่งปล่อย CO₂ ปีละ {show(per_tree * trees)} kg ถ้าต้นไม้ 1 ต้นดูดซับ CO₂ ได้ปีละ {per_tree} kg ต้องปลูกต้นไม้กี่ต้นจึงดูดซับได้เท่ากัน",
                       answer=trees, wrongs=[trees * 2, trees + 10, per_tree], unit="ต้น", topic=TOPIC_ACTION,
                       hint="จำนวนต้นไม้ = CO₂ ที่ปล่อย ÷ CO₂ ที่ต้นไม้ 1 ต้นดูดซับ")
