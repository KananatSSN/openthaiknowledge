"""การเกิดเมล็ดและผล

ชีวะ · ม.5 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 3 ม.5/15

Sets moved here from: science_wave_f58.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric
from otk.sets._support.science_wave_f58 import SUBJECT, UPPER_FIVE

PROVENANCE = Provenance("original")


TOPIC_SEED = "การเกิดเมล็ดและผล"


BECOMES = (("ออวุล", "เมล็ด"), ("รังไข่", "ผล"), ("ผนังรังไข่", "เปลือกผล (เพอริคาร์ป)"), ("เปลือกหุ้มออวุล (อินเทกิวเมนต์)", "เปลือกเมล็ด"),
           ("ไซโกต", "เอ็มบริโอ"), ("เซลล์ที่ได้จากสเปิร์มรวมกับโพลาร์นิวคลีไอ", "เอนโดสเปิร์ม"))


FRUIT_TYPES = {
    "ผลเดี่ยว": ("มะม่วง", "มะเขือเทศ", "ส้ม", "ถั่วลันเตา", "มะพร้าว"),
    "ผลกลุ่ม": ("น้อยหน่า", "สตรอว์เบอร์รี", "กระดังงา", "จำปี"),
    "ผลรวม": ("สับปะรด", "ขนุน", "ยอ", "หม่อน"),
}


FRUIT_MEANING = {"ผลเดี่ยว": "เกิดจากดอกเดียวที่มีรังไข่เดียว", "ผลกลุ่ม": "เกิดจากดอกเดียวที่มีหลายรังไข่",
                 "ผลรวม": "เกิดจากช่อดอกที่มีหลายดอกรวมกันเป็นผลเดียว"}


SEED_HINT = ("ออวุลเจริญเป็นเมล็ด รังไข่เป็นผล ผนังรังไข่เป็นเปลือกผล ไซโกตเป็นเอ็มบริโอ ผลเดี่ยวมาจากดอกเดียวรังไข่เดียว "
             "ผลกลุ่มมาจากดอกเดียวหลายรังไข่ ผลรวมมาจากหลายดอก")


EATEN = (
    ("มะม่วง", "เปลือกผลชั้นกลาง (เนื้อผล)"), ("มะพร้าว (เนื้อมะพร้าว)", "เอนโดสเปิร์ม"), ("ข้าว", "เอนโดสเปิร์ม"),
    ("ถั่วลิสง", "ใบเลี้ยง"), ("ถั่วเขียวที่เพาะเป็นถั่วงอก", "ต้นอ่อนที่มีใบเลี้ยง"), ("ส้ม", "ขนที่เจริญจากผนังรังไข่ชั้นใน (ถุงน้ำ)"),
    ("ขนุน", "กลีบรวมของดอกย่อย (ยวง)"), ("ลำไย", "เยื่อหุ้มเมล็ด (เนื้อลำไย)"),
)


@question_type(
    "biology.seed_fruit_foundation",
    display_name={"th": "ส่วนของดอกที่เจริญเป็นเมล็ดและผล"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_SEED,
)
class SeedFruitFoundation(QuestionType):
    """Ovule to seed, ovary to fruit, and the rest."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        part, becomes = rng.choice(BECOMES)
        others = rng.sample([b for b in BECOMES if b[0] != part], 3)
        if rng.random() < 0.5:
            return _labelled(stem=f"หลังการปฏิสนธิ {part}เจริญไปเป็นส่วนใด", correct=becomes, wrongs=tuple(b[1] for b in others),
                             topic=TOPIC_SEED, hint=SEED_HINT)
        return _labelled(stem=f"{becomes}เจริญมาจากส่วนใด", correct=part, wrongs=tuple(b[0] for b in others), topic=TOPIC_SEED,
                         hint=SEED_HINT)


@question_type(
    "biology.seed_fruit_fluency",
    display_name={"th": "ผลเดี่ยว ผลกลุ่ม และผลรวม"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_SEED,
)
class SeedFruitFluency(QuestionType):
    """One flower one ovary, one flower many ovaries, or many flowers."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        kind = rng.choice(sorted(FRUIT_TYPES))
        fruit = rng.choice(FRUIT_TYPES[kind])
        others = [k for k in FRUIT_TYPES if k != kind]
        roll = rng.random()
        if roll < 0.4:
            return _labelled(stem=f"ผล{fruit}จัดเป็นผลประเภทใด", correct=kind, wrongs=(*others, "ผลที่ไม่ได้เกิดจากรังไข่"),
                             topic=TOPIC_SEED, hint=SEED_HINT)
        if roll < 0.75:
            pool = [f for k in others for f in FRUIT_TYPES[k]]
            return _labelled(stem=f"ข้อใดเป็น{kind}", correct=fruit, wrongs=tuple(pool), topic=TOPIC_SEED, hint=SEED_HINT)
        return _labelled(stem=f"{kind} เช่น {fruit} เกิดขึ้นอย่างไร", correct=FRUIT_MEANING[kind],
                         wrongs=(*(FRUIT_MEANING[k] for k in others), "เกิดจากรังไข่ที่ไม่ได้รับการปฏิสนธิเท่านั้น"), topic=TOPIC_SEED,
                         hint=SEED_HINT)


@question_type(
    "biology.seed_fruit_application",
    display_name={"th": "ส่วนของเมล็ดและผลที่นำมาใช้ประโยชน์"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_SEED,
)
class SeedFruitApplication(QuestionType):
    """Which part of the fruit or seed we actually eat."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.7:
            food, part = rng.choice(EATEN)
            pool = sorted({p for f, p in EATEN if p != part})
            return _labelled(stem=f"ส่วนที่เรารับประทานของ{food}เจริญมาจากหรือเป็นส่วนใด", correct=part, wrongs=tuple(pool),
                             topic=TOPIC_SEED, hint="เนื้อมะม่วงคือเปลือกผลชั้นกลาง ข้าวและเนื้อมะพร้าวคือเอนโดสเปิร์ม ถั่วลิสงกินใบเลี้ยง")
        seeds = rng.randint(3, 40)
        return numeric(stem=f"ผลของพืชชนิดหนึ่งมี {seeds} เมล็ด ดอกที่เจริญเป็นผลนี้ต้องมีออวุลที่ได้รับการปฏิสนธิอย่างน้อยกี่ออวุล",
                       answer=seeds, wrongs=[2 * seeds, seeds + 1, 3 * seeds], unit="ออวุล", topic=TOPIC_SEED,
                       hint="ออวุลที่ได้รับการปฏิสนธิ 1 ออวุลเจริญเป็นเมล็ด 1 เมล็ด")
