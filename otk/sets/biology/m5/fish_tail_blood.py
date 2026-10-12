"""การไหลของเลือดในหางปลา

ชีวะ · ม.5 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 4 ม.5/9

Sets moved here from: science_wave_f61.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric
from otk.sets._support.science_wave_f61 import SUBJECT, UPPER_FIVE

PROVENANCE = Provenance("original")


TOPIC_TAIL = "การไหลของเลือดในหางปลา"


VESSEL_SEEN = (
    ("อาร์เทอรี", "เลือดไหลจากโคนหางไปปลายหาง ไหลเร็วและเป็นจังหวะ"),
    ("อาร์เทอรี", "เลือดไหลออกจากทิศทางของหัวใจด้วยแรงดันสูง"),
    ("เวน", "เลือดไหลจากปลายหางกลับไปโคนหาง ไหลช้ากว่าอาร์เทอรีและสม่ำเสมอ"),
    ("เวน", "หลอดเลือดขนาดใหญ่ที่รวบรวมเลือดจากหลอดเลือดฝอยกลับไปทางหัวใจ"),
    ("หลอดเลือดฝอย", "เซลล์เม็ดเลือดแดงเคลื่อนที่เรียงทีละเซลล์และช้าที่สุด"),
    ("หลอดเลือดฝอย", "หลอดเลือดเล็กที่สุดที่เชื่อมระหว่างอาร์เทอรีกับเวน"),
)


TAIL_HINT = ("อาร์เทอรีพาเลือดออกจากหัวใจไปปลายหาง ไหลเร็วเป็นจังหวะ เวนพาเลือดกลับ หลอดเลือดฝอยเล็กที่สุด "
             "แต่พื้นที่หน้าตัดรวมมากที่สุด เลือดจึงไหลช้าที่สุด")


TAIL_FACTS = (
    ("เหตุใดเลือดในหลอดเลือดฝอยจึงไหลช้าที่สุด", "หลอดเลือดฝอยมีพื้นที่หน้าตัดรวมมากที่สุด",
     ("หลอดเลือดฝอยแต่ละเส้นใหญ่ที่สุด", "หลอดเลือดฝอยอยู่ใกล้หัวใจที่สุด", "หลอดเลือดฝอยมีลิ้นกั้นมาก", "เลือดในหลอดเลือดฝอยข้นกว่า")),
    ("การที่เลือดในหลอดเลือดฝอยไหลช้ามีประโยชน์อย่างไร", "มีเวลาแลกเปลี่ยนแก๊สและสารกับเซลล์ได้มากขึ้น",
     ("ทำให้หัวใจเต้นช้าลง", "ทำให้เลือดแข็งตัว", "ป้องกันเลือดไหลย้อนกลับ", "ทำให้ความดันเลือดสูงขึ้น")),
    ("ความเร็วของเลือดในอาร์เทอรี หลอดเลือดฝอย และเวน เรียงจากเร็วไปช้าได้อย่างไร", "อาร์เทอรี > เวน > หลอดเลือดฝอย",
     ("หลอดเลือดฝอย > เวน > อาร์เทอรี", "เวน > อาร์เทอรี > หลอดเลือดฝอย", "อาร์เทอรี > หลอดเลือดฝอย > เวน", "เท่ากันทุกชนิด")),
    ("หลอดเลือดชนิดใดมีพื้นที่หน้าตัดรวมมากที่สุดในร่างกาย", "หลอดเลือดฝอย",
     ("เอออร์ตา", "เวนใหญ่", "อาร์เทอรีขนาดกลาง", "หลอดเลือดแดงปอด")),
    ("ถ้าพื้นที่หน้าตัดรวมของหลอดเลือดเพิ่มขึ้นในขณะที่ปริมาณเลือดที่ไหลต่อวินาทีเท่าเดิม ความเร็วของเลือดจะเป็นอย่างไร", "ลดลง",
     ("เพิ่มขึ้น", "เท่าเดิม", "เป็นศูนย์", "เพิ่มเป็นสองเท่าเสมอ")),
    ("เลือดในอาร์เทอรีไหลเป็นจังหวะเพราะเหตุใด", "เป็นไปตามจังหวะการบีบตัวของหัวใจ",
     ("หลอดเลือดฝอยบีบตัวดันเลือด", "เวนมีลิ้นเปิดปิด", "ปลาหายใจเป็นจังหวะ", "เซลล์เม็ดเลือดแดงเคลื่อนที่เอง")),
    ("การเตรียมปลาเพื่อสังเกตหางควรทำอย่างไร", "ห่อลำตัวปลาด้วยสำลีชุบน้ำ เหลือหางไว้วางบนสไลด์",
     ("ตัดหางปลาออกมาวางบนสไลด์", "ปล่อยปลาไว้บนสไลด์โดยไม่มีน้ำจนหยุดดิ้น", "ต้มปลาก่อนสังเกต", "ย้อมหางปลาด้วยไอโอดีนเข้มข้น")),
)


@question_type(
    "biology.fish_tail_blood_foundation",
    display_name={"th": "ระบุชนิดหลอดเลือดจากการสังเกตหางปลา"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_TAIL,
)
class FishTailBloodFoundation(QuestionType):
    """Which vessel is which under the microscope."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        vessel, seen = rng.choice(VESSEL_SEEN)
        if rng.random() < 0.5:
            names = sorted({v[0] for v in VESSEL_SEEN} - {vessel}) + ["หลอดน้ำเหลือง"]
            return _labelled(stem=f"ส่องหางปลาด้วยกล้องจุลทรรศน์ พบหลอดเลือดที่ \"{seen}\" เป็นหลอดเลือดชนิดใด", correct=vessel,
                             wrongs=tuple(names), topic=TOPIC_TAIL, hint=TAIL_HINT)
        pool = [v[1] for v in VESSEL_SEEN if v[0] != vessel] + ["ไม่มีเลือดไหลผ่านเลย"]
        return _labelled(stem=f"ในหางปลา ข้อใดเป็นลักษณะของ{vessel}", correct=seen, wrongs=tuple(pool), topic=TOPIC_TAIL,
                         hint=TAIL_HINT)


