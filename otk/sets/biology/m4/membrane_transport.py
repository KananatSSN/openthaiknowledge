"""การลำเลียงสารผ่านเยื่อหุ้มเซลล์

ชีวะ · ม.4 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 1 ม.4/14

Sets moved here from: science_wave_f47.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled
from otk.sets._support.science_wave_f47 import SUBJECT, UPPER_FOUR

PROVENANCE = Provenance("original")


TOPIC_TRANSPORT = "การลำเลียงสารผ่านเยื่อหุ้มเซลล์"


# (process, down or against the gradient, needs a membrane protein, needs ATP)
PROCESSES = (
    ("การแพร่แบบธรรมดา", "จากความเข้มข้นสูงไปต่ำ", "ไม่ใช้โปรตีนตัวพา", "ไม่ใช้ ATP"),
    ("ออสโมซิส", "น้ำเคลื่อนจากที่มีน้ำมาก (สารละลายเจือจาง) ไปที่มีน้ำน้อย", "ผ่านเยื่อเลือกผ่าน", "ไม่ใช้ ATP"),
    ("การแพร่แบบฟาซิลิเทต", "จากความเข้มข้นสูงไปต่ำ", "ใช้โปรตีนตัวพาหรือโปรตีนช่อง", "ไม่ใช้ ATP"),
    ("แอกทีฟทรานสปอร์ต", "จากความเข้มข้นต่ำไปสูง", "ใช้โปรตีนตัวพา", "ใช้ ATP"),
)


PROCESS_STATEMENTS = ("สารเคลื่อนที่จากความเข้มข้นสูงไปต่ำ", "สารเคลื่อนที่จากความเข้มข้นต่ำไปสูง",
                      "ต้องใช้โปรตีนตัวพาหรือโปรตีนช่อง", "สารผ่านชั้นฟอสโฟลิพิดได้โดยตรงไม่ต้องใช้โปรตีน",
                      "ต้องใช้พลังงานจาก ATP", "ไม่ต้องใช้พลังงานจาก ATP", "เป็นการเคลื่อนที่ของน้ำผ่านเยื่อเลือกผ่าน")


PROCESS_TRUTH = {
    "การแพร่แบบธรรมดา": PROCESS_STATEMENTS[0:1] + (PROCESS_STATEMENTS[3], PROCESS_STATEMENTS[5]),
    "ออสโมซิส": (PROCESS_STATEMENTS[5], PROCESS_STATEMENTS[6]),
    "การแพร่แบบฟาซิลิเทต": (PROCESS_STATEMENTS[0], PROCESS_STATEMENTS[2], PROCESS_STATEMENTS[5]),
    "แอกทีฟทรานสปอร์ต": (PROCESS_STATEMENTS[1], PROCESS_STATEMENTS[2], PROCESS_STATEMENTS[4]),
}


EXAMPLES = (
    ("O₂ ในถุงลมเข้าสู่เลือดในหลอดเลือดฝอย", "การแพร่แบบธรรมดา"), ("CO₂ จากเซลล์เข้าสู่เลือด", "การแพร่แบบธรรมดา"),
    ("น้ำเข้าสู่เซลล์ขนรากจากดิน", "ออสโมซิส"), ("น้ำออกจากเซลล์เม็ดเลือดแดงในน้ำเกลือเข้มข้น", "ออสโมซิส"),
    ("กลูโคสเข้าสู่เซลล์เม็ดเลือดแดงผ่านโปรตีนตัวพา", "การแพร่แบบฟาซิลิเทต"),
    ("ไอออนผ่านโปรตีนช่องของเยื่อหุ้มเซลล์ประสาทตามความเข้มข้น", "การแพร่แบบฟาซิลิเทต"),
    ("Na⁺ ถูกปั๊มออกจากเซลล์และ K⁺ ถูกปั๊มเข้าเซลล์", "แอกทีฟทรานสปอร์ต"),
    ("เซลล์ขนรากดูดแร่ธาตุที่ในดินมีความเข้มข้นต่ำกว่าในเซลล์", "แอกทีฟทรานสปอร์ต"),
    ("ไอโอดีนถูกลำเลียงเข้าต่อมไทรอยด์ที่มีไอโอดีนสูงกว่าในเลือด", "แอกทีฟทรานสปอร์ต"),
)


TONICITY = (
    ("สารละลายไฮโพโทนิก", "เซลล์เม็ดเลือดแดง", "น้ำเข้าเซลล์ เซลล์บวมและอาจแตก"),
    ("สารละลายไฮเพอร์โทนิก", "เซลล์เม็ดเลือดแดง", "น้ำออกจากเซลล์ เซลล์เหี่ยว"),
    ("สารละลายไอโซโทนิก", "เซลล์เม็ดเลือดแดง", "น้ำเข้าออกเท่ากัน เซลล์คงรูปร่าง"),
    ("สารละลายไฮโพโทนิก", "เซลล์พืช", "น้ำเข้าเซลล์ เซลล์เต่งแต่ไม่แตกเพราะมีผนังเซลล์"),
    ("สารละลายไฮเพอร์โทนิก", "เซลล์พืช", "น้ำออกจากเซลล์ เยื่อหุ้มเซลล์หดตัวแยกจากผนัง (พลาสโมไลซิส)"),
)


@question_type(
    "biology.membrane_transport_foundation",
    display_name={"th": "เปรียบเทียบวิธีลำเลียงสารผ่านเยื่อหุ้มเซลล์"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_TRANSPORT,
)
class MembraneTransportFoundation(QuestionType):
    """Direction, protein and energy tell the four apart."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        name, direction, protein, energy = rng.choice(PROCESSES)
        others = [p for p in PROCESSES if p[0] != name]
        if rng.random() < 0.5:
            true = PROCESS_TRUTH[name]
            # For osmosis, "high to low" and "straight through the bilayer" are arguable, so never offer them as wrong.
            arguable = {PROCESS_STATEMENTS[0], PROCESS_STATEMENTS[3]} if name == "ออสโมซิส" else set()
            false = [t for t in PROCESS_STATEMENTS if t not in true and t not in arguable]
            return _labelled(stem=f"ข้อใดเป็นลักษณะของ{name}", correct=rng.choice(true), wrongs=tuple(false),
                             topic=TOPIC_TRANSPORT,
                             hint="แอกทีฟทรานสปอร์ตเท่านั้นที่สวนความเข้มข้นและใช้ ATP ฟาซิลิเทตใช้โปรตีนแต่ไม่ใช้ ATP")
        right = f"{direction} {protein} และ{energy}"
        wrongs = tuple(f"{p[1]} {p[2]} และ{p[3]}" for p in others)
        return _labelled(stem=f"ข้อใดอธิบาย{name}ได้ถูกต้อง", correct=right, wrongs=wrongs, topic=TOPIC_TRANSPORT,
                         hint="แอกทีฟทรานสปอร์ตเท่านั้นที่สวนความเข้มข้นและใช้ ATP ฟาซิลิเทตใช้โปรตีนแต่ไม่ใช้ ATP")


