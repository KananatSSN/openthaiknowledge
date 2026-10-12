"""กลไกการต่อต้านสิ่งแปลกปลอม

ชีวะ · ม.5 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 4 ม.5/15

Sets moved here from: science_wave_f63.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric
from otk.sets._support.science_wave_f63 import SUBJECT, UPPER_FIVE

PROVENANCE = Provenance("original")


TOPIC_DEFENCE = "กลไกการต่อต้านสิ่งแปลกปลอม"


NONSPECIFIC = ("ผิวหนังที่ป้องกันไม่ให้เชื้อโรคผ่านเข้าไป", "เมือกและซิเลียในทางเดินหายใจดักจับเชื้อโรค",
               "กรดในกระเพาะอาหารทำลายเชื้อโรค", "ไลโซไซม์ในน้ำตาและน้ำลายย่อยผนังเซลล์แบคทีเรีย",
               "นิวโทรฟิลและแมโครฟาจกินเชื้อโรคด้วยฟาโกไซโทซิส", "การอักเสบทำให้บริเวณที่ติดเชื้อบวมแดงร้อน")


SPECIFIC = ("B ลิมโฟไซต์เปลี่ยนเป็นพลาสมาเซลล์สร้างแอนติบอดีที่จับกับแอนติเจนนั้น", "เซลล์ T ชนิดทำลายฆ่าเซลล์ที่ติดไวรัสชนิดนั้น",
            "เซลล์ความจำตอบสนองได้เร็วเมื่อพบเชื้อเดิมอีกครั้ง", "เซลล์ T ผู้ช่วยกระตุ้นการทำงานของ B และ T ลิมโฟไซต์")


CELLS = (
    ("พลาสมาเซลล์", "สร้างและหลั่งแอนติบอดี"),
    ("เซลล์ T ผู้ช่วย (helper T)", "หลั่งสารกระตุ้นให้ B และ T ลิมโฟไซต์ทำงาน"),
    ("เซลล์ T ชนิดทำลาย (cytotoxic T)", "ทำลายเซลล์ที่ติดเชื้อไวรัสหรือเซลล์มะเร็ง"),
    ("เซลล์ความจำ", "จดจำแอนติเจนและตอบสนองได้เร็วเมื่อพบซ้ำ"),
    ("แมโครฟาจ", "กินสิ่งแปลกปลอมและนำเสนอแอนติเจนแก่ลิมโฟไซต์"),
)


DEFENCE_HINT = ("กลไกไม่จำเพาะต่อต้านสิ่งแปลกปลอมทุกชนิดเหมือนกัน เช่น ผิวหนัง เมือก ฟาโกไซต์ การอักเสบ "
                "กลไกจำเพาะใช้ลิมโฟไซต์ที่จดจำแอนติเจนแต่ละชนิด เช่น แอนติบอดี เซลล์ T และเซลล์ความจำ")


@question_type(
    "biology.immune_defense_foundation",
    display_name={"th": "กลไกการต่อต้านสิ่งแปลกปลอมแบบไม่จำเพาะและแบบจำเพาะ"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_DEFENCE,
)
class ImmuneDefenseFoundation(QuestionType):
    """Sort each defence into non-specific or specific."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        specific = rng.random() < 0.5
        same, other = (SPECIFIC, NONSPECIFIC) if specific else (NONSPECIFIC, SPECIFIC)
        kind = "แบบจำเพาะ" if specific else "แบบไม่จำเพาะ"
        if rng.random() < 0.5:
            return _labelled(stem=f"ข้อใดเป็นกลไกการต่อต้านสิ่งแปลกปลอม{kind}", correct=rng.choice(same), wrongs=tuple(other),
                             topic=TOPIC_DEFENCE, hint=DEFENCE_HINT)
        return _labelled(stem=f"\"{rng.choice(same)}\" เป็นกลไกการต่อต้านสิ่งแปลกปลอมแบบใด", correct=f"กลไก{kind}",
                         wrongs=(f"กลไก{'แบบไม่จำเพาะ' if specific else 'แบบจำเพาะ'}", "ภูมิคุ้มกันรับมา", "ปฏิกิริยาภูมิแพ้"),
                         topic=TOPIC_DEFENCE, hint=DEFENCE_HINT)


@question_type(
    "biology.immune_defense_fluency",
    display_name={"th": "บทบาทของเซลล์ในระบบภูมิคุ้มกัน"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_DEFENCE,
)
class ImmuneDefenseFluency(QuestionType):
    """Plasma cells, helper and killer T, memory cells, macrophages."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        name, role = rng.choice(CELLS)
        others = rng.sample([c for c in CELLS if c[0] != name], 3)
        if rng.random() < 0.5:
            return _labelled(stem=f"{name}มีบทบาทอย่างไร", correct=role, wrongs=tuple(c[1] for c in others), topic=TOPIC_DEFENCE,
                             hint=DEFENCE_HINT)
        return _labelled(stem=f"เซลล์ใด{role}", correct=name, wrongs=tuple(c[0] for c in others), topic=TOPIC_DEFENCE, hint=DEFENCE_HINT)


@question_type(
    "biology.immune_defense_application",
    display_name={"th": "การตอบสนองทางภูมิคุ้มกันครั้งแรกและครั้งที่สอง"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_DEFENCE,
)
class ImmuneDefenseApplication(QuestionType):
    """Memory cells make the second response faster and larger."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        first_day = rng.randint(10, 16)
        second_day = rng.randint(3, 7)
        first_level = rng.randrange(10, 101, 10)
        times = rng.choice((5, 8, 10, 20, 50, 100))
        second_level = first_level * times
        if rng.random() < 0.5:
            return numeric(stem=f"ได้รับแอนติเจนครั้งแรก ระดับแอนติบอดีสูงสุด {first_level} หน่วยในวันที่ {first_day} เมื่อได้รับแอนติเจนเดิมอีกครั้ง "
                                f"ระดับแอนติบอดีสูงสุด {second_level} หน่วยในวันที่ {second_day} ระดับสูงสุดครั้งที่สองเป็นกี่เท่าของครั้งแรก",
                           answer=times, wrongs=[second_level - first_level, first_day - second_day, times * 2], unit="เท่า",
                           topic=TOPIC_DEFENCE, hint="ครั้งที่สอง ÷ ครั้งแรก")
        if rng.random() < 0.5:
            return numeric(stem=f"ระดับแอนติบอดีสูงสุดในการตอบสนองครั้งแรกเกิดในวันที่ {first_day} และครั้งที่สองในวันที่ {second_day} หลังได้รับแอนติเจน "
                                f"การตอบสนองครั้งที่สองถึงระดับสูงสุดเร็วกว่ากี่วัน", answer=first_day - second_day,
                           wrongs=[first_day + second_day, first_day, second_day], unit="วัน", topic=TOPIC_DEFENCE,
                           hint="ผลต่างของวันที่ถึงระดับสูงสุด")
        return _labelled(stem="เหตุใดการตอบสนองต่อแอนติเจนเดิมในครั้งที่สองจึงเร็วและมีแอนติบอดีมากกว่าครั้งแรก", correct="มีเซลล์ความจำที่จดจำแอนติเจนนั้นไว้แล้ว",
                         wrongs=tuple(("แอนติเจนอ่อนแอลงในครั้งที่สอง", "ร่างกายมีเม็ดเลือดแดงมากขึ้น", "แอนติบอดีจากครั้งแรกยังอยู่ครบทั้งหมด",
                                                  "ผิวหนังหนาขึ้นหลังติดเชื้อครั้งแรก")),
                         topic=TOPIC_DEFENCE, hint=DEFENCE_HINT)
