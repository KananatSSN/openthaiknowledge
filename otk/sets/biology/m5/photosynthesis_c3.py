"""กระบวนการสังเคราะห์ด้วยแสงของพืช C3

ชีวะ · ม.5 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 3 ม.5/10

Sets moved here from: science_wave_f56.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric
from otk.sets._support.science_wave_f56 import SUBJECT, UPPER_FIVE

PROVENANCE = Provenance("original")


TOPIC_C3 = "กระบวนการสังเคราะห์ด้วยแสงของพืช C3"


C3_STEPS = (
    ("ปฏิกิริยาที่ใช้แสง", "เยื่อไทลาคอยด์", "แยกน้ำ ปล่อย O₂ และสร้าง ATP กับ NADPH"),
    ("คาร์บอนฟิกเซชัน", "สโตรมา", "เอนไซม์รูบิสโกตรึง CO₂ เข้ากับ RuBP ได้ 3-ฟอสโฟกลีเซอเรต (PGA)"),
    ("รีดักชัน", "สโตรมา", "ใช้ ATP และ NADPH เปลี่ยน PGA เป็นกลีเซอรัลดีไฮด์-3-ฟอสเฟต (G3P)"),
    ("รีเจเนอเรชัน", "สโตรมา", "ใช้ ATP เปลี่ยน G3P ส่วนหนึ่งกลับเป็น RuBP"),
)


C3_HINT = ("ปฏิกิริยาที่ใช้แสงเกิดที่ไทลาคอยด์ ได้ O₂ ATP NADPH วัฏจักรคัลวินเกิดที่สโตรมา: ตรึง CO₂ ด้วยรูบิสโก → รีดิวซ์เป็น G3P "
           "→ สร้าง RuBP กลับคืน")


C3_FACTS = (
    ("แก๊ส O₂ ที่พืชปล่อยออกมาเกิดจากขั้นตอนใด", "การแยกน้ำในปฏิกิริยาที่ใช้แสง",
     ("การตรึง CO₂ ในวัฏจักรคัลวิน", "การสร้าง RuBP กลับคืน", "การรีดิวซ์ PGA", "การรีดิวซ์ PGA ในวัฏจักรคัลวิน")),
    ("ATP และ NADPH จากปฏิกิริยาที่ใช้แสงถูกนำไปใช้ที่ใด", "วัฏจักรคัลวินในสโตรมา",
     ("ไกลโคลิซิสในไซโทซอล", "การแยกน้ำในไทลาคอยด์", "การลำเลียงน้ำในไซเลม", "วัฏจักรเครบส์ในไมโทคอนเดรีย")),
    ("สารใดเป็นตัวรับ CO₂ ในวัฏจักรคัลวิน", "RuBP (ไรบูโลสบิสฟอสเฟต)", ("PGA (3-ฟอสโฟกลีเซอเรต)", "G3P (กลีเซอรัลดีไฮด์-3-ฟอสเฟต)", "NADPH (ตัวพาอิเล็กตรอน)", "ATP (สารพลังงานสูง)")),
    ("สารคาร์บอน 3 อะตอมตัวแรกที่เสถียรในพืช C3 คือสารใด", "PGA (3-ฟอสโฟกลีเซอเรต)", ("RuBP (ไรบูโลสบิสฟอสเฟต)", "กลูโคส (น้ำตาลโมเลกุลเดี่ยว)", "ซูโครส (น้ำตาลโมเลกุลคู่)", "OAA (ออกซาโลแอซีเตต)")),
    ("เอนไซม์ที่ตรึง CO₂ ในพืช C3 คือเอนไซม์ใด", "รูบิสโก", ("PEP คาร์บอกซิเลส", "ATP ซินเทส", "อะไมเลส", "DNA พอลิเมอเรส")),
    ("เหตุใดวัฏจักรคัลวินจึงหยุดไม่นานหลังจากปิดไฟ", "ขาด ATP และ NADPH ที่สร้างจากปฏิกิริยาที่ใช้แสง",
     ("ขาด O₂ จากอากาศที่ใช้สร้าง ATP ในคลอโรพลาสต์", "รูบิสโกถูกแสงทำลาย", "รูบิสโกถูกแสงทำลายจนตรึง CO₂ ไม่ได้", "CO₂ ในอากาศหมดทันที")),
    ("ผลิตภัณฑ์ของวัฏจักรคัลวินที่ถูกนำไปสร้างน้ำตาลคือสารใด", "G3P (กลีเซอรัลดีไฮด์-3-ฟอสเฟต)",
     ("RuBP (ไรบูโลสบิสฟอสเฟต)", "NADP⁺ (ตัวรับอิเล็กตรอน)", "O₂ (แก๊สออกซิเจน)", "PEP (ฟอสโฟอีนอลไพรูเวต)")),
)


@question_type(
    "biology.photosynthesis_c3_foundation",
    display_name={"th": "ขั้นตอนและตำแหน่งของการสังเคราะห์ด้วยแสง"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_C3,
)
class PhotosynthesisC3Foundation(QuestionType):
    """Each stage, where it happens, and what it does."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stage, place, event = rng.choice(C3_STEPS)
        others = [s for s in C3_STEPS if s[0] != stage]
        roll = rng.random()
        if roll < 0.35:
            places = ["เยื่อไทลาคอยด์", "สโตรมา", "เยื่อหุ้มชั้นนอกของคลอโรพลาสต์", "ไซโทซอล", "เมทริกซ์ของไมโทคอนเดรีย"]
            return _labelled(stem=f"ขั้น{stage}เกิดขึ้นที่ใด", correct=place, wrongs=tuple([p for p in places if p != place]),
                             topic=TOPIC_C3, hint=C3_HINT)
        if roll < 0.7:
            events = [s[2] for s in others] + ["สลายกลูโคสเป็นกรดไพรูวิก", "ปล่อย CO₂ จากการสลายสารอินทรีย์"]
            return _labelled(stem=f"ข้อใดเกิดขึ้นในขั้น{stage}", correct=event, wrongs=tuple(events), topic=TOPIC_C3,
                             hint=C3_HINT)
        stages = [s[0] for s in others] + ["ไกลโคลิซิส", "วัฏจักรเครบส์"]
        return _labelled(stem=f"\"{event}\" เป็นขั้นตอนใด", correct=stage, wrongs=tuple(stages), topic=TOPIC_C3,
                         hint=C3_HINT)