@question_type(
    "biology.membrane_transport_fluency",
    display_name={"th": "ระบุวิธีลำเลียงสารจากสถานการณ์"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_TRANSPORT,
)
class MembraneTransportFluency(QuestionType):
    """Name the process in a real case."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        case, right = rng.choice(EXAMPLES)
        if rng.random() < 0.5:
            others = [e[0] for e in EXAMPLES if e[1] != right]
            return _labelled(stem=f"ข้อใดเป็นตัวอย่างของ{right}", correct=case, wrongs=tuple(others),
                             topic=TOPIC_TRANSPORT, hint="ดูว่าสารสวนความเข้มข้นหรือไม่ ใช้โปรตีนหรือไม่ และสารคือน้ำหรือไม่")
        return _labelled(stem=f"\"{case}\" เป็นการลำเลียงแบบใด", correct=right,
                         wrongs=tuple(p[0] for p in PROCESSES if p[0] != right), topic=TOPIC_TRANSPORT,
                         hint="ดูว่าสารสวนความเข้มข้นหรือไม่ ใช้โปรตีนหรือไม่ และสารคือน้ำหรือไม่")


@question_type(
    "biology.membrane_transport_application",
    display_name={"th": "ผลของสารละลายต่อเซลล์และทิศทางการออสโมซิส"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_TRANSPORT,
)
class MembraneTransportApplication(QuestionType):
    """Water moves toward the more concentrated side."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            solution, cell, result = rng.choice(TONICITY)
            others = sorted({t[2] for t in TONICITY} - {result})
            return _labelled(stem=f"นำ{cell}ไปแช่ใน{solution} จะเกิดผลอย่างไร", correct=result, wrongs=tuple(others),
                             topic=TOPIC_TRANSPORT, hint="ไฮโพโทนิกน้ำเข้าเซลล์ ไฮเพอร์โทนิกน้ำออกจากเซลล์ พืชมีผนังเซลล์จึงไม่แตก")
        inside = rng.choice((0.9, 0.5, 1.2, 2.0, 0.3))
        outside = rng.choice([x for x in (0.1, 0.3, 0.5, 0.9, 1.5, 2.0, 3.0) if x != inside])
        right = "น้ำออสโมซิสออกจากเซลล์" if outside > inside else "น้ำออสโมซิสเข้าสู่เซลล์"
        other = "น้ำออสโมซิสเข้าสู่เซลล์" if outside > inside else "น้ำออสโมซิสออกจากเซลล์"
        return _labelled(stem=f"เซลล์มีตัวละลายเข้มข้นร้อยละ {inside} แช่ในสารละลายเข้มข้นร้อยละ {outside} (เยื่อหุ้มเซลล์ให้น้ำผ่านแต่ไม่ให้ตัวละลายผ่าน) จะเกิดอะไรขึ้น",
                         correct=right, wrongs=(other, "ตัวละลายแพร่ออกจากเซลล์จนเข้มข้นเท่ากัน", "ไม่มีการเคลื่อนที่ของน้ำ"),
                         topic=TOPIC_TRANSPORT, hint="น้ำเคลื่อนจากฝั่งที่ตัวละลายเจือจางไปฝั่งที่ตัวละลายเข้มข้นกว่า")