@question_type(
    "biology.fish_tail_blood_fluency",
    display_name={"th": "ความสัมพันธ์ระหว่างขนาดหลอดเลือดกับความเร็วของเลือด"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_TAIL,
)
class FishTailBloodFluency(QuestionType):
    """Total cross-section, not single-vessel size, sets the speed."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem, right, wrongs = rng.choice(TAIL_FACTS)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_TAIL, hint=TAIL_HINT)


@question_type(
    "biology.fish_tail_blood_application",
    display_name={"th": "คำนวณความเร็วของเลือดจากพื้นที่หน้าตัดรวม"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_TAIL,
)
class FishTailBloodApplication(QuestionType):
    """Speed = flow ÷ total cross-section; or distance ÷ time for one cell."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.6:
            flow = rng.choice((60, 80, 90, 100, 120))  # cm³/s
            vessels = (("เอออร์ตา", rng.choice((3, 4, 5))), ("หลอดเลือดฝอยทั้งหมด", rng.choice((2000, 2500, 4000, 5000))),
                       ("เวนใหญ่ทั้งหมด", rng.choice((8, 10, 12, 15, 20))))
            name, area = rng.choice(vessels)
            speed = Fraction(flow, area)
            if (speed * 100).denominator != 1:
                area = 5
                speed = Fraction(flow, area)
                name = "เอออร์ตา"
            return numeric(stem=f"หัวใจสูบฉีดเลือด {flow} cm³ ต่อวินาที ผ่าน{name}ซึ่งมีพื้นที่หน้าตัดรวม {area} cm² "
                                f"เลือดไหลผ่านบริเวณนี้ด้วยอัตราเร็วกี่เซนติเมตรต่อวินาที", answer=speed,
                           wrongs=[flow * area, Fraction(area, flow) if (Fraction(area, flow) * 100).denominator == 1 else speed * 10,
                                   speed * 2], unit="cm/s", topic=TOPIC_TAIL,
                           hint="อัตราการไหล = พื้นที่หน้าตัดรวม × อัตราเร็ว ดังนั้นอัตราเร็ว = อัตราการไหล ÷ พื้นที่หน้าตัดรวม")
        speed = rng.choice((200, 250, 300, 400, 500, 800, 1000))  # μm/s
        seconds = rng.choice((2, 4, 5, 8, 10))
        return numeric(stem=f"สังเกตเซลล์เม็ดเลือดแดงในหลอดเลือดฝอยหางปลาเคลื่อนที่ได้ {speed * seconds} μm ใน {seconds} วินาที "
                            f"อัตราเร็วเป็นกี่ไมโครเมตรต่อวินาที", answer=speed, wrongs=[speed * seconds, seconds, speed * 2], unit="μm/s",
                       topic=TOPIC_TAIL, hint="อัตราเร็ว = ระยะทาง ÷ เวลา")