@question_type(
    "biology.photosynthesis_c3_fluency",
    display_name={"th": "สารตั้งต้นและผลิตภัณฑ์ในแต่ละขั้นของการสังเคราะห์ด้วยแสง"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_C3,
)
class PhotosynthesisC3Fluency(QuestionType):
    """What goes in and comes out of each stage."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem, right, wrongs = rng.choice(C3_FACTS)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_C3, hint=C3_HINT)


@question_type(
    "biology.photosynthesis_c3_application",
    display_name={"th": "คำนวณ ATP NADPH และจำนวนรอบของวัฏจักรคัลวิน"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_C3,
)
class PhotosynthesisC3Application(QuestionType):
    """Per CO₂: 3 ATP and 2 NADPH; 3 CO₂ per exported G3P; 6 CO₂ per glucose."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        hint = "ตรึง CO₂ 1 โมเลกุลใช้ ATP 3 และ NADPH 2 โมเลกุล ต้องตรึง CO₂ 3 โมเลกุลจึงได้ G3P ส่งออก 1 โมเลกุล และ 6 โมเลกุลต่อกลูโคส 1 โมเลกุล"
        glucose = rng.randint(1, 20)
        co2 = 6 * glucose
        cases = (
            (f"การสร้างกลูโคส {glucose} โมเลกุลด้วยวัฏจักรคัลวินต้องตรึง CO₂ กี่โมเลกุล", co2, [glucose, 3 * glucose, 12 * glucose], "โมเลกุล"),
            (f"การสร้างกลูโคส {glucose} โมเลกุลด้วยวัฏจักรคัลวินต้องใช้ ATP กี่โมเลกุล", 18 * glucose, [12 * glucose, 6 * glucose, 3 * glucose], "โมเลกุล"),
            (f"การสร้างกลูโคส {glucose} โมเลกุลด้วยวัฏจักรคัลวินต้องใช้ NADPH กี่โมเลกุล", 12 * glucose, [18 * glucose, 6 * glucose, 2 * glucose], "โมเลกุล"),
            (f"วัฏจักรคัลวินตรึง CO₂ ได้ {3 * glucose} โมเลกุล ได้ G3P ที่ส่งออกไปสร้างน้ำตาลกี่โมเลกุล", glucose,
             [3 * glucose, 6 * glucose, 2 * glucose], "โมเลกุล"),
            (f"วัฏจักรคัลวินตรึง CO₂ ได้ {co2} โมเลกุล ต้องใช้ RuBP กี่โมเลกุล", co2, [co2 // 2, co2 * 2, glucose], "โมเลกุล"),
            (f"วัฏจักรคัลวินตรึง CO₂ ได้ {co2} โมเลกุล ได้ PGA กี่โมเลกุล", 2 * co2, [co2, co2 // 3, 3 * co2], "โมเลกุล"),
        )
        stem, answer, wrongs, unit = rng.choice(cases)
        return numeric(stem=stem, answer=answer, wrongs=wrongs, unit=unit, topic=TOPIC_C3, hint=hint)
